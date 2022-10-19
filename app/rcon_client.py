import json
import logging
import socket

import websocket
from websocket import WebSocketException

from app.config import settings


class RCONClient:
    DEFAULT_RCON_NAME = "WebRcon"
    SAVE_COMMAND = 'save'
    KICKALL_COMMAND = 'kickall'
    SAY_COMMAND = 'say'
    DEFAULT_WEBSOCKET_CHECK_CONNECTION_SECOND = 3

    def __init__(self, address: str = settings.RUST_SERVER_ADDRESS, password: str = settings.RUST_SERVER_PASSWORD):
        self.address: str = address
        self.password: str = password
        self.identifier = 1

    def _make_connection(self):
        return websocket.create_connection(f"ws://{self.address}/{self.password}")

    def check_connection(self) -> False:
        try:
            connect = websocket.create_connection(
                f"ws://{self.address}/{self.password}",
                timeout=self.DEFAULT_WEBSOCKET_CHECK_CONNECTION_SECOND,
            )
            print(1111)
            connect.close()
        except (WebSocketException, socket.error) as error:
            logging.info('При чеке коннекшнена ошибка:', error)
            return False
        return True

    def _make_message(self, command: str, name: str = DEFAULT_RCON_NAME) -> str:
        self.identifier += 1
        return json.dumps({
            "Identifier": self.identifier,
            "Message": command,
            "Name": name,
        })

    def _send_command(self, command: str):
        connection = self._make_connection()
        message = self._make_message(command)
        logging.info(f"Отправили по ркону сообщение:{message}")
        connection.send(message)
        result_message = connection.recv()
        logging.info(f"Получили по ркону сообщение:{result_message}")
        connection.close()

    def send_message_to_players(self, text: str):
        self._send_command(f'{self.SAY_COMMAND} {text}')

    def kickall(self):
        self._send_command(self.KICKALL_COMMAND)
        logging.info('Кикнули всех')

    def save(self):
        self._send_command(self.SAVE_COMMAND)
        logging.info('Сохранили мир')
