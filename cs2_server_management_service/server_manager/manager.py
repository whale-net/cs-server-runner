import logging
import time

from .server import CounterStrike2Server

logger = logging.getLogger(__name__)


class ServerManager:
    def __init__(self) -> None:
        self._servers: list[CounterStrike2Server] = []
        self._do_shutdown: bool = False
        # TODO is_running bool
        pass

    def create_server(self):
        logger.info("creating server")
        server = CounterStrike2Server()
        self._servers.append(server)
        logger.info("server created")

    def shutdown_server(self):
        logger.info("shutting down server")

    def send_command(self, command: str):
        logger.info(f"sending command to server: {command}")

    def execute_healthcheck(self):
        # check if any servers are dead
        # will eventually schedule a restart
        # but for now the main run loop handles that

        logger.info("beginning healthcheck")
        original_server_count = len(self._servers)
        logger.info(f"pre-healthcheck server count = {original_server_count}")

        healthy_servers: list[CounterStrike2Server] = []

        for server in self._servers:
            if server.is_healthy:
                logger.info(f"server name={server.name} is healthy")
                healthy_servers.append(server)
            else:
                logger.warning(f"server name={server.name} is dead")

        healthy_server_count = len(healthy_servers)

        logger.info(f"healthcheck complete")
        logger.info(f"{healthy_server_count} servers are healthy")
        logger.info(
            f"{original_server_count - healthy_server_count} servers are restart candidates"
        )

        # keep only healthy servers
        self._servers = healthy_servers

    def shutdown_manager(self):
        self._do_shutdown = True

    def run(self):
        while not self._do_shutdown:
            self.execute_healthcheck()

            # TODO - read from command queue
            if len(self._servers) == 0:
                self.create_server()

            # don't know final shape just yet, so going to sleep and come back
            # likely need to not sleep for command input
            # probably have to do async to avoid busy-waiting a lot
            time.sleep(10)
