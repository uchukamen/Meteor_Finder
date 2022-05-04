'''
YouTube から動画をキャプチャーして表示する
再生速度を調整する
'''
import cv2
import apafy as pafy
from datetime import datetime
import math
from icecream import ic

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

def main():
    video = pafy.new(url)
    best = video.getbest("mp4")
    cap = cv2.VideoCapture(best.url)

    FPS = cap.get(cv2.CAP_PROP_FPS) # FPSを取得
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # ビデオの幅を取得
    H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # ビデオの高さを取得
    ic(W, H, FPS)

    _frame_no = 0
    wait = 30 #　waitKey の初期値

    _tm = cv2.TickMeter() # FPS計測用
    _tm.start()

    while (True):
        _tm.start()
        ret, frame = cap.read()
        if ret == False:
            ic("動画の取得に失敗しました")
            break
        cv2.imshow('frame', frame)

        # 終了判定
        if cv2.waitKey(wait) & 0xFF == ESC_KEY:
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
        if _frame_no % 30 == 0:
            ic(f'{fps:.1f}', wait)

        _frame_no += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
