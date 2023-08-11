from fastapi import APIRouter
from api.unsecured import unsecured_router
from api.secured import secured_router
from api.user import user_router

api_router = APIRouter(prefix="/api")

api_router.include_router(unsecured_router, tags=["unsecured"], prefix="/u")
api_router.include_router(secured_router, tags=["secured"], prefix="/s")
api_router.include_router(user_router, tags=["user"], prefix="/user")