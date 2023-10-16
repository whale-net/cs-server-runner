from dataclasses import dataclass
from typing import Optional

from fastapi import APIRouter

from cs2_server_management_service.communication import (
    CommunicationHandler,
    Message,
    MessageSource,
    MessageType,
)

from ..common_response import CommonResponse

router = APIRouter()


@dataclass
class CommandRequest:
    command: str


@dataclass
class MultiCommandRequest:
    commands: list[CommandRequest]


@router.post("/server/command")
async def root(command: CommandRequest) -> CommonResponse:
    """
    curl --header "Content-Type: application/json" --request POST --data '{"command":"sv_cheats 1"}' http://127.0.0.1:5000/server/command
    """

    msg = Message(MessageType.COMMAND, command.command)

    cm = CommunicationHandler()
    cm.add_message(MessageSource.ServerManager, msg)

    return CommonResponse(message="server should be executing")


@router.post("/server/command/multi")
async def root(multi_command: MultiCommandRequest) -> CommonResponse:
    """
    curl --header "Content-Type: application/json" --request POST --data '{"commands":[{"command":"sv_cheats"},{"command":"sv_cheats 1"},{"command":"sv_cheats"}]}' http://127.0.0.1:5000/server/command/multi
    curl --header "Content-Type: application/json" --request POST --data '{"commands":["sv_cheats","sv_cheats 1","sv_cheats"]}' http://127.0.0.1:5000/server/command/multi
    """
    cm = CommunicationHandler()
    for command in multi_command.commands:
        msg = Message(MessageType.COMMAND, command.command)
        cm.add_message(MessageSource.ServerManager, msg)
    return CommonResponse(message="server should be executing many commands")
