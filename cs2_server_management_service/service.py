import logging


from cs2_server_management_service.config_manager import ConfigManager
# TODO - temp for building this out
from cs2_server_management_service.steamcmd import SteamCMD

logger = logging.getLogger(__name__)


def run_service():
    logger = logging.getLogger(__name__)
    logger.info("starting service")

    # creat config manager here, does nothing, but initializes before spawning other threads
    # not really sure this is thread safe other wise
    # need singleton lock
    cm = ConfigManager()

    steamcmd = SteamCMD()
    steamcmd.update_or_install(730)



if __name__ == '__main__':
    # TODO - is there a way to pickup stdout?
    # steamcmd subprocess info should be logged ideally
    from logging.config import fileConfig
    fileConfig('logging.ini', disable_existing_loggers=False)

    run_service()