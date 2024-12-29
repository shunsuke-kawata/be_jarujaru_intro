import os
from dotenv import load_dotenv

#envファイルから環境変数の読み込み
load_dotenv()

PORT = os.environ['BACKEND_PORT']

FRONTEND_SERVER_URL = os.environ['FRONTEND_SERVER_URL']
BACKEND_SERVER_URL = os.environ['BACKEND_SERVER_URL']
FIREBASE_CREDENTIALS_PATH = os.environ['FIREBASE_CREDENTIALS_PATH']

#firebase認証情報の絶対パス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDENTIALS_ABS_PATH = os.path.join(BASE_DIR, FIREBASE_CREDENTIALS_PATH)

JARUJARU_TOWER_CHANNEL_ID = 'UChwgNUWPM-ksOP3BbfQHS5Q'
JARUJARU_ISLAND_CHANNEL_ID = 'UCf-wG6PlxW7rpixx1tmODJw'
YOUTUBE_BASE_URL = 'https://www.googleapis.com/youtube/v3'

#更新を行う必要がある
JARUJARU_TOWER_PLAYLISTS = {
  "PLRdiaanKAFQl3AKF2ruBbuTKj0dZnVqaJ": {"title": "１億回記念！本気ネタ！","group":1},
  "PLRdiaanKAFQlq6BMs519ix5km2nz49zMb": {"title": "2億回記念!本気ネタ!","group":1},
  "PLRdiaanKAFQnFRkJiuhMVLAC-UdYjYk8k": {"title": "３億回記念！本気ネタ！","group":1},
  "PLRdiaanKAFQlWix5IgBtgxEY91fWNA4Fn": {"title": "５億回記念！本気ネタ！","group":1},
  "PLRdiaanKAFQlHOVLx1AHe2vIpjlakfkAN": {"title": "ジャルジャルコント","group":1},
  "PLRdiaanKAFQl5ERDgJHx2ZRKCcIl-I8fz": {"title": "１０８本！煩悩ネタ！","group":1},
  "PLRdiaanKAFQk30MsMqvwPyASD9tqKUInG": {"title": "リモートネタ生配信","group":1},
  "PLRdiaanKAFQmfZIu7THIitRCqrqnn8_SW": {"title": "会社員な奴ら","group":1},
  "PLRdiaanKAFQnNX7v2DO4t7vNgvFljziLa": {"title": "医者な奴ら","group":1},
  "PLRdiaanKAFQmx9QCmyWPIuo2gaHA15IV9": {"title": "学校の先生な奴ら","group":1},
  "PLRdiaanKAFQmfcVpdsVLoQUpdtSNojOKK": {"title": "耳でジャルジャルを楽しむ奴","group":1},
  "PLRdiaanKAFQmsC6fP_St6EgaSMeOMDGOS": {"title": "ジャルジャルに興味湧いてきた奴","group":1},
  "PLRdiaanKAFQliJh8AMvlV6t7NBrmNXCo-": {"title": "JARUJARUTOWER","group":1},
  "PLRdiaanKAFQlJKPO75in2WNF0wKJyo4qe": {"title": "本気ネタ","group":2},
  "PLRdiaanKAFQn3LjggPAIk7x2U9Ih2bwRk": {"title": "バリアフリー字幕つきな奴ら","group":3},
}

#更新を行う必要がある
JARUJARU_ISLAND_PLAYLISTS = {
  "PL52aY2wM99ikod2rVdEk05_oUPTv_hBBz": {"title": "朝メシ食う奴","group":0},
  "PL52aY2wM99incJsJwecCThKHP7oZs-ezp": {"title": "日常撮る奴","group":0},
  "PL52aY2wM99ikxrZXoP5wYvT-JHjtrouh9": {"title": "リモートする奴","group":0},
  "PL52aY2wM99inbkD2YXOiduokWKwk9qK1j": {"title": "真夜中に電話する奴","group":0},
  "PL52aY2wM99ilIbNCybsQ41s8zUxnRG7xC": {"title": "バリアフリー字幕ついてる奴","group":0},
  "PL52aY2wM99inhauDD7A5BBqbhBl7k08VC": {"title": "ハズレの先生が担任になった奴","group":0},
  "PL52aY2wM99im0j6U6dUMuwjG8ZDhFvUkC": {"title": "第17回祇園お笑い新人大賞","group":0},
  # "PL52aY2wM99ikQ36hBB6OunvfOFjWEi8Th": {"title": "ウルフルズに影響されてる奴",},
  # "PL52aY2wM99invD0-yZrnK03Ditpnjj7o9": {"title": "スターと出会う奴",},
  # "PL52aY2wM99imyKBkFK8wRzOMe6dKeEX9e": {"title": "変な司会者の奴",},
}


#groupのルール
# 1.『』内にタイトルがある
# 3.分岐が必要
