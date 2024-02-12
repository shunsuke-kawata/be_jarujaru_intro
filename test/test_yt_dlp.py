from yt_dlp import YoutubeDL
import random

def download_video_from_playlist(playlist_url, index):
    #オプションを指定
    ydl_opts = {
            'outtmpl' : './output/%(id)s.%(ext)s',
            'format' : 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  
                'preferredcodec': 'mp3',  #変換したい形式を指定
                'preferredquality': '192' #ビットレートを指定
            }],
            'playlist_items':str(index)
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

# プレイリストURLとインデックスを指定してダウンロードします
playlist_url = "https://www.youtube.com/playlist?list=PL52aY2wM99im0j6U6dUMuwjG8ZDhFvUkC"
index_to_download = random.randint(1,5) # ダウンロードしたい動画のインデックスを指定
download_video_from_playlist(playlist_url, index_to_download)