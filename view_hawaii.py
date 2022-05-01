import cv2
import apafy as pafy

# ハワイ・マウナケアの星空ライブ
url = "https://www.youtube.com/watch?v=eH90mZnmgD4"

video = pafy.new(url)
cap = cv2.VideoCapture(video.streams[4].url)

while (True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()