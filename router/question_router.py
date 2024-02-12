import sys
sys.path.append('../')
import config
from fastapi import APIRouter, HTTPException,status,Query
from fastapi.responses import JSONResponse
import requests
from typing import List
from yt_dlp import YoutubeDL

question_endpoint = APIRouter()

@question_endpoint.get("/question/", tags=["question"])
def root():
    return {"root": "question-endpoint"}

@question_endpoint.get("/question/create/", tags=["question"])
def create(num: int = Query(..., title="Number of items", description="The number of items to retrieve"),
                 playlist_id: List[str] = Query(..., title="Playlist IDs", description="IDs of the playlists to retrieve"),
                 is_logined:bool = Query(..., title="Option of creating questions", description="")):
    if num is None or playlist_id is None or is_logined is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both 'num' and 'playlist_id' parameters are required.")
    
    url = f"{config.BACKEND_SERVER_URL}/youtube/playlistItems/"
    print(url)
    params = {
        'playlist_id':playlist_id,
        'num':num
    }
    print(params)
    response = requests.get(url,params=params)
    if(response.status_code==status.HTTP_200_OK):
        num = response.json().get('num')
        items = response.json().get('items')
        
        ydl_options = {'format': 'best'}
        if(is_logined):
            return JSONResponse(status_code=status.HTTP_200_OK, content='音声ファイルを返す')
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.json())
            
    else:
        return JSONResponse(status_code=response.status_code, content=response.json())
    