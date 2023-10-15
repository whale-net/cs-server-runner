from fastapi import APIRouter
from cs2_server_management_service.config_manager import ConfigManager

router = APIRouter()


@router.get("/")
async def root() -> str:
    return "hello world"


@router.get("/test")
async def root() -> str:
    return "hello world test"
