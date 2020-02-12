import socket
import threading
import coms

def on_connection(clientsocket):
    sock = coms.CustomSocket(clientsocket)
    if sock.recv_str() == 'GETNET':
        sock.send_data(b'[network data]')
        print('Training results:', sock.recv_data())
        sock.send_str('OK')

if __name__ == "__main__":
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 4000))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        threading.Thread(target=lambda: on_connection(clientsocket), daemon=True).start()