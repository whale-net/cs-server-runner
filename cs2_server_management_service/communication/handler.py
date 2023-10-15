import logging
from .message import Message
from .response import Response, ResponseStatus
from .queue import CommunicationQueue, MessageSource, EmptyCommunicationQueueException

logger = logging.getLogger(__name__)


class CommunicationHandler:
    _instance: "CommunicationHandler" = None

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

    def _get_queue(self, message_source: MessageSource) -> CommunicationQueue:
        # workaround to get typehints
        return self._queues[message_source]

    def add_message(self, message_source: MessageSource, message: Message) -> Response:
        target_queue = self._get_queue(message_source)
        target_queue.put_message(message)

        # this is realistically the only point that makes sense for returning a response
        # for now...
        # this system isn't going to work for what I want to do and needs to be reconsidered
        return Response(
            response_status=ResponseStatus.OK,
            response="message submit",
            original_message=message,
        )

    def get_message(self, message_source: MessageSource) -> Message:
        # internal function throws exception
        target_queue = self._get_queue(message_source)
        message = target_queue.pop_message()
        return message

    def try_get_message(
        self, message_source: MessageSource
    ) -> tuple[bool, Message | None]:
        try:
            msg = self.get_message(message_source)
            return (True, msg)
        except EmptyCommunicationQueueException:
            return (False, None)
        except:
            raise
