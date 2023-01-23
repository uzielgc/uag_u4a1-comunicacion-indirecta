"""
    Assigment for U4 A1: Práctica de comunicación indirecta.

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: python node.py -r
"""

# Standar imports
import logging
import socket
import argparse


logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

# Initialize parser
PARSER = argparse.ArgumentParser()
# set argument to identify if process will run as message broker.
PARSER.add_argument("-r", "--receiver", action='store_true')
ARGS = PARSER.parse_args()

MCAST_GRP = '224.0.0.1' 
MCAST_PORT = 20001

def receiver():
    """Start server."""
    LOGGER.info('Multicast Receiver...')

    #MCAST_GRP = '224.0.0.1' 
    #MCAST_PORT = 20001
    r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    r_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    r_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
    r_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    r_socket.bind((MCAST_GRP, MCAST_PORT))
    host = socket.gethostbyname(socket.gethostname())

    r_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    r_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
                    socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

    while True:
        data = r_socket.recvfrom(10240)
        print(data[0].decode('UTF-8'))


def sender():
    #MCAST_GRP = '224.1.1.1'
    #MCAST_PORT = 20001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    LOGGER.info('Starting notification system...')

    while True:
        data = input('Send message to subscribed users: ')
        data = data.encode('UTF-8')
        sock.sendto(data, (MCAST_GRP, MCAST_PORT))

if __name__ == '__main__':

    if ARGS.receiver:
        receiver()
    else:
        sender()