"""Execution script for the server."""
import socket
import threading


BUFFER_SIZE = 4096


def recv_data(clientsocket: socket.socket):
    size = int(clientsocket.recv(BUFFER_SIZE).decode())
    print('Recived package of size:', size)
    package = bytes()
    for _ in range(size):
        package += clientsocket.recv(BUFFER_SIZE)
    return package


def task(clientsocket: socket.socket):
    print('Opened new socket')
    print(recv_data(clientsocket).decode())


if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 4000))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        threading.Thread(target=lambda: task(clientsocket), daemon=True).start()
