import json
import os
from dotenv import load_dotenv

#envファイルから環境変数の読み込み
load_dotenv()

YOUTUBE_DATA_API_KEY = os.environ['YOUTUBE_DATA_API_KEY']
BACKEND_SERVER_URL = os.environ['BACKEND_SERVER_URL']

JARUJARU_TOWER_CHANNEL_ID = 'UChwgNUWPM-ksOP3BbfQHS5Q'
JARUJARU_ISLAND_CHANNEL_ID = 'UCf-wG6PlxW7rpixx1tmODJw'
YOUTUBE_BASE_URL = 'https://www.googleapis.com/youtube/v3'


JARUJARU_TOWER_PLAYLISTS = {
    'PLRdiaanKAFQlJKPO75in2WNF0wKJyo4qe':{ 'title': '本気ネタ', 'number': 0},
    'PLRdiaanKAFQn3LjggPAIk7x2U9Ih2bwRk':{ 'title': 'バリアフリー字幕つきな奴ら', 'number': 1},
    'PLRdiaanKAFQmfZIu7THIitRCqrqnn8_SW':{ 'title': '会社員な奴ら', 'number': 2},
    'PLRdiaanKAFQnNX7v2DO4t7vNgvFljziLa':{ 'title': '医者な奴ら', 'number': 3}, 
    'PLRdiaanKAFQmx9QCmyWPIuo2gaHA15IV9':{ 'title': '学校の先生な奴ら', 'number': 4}, 
    'PLRdiaanKAFQlWix5IgBtgxEY91fWNA4Fn':{ 'title': '５億回記念！本気ネタ！', 'number': 5}, 
    'PLRdiaanKAFQmfcVpdsVLoQUpdtSNojOKK':{ 'title': '【作業用ネタ】耳でジャルジャルを楽しむ奴', 'number': 6}, 
    'PLRdiaanKAFQmsC6fP_St6EgaSMeOMDGOS':{ 'title': '【入門編】ジャルジャルに興味湧いてきた奴', 'number': 7},
    'PLRdiaanKAFQk30MsMqvwPyASD9tqKUInG':{ 'title': 'リモートネタ生配信', 'number': 8}, 
    'PLRdiaanKAFQl5ERDgJHx2ZRKCcIl-I8fz':{ 'title': '１０８本！煩悩ネタ！', 'number': 9}, 
    'PLRdiaanKAFQnFRkJiuhMVLAC-UdYjYk8k':{ 'title': '３億回記念！本気ネタ！', 'number': 10}, 
    'PLRdiaanKAFQlq6BMs519ix5km2nz49zMb':{ 'title': '2億回記念!本気ネタ!', 'number': 11}, 
    'PLRdiaanKAFQl3AKF2ruBbuTKj0dZnVqaJ':{ 'title': '１億回記念！本気ネタ！', 'number': 12},
    'PLRdiaanKAFQliJh8AMvlV6t7NBrmNXCo-':{ 'title': 'JARUJARUTOWER', 'number': 13}, 
    'PLRdiaanKAFQlHOVLx1AHe2vIpjlakfkAN':{ 'title': 'ジャルジャルコント', 'number': 14}
}

JARUJARU_ISLAND_PLAYLISTS = {
    'PL52aY2wM99ilIbNCybsQ41s8zUxnRG7xC':{ 'title': 'バリアフリー字幕ついてる奴', 'number': 0},
    'PL52aY2wM99inhauDD7A5BBqbhBl7k08VC':{ 'title': 'ハズレの先生が担任になった奴', 'number': 1},
    'PL52aY2wM99ikQ36hBB6OunvfOFjWEi8Th':{ 'title': 'ウルフルズに影響されてる奴', 'number': 2},
    'PL52aY2wM99im0j6U6dUMuwjG8ZDhFvUkC':{ 'title': '第17回祇園お笑い新人大賞', 'number': 3}, 
    'PL52aY2wM99ilMHtFDlVRvRO9e8Kvmj5n8':{ 'title': 'ゼロから新ネタ作る奴', 'number': 4},
    'PL52aY2wM99invD0-yZrnK03Ditpnjj7o9':{ 'title': 'スターと出会う奴', 'number': 5}, 
    'PL52aY2wM99ikxrZXoP5wYvT-JHjtrouh9':{ 'title': 'リモートする奴', 'number': 6},
    'PL52aY2wM99inbkD2YXOiduokWKwk9qK1j':{ 'title': '真夜中に電話する奴', 'number': 7},
    'PL52aY2wM99imyKBkFK8wRzOMe6dKeEX9e':{ 'title': '変な司会者の奴', 'number': 8}, 
    'PL52aY2wM99incJsJwecCThKHP7oZs-ezp':{ 'title': '日常撮る奴', 'number': 9}, 
    'PL52aY2wM99ikod2rVdEk05_oUPTv_hBBz':{ 'title': '朝メシ食う奴', 'number': 10}
}