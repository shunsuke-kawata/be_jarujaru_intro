import os
from fastapi import FastAPI
import uvicorn

from router.youtube_router import youtube_endpoint
from router.question_router import question_endpoint

#アプリケーションの作成,エンドポイントの追加
app = FastAPI()
app.include_router(youtube_endpoint)
app.include_router(question_endpoint)

@app.get("/")
async def root():
    return {"root": "jarujaru-intro"}

if __name__ == "__main__":
    uvicorn.run("app:app",port=8000,reload=True)