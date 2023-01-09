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

    _frame_no = 0

    fgbg = cv2.createBackgroundSubtractorMOG2(30, 30)

    _frame_sum = None  # 比較明合成結果
    _frame_no = 0

    while True:
        _tm.start()
        ret, _frame_cv2 = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # GPU を使用
        _frame = cv2.UMat(_frame_cv2)

        # 終了判定
        # ノイズ除去に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        # 比較明合成を実行
        if _frame_sum is None:
            _frame_sum = _frame
            _one = np.ones(_frame_cv2.shape, dtype="uint8")  # 減光用
            _one = cv2.UMat(_one)
        _frame_sum = cv2.max(_frame, _frame_sum)

        # 古いフレームデータを減光する
        if _frame_no % 4 == 0:
            _frame_sum = cv2.subtract(_frame_sum, _one)

        # 動き検出用 BW フレーム
        _frame_bw = cv2.cvtColor(_frame_sum, cv2.COLOR_RGB2GRAY)
        _frame_bw = cv2.UMat(_frame_bw)

        # 動き検出
        _fgmask = fgbg.apply(_frame_bw)

        # 輪郭を求める　find contours
        contours, hierarchy = cv2.findContours(
            _fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(0, len(contours)):
            contour = contours[i]

            if len(contour.get()) < 5:    # 領域が小さいものは除外
                continue

            size = cv2.contourArea(contour)

            # エリアサイズが小さな点は処理しない
            if size <= 30:
                continue

            # 動きを検出したエリアを描画する
            cv2.drawContours(_frame_sum, contours, i, GREEN, 1)

        cv2.imshow('info_frame', _frame_sum)

        # 30フレームごとに、FPS を表示する
        if _frame_no % 30 == 0:
            print(f'FPS: {get_fps(_tm):.1f}')

        _frame_no += 1


if __name__ == "__main__":
    main()
