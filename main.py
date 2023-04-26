from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = "2022-08-09"

birthday = "05-20"
city = "遵义"
app_id = "wx54bc83a8fc2ee41e"
app_secret = "cc354d95d58fda3fd090711bdb3b8884"

user_id = "oeDkj5-GP77_wanLHDs40LBrYEn4"
template_id = "ar9SNR_D9jbo-xaSx6Gz5DDV_zefanORzMbpxBOpW1g"



def get_weather():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=0aaf3d9a8ebe08b6709afe5661717245&city=520300"
  res = requests.get(url).json()
  weather = res['lives'][0]
  print("reporttime=====>",weather['reporttime'])
  print("math=====>",math.floor(int(weather['temperature'])))
  return weather['weather'], math.floor(int(weather['temperature']))

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return "一想到你，我这张脸就泛起微笑"
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"city":{"value":city, "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "temperature":{"value":temperature, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
