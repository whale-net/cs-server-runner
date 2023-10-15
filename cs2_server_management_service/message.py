import enum

from dataclasses import dataclass


class MessageType(enum.Enum):
    START = 1
    STOP = 2
    KILL = 3
    COMMAND = 4

    HEALTH = 1000


class ResponseStatus(enum.Enum):
    OK = 1
    WARNING = 2
    ERROR = 3


@dataclass
class Message:
    """
    unit of work for the server manager
    """

    message_type: MessageType
    message: str


@dataclass
class Response:
    """
    response to a unit of work
    """

    response_status: ResponseStatus
    response: str
    original_message: Message
