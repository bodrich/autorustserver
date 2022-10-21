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
    MINOR_UPDATE_SECONDS: int = 900
    PLANNED_REBOOT_SECONDS: int = 900
    MESSAGE_FOR_REBOOT: str = 'Сервер будет перезагружен через {} минут.'

    REBOOT_TIME_HOUR: int = 6

    CHECK_INTERVAL_SECONDS: int = 60 * 5


settings = Settings(_env_file='.environment')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

logger.setLevel(logging.INFO)
