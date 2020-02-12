import math
import socket


BUFFER_SIZE = 4096


def send_data(clientsocket: socket.socket, data):
    fragments = math.ceil(len(data) / 4096) # Calculate fragment count
    size_segment = str(fragments).encode() # Convert to bytes
    size_segment = b' ' * (BUFFER_SIZE - len(size_segment)) + size_segment # Add padding to fill buffer
    clientsocket.send(size_segment) # Send size
    # Send data
    for i in range(fragments):
        clientsocket.send(data[i * BUFFER_SIZE:(i + 1) * BUFFER_SIZE]) 


if __name__ == "__main__":
    clientsocket = socket.socket()
    clientsocket.connect((socket.gethostname(), 4000))
    send_data(clientsocket, ('Test playing' * int(1e5).encode())
