import json
import os
import time
from bson import ObjectId
from beanie import Document, PydanticObjectId, init_beanie
from app.core.database import db
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()


class LogRequest(BaseModel):
    service: str
    level: str
    payload: dict


class LogModel(Document):
    service: str
    level: str
    payload: dict
    date: str

    class Settings:
        name = "logs"


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db, document_models=[
        LogModel
        ],
    )

@app.post("/log")
async def log(payload: LogRequest):
    log_data = LogModel(
        service=payload.service,
        level=payload.level,
        payload=payload.payload,
        date=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    _reference = (await log_data.save()).id

    return {"reference": str(_reference)}


@app.get("/log/{reference}")
async def get_log(reference: str): 
    return await LogModel.get(PydanticObjectId(reference))
     

@app.get("/logs")
async def get_logs(service: str = None, level: str = None, limit: int = 100, offset: int = 0):
    query = {}
    if service:
        query["service"] = service
    if level:
        query["level"] = level
        
    logs = await LogModel.find(query).to_list(1_000_000_000_000_000)
    total_count = len(logs)
    
    paginated_logs = logs[offset : offset + limit]
    response = {
        "limit": limit,
        "offset": offset,
        "logs": paginated_logs,
        "total_count": total_count,
    }
    return response

