"""
    UDP server module. Assigment for U4 A1: Práctica de comunicación indirecta.

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: import server
"""

# Standar imports
import logging
import socketserver
import pickle
from typing import Callable
from signal import SIGQUIT


logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

class RequestHandler(socketserver.BaseRequestHandler):
    """
    Request handler class.
    """
    CLIENTS = set()

    # Handles requests and distribute to ALL clients.
    def handle(self):
        """Handle client requests."""
        data = self.request[0]
        s_socket = self.request[1]

        try:
            # Unpickle data (deserialize bytes to dict).
            # Expects a serialized dict {user: str, msg: str}
            dec_data = pickle.loads(data)
        except pickle.UnpicklingError:
            LOGGER.error('Unprocessable. Skipping broadcast.')
            return

        if self.client_address not in self.CLIENTS:
            # Register client in clients' "list".
            LOGGER.info('CLIENT Joined - %s', dec_data['user'])
            self.CLIENTS.add(self.client_address)

            data = {'user': 'SERVER', 'msg': f"{dec_data['user']} Joined!"}

        if dec_data['msg'] is SIGQUIT:
            # Remove client from clients' list.
            self.CLIENTS.remove(self.client_address)
            data = {'user': 'SERVER', 'msg': f"{dec_data['user']} Left!"}

        # Serialize message if required.
        if not isinstance(data, bytes):
            data = pickle.dumps(data)

        LOGGER.info('Broadcasting msg to cient list. Sending %s bytes.', len(data))
        print(f"People in alert group: {len(self.CLIENTS)}", end='\r')
        for client_addr in self.CLIENTS:
            if client_addr == self.client_address:
                continue
            try:
                s_socket.sendto(data, client_addr)
            except Exception:
                LOGGER.warning('Error sending msg to client, removing from list.')
                self.CLIENTS.remove(client_addr)

def init_server(host: str, port: int, Handler: Callable):
    """Initialize main server."""
    LOGGER.info('Initializing UDPServer...')

    LOGGER.info('Server will listen on port %d', port)
    server = socketserver.UDPServer((host, port), Handler)

    return server
