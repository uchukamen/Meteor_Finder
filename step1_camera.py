'''
STEP1 カメラから動画をキャプチャーして表示する
'''
import numpy as np
import cv2

ESC_KEY = 27

cap = cv2.VideoCapture(0)

while(True):
    # カメラからキャプチャーする
    ret, frame = cap.read()

    # キャプチャーした画像を表示する
    cv2.imshow('frame',frame)

    # 終了判定
    if cv2.waitKey(30) & 0xFF == ESC_KEY:
        break

# 終了処理
cap.release()
cv2.destroyAllWindows()