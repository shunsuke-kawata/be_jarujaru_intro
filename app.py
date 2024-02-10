import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

api = os.environ['YOUTUBE_DATA_API_KEY']
@app.get("/")
def read_root():
    return {"api": api }

if __name__ == "__main__":
    uvicorn.run(app,port=8000)