import time
from fastapi import APIRouter, Depends, Request, HTTPException
from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel
from api.models.log import SecureLogModel
from api.models.service import Service, NewService
from random import randint
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
                "access_code": 666
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


@user_router.post("/addService", dependencies=[Depends(FastJWT().login_required)])
async def add_service(payload: NewService):
    payload.name = payload.name.replace(" ", "_")
    
    access_code = randint(1000000, 9999999)
    # if await Service.find_one({"name": payload.name}):
        # raise HTTPException(status_code=409, detail="Service already exists")

    
    
    token = await FastJWT().encode({
        "service_name": payload.name,
        "access": payload.access,
        "access_code": access_code,
    })
    
    _s = await Service.find_one({"name": payload.name})
    if not _s:
        await Service(
            name=payload.name,
            description=payload.description,
            access=payload.access,
            access_code=access_code
        ).save()
    else:
        _s.access = payload.access
        _s.access_code = access_code
        await _s.save()
        
    return {
        "service_token": token,
        "name": payload.name,
        "access_code": access_code
    }