import time
from fastapi import APIRouter

from api.models.log import LogRequest, SecureLogModel

secured_router = APIRouter()

@secured_router.post("/log")
async def log(payload: LogRequest):
    
    log_data = SecureLogModel(
        service=payload.service,
        level=payload.level,
        payload=payload.payload,
        date=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    _reference = (await log_data.save()).id

    return {"reference": str(_reference)}
