import logging

import uvicorn

from cs2_server_management_service.config_manager import ConfigManager
from cs2_server_management_service.communication import CommunicationHandler
from cs2_server_management_service.thread_util import NamedThreadPool
from cs2_server_management_service.server_manager import ServerManager

logger = logging.getLogger(__name__)


def main():
    logger.info("starting service")

    # init singleton class to avoid anything weird
    CommunicationHandler()

    config_manager = ConfigManager()

    with NamedThreadPool() as threadpool:
        threadpool.submit(run_api, "api", config_manager)
        threadpool.submit(run_cs_server_manager, "cs_server_manager", config_manager)

    logger.info("service exiting")


def run_api(config_manager: ConfigManager):
    # this spawns a subprocess so the logging will be weird
    logger.info("starting uvicorn")
    config = uvicorn.Config(
        "cs2_server_management_service.api:app",
        port=config_manager.api_port,
        log_level="info",
        log_config="logging.ini",
        # use 127.0.0.1 for local development
        host="0.0.0.0",
    )
    server = uvicorn.Server(config)
    server.run()


def run_cs_server_manager(config_manager: ConfigManager):
    logger.info("starting server manager")
    manager = ServerManager()

    args = {}

    manager.run()


if __name__ == "__main__":
    # TODO - is there a way to pickup stdout?
    # steamcmd subprocess info should be logged ideally
    # TODO - how to sync uvicorn log with my log
    from logging.config import fileConfig

    fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    main()
