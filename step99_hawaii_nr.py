'''
YouTube ハワイ・マウナケアの星空ライブから
動画をキャプチャーして、ノイズを除去した動画を表示する
'''
import numpy as np 
import cv2
import apafy as pafy
from icecream import ic

ESC_KEY = 27
url = "https://www.youtube.com/watch?v=eH90mZnmgD4" # ハワイ・マウナケアの星空ライブ

def remove_noise(frame):
    ''' frame のノイズを除去する
    '''
    searchWindowSize = 5

    # バイラテラルフィルタBilateral Filter
    result_frame = cv2.bilateralFilter(frame, searchWindowSize, 5, 5)

    return result_frame
    
def main():        
    ''' ハワイの星空をノイズ除去して表示する 
    '''

    video = pafy.new(url)
    best = video.getbest("mp4")
    cap = cv2.VideoCapture(best.url)
    FPS = cap.get(cv2.CAP_PROP_FPS) # FPSを取得

    _tm = cv2.TickMeter() # FPS計測用
    _tm.start()

    _frame_no = 0
    wait = 30

    while True:
        _tm.start()
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # ノイズ除去
        _frame_nr = remove_noise(_frame)

        # 表示
        cv2.imshow('frame', _frame_nr)

        # 終了判定
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        # FPS を調整する
        _tm.stop()
        fps = _tm.getFPS()
        if FPS > fps and wait > 1:
            wait -= 1
        else:
            wait += 1
        _tm.reset()

        # 1秒ごとに、FPS を表示する
        # if _frame_no % 30 == 0:
        ic(f'{fps:.1f}', wait)

        _frame_no += 1


if __name__ == "__main__":
    main()    
