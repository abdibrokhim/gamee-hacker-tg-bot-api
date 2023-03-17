# start
import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django

django.setup()

from app.models import Account
# end

import core
import secrets
import uvicorn

from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_account(username: str, email: str) -> Union[Account, None]:
    try:
        account = Account.objects.get(username=username, email=email)
        if account:
            return account
        else:
            return None
    except Exception as e:
        return None
    

@app.post("/api/regenerate_api_key/")
def generate_new_api_key(username: str, email: str) -> dict:
    if username != "" or email != "":
        account = get_account(username, email)
        if account:
            return {"status": 200, "api_key": account.regenerate_api_key()}
        else:
            return {"status": 400, "message": "Account does not exists"}
    else:
        return {"status": 400, "message": "Either username or email is missing"}
    

@app.get("/api/get_api_key/{username}&{email}")
def get_valid_api_key(username: str, email: str) -> dict:
    if username != "" or email != "":
        account = get_account(username, email)
        if account:
            return {"status": 200, "api_key": account.get_api_key()}
        else:
            return {"status": 400, "message": "Account does not exists"}
    else:
        return {"status": 400, "message": "Either username or email is missing"}


@app.get("/api/get_user_data/{username}&{email}")
def get_user_data(username: str, email: str) -> dict:
    if username != "" or email != "":
        account = get_account(username, email)
        if account:
            return {"status": 200, "username": account.username, "email": account.email, "api_key": account.get_api_key(), "request_count": account.get_request_count(), "created_at": account.created_at}
        else:
            return {"status": 400, "message": "Account does not exists"}
    else:
        return {"status": 400, "message": "Username or API key is missing"}


@app.post("/api/update_score/")
def update_score(api_key: str, url: str, score: int, playtime: int = 0) -> dict:
    if api_key != "":
        account = Account.objects.get(api_key=api_key)
        if account:
            request_count = account.get_request_count()
            if request_count % 100 == 0:
                return {"status": 400, "message": "Request limit exceeded. Please regenerate your API key"}
            if url != "" and score != "":
                try:
                    gamee = core.GameeHacker(url, score, playtime)
                    gamee.send_score()
                    account.increase_request_count()

                    return {"status": 200, "message": "Score updated successfully"}
                except Exception as e:
                    return {"status": 400, "message": "Score update failed"}
            else:
                return {"status": 400, "message": "Either url or score is missing"}
        else:
            return {"status": 400, "message": "Invalid API key"}
    else:
        return {"status": 400, "message": "API key is missing"}
    

@app.post("/api/signup/")
def signup(username: str, email: str) -> dict:
    if username != "" or email != "":
        try:
            account = get_account(username, email)
            if account:
                return {"status": 400, "message": "Account already exists"}
            else:
                account = Account(username=username, email=email, api_key=secrets.token_urlsafe(16))
                account.save()
                return {"status": 200, "message": "Account created successfully"}
        except Exception as e:
            return {"status": 400, "message": "Account creation failed"}
    else:
        return {"status": 400, "message": "Either username or email is missing"}
    

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8080)