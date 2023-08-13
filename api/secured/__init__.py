import base64
import json
import time
from fastapi import APIRouter, Depends, Request, HTTPException
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from api.models.log import LogRequest, SecureLogModel, SecureLogRequest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.fastjwt import FastJWT

secured_router = APIRouter(dependencies=[Depends(FastJWT().login_required)])

@secured_router.post("/log")
async def log(payload: SecureLogRequest, request: Request):
    jwt_token = await FastJWT().decode(request.headers["Authorisation"])
    if "access_code" in jwt_token and jwt_token["access"] not in [1, 666]:
        raise HTTPException(status_code=401, detail="Invalid access code")

    log_data = SecureLogModel(
        service=jwt_token["service_name"],
        level=payload.level,
        payload=payload.payload,
        date=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )

    _reference = (await log_data.save()).id

    return {"reference": str(_reference)}


@secured_router.get("/log/{reference}")
async def get_log(reference: str, request: Request):
    jwt_token = await FastJWT().decode(request.headers["Authorisation"])
    if "access_code" in jwt_token and jwt_token["access"] not in [0, 666]:
        raise HTTPException(status_code=401, detail="Invalid access code")

    log = await SecureLogModel.get(reference)
    
    if not log:
        raise HTTPException(404, "Log not found")
    with open("private.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,
        )
    log = log.dict()
    try:
        decrypted  = private_key.decrypt(
            base64.b64decode(log["payload"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except:
        raise HTTPException(500, "Could not decrypt log")
    
    log["payload"] = json.loads(decrypted.decode())

    return log


@secured_router.get("/logs")
async def get_logs(request: Request, service: str = None, level: str = None, limit: int = 100, offset: int = 0):
    jwt = await FastJWT().decode(request.headers["Authorisation"])
    if "access_code" in jwt and jwt["access"] not in [0, 666]:
        raise HTTPException(status_code=401, detail="Invalid access code")
    
    query = {}
    if service:
        query["service"] = service
    if level:
        query["level"] = level
        
    logs =  SecureLogModel.find(query).skip(offset).limit(limit)
    logs = await logs.to_list()
    with open("private.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,
        )
    _logs = []
    for log in logs:
        log = log.dict()
        try:
            decrypted  = private_key.decrypt(
                base64.b64decode(log["payload"]),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            log["payload"] = json.loads(decrypted.decode())
            _logs.append(log)
        except:
            pass
        
    response = {
        "limit": limit,
        "offset": offset,
        "logs": _logs,
        "total_count": await SecureLogModel.find(query).count(),
    }

    return response