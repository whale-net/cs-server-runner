import logging
from logging.config import fileConfig

import uvicorn

from cs2_server_management_service.config_manager import ConfigManager
from cs2_server_management_service.thread_util import NamedThreadPool

# TODO - temp for building this out
from cs2_server_management_service.steamcmd import SteamCMD


fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def main():
    logger = logging.getLogger(__name__)
    logger.info("starting service")

    # creat config manager here, does nothing, but initializes before spawning other threads
    # not really sure this is thread safe other wise
    # need singleton lock
    cm = ConfigManager()

    with NamedThreadPool() as threadpool:
        threadpool.submit(run_api, "api")
        threadpool.submit(run_cs_server_manager, "cs_server_manager")

    logger.info("service exiting")


def run_api():
    config = uvicorn.Config(
        "cs2_server_management_service.api:app", port=5000, log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()


def run_cs_server_manager():
    # temp - replace with server stuff
    steamcmd = SteamCMD()
    steamcmd.update_or_install(730)
    pass


if __name__ == "__main__":
    # TODO - is there a way to pickup stdout?
    # steamcmd subprocess info should be logged ideally
    # TODO - how to sync uvicorn log with my log
    main()
