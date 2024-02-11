import json
import os
from dotenv import load_dotenv

#envファイルから環境変数の読み込み
load_dotenv()
YOUTUBE_DATA_API_KEY = os.environ['YOUTUBE_DATA_API_KEY']

JARUJARU_TOWER_CHANNEL_ID = 'UChwgNUWPM-ksOP3BbfQHS5Q'
JARUJARU_ISLAND_CHANNEL_ID = 'UCf-wG6PlxW7rpixx1tmODJw'
YOUTUBE_BASE_URL = 'https://www.googleapis.com/youtube/v3'

playlists = {
    
    'channel':JARUJARU_TOWER_CHANNEL_ID,
    'playlists':[
        {'id': 'PLRdiaanKAFQlJKPO75in2WNF0wKJyo4qe', 'title': '本気ネタ', 'number': 0},
        {'id': 'PLRdiaanKAFQn3LjggPAIk7x2U9Ih2bwRk', 'title': 'バリアフリー字幕つきな奴ら', 'number': 1},
        {'id': 'PLRdiaanKAFQmfZIu7THIitRCqrqnn8_SW', 'title': '会社員な奴ら', 'number': 2},
        {'id': 'PLRdiaanKAFQnNX7v2DO4t7vNgvFljziLa', 'title': '医者な奴ら', 'number': 3}, 
        {'id': 'PLRdiaanKAFQmx9QCmyWPIuo2gaHA15IV9', 'title': '学校の先生な奴ら', 'number': 4}, 
        {'id': 'PLRdiaanKAFQlWix5IgBtgxEY91fWNA4Fn', 'title': '５億回記念！本気ネタ！', 'number': 5}, 
        {'id': 'PLRdiaanKAFQmfcVpdsVLoQUpdtSNojOKK', 'title': '【作業用ネタ】耳でジャルジャルを楽しむ奴', 'number': 6}, 
        {'id': 'PLRdiaanKAFQmsC6fP_St6EgaSMeOMDGOS', 'title': '【入門編】ジャルジャルに興味湧いてきた奴', 'number': 7},
        {'id': 'PLRdiaanKAFQk30MsMqvwPyASD9tqKUInG', 'title': 'リモートネタ生配信', 'number': 8}, 
        {'id': 'PLRdiaanKAFQl5ERDgJHx2ZRKCcIl-I8fz', 'title': '１０８本！煩悩ネタ！', 'number': 9}, 
        {'id': 'PLRdiaanKAFQnFRkJiuhMVLAC-UdYjYk8k', 'title': '３億回記念！本気ネタ！', 'number': 10}, 
        {'id': 'PLRdiaanKAFQlq6BMs519ix5km2nz49zMb', 'title': '2億回記念!本気ネタ!', 'number': 11}, 
        {'id': 'PLRdiaanKAFQl3AKF2ruBbuTKj0dZnVqaJ', 'title': '１億回記念！本気ネタ！', 'number': 12},
        {'id': 'PLRdiaanKAFQliJh8AMvlV6t7NBrmNXCo-', 'title': 'JARUJARUTOWER', 'number': 13}, 
        {'id': 'PLRdiaanKAFQlHOVLx1AHe2vIpjlakfkAN', 'title': 'ジャルジャルコント', 'number': 14}
    ]
}