import enum

from dataclasses import dataclass


class MessageType(enum.Enum):
    START = 1
    STOP = 2
    KILL = 3
    COMMAND = 4

    HEALTH = 1000


@dataclass
class Message:
    """
    unit of work for the server manager
    """

    message_type: MessageType
    message: str
