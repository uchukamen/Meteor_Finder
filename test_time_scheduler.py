import requests
import json
from datetime import datetime, timedelta
import pytz
from icecream import ic
import os
import time

import threading

JST = pytz.timezone('Asia/Tokyo')
HST = pytz.timezone('US/Hawaii')
UTC = pytz.timezone("UTC")

_run_flag = True    # RUN フラグ

def to_hst(dt) -> datetime:
    ''' ハワイ標準時へ変更
    dt: datetime
    '''
    hst_tz = pytz.timezone("US/Hawaii")
    return dt.astimezone(hst_tz)


def astronomical_twilight_time(timezone):
    ''' すばる天文台の天文薄明(begin, end)を返す
        ただし、標高は 0m。
    '''
    # https://sunrise-sunset.org/api
    url = "https://api.sunrise-sunset.org/json?date=today&formatted=0&lat=19.8254376&lng=-155.4759826"

    # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
    response = requests.get(url)
    jsonData = response.json()

    # response.json()でJSONデータに変換して変数へ保存
    atb_str = jsonData['results']['astronomical_twilight_begin']
    ate_str = jsonData['results']['astronomical_twilight_end']

    atb = datetime.strptime(atb_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone)
    ic(f'{atb:%H:%M:%S %Z}')
    ate = datetime.strptime(ate_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone)
    ic(f'{ate:%H:%M:%S %Z}')

    return (atb, ate)

def is_night():
    '''
    '''
    (atb, ate) = astronomical_twilight_time(JST)
    ate_prev1d = ate - timedelta(days=1)
    now = datetime.now().astimezone(JST)
    ic(ate)
    ic(ate_prev1d)
    ic(now)
    ic(atb)
    if ate_prev1d < now and now < atb:
        return True
    else:
        return False

def scheduler():
    while(True):
        _run_flag = is_night()
        ic(_run_flag)
        time.sleep(10)



def main():
    # ターミネータースレッド
    thread_scheduler = threading.Thread(target=scheduler)
    thread_scheduler.start()
    
    thread_scheduler.join()


if __name__ == "__main__":
    if os.name == 'nt':
        # Windows VSCodeで、ic()の背景色がおかしくなる問題対応
        ic.configureOutput(outputFunction=print)
    main()
