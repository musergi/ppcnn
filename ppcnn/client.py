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

def run(address, target):
    clientsocket = socket.socket()
    clientsocket.connect((address, coms.PORT))
    sock = coms.CustomSocket(clientsocket)
    
    model = get_model(sock)
    # Train network
    sock.send_data(pickle.dumps(model.get_weights()))
    if sock.recv_str() == 'OK':
        print('Successful exchange, closing conection')
    else:
        print('An error happened')