import enum
import logging
import uuid
from collections import deque

from .message import Message
from .response import Response
from cs2_server_management_service.thread_util import raii_acquire_release, NamedLock

logger = logging.getLogger(__name__)


# TODO rename
class MessageSource(enum.Enum):
    API = 1
    ServerManager = 2


class EmptyCommunicationQueueException(Exception):
    pass


class CommunicationQueue:
    # @property
    # def incoming(self) -> deque[Message]:
    #     return self.incoming

    # @property
    # def outgoing(self) -> deque[Response]:
    #     return self._outgoing

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str = str(uuid.uuid4())) -> None:
        self._name = name

        self._incoming: deque[Message] = deque()
        self._outgoing: deque[Response] = deque()

        self._incoming_lock = NamedLock(f"{self.name}-incoming")
        self._outgoing_lock = NamedLock(f"{self.name}-outgoing")

    def put_message(self, message: Message):
        with raii_acquire_release(self._incoming_lock):
            self._incoming.append(message)

    def put_messages(self, messages: list[Message]):
        # although underlying function will acquire lock
        # acquire the lock again to ensure atomicity
        with raii_acquire_release(self._incoming_lock):
            for message in messages:
                self.put_message(message)

    def pop_message(self) -> Message:
        # don't need to acquire lock again
        messages = self.pop_messages(count=1)
        if len(messages) == 0:
            raise EmptyCommunicationQueueException
        return messages[0]

    def pop_messages(self, count: int) -> list[Message]:
        with raii_acquire_release(self._incoming_lock):
            num_messages_to_return = min(count, len(self._incoming))
            return_messages = [
                self._incoming.popleft() for _ in range(num_messages_to_return)
            ]
            return return_messages

    def put_response(self, response: Response):
        with raii_acquire_release(self._outgoing_lock):
            self._outgoing.append(response)

    def put_responses(self, responses: list[Response]):
        with raii_acquire_release(self._outgoing_lock):
            for response in responses:
                self.put_response(response)

    def pop_responses(self, count: int = 1) -> list[Response]:
        with raii_acquire_release(self._outgoing_lock):
            num_responses_to_return = min(count, len(self._outgoing))
            return_responses = [
                self._outgoing.popleft() for _ in range(num_responses_to_return)
            ]
            return return_responses
