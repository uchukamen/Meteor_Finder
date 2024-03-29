'''
YouTube から動画をキャプチャーして表示する
再生速度を調整する
'''
import cv2
import apafy as pafy
from icecream import ic

ESC_KEY = 27
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # ハワイ・マウナケアの星空ライブ

def main():
    video = pafy.new(URL)
    best = video.getbest("mp4")
    cap = cv2.VideoCapture(best.url)

    FPS = cap.get(cv2.CAP_PROP_FPS) # FPSを取得
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # ビデオの幅を取得
    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # ビデオの高さを取得
    print(f'WIDTH: {W}, HEIGHT: {H}, FPS: {FPS}')

    _frame_no = 0
    wait = 1 #　waitKey の初期値

    _tm = cv2.TickMeter() # FPS計測用
    _tm.start()

    while (True):
        _tm.start()
        ret, frame = cap.read()
        frame = cv2.UMat(frame)
        
        if ret == False:
            ic("動画の取得に失敗しました")
            break
        cv2.imshow('frame', frame)

        # 終了判定
        if cv2.waitKey(wait) & 0xFF == ESC_KEY:
            break

        # FPS を表示する
        _tm.stop()
        fps = _tm.getFPS()
        print(f'FPS: {fps:.1f}')
        _tm.reset()

        _frame_no += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
