import sys
sys.path.append('../')
import config
from fastapi import APIRouter, HTTPException,status,Query
import json
from fastapi.responses import JSONResponse
import requests
from typing import List
import random

youtube_endpoint = APIRouter()

@youtube_endpoint.get("/youtube/", tags=["youtube"])
def root():
    return {"root": "youtube-endpoint"}

@youtube_endpoint.get("/youtube/playlists/{channel_id}", tags=["youtube"])
def playlists(channel_id):
    url = f"{config.YOUTUBE_BASE_URL}/playlists"
    params = {
        'part': 'snippet',
        'maxResults':100,
        'channelId': channel_id,
        'key': config.YOUTUBE_DATA_API_KEY
    }
    response = requests.get(url, params=params)
    if(response.status_code==status.HTTP_200_OK):
        items = response.json().get('items')
        res_endpoint = {}
        for item in items:
            id = item.get('id')
            playlist_url = f"{config.YOUTUBE_BASE_URL}/playlistItems"
            params = {
                'part': 'snippet',
                'maxResults':100,
                'playlistId': id,
                'key': config.YOUTUBE_DATA_API_KEY
            }
            results_in_tower = config.JARUJARU_TOWER_PLAYLISTS.get(id)
            results_in_island = config.JARUJARU_ISLAND_PLAYLISTS.get(id)
            if(results_in_tower is None and results_in_island is None):
                continue
            response = requests.get(playlist_url, params=params)
            if(response.status_code==status.HTTP_200_OK):
                total_results = response.json().get('pageInfo').get('totalResults')
                tmp_value = {
                    'title':item.get('snippet').get('title'),
                    'total_results':total_results
                }
                res_endpoint[id] = tmp_value
        return JSONResponse(status_code=status.HTTP_200_OK, content=res_endpoint)
    else:
        try:
            error_content = json.loads(response.content.decode('utf-8')).get('error')
            error_code = error_content.get('code')
            error_message = error_content.get('errors')
            return JSONResponse(status_code=error_code, content=error_message)
        except:
            error_message = {
                    "message": "Internal Server Error",
                    "domain": "global",
                    "reason": "Internal Server Error"
                }
            
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)
        
@youtube_endpoint.get("/youtube/playlistItems/", tags=["youtube"])
def playlist_items(num: int = Query(..., title="Number of items", description="The number of items to retrieve"),
                         playlist_id: List[str] = Query(..., title="Playlist IDs", description="IDs of the playlists to retrieve")):
    if num is None or playlist_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both 'num' and 'playlist_id' parameters are required.")
    
    url = f"{config.YOUTUBE_BASE_URL}/playlistItems"

    all_items = []
    is_success = True
    for id in playlist_id:
        results_in_tower = config.JARUJARU_TOWER_PLAYLISTS.get(id)
        results_in_island = config.JARUJARU_ISLAND_PLAYLISTS.get(id)
        if(results_in_tower is None and results_in_island is None):
            error_message = {
                "message": "Bad Request",
                "domain": "global",
                "reason": "playlist_id is invalid"
            }
            
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)
            
        params = {
            'part': 'snippet',
            'maxResults':50,
            'playlistId': id,
            'key': config.YOUTUBE_DATA_API_KEY
        }
        response = requests.get(url, params=params)

        if(response.status_code==status.HTTP_200_OK):
            next_page_token = response.json().get('nextPageToken')
            total_results = response.json().get('pageInfo').get('totalResults')
            results_per_page = response.json().get('pageInfo').get('resultsPerPage')
            items = response.json().get('items')
            all_items.extend(items)
            
            #リクエストを追加で送る回数
            page_count = int(total_results/results_per_page)
            #追加の分だけリクエストを送る
            for _ in range(page_count):
                if(next_page_token is None or response.status_code!=status.HTTP_200_OK):
                    is_success = False
                    break
                params = {
                    'part': 'snippet',
                    'maxResults':50,
                    'playlistId': playlist_id[0],
                    'key': config.YOUTUBE_DATA_API_KEY,
                    'pageToken':next_page_token
                }
                response = requests.get(url, params=params)
                next_page_token = response.json().get('nextPageToken')
                items = response.json().get('items')
                all_items.extend(items)
        else:
            is_success = False
            break

    if(is_success):
        random.shuffle(all_items)
        if(len(all_items)<num):
            content = {
                'num':len(all_items),
                'items':all_items
            }
        else:
            content = {
                'num':num,
                'items':all_items[0:num]
            }
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    else:
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while creating the question"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)

@youtube_endpoint.get("/youtube/playlistInfo/{playlist_id}", tags=["youtube"])
def playlist_info(playlist_id):
    results_in_tower = config.JARUJARU_TOWER_PLAYLISTS.get(playlist_id)
    results_in_island = config.JARUJARU_ISLAND_PLAYLISTS.get(playlist_id)
    if(results_in_tower is None and results_in_island is None):
            error_message = {
                "message": "Bad Request",
                "domain": "global",
                "reason": "playlist_id is invalid"
            }
            
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)
    
    url = f"{config.YOUTUBE_BASE_URL}/playlistItems"
    params = {
        'part': 'snippet',
        'maxResults':1,
        'playlistId': playlist_id,
        'key': config.YOUTUBE_DATA_API_KEY
    }
    response = requests.get(url, params=params)
    if(response.status_code==status.HTTP_200_OK):
        total_results = response.json().get('pageInfo').get('totalResults')
        
        content = {
            'playlist_id':playlist_id,
            'total_results':total_results
        }
        
        return JSONResponse(status_code=status.HTTP_200_OK,content=content)
    else:
        error_message = {
            "message": "Internal Server Error",
            "domain": "global",
            "reason": "An error occurred while getting infomation"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_message)
    