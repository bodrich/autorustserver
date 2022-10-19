import logging
import subprocess
from app.utils.exceptions import ShellCommandErrorException


def run_command(command: str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    logging.info(f'Выполнение команды: {command}. Вывод: {output}')

    if error:
        raise ShellCommandErrorException(f"Ошибка исполнения команды {command}. Ошибка: {error}")

    return output
