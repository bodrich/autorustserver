import logging
import sys

from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    SQLITE_FILE_NAME: str = 'db.sqlite'
    RUST_SERVER_ADDRESS: str
    RUST_SERVER_PASSWORD: str
    PATH_FOR_MANIFEST: FilePath
    PATH_FOR_CONFIG: FilePath
    PATH_FOR_RUSTSERVER_SCRIPT: FilePath
    MINOR_UPDATE_MINUTES: int = 15
    MINOR_UPDATE_SECONDS: int = MINOR_UPDATE_MINUTES * 60
    PLANNED_REBOOT_MINUTES: int = 15
    PLANNED_REBOOT_SECONDS: int = PLANNED_REBOOT_MINUTES * 60
    MESSAGE_FOR_REBOOT: str = 'Сервер будет перезагружен через {} минут.'

    REBOOT_TIME_HOUR: int = 6

    CHECK_INTERVAL_SECONDS: int = 60 * 5

    #PATH_FOR_MANIFEST: str = '../serverfiles/steamapps/appmanifest_258550.acf'


settings = Settings(_env_file='.environment')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

logger.setLevel(logging.INFO)
