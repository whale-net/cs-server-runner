import logging
from .queue import CommunicationQueue, MessageSource

logger = logging.getLogger(__name__)


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
