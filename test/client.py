import sys
import socket
from threading import Thread

from utils import send_string, receive_string


class TerminalsClient:
    def __init__(self):
        self.host, self.port = 'bilicuda', 2000
        self.running = True

    def init_connection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print('Connectin to {0}:{1} established'.format(self.host, self.port))
        except :
            print('Could not connect to {0}:{1}'.format(self.host, self.port))

    def close_connection(self):
        print('Conection to {0}:{1} was closed'.format(self.host, self.port))
        self.socket.close()
            
    def send_commands(self):
        while self.running:
            line = raw_input()
            send_string(self.socket, line)

    def recv_responses(self):
        self.init_connection()
        while self.running:
            try:
                reply = receive_string(self.socket)
	        print(reply)
            except socket.error as error:
                print('Connection was dropped')
                self.close_connection()
                self.init_connection()

    def start(self):
        self.recv_thread = Thread(target=self.recv_responses)
        self.recv_thread.start()
        self.send_thread = Thread(target=self.send_commands)
        self.send_thread.start()

client = TerminalsClient()
client.start()

while True:
     pass
