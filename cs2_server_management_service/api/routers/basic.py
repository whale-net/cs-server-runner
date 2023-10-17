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


@router.post("/server/shutdown")
async def root() -> CommonResponse:
    """
    curl --request POST http://127.0.0.1:5000/server/shutdown
    """
    msg = Message(message_type=MessageType.STOP, message="stop from API")

    cm = CommunicationHandler()
    cm.add_message(MessageSource.ServerManager, message=msg)
    return CommonResponse(message="OK")


@router.post("/server/start")
async def root() -> CommonResponse:
    """
    curl --request POST http://127.0.0.1:5000/server/start
    """
    msg = Message(message_type=MessageType.START, message="starting server")

    cm = CommunicationHandler()
    cm.add_message(MessageSource.ServerManager, msg)
    return CommonResponse(message="OK")
