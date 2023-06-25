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

if not os.path.exists(os.path.join(os.getcwd(), 'temp_storage')):
    os.mkdir(os.path.join(os.getcwd(), 'temp_storage'))

open('extensions.cnf', 'w+').write(X509_EXTENSIONS)

#generating root cert
subprocess.run('openssl genpkey -algorithm RSA -out root_keypair.pem')
subprocess.run('openssl req -new -subj "/CN=ROOT CA" -addext "basicConstraints=critical,CA:TRUE" -key root_keypair.pem -out root_csr.pem')
subprocess.run('openssl req -in root_csr.pem -noout -text')
subprocess.run('openssl x509 -req -in root_csr.pem -signkey root_keypair.pem -days 3650 -out root_cert.pem')
# subprocess.run('openssl x509 -in root_cert.pem -noout -text')

#generating intermediate cert
subprocess.run('openssl genpkey -algorithm RSA -out intermediate_keypair.pem')
subprocess.run('openssl req -new -subj "/CN=INTERMEDIATE CA" -addext "basicConstraints=critical,CA:TRUE" -key intermediate_keypair.pem -out intermediate_csr.pem')
subprocess.run('openssl x509 -req -in intermediate_csr.pem -extfile extensions.cnf -extensions nonLeaf -CA root_cert.pem -CAkey root_keypair.pem -days 3650 -out intermediate_cert.pem')
# subprocess.run('openssl x509 -in intermediate_cert.pem -noout -text')

os.remove('root_csr.pem')
os.remove('intermediate_csr.pem')

subprocess.run('openssl x509 -in intermediate_cert.pem -pubkey -noout -out inter_pubkey.pem')

peers = []


class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFF_SIZE = 4096
    FTRANSFERINPROGRESS = False
    FTRANSFERFILENAME = ''
    global peers
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        peers.append(self.client_address[1])
        self.data = self.request.recv(self.BUFF_SIZE)
        f = open('extensions.cnf', 'rb')
        resp = f.read()
        f.close()
        self.request.sendall(resp)
        self.request.recv(self.BUFF_SIZE)
        f = open('intermediate_cert.pem', 'rb')
        resp = f.read()
        f.close()
        self.request.sendall(resp)
        f = open(f'cert_{self.client_address[1]}.pem', 'wb+')
        f.write(self.request.recv(4096))
        f.close()
        t = subprocess.run(
            f'openssl verify -verbose -show_chain -trusted root_cert.pem -untrusted intermediate_cert.pem cert_{self.client_address[1]}.pem',
            capture_output=True)
        if b"cert.pem: OK" in t.stdout:
            self.request.sendall(open('inter_pubkey.pem', 'rb').read())
        while True:
            while True:
                part = self.request.recv(self.BUFF_SIZE)
                self.data += part
                if len(part) < self.BUFF_SIZE:
                    break
            if re.match(b'filename:.*', self.data):
                f = open(f'{self.data.decode("utf-8")[9:]}', 'wb+')
                f.close()
                self.FTRANSFERINPROGRESS = True
                self.FTRANSFERFILENAME = self.data.decode('utf-8')[9:]
                if self.FTRANSFERFILENAME == 'pubkey.pem':
                    self.FTRANSFERFILENAME = self.FTRANSFERFILENAME.split('.')[0] + "_" + str(self.client_address[1]) + self.FTRANSFERFILENAME.split('.')[1]
                self.request.sendall(b'Ready')
            elif self.FTRANSFERINPROGRESS and re.match('.*\.enc', self.FTRANSFERFILENAME):
                f = open(f"{self.FTRANSFERFILENAME}", 'wb+')
                f.write(self.data)
                f.close()
                self.FTRANSFERINPROGRESS = False
                subprocess.run(f'openssl rsautil -decrypt -inkey intermediate_keypair.pem -in {self.FTRANSFERFILENAME} -out {self.FTRANSFERFILENAME}.dec')
                subprocess.run(f'openssl dgst -sha256 -sign intermediate_keypair.pem -out sign.bin {self.FTRANSFERFILENAME}.dec')
                os.remove(self.FTRANSFERFILENAME)
                os.remove(f'{self.FTRANSFERFILENAME}.dec')
            elif self.FTRANSFERINPROGRESS:
                f = open(f"{self.FTRANSFERFILENAME}", 'wb+')
                f.write(self.data)
                f.close()
                self.FTRANSFERINPROGRESS = False
            elif not self.FTRANSFERINPROGRESS:
                break
        for i in peers:
            if self.client_address[1] != i:
                t = os.listdir(os.getcwd())
                for j in t:
                    if not re.match('cert_.*\.pem', j) or not re.match('pubkey_.*\.pem', j) or not re.match('sign.bin', j):
                        subprocess.run(f'openssl rsautil  -encrypt -inkey pubkey_{i}.pem -pubin -in {j} -out {j.split(".")[0]}.enc"')
                        self.request.sendall(open(j, 'rb').read())
                        self.request.recv(1024)
                        self.request.sendall(open('sign.bin', 'rb').read())
                        self.request.recv(1024)
                        os.remove(j)
                        os.remove('sign.bin')
                        break
                break


# Create the server, binding to localhost on port 9999
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

