''' ハワイ・マウナケアのタイムラプスを作成する
    入力
        ~/documents/hawaii_timelapse/UTC_DATE/*.jpg
        ~/documents/hawaii_timelapse/UTC_DATE/*_comp.jpg
    出力
        ~/documents/hawaii_timelapse/UTC_DATE/*.mp4
        ~/documents/hawaii_timelapse/UTC_DATE/*_comp.mp4
    備考
        UTC_DATEは、UTC時間の日付
        *.mp4 は1分ごとのタイムラプス
        *_comp.mp4 は1分間の比較明合成
'''
import os
import cv2
from datetime import datetime, timedelta, time
from icecream import ic
import pytz

# セーブディレクトリ
SAVE_DIR = os.path.join(os.environ['HOME'], "documents/hawaii_timelapse")
# 取得できなかったフレームをブラックフレームで補完するかどうか
COMPLEMENT = False


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


def _create_timelapse(utc_date) -> str:
    '''  タイムラプスを作成し、
    ビデオファイルのパスを返す
    '''
    _utc_date_str = f'{utc_date:%Y%m%d}'       # ディレクトリの日にちは UTC表記

    # ビデオファイル名は、YYYYmmDD.mp4
    if os.name == 'posix':
        video_out = os.path.join(
            SAVE_DIR, _utc_date_str, f'{_utc_date_str}_timelapse.mp4')
    else:
        raise(NotImplementedError(os.name))

    # ビデオファイルが存在する場合は、削除する
    if os.path.exists(video_out):
        os.remove(video_out)
        print("ビデオファイルを削除 :", video_out)

    _fourcc = cv2.VideoWriter_fourcc(* 'avc1')
    _fps = 30
    _out_HD = cv2.VideoWriter(video_out, _fourcc, _fps, (1920, 1080))

    _yesterday = utc_date - timedelta(days=1)
    _start_time = datetime.combine(_yesterday, time(12))  # 開始時間　ハワイ時間 前日の12:00
    _end_time = _start_time + timedelta(days=1)     # 開始時間　ハワイ時間 今日の12:00

    _black_frame = cv2.imread("black_HD.jpg", cv2.IMREAD_COLOR)

    dt = _start_time
    while(dt < _end_time):
        _filename = f'{dt:%Y%m%d%H%M}_comp.jpg'  # ファイル名は HST表記

        _filepath = os.path.join(SAVE_DIR, _utc_date_str, _filename)

        dt += timedelta(minutes=1)  # 1分ごと
        img = cv2.imread(_filepath, cv2.IMREAD_COLOR)
        if img is None:
            if COMPLEMENT:
                img = _black_frame   # 画像が存在しないので、ブラックフレームで補完する
                print("imreadエラー ブラックフレームで補完する")
            else:
                print("imreadエラー スキップする")
                continue
        print("out.write: ", _filepath)
        _out_HD.write(img)
    _out_HD.release()

    print("create_timelapse 終了", video_out)
    return video_out


def main():
    '''
    タイムラプスを作成する
    '''
    # # タイムラプスを作成する
    utc_date = datetime.now().date() - timedelta(days=1)
    video_in = _create_timelapse(utc_date)

    # # 古いファイルを削除
    # delete_old_files.delete_old_files()

    ic("正常終了", video_in)


if __name__ == "__main__":
    if os.name == 'nt':
        # Windows VSCodeで、ic()の背景色がおかしくなる問題対応
        ic.configureOutput(outputFunction=print)
    main()
