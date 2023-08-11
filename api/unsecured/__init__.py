import time
from beanie import PydanticObjectId
from fastapi import APIRouter

from api.models.log import LogModel, LogRequest

unsecured_router = APIRouter()


@unsecured_router.post("/log")
async def log(payload: LogRequest):
    log_data = LogModel(
        service=payload.service,
        level=payload.level,
        payload=payload.payload,
        date=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    _reference = (await log_data.save()).id

    return {"reference": str(_reference)}


@unsecured_router.get("/log/{reference}")
async def get_log(reference: str): 
    return await LogModel.get(PydanticObjectId(reference))
     

@unsecured_router.get("/logs")
async def get_logs(service: str = None, level: str = None, limit: int = 100, offset: int = 0):
    query = {}
    if service:
        query["service"] = service
    if level:
        query["level"] = level
        
    logs = await LogModel.find(query).to_list(1_000_000_000_000_000).skip(offset).limit(limit)

    response = {
        "limit": limit,
        "offset": offset,
        "logs": logs,
        "total_count": LogModel.find(query).count(),
    }
    return response
