import logging
import time

from .server import CounterStrike2Server
from cs2_server_management_service.communication import (
    Message,
    MessageType,
    Response,
    ResponseStatus,
)

logger = logging.getLogger(__name__)


class ServerManager:
    def __init__(self) -> None:
        self._servers: list[CounterStrike2Server] = []
        self._do_shutdown: bool = False
        # TODO is_running bool
        pass

    def process_message(self, message: Message) -> Response:
        logger.info("processing message %s", message)
        if message.message_type == MessageType.START:
            self._create_server()
        elif message.message_type == MessageType.STOP:
            self._shutdown_server()
        elif message.message_type == MessageType.KILL:
            self._kill_server()
        elif message.message_type == MessageType.COMMAND:
            self._send_command(message.message)
        elif message.message_type == MessageType.HEALTH:
            self.execute_healthcheck()

        return Response()  # TODO

    def _create_server(self):
        logger.info("creating cs2 server")
        server = CounterStrike2Server()
        server.start()
        self._servers.append(server)
        logger.info("cs2 server created")

    def _shutdown_server(self):
        logger.info("shutting down server")

    def _kill_server(self):
        logger.info("killing down server")

    def _send_command(self, command: str):
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
                self._create_server()

            # don't know final shape just yet, so going to sleep and come back
            # likely need to not sleep for command input
            # probably have to do async to avoid busy-waiting a lot
            time.sleep(10)
