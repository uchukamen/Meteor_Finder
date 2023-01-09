''' OpenCV のFPS を調査
'''
import cv2
import apafy as pafy
from icecream import ic
import time

ESC_KEY = 27

# ハワイ・マウナケアの星空ライブ
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # Hawaii

def main():
    video = pafy.new(URL)
    best = video.getbest("mp4")
    cap = cv2.VideoCapture(best.url)

    FPS = cap.get(cv2.CAP_PROP_FPS) # FPSを取得
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # ビデオの幅を取得
    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # ビデオの高さを取得
    print(f'WIDTH: {W}, HEIGHT: {H}, FPS: {FPS}')

    _tm = cv2.TickMeter() # FPS計測用

    # CASE1 1/30 秒
    _tm.start()
    time.sleep(1./30.)  
    _tm.stop()
    fps = _tm.getFPS()
    print(f'FPS 1/30 sec: {fps:.1f}')
    _tm.reset()

    # CASE2 1秒
    _tm.start()
    time.sleep(1.0)
    _tm.stop()
    fps = _tm.getFPS()
    print(f'FPS 1 sec: {fps:.1f}')
    _tm.reset()

    # CASE3 100フレーム
    _tm.start()
    
    _frame_no = 0
    while (_frame_no < 100):
        ret, frame = cap.read()
        frame = cv2.UMat(frame)
        
        if ret == False:
            ic("動画の取得に失敗しました")
            break
        cv2.imshow('frame', frame)

        # 終了判定
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        _frame_no += 1

    _tm.stop()
    fps = _tm.getFPS() * 100.
    print(f'平均FPS: {fps:.1f}')
    _tm.reset()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
