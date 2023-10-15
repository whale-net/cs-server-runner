import enum
import logging
import uuid
from collections import deque

from cs2_server_management_service.message import Message, Response
from cs2_server_management_service.thread_util import raii_acquire_release, NamedLock

logger = logging.getLogger(__name__)


class MessageSource:
    API = 1
    ServerManager = 2


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

        self._incoming = deque[Message]
        self._outgoing = deque[Response]

        self._incoming_lock = NamedLock(f"{self.name}-incoming")
        self._outgoing_lock = NamedLock(f"{self.name}-outgoing")

    def put_message(self, message: Message):
        with raii_acquire_release(self._incoming_lock):
            self._incoming.append(message)

    def put_messages(self, messages: list[Message]):
        with raii_acquire_release(self._incoming_lock):
            for message in messages:
                self.put_message(message)

    def pop_messages(self, count: int = 1) -> list[Message]:
        # batch processing by default
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


class CommunicationHandler:
    _instance: "CommunicationHandler"

    def __init__(self):
        pass

    def __new__(
        cls,
    ):
        # singleton
        # not thread safe, but if i create once in service entrypoint then we should be safe
        if cls._instance is None:
            logger.info("creating MessageQueue singleton")

            # need to instantiate this way to avoid recursion
            cls._instance = super(CommunicationHandler, cls).__new__(cls)

            # create communication queues for each message source
            #
            cls._instance._queues: dict[MessageSource, CommunicationQueue] = {
                msg_src: CommunicationQueue() for msg_src in MessageSource
            }

        return cls._instance
