import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from router.youtube import youtube_router

#環境変数の読み込み
load_dotenv()

app = FastAPI()
app.include_router(youtube_router)


api = os.environ['YOUTUBE_DATA_API_KEY']
@app.get("/")
async def root():
    return {"api": api }

if __name__ == "__main__":
    uvicorn.run(app,port=8000)