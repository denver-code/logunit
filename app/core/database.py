import motor.motor_asyncio
from beanie import Document
from datetime import datetime


client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017", uuidRepresentation="standard"
)
db = client["logunit"]