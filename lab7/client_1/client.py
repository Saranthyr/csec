import subprocess
import sys
import socket
import selectors
import time
import types

HOST = 'localhost'
PORT = 5110
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
#     sk.connect((HOST, PORT))
#     data = b'Cert request'
#     sk.sendall(data)
#     cert_data = b''
#     while True:
#         part = sk.recv(1024)
#         cert_data += part
#         if len(part) < 1024:
#             break
#     f = open('cert.pem', 'wb+')
#     f.write(cert_data)
#     f.close()
#     data = b'filename:cert.pem'
#     sk.sendall(data)
#     f = open('cert.pem', 'rb')
#     data = f.read()
#     f.close()
#     sk.sendall(data)
#     # else:
#     # file = open('Facial_Animation_-_RimhammerDwarves.xml', 'rb')
#     # data = file.read()
#     # file.close()
import socket
import sys

# data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(b'Cert request')

    data = sock.recv(4096)
    f = open('extensions.cnf', 'wb+')
    f.write(data)
    f.close()
    sock.sendall(b'Ready')
    data = sock.recv(4096)
    f = open('intermediate_cert.pem', 'wb+')
    f.write(data)
    f.close()

    subprocess.run('openssl genpkey -algorithm RSA -out leaf_keypair.pem')
    subprocess.run('openssl req -new -subj "/CN=LEAF" -addext "basicConstraints=critical,CA:FALSE" -key leaf_keypair.pem -out leaf_csr.pem')
    subprocess.run('openssl x509 -req -in leaf_csr.pem -extfile extensions.cnf -extensions Leaf -CA intermediate_cert.pem -days 3650 -out cert.pem')

    f = open('cert.pem', 'rb')
    cert_data = f.read()
    f.close()
    sock.sendall(cert_data)
    f = open('server_pubkey.pem', 'wb+')
    f.write(sock.recv(4096))
    f.close()


    def send_file(filename):
        subprocess.run(f'openssl rsautl -encrypt -inkey server_pubkey.pem -pubin -in {filename} -out {filename.split(".")[0]+ ".enc"}')
        f = open(f'{filename.split(".")[0]+ ".enc"}', 'rb')
        data = f.read()
        f.close()
        sock.sendall(f'filename:{filename.split(".")[0]+ ".enc"}')
        sock.recv(1024)
        sock.sendall(data)
        sock.recv(1024)
        sock.sendall(bytes(filename, encoding='utf-8'))
        sock.recv(1024)
        sock.sendall(open(filename, 'rb').read())


    while True:
        filename = input('Type name of file to be sent to another client')
        send_file(filename)
