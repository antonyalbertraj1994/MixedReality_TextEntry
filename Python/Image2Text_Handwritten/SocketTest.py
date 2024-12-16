import socket
import time

HOST = '0.0.0.0'
port = 9003
print("Started")
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, port))
socket.listen(5)

client_socket, client_address = socket.accept()
data = client_socket.recv(1024).strip()

while True:
    print("Sending")
    client_socket.send("1\n".encode('utf-8'))

    data = client_socket.recv(1024).strip()
    lightval = data.decode('utf-8')
    print(lightval)
    time.sleep(3)