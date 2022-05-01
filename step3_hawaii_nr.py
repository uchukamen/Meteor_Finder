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
    cap = cv2.VideoCapture(video.streams[4].url)

    _frame_comp = None  # 比較明合成結果

    while True:
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # ノイズ除去
        _frame_nr = remove_noise(_frame)

        # 表示
        cv2.imshow('frame', _frame_nr)

        # 終了判定
        if cv2.waitKey(30) & 0xFF == ESC_KEY:
            break


if __name__ == "__main__":
    main()    
