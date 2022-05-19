import requests
from datetime import datetime, timedelta
import pytz
from icecream import ic
import os
import threading
import schedule
import time

JST = pytz.timezone('Asia/Tokyo')
HST = pytz.timezone('US/Hawaii')
UTC = pytz.timezone("UTC")


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class TwilightTime(Singleton):

    def __new__(cls):
        if not cls._instance:
            super().__new__(cls)
            # ======== 初期化 ======== #  
            cls.update(JST)
            # ======== 初期化 ======== #  
        return cls._instance

    def __init__(self):
        pass
    

    def update(self, timezone=JST):
        ''' すばる天文台の天文薄明時間を更新する
            ただし、標高は 0m。
        '''
        # https://sunrise-sunset.org/api
        _url = "https://api.sunrise-sunset.org/json?date=today&formatted=0&lat=19.8254376&lng=-155.4759826"

        _response = requests.get(_url)
        _jsonData = _response.json()

        _atb_str = _jsonData['results']['astronomical_twilight_begin']
        _ate_str = _jsonData['results']['astronomical_twilight_end']

        TwilightTime.ate = datetime.strptime(_ate_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone) # 薄明終了（当日）
        TwilightTime.obs_start = TwilightTime.ate - timedelta(days=1, minutes=10) # 観測開始：薄明開始10分前（前日）
        TwilightTime.ate_prev1d = TwilightTime.ate - timedelta(days=1) # 薄明終了（前日）
        TwilightTime.atb = datetime.strptime(_atb_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone)
        TwilightTime.obs_stop = TwilightTime.atb + timedelta(minutes=10) # 観測終了：薄明開始から10分後
        TwilightTime.obs_terminate = TwilightTime.atb + timedelta(minutes=30) # 薄明開始から30分後

        print('観測開始、薄明終了10分前（前日）', f'{TwilightTime.obs_start:%H:%M:%S %Z}')
        print('薄明終了', f'{TwilightTime.ate_prev1d:%H:%M:%S %Z}')
        print('薄明開始', f'{TwilightTime.atb:%H:%M:%S %Z}')
        print('観測終了、薄明開始から10分後', f'{TwilightTime.obs_stop:%H:%M:%S %Z}')
        print('プログラム終了、薄明開始から30分後', f'{TwilightTime.obs_terminate:%H:%M:%S %Z}')


    
def is_night(self) -> bool:
    ''' ハワイ・マウナケアの天文学的夜かどうかを判定する
    '''
    now = datetime.now().astimezone(JST)
    self = TwilightTime.ate_prev1d < now and now < TwilightTime.atb_plus10
    return self

# ======== スケジューラ ========
def start_observation(self):
    print("観測開始", TwilightTime().ate)

def stop_observation(self):
    print("観測終了", TwilightTime().atb_plus10)
    self._is_night = False

def end_program(self):
    print("プログラム終了", TwilightTime().atb_plus30)


def scheduler():
    _obs_start_time = f'{TwilightTime().obs_start:%H:%M}'
    _obs_stop_time = f'{TwilightTime().obs_stop:%H:%M}'
    _obs_terminate_time = f'{TwilightTime().obs_terminate:%H:%M}'
    schedule.every().day.at(_obs_start_time).do(start_observation)  # 観測開始
    schedule.every().day.at(_obs_stop_time).do(stop_observation)  # 観測終了
    schedule.every().day.at(_obs_terminate_time).do(end_program)  # プログラム終了
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1分 スリープ

        
def main():
    ''' 別スレッドでスケジューラを起動
    '''
    thread_scheduler = threading.Thread(target=scheduler)
    thread_scheduler.start()
    thread_scheduler.join()


if __name__ == "__main__":
    if os.name == 'nt':
        # Windows VSCodeで、ic()の背景色がおかしくなる問題対応
        ic.configureOutput(outputFunction=print)
    main()
