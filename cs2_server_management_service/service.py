import logging

import uvicorn

from cs2_server_management_service.config_manager import ConfigManager
from cs2_server_management_service.communication import CommunicationHandler
from cs2_server_management_service.thread_util import NamedThreadPool
from cs2_server_management_service.server_manager import ServerManager

logger = logging.getLogger(__name__)


def main():
    logger.info("starting service")

    # init singleton classes to avoid anything weird
    ConfigManager()
    CommunicationHandler()

    with NamedThreadPool() as threadpool:
        threadpool.submit(run_api, "api")
        threadpool.submit(run_cs_server_manager, "cs_server_manager")

    logger.info("service exiting")


def run_api():
    # this spawns a subprocess so the logging will be weird
    logger.info("starting uvicorn")
    config = uvicorn.Config(
        "cs2_server_management_service.api:app",
        port=5000,
        log_level="info",
        log_config="logging.ini",
    )
    server = uvicorn.Server(config)
    server.run()


def run_cs_server_manager():
    logger.info("starting server manager")
    manager = ServerManager()
    manager.run()


if __name__ == "__main__":
    # TODO - is there a way to pickup stdout?
    # steamcmd subprocess info should be logged ideally
    # TODO - how to sync uvicorn log with my log
    from logging.config import fileConfig

    fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    main()
