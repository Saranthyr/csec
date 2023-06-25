import os
import socket
import subprocess
import sys
import time

HOST, PORT_INTER, PORT_FINAL = "localhost", 5110, 8000


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT_INTER))

        pubkey = sock.recv(4096)
        f = open('pubkey.pem', 'wb+')
        f.write(pubkey)
        f.close()

        data = input('Welcome to golosovanie. Print number for candidates: 1 for cand 1, 2 for cand, 3 for cand 3\n')

        f = open('voice.txt', 'wb+')
        f.write(bytes(data, 'utf-8'))
        f.close()

        subprocess.run('openssl rsautl -encrypt -inkey pubkey.pem -pubin -in voice.txt -out voice.enc')

        sock.sendall(open('voice.enc', 'rb').read())

        sign = sock.recv(4096).strip()
        sock.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT_FINAL))
        sock.sendall(open('voice.txt', 'rb').read())
        time.sleep(0.1)
        sock.sendall(sign)
        time.sleep(0.1)
        sock.sendall(open('pubkey.pem', 'rb').read())
        print(sock.recv(4096).decode('utf-8'))
        sock.close()
        os.remove('voice.txt')
        os.remove('pubkey.pem')
        os.remove('voice.enc')

    while True:
        continuation = input('Do you wish to vote again? y/n\n')
        if continuation != "n" and continuation != "y":
            print('Wrong input.')
        else:
            break
    if continuation == "n":
        break
    elif continuation == "y":
        pass
