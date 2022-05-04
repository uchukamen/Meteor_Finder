import requests
import json
from datetime import datetime
import pytz
from icecream import ic

JST = pytz.timezone('Asia/Tokyo')
HST = pytz.timezone('US/Hawaii')
UTC = pytz.timezone("UTC")


def to_hst(dt) -> datetime:
    ''' ハワイ標準時へ変更
    dt: datetime
    '''
    hst_tz = pytz.timezone("US/Hawaii")
    return dt.astimezone(hst_tz)


# https://sunrise-sunset.org/api
url = "https://api.sunrise-sunset.org/json?date=today&formatted=0&lat=19.8254376&lng=-155.4759826"

# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
response = requests.get(url)

# response.json()でJSONデータに変換して変数へ保存
jsonData = response.json()
sunrise = jsonData['results']['sunrise']
ic(sunrise)
sunset = jsonData['results']['sunset']
ic(sunset)
sunrise = datetime.strptime(sunrise, "%Y-%m-%dT%H:%M:%S%z").astimezone(HST)
ic(f'{sunrise:%H:%M:%S %Z}')
sunset = datetime.strptime(sunset, "%Y-%m-%dT%H:%M:%S%z").astimezone(HST)
ic(f'{sunset:%H:%M:%S %Z}')

atb_str = jsonData['results']['astronomical_twilight_begin']
ate_str = jsonData['results']['astronomical_twilight_end']


atb = datetime.strptime(atb_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(HST)
ic(f'{atb:%H:%M:%S %Z}')
ate = datetime.strptime(ate_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(HST)
ic(f'{ate:%H:%M:%S %Z}')

atb = datetime.strptime(atb_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(JST)
ic(f'{atb:%H:%M:%S %Z}')
ate = datetime.strptime(ate_str, "%Y-%m-%dT%H:%M:%S%z").astimezone(JST)
ic(f'{ate:%H:%M:%S %Z}')




# https://sunrise-sunset.org/api
# url = "https://api.sunrise-sunset.org/json?date=today&formatted=0&lat=19.8254376&lng=-155.4759826"

# リターンデータ
# このJSONオブジェクトは、連想配列（Dict）っぽい感じのようなので
# JSONでの名前を指定することで情報がとってこれる
# print(jsonData['results']['sunrise'])
# {
#     'results':
#     {
#         'sunrise': '3:49:45 PM',
#         'sunset': '4:47:32 AM',
#         'solar_noon':
#         '10:18:39 PM',
#         'day_length': '12:57:47',
#         'civil_twilight_begin': '3:27:46 PM',
#         'civil_twilight_end': '5:09:32 AM',
#         'nautical_twilight_begin': '3:00:27 PM',
#         'nautical_twilight_end': '5:36:51 AM',
#         'astronomical_twilight_begin': '2:32:34 PM',
#         'astronomical_twilight_end': '6:04:44 AM'
#     },
#     'status': 'OK'
# }

