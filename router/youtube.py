import os
from fastapi import APIRouter,status
import json
from fastapi.responses import JSONResponse
import requests

from dotenv import load_dotenv

youtube_router = APIRouter()
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"
#環境変数の読み込み
load_dotenv()
API_KEY = os.environ['YOUTUBE_DATA_API_KEY']

@youtube_router.get("/youtube/", tags=["youtube"])
async def root():
    return {"root": "youtube"}

@youtube_router.get("/youtube/playlists/{channel_id}", tags=["youtube"])
async def playlists(channel_id):
    url = f"{YOUTUBE_BASE_URL}/playlists"
    params = {
        'part': 'snippet',
        'maxResults':100,
        'channelId': channel_id,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if(response.status_code==200):
        items = response.json().get('items')
        res_endpoint = []
        for item in items:    
            tmp = {
                'id':item.get('id'),
                'title':item.get('snippet').get('title')
            }
            res_endpoint.append(tmp)
        return JSONResponse(status_code=status.HTTP_200_OK, content=res_endpoint)
    else:
        return JSONResponse(status_code=response.status_code, content=res_endpoint)