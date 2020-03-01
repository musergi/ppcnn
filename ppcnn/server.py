import socket
import threading
import pickle
from ppcnn import nets, coms

SERVER_INIT_FILE = '.sync/server_ready.out'

def on_connection(clientsocket):
    # Create socket manager
    sock = coms.CustomSocket(clientsocket)

    # Check client action
    if sock.recv_str() == 'GETNET':
        # Send net and weights
        sock.send_str(nets.Controller().to_json())
        sock.send_data(pickle.dumps(nets.Controller().get_weights())) # Serialize and send weight data

        # Update weights
        new_weights = pickle.loads(sock.recv_data())
        nets.Controller().set_weights(new_weights)
        sock.send_str('OK')

        # Save network in file
        nets.Controller().checkpoint()


def run():
    print('Starting server')

    # Create Network
    nets.Controller().create_network()

    # Open server socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), coms.PORT))
    serversocket.listen(5) # 5 represents queue size
    print('Server listening')

    # Create file and write the ip
    with open(SERVER_INIT_FILE, 'w') as f:
        f.write(socket.gethostname()) 

    # Serve clients
    while True:
        (clientsocket, _) = serversocket.accept()
        threading.Thread(target=lambda: on_connection(clientsocket), daemon=True).start()