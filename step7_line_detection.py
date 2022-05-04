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

# ハワイ・マウナケアの星空ライブ
# url = "https://www.youtube.com/watch?v=eH90mZnmgD4"
# 東京大の天文台から星空と流れ星ライブ（長野・木曽）
url = "https://www.youtube.com/watch?v=mrusJKLhxAw"
# 福島・滝川渓谷近くから、流星群と星空をライブ
# url = "https://www.youtube.com/watch?v=GHzzILvuwFo"
# 羽田空港
# url = "https://www.youtube.com/watch?v=pS5khAKucq8"
# 羽田空港 D滑走路
# url = "https://www.youtube.com/watch?v=nkoGWDdJvkU"


def remove_noise(frame):
    ''' frame のノイズを除去する
    '''
    searchWindowSize = 5

    # バイラテラルフィルタBilateral Filter
    result_frame = cv2.bilateralFilter(frame, searchWindowSize, 5, 5)

    return result_frame


def get_fps(tm):
    # FPS を調整する
    tm.stop()
    fps = tm.getFPS()
    tm.reset()
    return fps


def main():
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    video = pafy.new(url)
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
        _frame_bw = cv2.cvtColor(_frame_sum, cv2.COLOR_RGB2GRAY)

        edges = cv2.Canny(_frame_bw, 100, 200, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi /
                                180, threshold=0, minLineLength=50, maxLineGap=5)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(_frame_sum, (x1, y1), (x2, y2),
                         (0, 0, 255), 3)  # 緑色で直線を引く

        cv2.imshow('info_frame', _frame_sum)

        # 1秒ごとに、FPS を表示する
        if _frame_no % 30 == 0:
            fps = f'{get_fps(_tm):.1f}'
            ic(fps)

        _frame_no += 1


if __name__ == "__main__":
    main()
