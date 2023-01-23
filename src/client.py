"""
    UDP client module. Assigment for U4 A1: Práctica de comunicación indirecta.

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: import client
"""

# Standar imports
import os
import logging
import pickle
from signal import SIGQUIT, SIGTTIN

# Custom imports
from server import RequestHandler

REMOTE_IP = "127.0.0.1"
REMOTE_PORT = 20001

logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

class ClientMessageHandler(RequestHandler):

    def handle(self):
        data = pickle.loads(self.request[0])
        print(f"\r{data['user']}: {data['msg']}")
        print("YOU:", end=" ", flush=True)

class Client():
    """Encapsulates client methods."""

    def __init__(self, socket) -> None:
        self.socket = socket
        self.name = input('Enter User Name:')
        self._join()

    def _join(self):
        """Send signal to server to identify new user."""
        self._send_data(SIGTTIN)

    def _send_data(self, data):
        """Serialize and send data to server."""
        data = {'user': self.name, 'msg': data}
        data = pickle.dumps(data)

        self.socket.sendto(data, (REMOTE_IP, REMOTE_PORT))
    
    def _quit_chat(self):
        """Send signal to server to remove user from chat."""
        self._send_data(SIGQUIT)

    def send(self):
        while True:
            data = input('YOU: ')
            # Skip empty messages.
            if not data:
                continue
            if data == 'q!':
                self._quit_chat()
                LOGGER.info('Leaving chat!')
                os._exit(0)
            
            self._send_data(data)
