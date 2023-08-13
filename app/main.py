from beanie import  init_beanie
from api.models.log import LogModel, SecureLogModel
from api.models.service import Service
from app.core.database import db
from fastapi import FastAPI
from api.api import api_router


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db, document_models=[
        LogModel,
        SecureLogModel,
        Service
        ],
    )

app.include_router(api_router)