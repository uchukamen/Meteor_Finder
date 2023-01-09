''' YouTube から動画をキャプチャーして表示する
'''
import cv2
import apafy as pafy

ESC_KEY = 27
URL = "https://www.youtube.com/watch?v=_8rp1p_tWlc"  # ハワイ・マウナケアの星空ライブ

video = pafy.new(URL)
best = video.getbest("mp4")
cap = cv2.VideoCapture(best.url)

while (True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)

    # 終了判定
    if cv2.waitKey(1) & 0xFF == ESC_KEY:
        break

cap.release()
cv2.destroyAllWindows()