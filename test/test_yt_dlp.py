import json
import time
import csv
from yt_dlp import YoutubeDL
import io
import sys
sys.path.append('../')
import config
from router import question_router

def download_audio_from_playlist(playlist_url, index):
    # オプションを指定
    ydl_opts = {
        'format': 'bestaudio',  # 最適な形式を選択
        'outtmpl': '-',  # 標準出力にダウンロード
        'playlist_items': str(index)  # プレイリストからのインデックスを指定
    }

    with YoutubeDL(ydl_opts) as ydl:
        # ダウンロードを実行し、標準出力からデータを読み込む
        result = ydl.extract_info(playlist_url, download=True)
        print(result)
        # audio_bytes = io.BytesIO(result['formats'][0]['data'])

    return result
def count_videos_in_playlist(playlist_url):
    # オプションを指定
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        # プレイリストから情報を取得
        playlist_info = ydl.extract_info(playlist_url, download=False)
        # プレイリスト内の動画数を取得
        num_videos = playlist_info.get('entries', [])
        return len(num_videos)

# 使用例
# playlist_url = 'https://www.youtube.com/playlist?list=PLRdiaanKAFQliJh8AMvlV6t7NBrmNXCo-'
# num_videos_in_playlist = count_videos_in_playlist(playlist_url)
# print("Number of videos in playlist:", num_videos_in_playlist)
# index_to_download = 1  # ダウンロードしたい動画のインデックスを指定
# audio_bytes = download_audio_from_playlist(playlist_url, index_to_download)

# for i in config.JARUJARU_ISLAND_PLAYLISTS:
#     playlist_url = f"https://www.youtube.com/playlist?list={i}"
#     info = question_router.get_infomation_of_playlist(playlist_url=playlist_url)
#     print(info)
#     time.sleep(1)
#     header = ['id',info.get('id')]
#     with open(f"./island/{info.get('title')}.csv", 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(header)
#         entries = info.get('entries')
#         for index,entry in enumerate(entries):
#             tmp = [str(index+1),entry.get('title')]
#             writer.writerow(tmp)
            
#     with open(f"./island/{info.get('title')}.json", "w",encoding='utf-8') as f:
#         json.dump(info, f, indent=2,ensure_ascii=False)

path = './island/朝メシ食う奴.csv'

with open(path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if(row[0]=='id'):
            continue
        print(row[0],question_router.get_answer_title(row[1],4))