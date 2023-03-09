import socket
import sys

def run_client(ip = '127.0.0.1', port= 16201, path='/'):
    sock = socket.socket()
    sock.connect((ip, port))
    sock.send(f'GET {path} HTTP/1.1/r/n'.encode())

    data = sock.recv(1024)
    sock.close()

    print(data)

if __name__ == '__main__':
    ip, port = None, None

    args = sys.argv[1:]

    if len(args) == 3:
        ip, port, path = args
        run_client(ip, int(port), path)
    else:
        print('expected 3 arguments')
