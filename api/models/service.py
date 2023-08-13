from beanie import Document
from pydantic import BaseModel


class Service(Document):
    name: str
    description: str
    access: int
    # token: str
    # 0 - read only
    # 1 - write only
    # 2 - read and write
    access_code: int
    
    class Settings:
        name = "services"


class NewService(BaseModel):
    name: str
    description: str
    access: int