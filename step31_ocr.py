'''
YouTube から動画をキャプチャーして表示する
再生速度を調整する
'''
import cv2
import apafy as pafy
from datetime import datetime
import math
from icecream import ic
from PIL import Image
import pyocr
import os

ESC_KEY = 27

# ハワイ・マウナケアの星空ライブ
url = "https://www.youtube.com/watch?v=_8rp1p_tWlc"

def ocr(image)->str:

    #インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
    #OS自体に設定してあれば以下の2行は不要
    path='/opt/homebrew/bin/'
    os.environ['PATH'] = os.environ['PATH'] + path
    
    #pyocrへ利用するOCRエンジンをTesseractに指定する。
    tools = pyocr.get_available_tools()
    tool = tools[0]
    
    pil_img = Image.fromarray(image)


    #画像から文字を読み込む
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    text = tool.image_to_string(pil_img, lang="eng", builder=builder)
    text = text.replace('F', '7')
    
    return text

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

        # 終了判定
        if cv2.waitKey(wait) & 0xFF == ESC_KEY:
            break

        # clock_img = frame[970:1040, 1650:1920,:]

        clock_img = frame[970:1040, 1650:1900,:]
        clock_gray = cv2.cvtColor(clock_img, cv2.COLOR_RGB2GRAY)
        ret2, clock_bw = cv2.threshold(clock_gray, 80, 255, cv2.THRESH_BINARY)
        cv2.imshow('time', clock_bw)

        date_img = frame[1030:1080, 0:200,:]
        date_gray = cv2.cvtColor(date_img, cv2.COLOR_RGB2GRAY)
        ret2, date_bw = cv2.threshold(date_gray, 80, 255, cv2.THRESH_BINARY)
        cv2.imshow('date', date_bw)

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
            # ic(f'{fps:.1f}', wait)

            result_str = ocr(clock_bw)
            print(result_str)

            result_str = ocr(date_bw)
            print(result_str)


        _frame_no += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
