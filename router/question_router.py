import io
import os
import aiofiles
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse, StreamingResponse
import config
from pydub import AudioSegment
import random
import tempfile
from typing import List
from utils.util import get_answer_title, get_infomation_of_playlist, download_mp3

# エンドポイントの作成
question_endpoint = APIRouter()

@question_endpoint.get("/question/download", tags=["question"])
async def download(playlist_id: List[str] = Query(..., title="Playlist IDs")):
    if not playlist_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist IDs are required.")

    selected_playlist_id = random.choice(playlist_id)
    playlist_url = f"https://www.youtube.com/playlist?list={selected_playlist_id}"

    try:
        info = get_infomation_of_playlist(playlist_url=playlist_url)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "message": "Failed to fetch playlist information",
            "reason": str(e)
        })

    playlist_count = info.get('playlist_count')
    if not playlist_count:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid playlist data")

    selected_index = random.randint(1, playlist_count)
    result_info = download_mp3(playlist_url=playlist_url, playlist_items=selected_index)

    if len(result_info.get('entries', [])) > 0:
        video_info = result_info['entries'][0]
        video_id = video_info['id']
        title = video_info['title']
        if(config.JARUJARU_TOWER_PLAYLISTS.get(selected_playlist_id) is not None):
            group = config.JARUJARU_TOWER_PLAYLISTS.get(selected_playlist_id).get('group')

        elif(config.JARUJARU_ISLAND_PLAYLISTS.get(selected_playlist_id) is not None):
            group = config.JARUJARU_ISLAND_PLAYLISTS.get(selected_playlist_id)

        if not group:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Group not found")

        answer_title = get_answer_title(original_title=title, group=group)
        question_dict = {
            'id': video_id,
            'title': answer_title,
            'original_file_path': f"./origin_mp3/{video_id}.mp3"
        }
        print(question_dict)

        return JSONResponse(status_code=status.HTTP_200_OK, content=question_dict)

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No entries found in the playlist")

#ダウンロードしたデータをバイト形式で返却する
@question_endpoint.get("/question/fetch/{video_id}", tags=["question"])
async def fetch(video_id: str):
    mp3_path = f"./origin_mp3/{video_id}.mp3"

    if not os.path.exists(mp3_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # 一時ファイルを作成して処理
    try:
        async with aiofiles.open(mp3_path, mode="rb") as file:
            file_data = await file.read()

        audio = AudioSegment.from_file(io.BytesIO(file_data), format="mp3")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            audio.export(tmp_file.name, format="mp3")
            tmp_file_path = tmp_file.name

        # ファイルをストリームとして返す
        async def file_streamer():
            async with aiofiles.open(tmp_file_path, mode="rb") as tmp_file:
                while chunk := await tmp_file.read(1024):
                    yield chunk
            os.remove(tmp_file_path)  # 一時ファイルの削除

        return StreamingResponse(file_streamer(), media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)  # 元のMP3ファイルを削除