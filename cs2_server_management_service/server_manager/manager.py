import logging
import datetime
import time

from cs2_server_management_service.communication import (
    Message,
    MessageType,
    Response,
    ResponseStatus,
    CommunicationHandler,
    MessageSource,
)
from cs2_server_management_service.util import get_epoch

from .server import CounterStrike2Server

logger = logging.getLogger(__name__)


class ServerManager:
    MESSAGE_SOURCE: MessageSource = MessageSource.ServerManager

    def __init__(self) -> None:
        self._servers: list[CounterStrike2Server] = []
        self._do_shutdown: bool = False

        self._com_handler: CommunicationHandler = CommunicationHandler()

        self._last_health_check: datetime.datetime = get_epoch()
        # make configurable?
        self._health_check_period: datetime.timedelta = datetime.timedelta(seconds=10)
        pass

    def process_message(self, message: Message) -> Response:
        logger.info("processing message %s", message)
        # route messages
        if message.message_type == MessageType.START:
            self._create_server()
        elif message.message_type == MessageType.STOP:
            self._shutdown_server()
        elif message.message_type == MessageType.KILL:
            self._kill_server()
        elif message.message_type == MessageType.COMMAND:
            self._send_command(message.message)
        elif message.message_type == MessageType.HEALTH:
            self._execute_healthcheck()

        return Response(
            original_message=message,
            response_status=ResponseStatus.OK,
            response="on it sir - o7",
        )

    def _create_server(self):
        if len(self._servers) > 0:
            logger.warning("unable to start server, server already exists")
            return

        logger.info("creating cs2 server")
        server = CounterStrike2Server()
        server.start()
        self._servers.append(server)
        logger.info("cs2 server created")

    def _shutdown_server(self):
        logger.info("shutting down server - cheating by killing")
        self._kill_server()

    def _kill_server(self):
        for server in self._servers:
            server.kill()

    def _send_command(self, command: str):
        for server in self._servers:
            server.execute_command(command)

    def _execute_healthcheck(self):
        # check if any servers are dead
        # will eventually schedule a restart
        # but for now the main run loop handles that

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

        logger.info(f"{healthy_server_count} servers are healthy")
        logger.info(
            f"{original_server_count - healthy_server_count} servers are restart candidates"
        )

        # keep only healthy servers
        self._servers = healthy_servers
        self._last_health_check = datetime.datetime.now()

    def shutdown(self):
        self._do_shutdown = True

    def run(self):
        # create server message
        initial_create_message = Message(message_type=MessageType.START, message="")
        self._com_handler.add_message(
            ServerManager.MESSAGE_SOURCE, initial_create_message
        )

        no_message_count: int = 0
        max_count: int = 5000
        while not self._do_shutdown:
            current_time = datetime.datetime.now()

            # TODO await?
            has_message, msg = self._com_handler.try_get_message(
                ServerManager.MESSAGE_SOURCE
            )
            if has_message:
                self.process_message(msg)
            else:
                no_message_count += 1

            if no_message_count >= max_count:
                logger.info("hello still here")
                logger.info(f"no messages {max_count} times in a row")
                no_message_count = 0

            # submit health_check if it's been too long
            if current_time - self._last_health_check > self._health_check_period:
                health_message = Message(
                    MessageType.HEALTH, f"health_check:{current_time}"
                )
                self._com_handler.add_message(
                    ServerManager.MESSAGE_SOURCE, health_message
                )

            # don't know final shape just yet, so going to sleep and come back
            # likely need to not sleep for command input
            # probably have to do async to avoid busy-waiting a lot
            #
            # do want async, need to set that up so that multiple messages can be picked up
            # however, polling at 100ms is probably fine, for now
            time.sleep(0.1)
            # time.sleep(5)
