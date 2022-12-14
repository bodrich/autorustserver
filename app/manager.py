import logging
import re
from time import sleep
from typing import Type

from pydantic import FilePath

from app.config import settings
from app.db_client import DBClient
from app.rcon_client import RCONClient
from app.utils.utils import run_command


class RustManager:
    MINOR_UPDATE_SECONDS: int = settings.MINOR_UPDATE_SECONDS
    PLANNED_REBOOT_SECONDS: int = settings.PLANNED_REBOOT_SECONDS
    MESSAGE_FOR_REBOOT: str = settings.MESSAGE_FOR_REBOOT
    DEFAULT_RCON_CLIENT: Type[RCONClient] = RCONClient
    COMMAND_FOR_CHECK_SERVER: str = 'ps -aux'
    FIND_TEXT_FOR_CHECK_SERVER: str = r'./RustDedicated'

    def __init__(self):
        self.client: RCONClient = self.DEFAULT_RCON_CLIENT()

    def _start_update(self):
        run_command(f'{settings.PATH_FOR_RUSTSERVER_SCRIPT} force-update')

    def stop_server(self):
        run_command(f'{settings.PATH_FOR_RUSTSERVER_SCRIPT} stop')

    def start_server(self):
        run_command(f'{settings.PATH_FOR_RUSTSERVER_SCRIPT} start')

    def check_running_server(self):
        return RCONClient().check_connection()

    def _reset_seed(self, path_for_config: FilePath = settings.PATH_FOR_CONFIG):
        logging.info('Сброс сида')
        with open(path_for_config, 'r') as fp:
            text = fp.read()

        with open(path_for_config, 'w') as fp:
            fp.write(re.sub("""seed="(.+?)\"""", 'seed=""', text))
            fp.flush()

    def _alert_reboot(self, full_seconds: int):
        for seconds in range(full_seconds, 0, -60):
            #self.client.send_message_to_players(self.MESSAGE_FOR_REBOOT.format(int(seconds / 60)))
            print(print(self.MESSAGE_FOR_REBOOT.format(int(seconds / 60))))
            #sleep(60)

    def minor_update(self):
        self._alert_reboot(self.MINOR_UPDATE_SECONDS)
        self.client.kickall()
        self.client.save()
        self._start_update()
        DBClient().insert_reboot_timestamp()

    def planned_reboot(self):
        self._alert_reboot(self.PLANNED_REBOOT_SECONDS)
        self.client.kickall()
        self.client.save()
        self.stop_server()
        self.start_server()
        DBClient().insert_reboot_timestamp()

    def major_update(self):
        self._reset_seed()
        self.stop_server()
        self._start_update()
        DBClient().insert_wipe_timestamp()
        DBClient().insert_reboot_timestamp()

