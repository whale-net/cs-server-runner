from fastapi import APIRouter
from cs2_server_management_service.communication import (
    CommunicationHandler,
    Message,
    MessageSource,
    MessageType,
)
from ..common_response import CommonResponse

router = APIRouter()


@router.get("/")
async def root() -> CommonResponse:
    return CommonResponse(message="hello world")


@router.get("/server/shutdown")
async def root() -> CommonResponse:
    msg = Message(MessageType.STOP, "stop from API")

    cm = CommunicationHandler()
    cm.add_message(MessageSource.ServerManager, msg)
    return CommonResponse(message="OK")
