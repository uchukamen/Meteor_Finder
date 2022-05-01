'''
YouTube ハワイ・マウナケアの星空ライブから
動画をキャプチャーして、ノイズを除去し、さらに
比較明合成（コンポジット）した動画を表示する
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
    ''' ハワイの星空を比較明合成(Composite)して表示する    
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

        # 比較明合成を実行
        if _frame_comp is None:
            _frame_comp = _frame_nr
        _frame_comp = np.maximum(_frame_nr, _frame_comp)

        cv2.imshow('frame', _frame_comp)

        # 終了判定
        # ノイズ除去に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break


if __name__ == "__main__":
    main()    
