import sys
import subprocess
import struct
import SocketServer
from threading import Thread

from utils import send_int, receive_int, send_string, receive_string

my_unix_command = ['bc']
HOST = ''
PORT = 2000


def pipe_command(arg_list, standard_input=False):
    "arg_list is [command, arg1, ...], standard_input is string"
    pipe = subprocess.PIPE if standard_input else None
    subp = subprocess.Popen(arg_list, stdin=pipe, stdout=subprocess.PIPE)
    if not standard_input:
        return subp.communicate()[0]
    return subp.communicate(standard_input)[0]

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    """
    One instance per connection.  Override handle(self) to customize action.
    """
    def handle(self):
        print('Client connected')
        # self.request is the client connection
        while True:
            data = receive_string(self.request)
            print('Data retrieved : {0}'.format(data))
            reply = pipe_command(data)
            if reply is None:
                print('Client disconnected')
                break
            print('Reply is : {0}'.format(reply))
            send_string(self.request, reply)
        self.request.close()


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

