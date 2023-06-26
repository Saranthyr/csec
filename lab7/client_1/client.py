import subprocess
import sys
import socket
import selectors
import time
import types

HOST = 'localhost'
PORT = 5110

import socket
import sys


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(b'Cert request')

    data = sock.recv(4096)
    f = open('extensions.cnf', 'wb+')
    f.write(data)
    f.close()
    subprocess.run('openssl genpkey -algorithm RSA -out leaf_keypair.pem')
    sock.sendall(open('leaf_keypair.pem', 'rb').read())

    f = open('cert.pem', 'wb+')
    f.write(sock.recv(4096))
    f.close()

    sock.sendall(b'Requesting peers')
    peers = sock.recv(1024)
    peers = peers.decode('utf-8').split(', ')
    for i in range(len(peers)):
        if peers[i] == '':
            del peers[i]
        else:
            peers[i] = int(peers[i])
    print(peers)