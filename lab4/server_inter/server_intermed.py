import os
import socketserver
import subprocess


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(open('pubkey.pem', 'rb').read())
        self.data = b''
        while True:
            part = self.request.recv(4096).strip()
            self.data += part
            if len(part) < 4096:
                break
        f = open('v_enc.txt', 'wb+')
        f.write(self.data)
        f.close()

        subprocess.run('openssl rsautl -decrypt -inkey pkey.pem -in v_enc.txt -out voice.dec')
        subprocess.run('openssl dgst -sha256 -sign pkey.pem -out sign.bin voice.dec')

        self.request.sendall(open('sign.bin', 'rb').read())
        os.remove('voice.dec')
        os.remove('sign.bin')
        os.remove('v_enc.txt')


with socketserver.TCPServer(('localhost', 5110), MyTCPHandler) as server:
    subprocess.run('openssl genpkey -algorithm rsa -out pkey.pem -pkeyopt rsa_keygen_bits:1024')
    subprocess.run(f'openssl rsa -pubout -in pkey.pem -out pubkey.pem')
    server.serve_forever()
