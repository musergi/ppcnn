import socket
import threading
import pickle
import coms
import nets


def on_connection(clientsocket):
    sock = coms.CustomSocket(clientsocket)
    if sock.recv_str() == 'GETNET':
        sock.send_str(nets.Controller().to_json())
        sock.send_data(pickle.dumps(nets.Controller().get_weights())) # Serialize and send weight data
        print('Training results:', len(sock.recv_data()))
        sock.send_str('OK')


if __name__ == "__main__":
    nets.Controller().create_network()
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), 4000))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        threading.Thread(target=lambda: on_connection(clientsocket), daemon=True).start()