''' Atom Cam2 から動画をキャプチャーして表示する
    環境変数 ATOM_CAM_IP に Atom Cam2 のIPアドレスを設定する
'''
import cv2
import os

ESC_KEY = 27

ATOM_CAM_IP = os.environ.get("ATOM_CAM_IP", "192.168.0.4")
ATOM_CAM_RTSP = "rtsp://6199:4003@{}/live".format(ATOM_CAM_IP)

cap = cv2.VideoCapture(ATOM_CAM_RTSP)

while (True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)

    # 終了判定
    if cv2.waitKey(30) & 0xFF == ESC_KEY:
        break

cap.release()
cv2.destroyAllWindows()