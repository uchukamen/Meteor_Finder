''' 動き検出＋直線検出
'''
import numpy as np
import cv2
from icecream import ic
import os

ESC_KEY = 27
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # ハワイ・マウナケアの星空ライブ
mp4_file = os.path.join(os.getcwd(), "test_data/fast_cloud1.mp4")


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

    # video = pafy.new(URL)
    # best = video.getbest(preftype="mp4")
    # cap = cv2.VideoCapture(best.url)
    cap = cv2.VideoCapture(mp4_file)

    _tm = cv2.TickMeter()  # FPS計測用

    _frame_no = 0

    fgbg = cv2.createBackgroundSubtractorMOG2(30, 30)

    _frame_sum = None  # 比較明合成結果
    _frame_no = 0

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
            one = np.ones(_frame.shape, dtype="uint8")  # 減光用
        _frame_sum = np.maximum(_frame, _frame_sum)

        # 古いフレームデータを減光する
        if _frame_no % 4 == 0:
            _frame_sum = cv2.subtract(_frame_sum, one)

        # 動き検出用 BW フレーム
        _frame_bw = cv2.cvtColor(_frame_sum, cv2.COLOR_RGB2GRAY)

        _frame_md = np.zeros((1080, 1920), dtype="uint8")  # 減光用
        _frame_ld = np.zeros((1080, 1920), dtype="uint8")  # 減光用

        # 動き検出
        _fgmask = fgbg.apply(_frame_bw)

        # 輪郭を求める　find contours
        contours, hierarchy = cv2.findContours(
            _fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(0, len(contours)):
            contour = contours[i]

            if len(contour) < 5:    # 領域が小さいものは除外
                continue

            size = cv2.contourArea(contour)

            # エリアサイズが小さな点は処理しない
            if size <= 30:
                continue

            # 動きを検出したエリアを描画する
            cv2.drawContours(_frame_ld, contours, i, 255, 1)
            cv2.drawContours(_frame, contours, i, (255, 0, 0), 3)

        edges = cv2.Canny(_frame_ld, 100, 200, apertureSize=3)

        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi /
                                180, threshold=0, minLineLength=15, maxLineGap=5)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(_frame, (x1, y1), (x2, y2),
                         (0, 0, 255), 3)  # 緑色で直線を引く

        cv2.imshow('frame', _frame)

        # 30フレームごとに、FPS を表示する
        if _frame_no % 30 == 0:
            print(f'FPS: {get_fps(_tm):.1f}')

        _frame_no += 1


if __name__ == "__main__":
    main()
