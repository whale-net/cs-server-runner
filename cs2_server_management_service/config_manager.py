import inspect
import logging
import os
import sys

logger = logging.getLogger(__name__)

class ConfigManager():
    _instance: 'ConfigManager' = None

    DEFAULT_CS_PORT: int = 27015
    DEFAULT_ENVIRONMENT_FILE_NAME: str = '.env'

    def __init__(self):
        calling_function = inspect.stack()[1].function
        logger.info(f'ConfigManager accessed by {calling_function}')


    def __new__(cls, ):
        # singleton
        # not thread safe, but if i create once in service entrypoint then we should be safe
        if cls._instance is None:
            logger.info('creating singleton')
            # need to instantiate this way to avoid recursion
            cls._instance = super(ConfigManager, cls).__new__(cls)
            
            # intialize in 3 steps
            # 1 - hardcoded defaults
            # 2 - environment file based
            # ? - environment variable - will do if needed
            # 3 - argv

            # 1 - defaults
            cls._instance._steam_username: str = str()
            cls._instance._steam_password: str = str()
            cls._instance._cs_server_port: int = ConfigManager.DEFAULT_CS_PORT

            # parse args here to pickup environment filepath override
            # TODO pickup args env file path if present else default
            environment_file_path = cls.DEFAULT_ENVIRONMENT_FILE_NAME

            # 2 - file load
            cls._instance._load_from_file(environment_file_path)

            # 3 - parse cli args

        return cls._instance


    def _load_from_file(self, environment_file_path):
        if not os.path.exists(environment_file_path):
            logger.warning('provided environment_file_path does not exist')
            logger.warning('path={environment_file_path}')
            logger.warning('skipping file-based configuration')
            return
        logger.critical('_load_from_file not implemented')