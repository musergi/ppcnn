import socket
import coms

if __name__ == "__main__":
    clientsocket = socket.socket()
    clientsocket.connect((socket.gethostname(), coms.PORT))
    sock = coms.CustomSocket(clientsocket)
    sock.send_str('GETNET')
    print('NN data:', sock.recv_data())
    sock.send_data(b'[net train results]')
    if sock.recv_str() == 'OK':
        print('Successful exchange, closing conection')
    else:
        print('An error happened')