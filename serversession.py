
'''
import sys
import time
import json
import socket
import threading
from threading import Thread

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3333


class Client:
    def __init__(self, operation):
        self.operation = operation
        self.send_operation(operation)

    def send_operation(self, operation):
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
            msg = json.dumps(operation)
            sock.send(msg.encode('utf-8'))

            print(f'Thread #{threading.get_ident()} - sending', msg)
            
            data = sock.recv(1024)

            print("-------------RESPONSE-------------")
            print(data.decode('utf-8'))


    while True:
        Client(operation)
        time.sleep(1)
'''