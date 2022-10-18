import logging
from time import sleep
from typing import Any

from app.config import settings
from app.manager import RustManager
from app.utils.updater import Updater


class Scheduler:
    DEFAULT_MANAGER: Any = RustManager
    DEFAULT_UPDATER: Any = Updater

    def run_cycle(self):
        manager = self.DEFAULT_MANAGER()
        updater = self.DEFAULT_UPDATER()

        if updater.check_wipe():
            logging.info('Глобальное обновление')
            return manager.major_update()

        if updater.check_new_versions():
            logging.info('Вышло минорное обновление')
            return manager.minor_update()

        if updater.check_reboot_server():
            logging.info('Необходим обычный ребут')
            return manager.planned_reboot()

    def run(self):
        while True:
            logging.info('Старт цикла')
            self.run_cycle()
            logging.info(f'Конец цикла, спим {settings.CHECK_INTERVAL_SECONDS} секунд')

            sleep(settings.CHECK_INTERVAL_SECONDS)
