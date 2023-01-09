'''
YouTube ハワイ・マウナケアの星空ライブから
動画をキャプチャーして、ノイズを除去し、さらに
比較明合成（コンポジット）した動画を表示する
'''
import numpy as np
import cv2
import apafy as pafy
from icecream import ic
from datetime import datetime
import math

ESC_KEY = 27
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # ハワイ・マウナケアの星空ライブ


def get_fps(tm) -> float:
    # FPS を印刷する
    tm.stop()
    fps = tm.getFPS()
    tm.reset()
    return fps

def remove_noise(frame):
    ''' frame のノイズを除去する
    '''
    searchWindowSize = 5

    # バイラテラルフィルタBilateral Filter
    result_frame = cv2.bilateralFilter(frame, searchWindowSize, 5, 5)

    return result_frame


def main():
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    video = pafy.new(URL)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)

    _tm = cv2.TickMeter()  # FPS計測用
    _tm.start()

    _frame_comp = None  # 比較明合成結果
    _frame_no = 0

    # マスクをロード
    mask_path = 'mask.png'
    _mask_image = cv2.imread(mask_path)
    _mask_image_bw = cv2.cvtColor(_mask_image, cv2.COLOR_RGB2GRAY)

    fgbg = cv2.createBackgroundSubtractorMOG2(30, 30)

    _frame_sum = None  # 比較明合成結果
    _frame_no = 0
    start_time = datetime.now()
    while True:
        _tm.start()
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # 終了判定
        # ノイズ除去に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        # 比較明合成を実行
        if _frame_sum is None:
            _frame_sum = _frame
            info_frame = np.zeros(_frame.shape, dtype="uint8")  # 減光用
            one = np.ones(_frame.shape, dtype="uint8")  # 減光用
        _frame_sum = np.maximum(_frame, _frame_sum)

        # 古いフレームデータを減光する
        if _frame_no % 2 == 0:
            _frame_sum = cv2.subtract(_frame_sum, one)

        # 直線検出用 BW フレーム
        _frame_bw = cv2.cvtColor(_frame, cv2.COLOR_RGB2GRAY)

        # マスキング
        _masked_frame_bw = cv2.bitwise_and(_frame_bw, _mask_image_bw)

        edges = cv2.Canny(_masked_frame_bw, 100, 200, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi /
                                180, threshold=0, minLineLength=15, maxLineGap=5)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(_frame_sum, (x1, y1), (x2, y2),
                         (0, 0, 255), 3)  # 緑色で直線を引く

        cv2.imshow('info_frame', _frame_sum)

        # 30フレームごとに、FPS を表示する
        if _frame_no % 30 == 0:
            print(f'FPS: {get_fps(_tm):.1f}')

        _frame_no += 1


if __name__ == "__main__":
    main()
