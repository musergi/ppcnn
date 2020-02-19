import socket
import pickle
from ppcnn import coms
import tensorflow as tf


def get_model(sock):
    sock.send_str('GETNET')
    net_json = sock.recv_str()
    model = tf.keras.models.model_from_json(net_json)
    weights = pickle.loads(sock.recv_data())
    model.set_weights(weights)
    model.summary()
    return model

#No se com fer això: el que vull es actualitzar correctament els pesos
def update_weights (new_weights):
    for delta_weights in weights:
        delta_weights -= new_weights
        return delta_weights

def run():
    clientsocket = socket.socket()
    clientsocket.connect((socket.gethostname(), coms.PORT))
    sock = coms.CustomSocket(clientsocket)
    
    model = get_model(sock)
    # Train network
    sock.send_data(pickle.dumps(model.get_weights()))
    if sock.recv_str() == 'OK':
        print('Successful exchange, closing conection')
    else:
        print('An error happened')