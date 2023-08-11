from beanie import Document
from pydantic import BaseModel


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


class SecureLogModel(Document):
    service: str
    level: str
    payload: dict
    date: str

    class Settings:
        name = "secure_logs"