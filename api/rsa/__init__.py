from fastapi import APIRouter
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization

rsa_router = APIRouter()

@rsa_router.get("/publicKey")
async def get_public_key():
    with open("public.pem", "rb") as pub_file:
        publicKey = load_pem_public_key(pub_file.read())

    return publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

@rsa_router.post("/validateKey")
async def validate_key(payload: dict):
    with open("public.pem", "rb") as pub_file:
        publicKey = load_pem_public_key(pub_file.read()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    if publicKey == payload.get("key"):
        return True
    return False