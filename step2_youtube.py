'''
YouTube から動画をキャプチャーして表示する
'''
import cv2
import apafy as pafy

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

video = pafy.new(url)
best = video.getbest("mp4")
cap = cv2.VideoCapture(best.url)

while (True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)

    # 終了判定
    if cv2.waitKey(30) & 0xFF == ESC_KEY:
        break

cap.release()
cv2.destroyAllWindows()