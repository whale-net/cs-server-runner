import logging
import subprocess
import os

from cs2_server_management_service.config_manager import ConfigManager


logger = logging.getLogger(__name__)

class SteamCMD():

    def __init__(self) -> None:
        self._config_manager: ConfigManager = ConfigManager()
        self._steamcmd = self._config_manager.steamcmd_executable
        logger.info(f'using steamcmd executable: {self._steamcmd}')


    def update_or_install(self, app_id: int):
        
        # install_dir is not full path, just path to 
        install_dir = os.path.join(self._config_manager.server_install_directory, str(app_id))
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        steamcmd_args: list[str] = []
        stdin_args: list[str] = []

        steamcmd_args.append('+force_install_dir')
        steamcmd_args.append(f'"{install_dir}"')
        
        steamcmd_args.append('+login')
        steamcmd_args.append(f'{self._config_manager.steam_username}')
        # password must run via stdin
        stdin_args.append(self._config_manager.steam_password)
        
        self._exec(steamcmd_args, stdin_args)

    def _exec(self, command_args: list[str], stdin_args: list[str]):        
        subprocess_command = [self._config_manager.steamcmd_executable]
        subprocess_command += command_args
        
        pretty_subprocess_command = ' '.join(subprocess_command)
        logger.info(f'about to execute:: {pretty_subprocess_command}')

        # don't log stdin since that has password
        # not yet sure how to handle that
        stdin_command_string = ''.join(arg + '\n' for arg in stdin_args)
        stdin_input: bytes = bytes(stdin_command_string, encoding='ascii')
        
        proc = subprocess.run(subprocess_command)
        #proc = subprocess.run(subprocess_command, input=stdin_input)

        logger.info('finished running steamcmd')
