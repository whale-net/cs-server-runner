import enum
from dataclasses import dataclass

from .message import Message


class ResponseStatus(enum.Enum):
    OK = 1
    WARNING = 2
    ERROR = 3


@dataclass
class Response:
    """
    response to a unit of work
    """

    response_status: ResponseStatus
    response: str
    original_message: Message
