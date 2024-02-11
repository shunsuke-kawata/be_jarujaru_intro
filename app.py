import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from router.youtube import youtube_router

#環境変数の読み込み
load_dotenv()

app = FastAPI()
app.include_router(youtube_router)


@app.get("/")
async def root():
    return {"root": "jarujaru_intro" }

if __name__ == "__main__":
    uvicorn.run("app:app",port=8000,reload=True)