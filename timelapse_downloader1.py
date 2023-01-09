''' YouTube ハワイ・マウナケアの星空ライブから
    動画をキャプチャーして、比較明合成（コンポジット）した動画を表示する
'''
import cv2
import apafy as pafy
from icecream import ic
import os
import pytz
from datetime import datetime
from pathlib import Path
import time

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


def to_utc(dt) -> datetime:
    ''' 世界標準時へ変更
        dt: datetime
    '''
    hst_tz = pytz.timezone("UTC")
    return dt.astimezone(hst_tz)


def _create_dir(filepath):
    ''' ディレクトリがなければ作成する
    '''
    _dirpath = Path(filepath).parent
    os.makedirs(_dirpath, exist_ok=True)

def _get_timelapse_image_path(dt) -> str:
    ''' ファイルのパスを取得する
    '''
    _utc_date_str = f'{to_utc(dt):%Y%m%d}'       # ディレクトリの日にちは UTC表記
    _filename = f'{to_hst(dt):%Y%m%d%H%M}.jpg'  # ファイル名は HST表記

    if os.name == 'posix':
        _filepath = os.path.join(SAVE_DIR, _utc_date_str, _filename)
        _filepath_comp = _filepath.replace(".jpg", "_comp.jpg")
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
            print("動画読込ができませんでした。", f'{datetime.now():%y/%m/%d %H:%M:%S}')
            time.sleep(10)  # 10秒スリープ

        # 終了判定
        if cv2.waitKey(1) & 0xFF == ESC_KEY:
            break
            
        # 比較明合成を実行
        if _frame_comp is None:
            _frame_comp = _frame
        # cv2 で比較明合成を実行
        _frame_comp = cv2.max(_frame, _frame_comp)

        # =============================================
        # 60秒に１回、タイムラプス用にフレームを書き出す
        # =============================================
        if _frame_no % (30 * 60) == 0:
            dt = datetime.now()
            _filepath, _filepath_comp = _get_timelapse_image_path(dt)
            _create_dir(_filepath)
            cv2.imwrite(_filepath, _frame)
            cv2.imwrite(_filepath_comp, _frame_comp)
            # 比較明合成をリセット
            _frame_comp = _frame

        cv2.imshow('frame', _frame_comp)

        _frame_no += 1


if __name__ == "__main__":
    main()    
