import socket
import pickle
import coms
import tensorflow as tf


if __name__ == "__main__":
    clientsocket = socket.socket()
    clientsocket.connect((socket.gethostname(), coms.PORT))
    sock = coms.CustomSocket(clientsocket)
    sock.send_str('GETNET')
    net_json = sock.recv_str()
    model = tf.keras.models.model_from_json(net_json)
    model.summary()
    weights = pickle.loads(sock.recv_data())
    model.set_weights(weights)
    # Train network
    sock.send_data(pickle.dumps(model.get_weights()))
    if sock.recv_str() == 'OK':
        print('Successful exchange, closing conection')
    else:
        print('An error happened')