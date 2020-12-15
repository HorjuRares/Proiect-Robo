import socket

HOST = '192.168.1.2'
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

data = s.recv(1024)
print(repr(data))