import sys
sys.path.append('../')
import config
from fastapi import APIRouter,status
import json
from fastapi.responses import JSONResponse
import requests

youtube_router = APIRouter()

@youtube_router.get("/youtube/", tags=["youtube"])
async def root():
    return {"root": "youtube"}

@youtube_router.get("/youtube/playlists/{channel_id}", tags=["youtube"])
async def playlists(channel_id):
    url = f"{config.YOUTUBE_BASE_URL}/playlists"
    params = {
        'part': 'snippet',
        'maxResults':100,
        'channelId': channel_id,
        'key': config.YOUTUBE_DATA_API_KEY
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
        try:
            error_content = json.loads(response.content.decode('utf-8')).get('error')
            error_code = error_content.get('code')
            error_message = error_content.get('errors')
            return JSONResponse(status_code=error_code, content=error_message)
        except:
            error_message = [
                {
                    "message": "Internal Server Error",
                    "domain": "global",
                    "reason": "Internal Server Error"
                }
            ]
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=json.loads(error_message))
        
@youtube_router.get("/youtube/videos/", tags=["youtube"])
async def videos(playlist_ids):
    url = f"{config.YOUTUBE_BASE_URL}/playlistItems"
    params = {
        'part': 'snippet',
        'maxResults':3,
        'playlistId': playlist_ids,
        'key': config.YOUTUBE_DATA_API_KEY
    }
    response = requests.get(url, params=params)

    if(response.status_code==200):
        next_page_token = response.json().get('nextPageToken')
        print(next_page_token)
        while(True):
            if(next_page_token is None):
                break
            params = {
                'part': 'snippet',
                'maxResults':20,
                'playlistId': playlist_ids,
                'key': config.YOUTUBE_DATA_API_KEY,
                'pageToken':next_page_token
            }
            response = requests.get(url, params=params)
            next_page_token = response.json().get('nextPageToken')
            print(next_page_token)
            
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.json())
    else:
        error_message = [
            {
                "message": "Internal Server Error",
                "domain": "global",
                "reason": "Internal Server Error"
            }
        ]
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=json.loads(error_message))