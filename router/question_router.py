import os
import sys
sys.path.append('../')
import config
from fastapi import APIRouter, HTTPException,status,Query
from fastapi.responses import JSONResponse,Response
import requests
from typing import List
from yt_dlp import YoutubeDL
import random
import io
from pydub import AudioSegment

def get_infomation_of_playlist(playlist_url):
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

def download_mp3(playlist_url,playlist_items,max_downloads=1):
    #オプションを指定
    ydl_opts = {
            'outtmpl' : './origin_mp3/%(id)s.%(ext)s',
            'format' : 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  
                'preferredcodec': 'mp3',  #変換したい形式を指定
                'preferredquality': '192' #ビットレートを指定
            }],
            'playlist_items': str(playlist_items)
    }
    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=True)
        return playlist_info

question_endpoint = APIRouter()

@question_endpoint.get("/question/", tags=["question"])
def root():
    return {"root": "question-endpoint"}

#まとめて問題を作成する
@question_endpoint.get("/question/questions", tags=["question"])
def questions(playlist_id: List[str] = Query(..., title="Playlist IDs", description="IDs of the playlists to retrieve"),
              num:int=Query(...,title="Number", description="Number Of Questions")):
    if playlist_id is None or num is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both 'num' and 'playlist_id' parameters are required.")

    id_list = []
    print('start')
    for _ in range(num):
        selected_playlist_id = random.choice(playlist_id)
        playlist_url = f"https://www.youtube.com/playlist?list={selected_playlist_id}"
        try:
            download_mp3(playlist_url=playlist_url,max_downloads=1)
        except Exception as e:
            print(e)
            
    
    if(len(id_list)==0):
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while creating the question"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)

    return JSONResponse(status_code=status.HTTP_200_OK, content=id_list)


#単体の問題を作る
@question_endpoint.get("/question/download", tags=["question"])
def download(playlist_id: List[str] = Query(..., title="Playlist IDs", description="IDs of the playlists to retrieve")):
    if playlist_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both 'num' and 'playlist_id' parameters are required.")

        
    selected_playlist_id = random.choice(playlist_id)
    playlist_url = f"https://www.youtube.com/playlist?list={selected_playlist_id}"
    #プレイリストの情報を取得
    try:
        info=get_infomation_of_playlist(playlist_url=playlist_url)
    except Exception as e:
        print(e)
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while creating the question"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)

    playlist_count = info.get('playlist_count')
    
    if(playlist_count is None):
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while creating the question"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)
       
        
    selected_index = random.randint(1,playlist_count)
    result_info = download_mp3(playlist_url=playlist_url,playlist_items=selected_index)
    
    if(len(result_info.get('entries'))>0):
        video_info = result_info.get('entries')[0]
        id = video_info.get('id')
        title = video_info.get('title')
        question_dict = {
            'id':id,
            'title':title,
            'original_file_path':f"./origin_mp3/{id}.mp3"
        }
        # ローカルのMP3ファイルをバイナリモードで読み込み
            
        return JSONResponse(status_code=status.HTTP_200_OK, content=question_dict)
    
    error_message = {
        "message": "Internal Server Error",
        "domain": "global",
        "reason": "An error occurred while creating the question"
     }
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)

@question_endpoint.get("/question/fetch/{video_id}", tags=["question"])
def fetch(video_id):
    mp3_path = f"./origin_mp3/{video_id}.mp3"
     # ファイルが存在するか確認します
    if not os.path.exists(mp3_path):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="File not found")

    origimnal_mp3 = AudioSegment.from_file(file=mp3_path, format="mp3")
    
    if(origimnal_mp3.duration_seconds>120):
        trimmed_mp3 = origimnal_mp3[:120*1000]
    else:
        trimmed_mp3 = origimnal_mp3
    
    try:
        # trimmed_mp3.export(f"./trimmed_mp3/{video_id}.mp3", format="mp3")
            # BytesIO を使用してファイルをメモリ上で処理
        return_buttfer = io.BytesIO()
        trimmed_mp3.export(return_buttfer, format="mp3")
        return_buttfer.seek(0)
        return Response(content=return_buttfer.getvalue(), media_type="audio/mp3")
        
    except:
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while creating the question"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)