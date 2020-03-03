import math
import socket

PORT = 4000
BUFFER_SIZE = 4096
DATA_STORAGE = 'scripts/data_storage.txt'

class CustomSocket:
    def __init__(self, socket: socket.socket):
        self.socket = socket

    def send_data(self, data):
        # FTP.storbinary(data, "fp.txt")

        with open(DATA_STORAGE, 'wb') as f:
            f.write(data)
        f.closed
        """fragment_count = math.ceil(len(data) / 4096) # Calculate fragment count
        size_fragment = b' ' * (BUFFER_SIZE - len(size_fragment)) + size_fragment # Add padding to fill buffer
        self.socket.send(size_fragment) # Send size
        # Send data
        for i in range(fragment_count):
            self.socket.send(data[i * BUFFER_SIZE:(i + 1) * BUFFER_SIZE])"""

    def recv_data(self):

        with open(DATA_STORAGE, 'wb') as f:
            read_data = f.read()

        """ size = int(self.socket.recv(BUFFER_SIZE).decode())
        print('Reciving package of size:', size)
        package = bytes()
        for _ in range(size):
            package += self.socket.recv(BUFFER_SIZE)
        return package """

    def send_str(self, string: str):
        self.send_data(string.encode())

    def recv_str(self):
        return self.recv_data().decode()