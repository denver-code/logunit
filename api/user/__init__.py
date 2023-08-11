import time
from fastapi import APIRouter, Request
from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel
from api.models.log import SecureLogModel

from app.core.fastjwt import FastJWT

load_dotenv()

class User(BaseModel):
    username: str
    password: str

user_router = APIRouter()

@user_router.post("/")
async def authorise_user(payload: User, request: Request):
    if payload.username == getenv("root_username") and payload.password == getenv("root_password"):
        token = await FastJWT().encode({
                "username": payload.username,
                "access": 666
            })
        return {"token": token}
    else:
        await SecureLogModel(
            service="internal_auth_api",
            level="critical",
            payload={
                "username": payload.username,
                "password": payload.password,
                "ip": request.client.host,
                "user_agent": request.headers["user-agent"],
            },
            date=time.strftime("%Y-%m-%dT%H:%M:%S"),
        ).save()
        return {"status": "error"}