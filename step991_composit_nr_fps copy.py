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

ESC_KEY = 27
# url = "https://www.youtube.com/watch?v=eH90mZnmgD4" # ハワイ・マウナケアの星空ライブ
url = "https://www.youtube.com/watch?v=nkoGWDdJvkU"  # 羽田空港D


def remove_noise(frame):
    ''' frame のノイズを除去する
    '''
    searchWindowSize = 5

    # バイラテラルフィルタBilateral Filter
    result_frame = cv2.bilateralFilter(frame, searchWindowSize, 5, 5)

    return result_frame


def _get_fps(start_time, frame_no) -> int:
    ''' １秒当たりのフレームの処理速度 
        FPS を返す
    '''
    if frame_no == 0:
        return 0
    now = datetime.now()
    dt = now-start_time
    dtsec = dt.seconds + dt.microseconds/(1000 * 1000)
    if dtsec != 0:
        fps = int(frame_no/dtsec)
        return fps
    else:
        return 0


def main():
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''

    video = pafy.new(url)
    cap = cv2.VideoCapture(video.streams[4].url)

    _frame_comp = None  # 比較明合成結果
    _frame_no = 0
    start_time = datetime.now()
    while True:
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # ノイズ除去 
        # _frame = remove_noise(_frame)

        # 比較明合成を実行
        if _frame_comp is None:
            _frame_comp = _frame
            one = np.ones(_frame.shape, dtype="uint8")  # 減光用
        _frame_comp = np.maximum(_frame, _frame_comp)

        # 古いフレームデータを減光する
        if _frame_no % 2 == 0:
            _frame_comp = cv2.subtract(_frame_comp, one)

        cv2.imshow('frame', _frame_comp)

        # 終了判定
        # ノイズ除去に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(11) & 0xFF == ESC_KEY:
            break

        # 1秒に1回、フレームレートを表示
        if _frame_no % 30 == 0:
            print(_get_fps(start_time, _frame_no))
        _frame_no += 1


if __name__ == "__main__":
    main()
