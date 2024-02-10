import os
from fastapi import APIRouter
from apiclient.discovery import build

from dotenv import load_dotenv

youtube_router = APIRouter()

#環境変数の読み込み
load_dotenv()
api = os.environ['JARUJARU_CHANNEL_ID']

@youtube_router.get("/youtube/", tags=["youtube"])
async def root():
    return {"root": "youtube"}

@youtube_router.get("/youtube/playlists/{id}", tags=["youtube"])
async def playlists(id):
    return {"id": id}