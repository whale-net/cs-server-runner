import logging


from cs2_server_management_service.config_manager import ConfigManager

logger = logging.getLogger(__name__)


def run_service():
    logger = logging.getLogger(__name__)
    logger.info("starting service")

    cm = ConfigManager()




if __name__ == '__main__':
    from logging.config import fileConfig
    fileConfig('logging.ini', disable_existing_loggers=False)

    run_service()