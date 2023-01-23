"""
    P2P Node. Assigment for U4 A1: Práctica de comunicación indirecta.

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: python node.py [-s]
    -s run as main server.

    if run as client send "q!" to exit.
"""

# Standar imports
import threading
import random
import argparse

# Custom imports
import client
import server
 
# Initialize parser
PARSER = argparse.ArgumentParser()
# set argument to identify if process will run as message broker.
PARSER.add_argument("-s", "--server", action='store_true')
ARGS = PARSER.parse_args()


if __name__ == '__main__':
    """Control process workflow."""

    server_ip = '127.0.0.1'
    main_s_port = 20001
    port = random.randint(20002, 21000)

    if ARGS.server:
        # initialize UDP server (message broker).
        server_ = server.init_server(server_ip, main_s_port, server.RequestHandler)
        srv_th = threading.Thread(target=server_.serve_forever)
        srv_th.start()
    else:
        port = random.randint(20002, 21000)
        # Initialize server and client.
        client_srv = server.init_server(server_ip, port, client.ClientMessageHandler)
        client_ = client.Client(client_srv.socket)

        # start client and server threads
        cli_srv_th = threading.Thread(target=client_srv.serve_forever)
        cli_th = threading.Thread(target=client_.send)

        cli_srv_th.start()
        cli_th.start()
