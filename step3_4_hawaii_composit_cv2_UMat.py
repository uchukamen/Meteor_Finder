''' YouTube ハワイ・マウナケアの星空ライブから
    動画をキャプチャーして、比較明合成（コンポジット）した動画を表示する
'''
import numpy as np 
import cv2
import apafy as pafy
from icecream import ic

ESC_KEY = 27

ESC_KEY = 27
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # ハワイ・マウナケアの星空ライブ

def get_fps(tm) -> float:
    # FPS を印刷する
    tm.stop()
    fps = tm.getFPS()
    tm.reset()
    return fps

    
def main():        
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''

    video = pafy.new(URL)
    best = video.getbest("mp4")
    cap = cv2.VideoCapture(best.url)

    _frame_comp = None  # 比較明合成結果
    _frame_no = 0

    _tm = cv2.TickMeter()  # FPS計測用
    _tm.start()
    while _frame_no < 100:
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break
        # GPU を使用
        _frame = cv2.UMat(_frame)

        # 終了判定
        # 処理に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        # 比較明合成を実行
        if _frame_comp is None:
            _frame_comp = _frame
        _frame_comp = cv2.max(_frame, _frame_comp)

        cv2.imshow('frame', _frame_comp)

        _frame_no += 1

    print(f'FPS: {get_fps(_tm) * 100.:.1f}')

if __name__ == "__main__":
    main()    
