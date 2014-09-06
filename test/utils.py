import struct
import socket


def send_int(socket, value):
    socket.send(struct.Struct('I').pack(value))

def receive_int(socket):
    return struct.Struct('I').unpack(socket.recv(4))[0]


def send_string(socket, string):
    try:
        if isinstance(string, unicode):
            string = string.encode('utf-8')
    except:
        message = "Could not encode: {0}".format(''.join(":{0:02x}".format(ord(c)) for c in string))
        logger.warning(message)
    send_int(socket, len(string))
    socket.send(string)

def receive_string(socket):
    length = receive_int(socket)
    if(length > 0):
        string = socket.recv(length)
        return string.decode()
    else:
        return ""

