#!/bin/env python3

from common.hostrecord import HostRecord
import sys
import socket
import os
from base64 import b64encode, b64decode
import select
# todo reimport import readline
from pyreadline import Readline
import logging
import common.constants as CONSTANTS


class ServerSession():

    def __init__(self, server, port=8421, username=None, password=None, BUFFER_SIZE=8192):
        self.port = port
        self.host = server
        self.BUFFER_SIZE = BUFFER_SIZE
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_state(True)
        self.error_ct = 0
        self.run()

    def die(self, *args):
        '''Fatal error handling function for issuing none, one or many warnings before exiting'''
        for msg in args:
            print(msg)
        self.stop_socket(True)

    def socket_state(self, state):
        self.running_state = state

    def stop_socket(self, stop=False):
        if stop and self.running_state:
            print("INFO: Socket client will exit")
            self.socket_state(False)
            self.close_socket()
        elif stop and not self.running_state:
            print("INFO: Waiting for all active transactions to complete.")

        self.report()

    def close_socket(self):
        self.tcpClient.shutdown(socket.SHUT_RDWR)
        self.tcpClient.close()

    def com_drop(self):
        print("COMDROP")
        self.tcpClient.setblocking(False)
        self.com_drop_status = True
        while True:
            clear_socket = select.select([self.tcpClient], [], [], 2)
            if clear_socket[0]:
                try:
                    self.dump_socket_data = self.read_socket()
                    if self.dump_socket_data == '' or self.dump_socket_data == ' ':
                        break
                except:
                    break
            else:
                break

        self.tcpClient.setblocking(True)

    def report(self):
        if self.running_state:
            print(
                "INFO: Socket Cliente rodando:")
        else:
            print("INFO: Socket Cliente parado:")

    def message_com(self, data, buffer=8192):
        if data == '00xSOT00x':
            self.tcpClient.sendall(b64encode('00xSOT00x'.encode(CONSTANTS.CHAR_SET)))
            return True

        elif data == '00xEOT00x':
            self.tcpClient.sendall(b64encode('00xEOT00x'.encode(CONSTANTS.CHAR_SET)))
            return False

        elif data == '01xSOM01x':
            self.tcpClient.sendall(b64encode('01xSOM01x'.encode(CONSTANTS.CHAR_SET)))

            self.tcpClient.setblocking(False)
            socRDY = select.select([self.tcpClient], [], [], 2)
            if socRDY[0]:
                data = self.read_socket()
                print(data)
            else:
                self.tcpClient.sendall(b64encode('01xROM01x'.encode(CONSTANTS.CHAR_SET)))
                print("INFO: Timed out waiting for a response from server.")
                return False

            self.tcpClient.setblocking(True)

            self.tcpClient.sendall(b64encode('01xROM01x'.encode(CONSTANTS.CHAR_SET)))
            return True

        elif data == '01xEOM01x':
            self.tcpClient.sendall(b64encode('01xEOM01x'.encode(CONSTANTS.CHAR_SET)))
            return True

        elif data == '00xEOT00x':
            self.tcpClient.sendall(b64encode('00xEOT00x'.encode(CONSTANTS.CHAR_SET)))
            return True

        elif data == '009x0DT000x0':
            self.com_drop()
            return False
        else:
            self.tcpClient.sendall(b64encode('009x0SET000x0'.encode(CONSTANTS.CHAR_SET)))
            self.com_drop()
            if self.error_ct >= 20:
                self.stop_socket(True)
                return False
            return False

    def send_request(self, request):
        self.tcpClient.sendall(b64encode(request.encode(CONSTANTS.CHAR_SET)))

        while True:
            self.srvdata = self.read_socket()
            if not self.message_com(self.srvdata):
                break

    def init_sync(self):
        self.srvdata = self.read_socket()
        if self.srvdata != CONSTANTS.HELLO:
            self.die("Erro de comunicação inicial")
        else:
            self.tcpClient.sendall(b64encode(CONSTANTS.HELLO.encode(CONSTANTS.CHAR_SET)))

    def decode_data(self, data):
        return b64decode(data).decode(CONSTANTS.CHAR_SET)

    def read_socket(self, buffer=8192):
        data = self.tcpClient.recv(buffer)
        return self.decode_data(data)

    def run(self):
        self.tcpClient.connect((self.host, (self.port)))
        self.init_sync()

        # todo pyreadline é a versão para windows do readline
        readLine = Readline()
        readLine.set_completer(self.completer)
        readLine.parse_and_bind('tab: complete')

        while self.running_state:
            try:
                myHost = HostRecord.getFromComputer()
                data = CONSTANTS.DATAHEADER + 'JSON=' + myHost.export()
                self.error_ct = 0
                self.toserver = data
                #self.toserver = input("Input :: <= ")
            except KeyboardInterrupt:
                self.stop_socket(True)
                break

            if self.toserver in ['Exit', 'Quit', 'exit', 'quit', 'q', 'bye', 'Bye']:
                self.send_request(self.toserver)
                break

            if self.toserver == '' or self.toserver is None or not self.toserver:
                continue
            elif self.toserver == 'clear':
                os.system("clear")
                continue

            self.send_request(self.toserver)


if __name__ == "__main__":
    cli = None
    try:
        cli = ServerSession(server=sys.argv[1])
    except KeyboardInterrupt:
        cli.stop_socket(True)
