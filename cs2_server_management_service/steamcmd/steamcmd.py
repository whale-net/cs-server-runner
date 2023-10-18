import logging
import subprocess
import os

from typing import Optional

logger = logging.getLogger(__name__)


class SteamCMD:
    ANONYMOUS_USER: str = "anonymous"

    def __init__(
        self,
        steamcmd_installation_root_path: str,
        steamcmd_executable: str = "steamcmd",
        steam_username=ANONYMOUS_USER,
        steam_password: Optional[str] = None,
    ) -> None:
        self._steamcmd_executable = steamcmd_executable
        self._steamcmd_installation_root_path = steamcmd_installation_root_path
        self._steam_username = steam_username
        self._steam_password = steam_password
        logger.info(f"using steamcmd executable: {self._steamcmd_executable}")

    @property
    def steamcmd_installation_root_path(self) -> str:
        return self._steamcmd_installation_root_path

    def update_or_install(self, app_id: int, installation_name: str):
        """
        updates or install provided app_id
        limited to a single server per app_id

        :param app_id: steam app_id
        """
        install_dir = self.steamcmd_installation_root_path
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # TODO this should be replaced with a generic command builder
        steamcmd_args: list[str] = []
        stdin_args: list[str] = []

        steamcmd_args.append("+force_install_dir")
        steamcmd_args.append(install_dir)

        steamcmd_args.append("+login")
        steamcmd_args.append(self._steam_username)
        # password must run via stdin
        stdin_args.append(self._steam_password)

        steamcmd_args.append("+app_update")
        steamcmd_args.append(str(app_id))

        # remember to exit, otherwise steamcmd will hang
        steamcmd_args.append("+exit")

        self._exec(steamcmd_args, stdin_args)

    def _exec(self, command_args: list[str], stdin_args: list[str]):
        subprocess_command = [self._steamcmd_executable]
        subprocess_command += command_args

        pretty_subprocess_command = " ".join(subprocess_command)
        logger.info(f"about to execute:: {pretty_subprocess_command}")

        # don't log stdin since that has password
        # not yet sure how to handle that
        stdin_command_string = "".join(arg + "\n" for arg in stdin_args)
        stdin_input: bytes = bytes(stdin_command_string, encoding="ascii")

        proc = subprocess.run(subprocess_command, input=stdin_input)

        logger.info("finished running steamcmd")
