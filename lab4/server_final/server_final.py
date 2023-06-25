import os
import socketserver
import subprocess


def verify_sign():
    t = subprocess.run('openssl dgst -sha256 -verify pubkey.pem -signature sign.bin voice.txt', capture_output=True)
    if b"OK" in t.stdout:
        return True
    else:
        return False


VOICES_CAND_1 = 0
VOICES_CAND_2 = 0
VOICES_CAND_3 = 0


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global VOICES_CAND_1
        global VOICES_CAND_2
        global VOICES_CAND_3
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096).strip()
        f = open('voice.txt', 'wb+')
        f.write(self.data)
        f.close()

        self.data = self.request.recv(4096).strip()
        f = open('sign.bin', 'wb+')
        f.write(self.data)
        f.close()

        self.data = self.request.recv(4096).strip()
        f = open('pubkey.pem', 'wb+')
        f.write(self.data)
        f.close()

        if verify_sign():
            voice = open('voice.txt', 'rb')
            sel = voice.read()
            voice.close()
            if sel == b'1':
                VOICES_CAND_1 += 1
            elif sel == b'2':
                VOICES_CAND_2 += 1
            elif sel == b'3':
                VOICES_CAND_3 += 1

        self.request.sendall(bytes(f'Current results: \n Candidate 1 - {VOICES_CAND_1} voices\n '
                                   f'Candidate 2 - {VOICES_CAND_2} voices\n '
                                   f'Candidate 3 - {VOICES_CAND_3} voices\n', encoding='utf-8'))
        os.remove('voice.txt')
        os.remove('pubkey.pem')
        os.remove('sign.bin')


with socketserver.TCPServer(('localhost', 8000), MyTCPHandler) as server:
    server.serve_forever()
