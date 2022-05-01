import numpy as np 
import cv2
import apafy as pafy

ESC_KEY = 27

def main():        
    # ハワイ・マウナケアの星空ライブ
    url = "https://www.youtube.com/watch?v=eH90mZnmgD4"

    video = pafy.new(url)
    cap = cv2.VideoCapture(video.streams[4].url)

    _frame_sum = None  # 比較明合成結果

    while True:
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        if _frame is None:
            break
        if _frame_sum is None:
            _frame_sum = _frame

        # 比較明合成を実行
        if _frame_sum is None:
            _frame_sum = _frame
        _frame_sum = np.maximum(_frame, _frame_sum)

        cv2.imshow('frame', _frame_sum)

        # waitKey の間に描画している。
        keyboard = cv2.waitKey(1) & 0xFF
        if keyboard == ESC_KEY:
            break


if __name__ == "__main__":
    main()    

