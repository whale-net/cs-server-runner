import enum
import threading

import pydantic


class MessageType(enum.Enum):
    START = 1
    STOP = 2
    KILL = 3
    COMMAND = 4

    HEALTH = 1000


class Message(pydantic.BaseModel):
    """
    unit of work for the server manager
    """

    message_type: MessageType
    message: str


class CallbackMessge(Message):
    """
    unit of work with response and condition variable
    """

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    response: str

    _condition: threading.Condition = threading.Condition()
