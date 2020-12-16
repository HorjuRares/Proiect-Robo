import socket

HOST = '192.168.1.3'
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
with conn:
    print(addr)
    s.sendall(b'RAPA')
