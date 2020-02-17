import argparse
from ppcnn import client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', action='store_true', help='run server instead of client')
    parser.add_argument('-a', '--address', type=str, help='specify server address to client')
    parser.add_argument('-t', '--target', type=str,help='target data to train on')
    args = parser.parse_args()

    if args.server:
        print('Running server')
    else:
        client.run()