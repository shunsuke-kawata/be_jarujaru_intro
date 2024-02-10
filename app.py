from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"app": "jarujaru"}

if __name__ == "__main__":
    uvicorn.run(app,port=8000)