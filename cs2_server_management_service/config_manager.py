import argparse
import inspect
import logging
import os

logger = logging.getLogger(__name__)


class ConfigManager:
    _instance: "ConfigManager" = None

    DEFAULT_CS_PORT: int = 27015
    DEFAULT_ENVIRONMENT_FILE_NAME: str = "config.json"
    DEFAULT_STEAMCMD_EXECUTABLE: str = "steamcmd"
    DEFAULT_SERVER_INSTALL_DIRECTORY: str = os.path.join(os.getcwd(), "server_files")

    @property
    def steam_username(self) -> str:
        return self._steam_username

    @property
    def steam_password(self) -> str:
        return self._steam_password

    @property
    def cs_server_port(self) -> int:
        return self._cs_server_port

    @property
    def steamcmd_executable(self) -> str:
        return self._steamcmd_executable

    @property
    def server_install_directory(self) -> str:
        return self._server_install_directory

    def __init__(self):
        calling_function = inspect.stack()[1].function
        logger.info(f"ConfigManager accessed by {calling_function}")

    def __new__(
        cls,
    ):
        # singleton
        # not thread safe, but if i create once in service entrypoint then we should be safe
        if cls._instance is None:
            logger.info("creating singleton")
            # need to instantiate this way to avoid recursion
            cls._instance = super(ConfigManager, cls).__new__(cls)

            # intialize in 3 steps
            # TODO - use argparse defaults, and load from file, then load from args
            # then use single args object for everything
            # this entire intialization needs to be redone I think
            # but at least I have my properties
            # 1 - hardcoded defaults
            # 2 - environment file based - removed until above is
            # ? - environment variable - will do if needed
            # 3 - argv

            # 1 - defaults
            cls._instance._init_defaults()

            # parse args here to pickup environment filepath override
            arg_parser = cls._create_arg_parser()
            args = arg_parser.parse_args()
            arg_parser.parse_args()

            # 2 - file load
            # environment_file_path = (
            #     args.env_file if args.env_file is not None
            #     else cls.DEFAULT_ENVIRONMENT_FILE_NAME
            # )
            # cls._instance._init_from_file(environment_file_path)

            # 3 - parse cli args
            cls._instance._init_from_args(args)

        return cls._instance

    def _init_defaults(self):
        self._instance._steam_username: str = str()
        self._instance._steam_password: str = str()
        self._instance._cs_server_port: int = ConfigManager.DEFAULT_CS_PORT
        self._instance._steamcmd_executable: str = (
            ConfigManager.DEFAULT_STEAMCMD_EXECUTABLE
        )
        self._instance._server_install_directory: str = (
            ConfigManager.DEFAULT_SERVER_INSTALL_DIRECTORY
        )

    # def _init_from_file(self, environment_file_path: str):
    #     if not os.path.exists(environment_file_path):
    #         logger.warning('provided environment_file_path does not exist')
    #         logger.warning(f'path={environment_file_path}')
    #         logger.warning('skipping file-based configuration')
    #         return
    #     logger.critical('_init_from_file not implemented')

    def _init_from_args(self, args):
        # TODO - what type is args?
        logger.error("_init_from_args partially implemented")

        if args.steam_username is not None:
            self._steam_username = args.steam_username
        if args.steam_password is not None:
            self._steam_password = args.steam_password

        if args.steamcmd is not None:
            self._steamcmd_executable = args.steamcmd

        if args.server_install_directory is not None:
            self._server_install_directory = args.server_install_directory

    @staticmethod
    def _create_arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--steam_username",
            dest="steam_username",
            help="username used by steamcmd",
            type=str,
            nargs="?",
            default=None,
        )
        parser.add_argument(
            "--steam_password",
            dest="steam_password",
            help="password used by steamcmd user",
            type=str,
            nargs="?",
            default=None,
        )

        parser.add_argument(
            "--env_file",
            dest="env_file",
            help="overwrite default environment file",
            type=str,
            nargs="?",
            default=None,
        )

        parser.add_argument(
            "--steamcmd",
            dest="steamcmd",
            help="overwrite default steamcmd executable",
            type=str,
            nargs="?",
            default=None,
        )
        parser.add_argument(
            "--server_install_directory",
            dest="server_install_directory",
            help="overwrite default server install directory",
            type=str,
            nargs="?",
            default=None,
        )
        return parser

    def get_game_install_path(self, installation_name: str) -> str:
        return os.path.join(self.server_install_directory, installation_name)
