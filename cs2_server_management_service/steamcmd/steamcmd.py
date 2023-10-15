import logging
import subprocess
import os

from cs2_server_management_service.config_manager import ConfigManager


logger = logging.getLogger(__name__)


class SteamCMD:
    def __init__(self) -> None:
        self._config_manager: ConfigManager = ConfigManager()
        self._steamcmd = self._config_manager.steamcmd_executable
        logger.info(f"using steamcmd executable: {self._steamcmd}")

    def update_or_install(self, app_id: int, installation_name: str):
        """
        updates or install provided app_id
        limited to a single server per app_id

        :param app_id: steam app_id
        """
        install_dir = self._config_manager.get_game_install_path(installation_name)
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # TODO this should be replaced with a generic command builder
        steamcmd_args: list[str] = []
        stdin_args: list[str] = []

        steamcmd_args.append("+force_install_dir")
        steamcmd_args.append(install_dir)

        steamcmd_args.append("+login")
        steamcmd_args.append(self._config_manager.steam_username)
        # password must run via stdin
        stdin_args.append(self._config_manager.steam_password)

        steamcmd_args.append("+app_update")
        steamcmd_args.append(str(app_id))

        # remember to exit, otherwise steamcmd will hang
        steamcmd_args.append("+exit")

        self._exec(steamcmd_args, stdin_args)

    def _exec(self, command_args: list[str], stdin_args: list[str]):
        subprocess_command = [self._config_manager.steamcmd_executable]
        subprocess_command += command_args

        pretty_subprocess_command = " ".join(subprocess_command)
        logger.info(f"about to execute:: {pretty_subprocess_command}")

        # don't log stdin since that has password
        # not yet sure how to handle that
        stdin_command_string = "".join(arg + "\n" for arg in stdin_args)
        stdin_input: bytes = bytes(stdin_command_string, encoding="ascii")

        proc = subprocess.run(subprocess_command, input=stdin_input)

        logger.info("finished running steamcmd")
