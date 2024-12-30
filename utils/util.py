import base64
import os
import re
from yt_dlp import YoutubeDL,utils
from cryptography.fernet import Fernet
import sys
sys.path.append('../')
import config

#動画音声を取得する関数
def download_mp3(playlist_url:str, playlist_items:int, max_downloads=1):
    # オプションを指定
    ydl_opts = {
        'outtmpl': './origin_mp3/%(id)s.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  
            'preferredcodec': 'mp3',  # 変換したい形式を指定
            'preferredquality': '192'  # ビットレートを指定
        }],
        'playlist_items': str(playlist_items),
        'download_ranges': utils.download_range_func([], [[0.0, 120.0]]),  # 最初の2分間を指定
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=True)
        return playlist_info
    
#プレイリストの情報を返却する関数
def get_infomation_of_playlist(playlist_url:str):
    # オプションを指定
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    #実際のダウンロードは行わない
    with YoutubeDL(ydl_opts) as ydl:
        # プレイリストから情報を取得
        playlist_info = ydl.extract_info(playlist_url, download=False)
        return playlist_info
  
#youtube公式の動画タイトルからネタタイトルを抽出する関数  
def get_answer_title(original_title:str,group:int):
    return_title = ""
    if(group==1):
        match = re.search(r'[『【](.+?)[』】]', original_title)
        if match:
            return_title = match.group(1)
    elif(group==2):
        str_end = original_title[-1]
        if str_end == '】':
            # 開始記号が '】' で終わっている場合、4文字目以降の '】' と '【' の間を抽出
            match = re.search(r'】(.*?)【', original_title[4:])
        elif str_end == '』':
            # '』' で終わっている場合、全体の '『' と '』' の間を抽出
            match = re.search(r'『(.*?)』', original_title)
        else:
            # それ以外の場合、4文字目以降の '】' 以降のすべてを抽出
            match = re.search(r'】(.*)$', original_title[4:])
        
        if match:
           return_title = match.group(1)  # 抽出部分を返す
    elif(group==3):
        match = re.search(r'『(.*?)』', original_title)  # '『' と '』' の間を抽出
        if not match:  # マッチしない場合
            match = re.search(r'】(.*)$', original_title[4:])  # 4文字目以降の '】' 以降を抽出
        
        if match:
            return_title = match.group(1)  # 抽出部分を返す
    elif(group==4):
    # 正規表現で『』の間を優先的に抽出
        match = re.search(r'『(.*?)』', original_title)
        
        if match:
            # 『』が見つかった場合、その中身を返す
            return_title =  match.group(1)
        
        # 『』が見つからない場合、【】の位置を確認
        match = re.search(r'(.*?)【', original_title[4:])
        if match:
            # 4文字目以降で【が見つかった場合、その前の部分を返す
            return_title = original_title[:4] + match.group(1)
        
    elif(group==5):
        pass
    return return_title

def generate_fernet_key_from_env() -> bytes:

    # 環境変数から文字列を取得
    key_str = config.DECRYPTION_KEY
    if not key_str:
        raise ValueError(f"環境変数 '{key_str}' が設定されていません。")

    # 必要に応じて長さを32バイトに調整
    key_bytes = key_str.encode()
    padded_key = key_bytes.ljust(32, b' ')[:32]  # 長さが32バイトになるように調整

    # Base64エンコード
    fernet_key = base64.urlsafe_b64encode(padded_key)
    return fernet_key

def encrypt_string(plaintext:str, key:str)->str:
    
    # Fernetオブジェクトを作成
    f = Fernet(key)
    
        # メッセージをバイト列に変換
    plaintext_bytes = plaintext.encode()

    # メッセージを暗号化
    encrypted_message = f.encrypt(plaintext_bytes)

    #暗号化キーを生成
    
    return encrypted_message

def decrypt_string(encrypted_message:str, key:str)->str:
    # Fernetオブジェクトを作成
    f = Fernet(bytes(key))
    
    # メッセージを復号
    decrypted_message = f.decrypt(encrypted_message)
    
    # バイト列を文字列に変換
    plaintext = decrypted_message.decode()
    
    return plaintext
