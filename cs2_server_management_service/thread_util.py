import logging
import threading

logger = logging.getLogger(__name__)


class NamedThreadPool:
    def __init__(self, thread_name_prefix: str = "") -> None:
        logger.info("NamedThreadPool initialized")

        self._threads: list[threading.Thread] = []
        self.thread_name_prefix: str = thread_name_prefix

        logger.info(f"thread_name_prefix={self.thread_name_prefix}")

    def __enter__(self) -> "NamedThreadPool":
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        _summary_

        :param exc_type: exception type
        :param exc_value: exception value
        :param exc_tb: exception traceback
        """

        logger.info("all work submitted, beginning to join threads")

        for thread in self._threads:
            try:
                logger.info(f"joining thread: {thread.name} id={thread.native_id}")
                thread.join()
                logger.info(f"thread completed: {thread.name} id={thread.native_id}")
            except KeyboardInterrupt:
                logger.warning(
                    f"KeyboardInterrupt recieved for thread: {thread.name} id={thread.native_id}"
                )

    def submit(self, target, name: str, *args, **kwargs):
        thread_name = name
        if len(self.thread_name_prefix) > 0:
            thread_name = f"{self.thread_name_prefix}.{name}"

        logger.info(f"creating thread {thread_name} target={target.__name__}")
        thread = threading.Thread(target=target, name=thread_name, *args, **kwargs)
        thread.start()
        self._threads.append(thread)
