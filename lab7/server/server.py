import os
import sys
import socket
import selectors
import time
import types
import subprocess
import re
import socketserver


HOST = 'localhost'
PORT = 5110

X509_EXTENSIONS = "[nonLeaf]\n" \
                "basicConstraints=critical,CA:TRUE\n" \
                "\n" \
                "[Leaf]\n" \
                "basicConstraints=CA:FALSE"

open('extensions.cnf', 'w+').write(X509_EXTENSIONS)

#generating root cert
subprocess.run('openssl genpkey -algorithm RSA -out root_keypair.pem')
subprocess.run('openssl req -new -subj "/CN=ROOT CA" -addext "basicConstraints=critical,CA:TRUE" -key root_keypair.pem -out root_csr.pem')
subprocess.run('openssl req -in root_csr.pem -noout -text')
subprocess.run('openssl x509 -req -in root_csr.pem -signkey root_keypair.pem -days 3650 -out root_cert.pem')

#generating intermed cert
subprocess.run('openssl genpkey -algorithm RSA  -out intermediate_keypair.pem')
subprocess.run('openssl req -new -subj "/CN=INTERMEDIATE CA" -addext "basicConstraints=critical,CA:TRUE" -key intermediate_keypair.pem -out intermediate_csr.pem')
subprocess.run('openssl x509 -req -in intermediate_csr.pem -CA root_cert.pem -CAkey root_keypair.pem -extfile extensions.cnf -extensions nonLeaf -days 3650 -out intermediate_cert.pem')


peers = []


class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFF_SIZE = 4096
    global peers
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        peers.append(str(self.client_address[1]))
        self.request.recv(1024)
        self.request.sendall(open('extensions.cnf', 'rb').read())
        f = open('leaf_keypair.pem', 'wb+')
        f.write(self.request.recv(4096))
        f.close()
        subprocess.run('openssl req -new -subj "/CN=LEAF" -addext "basicConstraints=critical,CA:FALSE" -key leaf_keypair.pem -out leaf_csr.pem')
        subprocess.run('openssl x509 -req -in leaf_csr.pem -CA intermediate_cert.pem -CAkey intermediate_keypair.pem -extfile extensions.cnf -extensions Leaf -days 3650 -out leaf_cert.pem')
        self.request.sendall(open('leaf_cert.pem', 'rb').read())
        while True:
            req = self.request.recv(1024)
            if req == b'Requesting peers':
                data = b''
                for i in peers:
                    data += bytes(i, encoding='utf-8')
                self.request.sendall(data)



# Create the server, binding to localhost on port 9999
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

