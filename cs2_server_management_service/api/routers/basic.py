from fastapi import APIRouter
from cs2_server_management_service.communication import (
    CommunicationHandler,
    Message,
    MessageSource,
    MessageType,
)

router = APIRouter()


@router.get("/")
async def root() -> str:
    return "hello world"


@router.get("/test")
async def root() -> str:
    msg = Message(MessageType.KILL, "kill from API")

    cm = CommunicationHandler()
    cm.add_message(MessageSource.ServerManager, msg)
    return "hope it works"
