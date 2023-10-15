import logging
import threading
from contextlib import contextmanager

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


class NamedLock:
    """
    wrapper class that gives name to a threading.Lock
    """

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        logger.info("creating lock named %s", self.name)

        self._lock: threading.Lock = threading.Lock()

    # def acquire(self, blocking: bool = True, timeout: int = -1) -> bool
    def acquire(self) -> bool:
        return self._lock.acquire()

    def release(self) -> None:
        self._lock.release()

    def locked(self) -> bool:
        return self._lock.locked()

    def __repr__(self) -> str:
        return self.name


@contextmanager
def raii_acquire_release(lock: NamedLock):
    """
    context manager used to handle acquring and releasing a lock

    :param lock: _description_
    """

    logger.debug("acquring lock %s", lock)
    lock.acquire()
    logger.debug("lock acquired")
    yield
    logger.debug("about to release lock")
    lock.release()
    logger.debug("lock released %s", lock)
