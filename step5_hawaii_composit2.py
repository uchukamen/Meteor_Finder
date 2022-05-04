'''
YouTube ハワイ・マウナケアの星空ライブから
動画をキャプチャーして、比較明合成（コンポジット）した動画を表示する
'''
import numpy as np
import cv2
import apafy as pafy
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


def get_fps(tm):
    # FPS を調整する
    tm.stop()
    fps = tm.getFPS()
    tm.reset()
    return fps


def main():
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''

    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)

    _tm = cv2.TickMeter()  # FPS計測用
    _tm.start()

    _frame_comp = None  # 比較明合成結果
    _frame_no = 0

    while True:
        _tm.start()
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # 終了判定
        # 処理に時間がかかるため、waitKeyの待ち時間を短くする
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

        # 比較明合成を実行
        if _frame_comp is None:  # 初期化
            _frame_comp = _frame
            one = np.ones(_frame.shape, dtype="uint8")
        _frame_comp = np.maximum(_frame, _frame_comp)

        # 古いフレームデータを減光する
        if _frame_no % 2 == 0:
            _frame_comp = cv2.subtract(_frame_comp, one)

        cv2.imshow('frame', _frame_comp)

        # 1秒ごとに、FPS を表示する
        if _frame_no % 30 == 0:
            fps = f'{get_fps(_tm):.1f}'
            ic(fps)

        _frame_no += 1


if __name__ == "__main__":
    main()
