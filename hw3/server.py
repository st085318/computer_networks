import socket
import os
import sys

def get_response_data(path):
    content_type = 'text/plain; charset=utf-8'
    if os.path.isfile(path):
        with open(path, 'rb') as file:
            content = file.read()
        code = 200 
        status = 'OK'
    elif os.path.isdir(path):
        content = str('\n'.join(os.listdir(path))).encode()
        code = 200 
        status = 'OK'
    elif path == '':
        content = str('\n'.join(os.listdir(path='.'))).encode()
        code = 200 
        status = 'OK'
    else:
        code = 404
        status = 'Not Found'
        content = b'404 Not Found ERROR'
    headers = {'Content-Type': content_type, 'Content-Length': len(content)}
    return {'code': code, 'status': status, 'headers': headers, 'content': content}

def make_response(response_data):
    code, status, headers, content = response_data.values()
    resp = f'HTTP/1.1 {code} {status}\r\n'.encode()
    for (key, value) in headers.items():
        resp += f'{key}: {value}\r\n'.encode()
    resp += b'\r\n'

    resp += content
    return resp

def customer_service(client_sock):
    while True:
        data = client_sock.recv(1024)
        begin_header = str(data, 'iso-8859-1').split('\r\n')[0].split()
        print(begin_header)
        if len(begin_header) != 3:
            print('Incorrect header')
            break
        path = begin_header[1]
        wfile = client_sock.makefile('wb')

        response_data = get_response_data(path[1:])
        response = make_response(response_data)
        wfile.write(response)
        wfile.flush()
        wfile.close()

def run_server(ip = '127.0.0.1', port = 16201):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as serv_sock:
        serv_sock.bind((ip, port))
        serv_sock.listen(1)
        while True:
            print("listen")
            client_sock, client_addr = serv_sock.accept()
            print('Connected by', client_addr)

            customer_service(client_sock)

            client_sock.close()
            print('Connection close', client_addr)

if __name__ == '__main__':
    ip, port = None, None

    args = sys.argv[1:]

    if len(args) == 1:
        ip = args[0]
        run_server(ip)
    elif len(args) == 2:
        ip, port = args
        run_server(ip, int(port))
    elif len(args) == 0:
        run_server()

    
