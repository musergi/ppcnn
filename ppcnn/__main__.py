import argparse
from ppcnn import client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='run server instead of client')
    args = parser.parse_args()

    client.run()