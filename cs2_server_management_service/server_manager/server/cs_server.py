import datetime
import logging

from cs2_server_management_service.steamcmd import SteamCMD

logger = logging.getLogger(__name__)

# import asyncio

# async def test_run():
#     process = await asyncio.create_subprocess_exec('echo', 'hello', 'world'
#                                                    #, stdin=asyncio.subprocess.PIPE
#                                                    , stdout=asyncio.subprocess.PIPE)
#     await process.wait()
#     stdout, stderr = await process.communicate()
#     print(stdout)
#     print(stderr)


# use regualr Popen?
# has poll, communicate, terminate, kill


# TODO base class once this takes shape
class CounterStrike2Server:
    APP_ID = 730

    def __init__(self) -> None:
        self._last_update_run: datetime.datetime = datetime.datetime.utcfromtimestamp(0)
        pass

    @property
    def is_healthy(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return "cs_server"

    def run(self):
        self.update_or_install()

        pass

    def update_or_install(self):
        if self._last_update_run != datetime.datetime.utcfromtimestamp(0):
            logger.info("updating or installing server")
            # this will eventually have custom path support
            steamcmd = SteamCMD()
            steamcmd.update_or_install(CounterStrike2Server.APP_ID)
            self._last_update_run = datetime.datetime.now()
            logger.info("server updated/installed")
        else:
            logger.info("CounterStrike2Server already updated")
