import logging
from datetime import datetime

import requests
import re

from pydantic import HttpUrl

from app.config import settings
from app.constants import INTERVAL_MONTH_WIPE, THURSDAY_NUMBER, INTERVAL_REBOOT
from app.db_client import DBClient
from app.utils.exceptions import NotFoundBuildIdException, RequestException


class Updater:
    DEPOT_VERSION_URL: HttpUrl = 'https://api.steamcmd.net/v1/info/258550'

    @staticmethod
    def _get_local_build_id() -> str:
        with open(settings.PATH_FOR_MANIFEST, 'r') as fp:
            version = re.findall("""buildid"\t\t"(.+?)\"""", fp.read())
            if len(version) < 1:
                raise NotFoundBuildIdException('Не смогли найти версию buildid в манифесте приложения')
            return version[0]

    def _get_remote_build_id(self) -> str:
        try:
            result = requests.get(self.DEPOT_VERSION_URL).json()
        except requests.exceptions.RequestException as error:
            raise RequestException(f'Ошибка получения версии с апи, ошибка: {error}')

        try:
            return result['data']['258550']['depots']['branches']['public']['buildid']
        except KeyError:
            raise NotFoundBuildIdException('Не смогли найти версию buildid в ответе от api.steamcmd.net')

    def check_new_versions(self) -> bool:
        local_build_id = self._get_local_build_id()
        remote_build_id = self._get_remote_build_id()

        logging.info(f'Локальная версия {local_build_id}, удаленная версия {remote_build_id}')

        return local_build_id != remote_build_id

    @staticmethod
    def check_wipe() -> bool:
        """
        Проверяем, как давно вайпался сервак, если сегодня четверг и вайп был месяц назад, то тогда надо вайпить
        :return: надо вайп или нет
        """
        last_wipe_datetime = DBClient().get_last_wipe()

        logging.info(f'Последний вайп {last_wipe_datetime}')

        if datetime.now() - last_wipe_datetime > INTERVAL_MONTH_WIPE and datetime.today().weekday() == THURSDAY_NUMBER:
            return True
        return False

    @staticmethod
    def check_reboot_server() -> bool:
        last_reboot_datetime = DBClient().get_last_reboot()

        now = datetime.now()

        logging.info(f"""
        Последний ребут {last_reboot_datetime}, 
        Интервал между ребутами: f{INTERVAL_REBOOT}, Ребутить в {settings.REBOOT_TIME_HOUR} часов.
        """)

        if now - last_reboot_datetime > INTERVAL_REBOOT and now.hour == settings.REBOOT_TIME_HOUR:
            return True
        return False
