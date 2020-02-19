import socket
import threading
import pickle
from ppcnn import nets, coms

weights = nets.Controller().get_weights()

def on_connection(clientsocket):
    sock = coms.CustomSocket(clientsocket)
    if sock.recv_str() == 'GETNET':
        sock.send_str(nets.Controller().to_json())
        sock.send_data(pickle.dumps(weights)) # Serialize and send weight data
        new_weights = pickle.loads(sock.recv_data())
        sock.send_str('OK')
    elif sock.recv_str() == 'VALNET':
        print('Load validation dataset and print result')
    return new_weights


def run():
    nets.Controller().create_network()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), coms.PORT))
    serversocket.listen(5)

    while True:
        (clientsocket, _) = serversocket.accept()
        threading.Thread(target=lambda: on_connection(clientsocket), daemon=True).start()