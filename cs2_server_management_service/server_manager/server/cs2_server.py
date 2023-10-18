import datetime
import logging
import subprocess
import os

from cs2_server_management_service.steamcmd import SteamCMD
from cs2_server_management_service.util import get_epoch

logger = logging.getLogger(__name__)

# use regualr Popen?
# has poll, communicate, terminate, kill


class ServerNotStartedException(Exception):
    pass


# TODO base class once this takes shape
class CounterStrike2Server:
    STEAM_APP_ID = 730
    DEFAULT_PORT: int = 27015

    def __init__(
        self,
        port: int = DEFAULT_PORT,
        root_installation_path: str = ".",
        update_server: bool = True,
    ) -> None:
        self._last_update_run: datetime.datetime = get_epoch()
        self._last_run_start: datetime = get_epoch()
        self._root_installation_path = root_installation_path
        self._port = port
        self._update_server = update_server

        self._executable_path = os.path.join(
            self._root_installation_path, "game/bin/linuxsteamrt64/cs2"
        )
        pass

    @property
    def is_healthy(self) -> bool:
        """
        external facing property to check if server is healthy (running)

        :return: true if healthy
        """
        # this method is distinct from self._is_running
        # because healthchecks may redefine themselves in the future
        return self._is_running

    @property
    def name(self) -> str:
        return "cs2"

    @property
    def port(self) -> int:
        return self._port

    @property
    def _proc(self) -> subprocess.Popen:
        """
        access underlying server subprocess

        :raises ServerNotStartedException: returns when server is not started
        :return: underlying Popen subprocess
        """
        if self._last_run_start == get_epoch():
            raise ServerNotStartedException(f"Server {self.name} not started")

        return self.__proc

    @property
    def _is_running(self) -> bool:
        """
        is server running
        use is_healthy for external health checks

        :return: true if running
        """
        try:
            return self._proc.poll() is None
        except ServerNotStartedException:
            return False
        except:
            raise

    def start(self):
        self.update_or_install()

        # TODO replace with command builder
        command: list[str] = [self._executable_path, "-dedicated"]

        command.append("-port")
        command.append(str(self.port))

        command.append("+map")
        command.append("de_ancient")

        logger.info(command)

        self.__proc = subprocess.Popen(command, stdin=subprocess.PIPE)
        self._last_run_start = datetime.datetime.now()
        logger.info("%s has been started", self.name)

    def update_or_install(self):
        has_update_ran = not self._last_update_run == get_epoch()

        if not has_update_ran:
            if not self.update_server:
                # set to an obviosuly faked non-epoch timestamp
                self._last_update_run = datetime.datetime.utcfromtimestamp(1)
                logger.info(
                    "skip_server_update flag enabled, skipping update for %s", self.name
                )
                return

            logger.info("updating or installing server")
            steamcmd = SteamCMD()
            steamcmd.update_or_install(CounterStrike2Server.STEAM_APP_ID, self.name)
            self._last_update_run = datetime.datetime.now()
            logger.info("server updated/installed")
        else:
            logger.info("CounterStrike2Server already updated")

    def kill(self):
        logger.info("killing %s o7", self.name)
        # cs2 won't be killed in this way
        self._proc.kill()

    def execute_command(self, command: str):
        if len(command) == 0:
            return
        command = command + "\n"

        logger.info("server %s about to execute command=%s", self.name, command)

        command_bytes = bytes(command, encoding="ascii")
        # self._proc.communicate(command_bytes)
        # apparently this is wrong, but it's what I think I have to do
        self._proc.stdin.write(command_bytes)
        self._proc.stdin.flush()
