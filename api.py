import sys
import os
import uvicorn

from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import core

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/update_score/")
def update_score(url: str, score: int, playtime: int = 0) -> dict:
    if url != "" and score != "":
        try:
            gamee = core.GameeHacker(url, score, playtime)
            r = gamee.send_score()
            return {"status": 200, "message": "Score updated successfully"}
        except Exception as e:
            return {"status": 400, "message": "Score update failed"}
    return {"status": 400, "message": "Either url or score is missing"}
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)