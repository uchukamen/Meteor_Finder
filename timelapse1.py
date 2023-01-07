''' YouTube ハワイ・マウナケアの星空ライブから
    動画をキャプチャーして、比較明合成（コンポジット）した動画を表示する
'''
import numpy as np 
import cv2
import apafy as pafy
from icecream import ic
import os
import pytz
from datetime import datetime, date, timedelta, time
from pathlib import Path

# 定義
ESC_KEY = 27
SAVE_DIR = os.path.join(os.environ['HOME'], "documents/hawaii_timelapse")
# ハワイ・マウナケアの星空ライブ
URL_HAWAII = "https://www.youtube.com/watch?v=_8rp1p_tWlc"

def to_hst(dt) -> datetime:
    ''' ハワイ標準時へ変更
        dt: datetime
    '''
    hst_tz = pytz.timezone("US/Hawaii")
    return dt.astimezone(hst_tz)


def _create_dir(filepath):
    ''' ディレクトリがなければ作成する
    '''
    _dirpath = Path(filepath).parent
    os.makedirs(_dirpath, exist_ok=True)

def _get_timelapse_image_path(dt) -> str:
    ''' ファイルのパスを取得する
    '''
    hst = to_hst(dt)
    date_str = f'{hst:%Y%m%d}'
    datetime_stamp = f'{hst:%Y%m%d%H%M}'

    if os.name == 'posix':
        _filepath = os.path.join(
            SAVE_DIR, "timelapse", datetime_stamp + ".jpg")
        _filepath_comp = os.path.join(
            SAVE_DIR, "timelapse", datetime_stamp + "_comp.jpg")
    else:
        raise(NotImplementedError(os.name))
    return _filepath, _filepath_comp

def main():        
    ''' ハワイの星空を比較明合成(Composite)して表示する    
    '''
    _video = pafy.new(URL_HAWAII)
    _best = _video.getbest("mp4")
    _cap = cv2.VideoCapture(_best.url)

    _tm = cv2.TickMeter() # FPS計測用
    _tm.start()

    _frame_comp = None  # 比較明合成結果
    _frame_no = 0

    while True:
        _tm.start()
        _ret, _frame = _cap.read()
        if _ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        # 終了判定
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break

            
        # 比較明合成を実行
        if _frame_comp is None:
            _frame_comp = _frame
        # cv2 で比較明合成を実行
        _frame_comp = cv2.max(_frame, _frame_comp)


        # =============================================
        # １分に１回、タイムラプス用にフレームを書き出す
        # =============================================
        if _frame_no % (30 * 60) == 0:
            dt = datetime.now()
            _filepath, _filepath_comp = _get_timelapse_image_path(dt)
            _create_dir(_filepath)
            cv2.imwrite(_filepath, _frame)
            cv2.imwrite(_filepath_comp, _frame_comp)
            # 比較明合成を1分ごとにリセット
            _frame_comp = _frame

        cv2.imshow('frame', _frame_comp)

        _frame_no += 1


if __name__ == "__main__":
    main()    
