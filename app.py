import os
from fastapi import FastAPI
import uvicorn

import config
from router.youtube_router import youtube_endpoint
from router.question_router import question_endpoint
from fastapi.middleware.cors import CORSMiddleware

#CORSの設定
origins = [
    config.FRONTEND_SERVER_URL,
    config.BACKEND_SERVER_URL,
    "http://localhost",
    "http://localhost:8080",
]

#アプリケーションの作成,エンドポイントの追加
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_endpoint)
app.include_router(question_endpoint)

@app.get("/")
async def root():
    return {"root": "jarujaru-intro"}

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=int(config.PORT),reload=True)