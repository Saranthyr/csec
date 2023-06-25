import sys
import socket
import selectors
import time
import types

HOST = 'localhost'
PORT = 5110

data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
#     sk.connect((HOST, PORT))
#     print('Press 1 to receive certificate, press 2 to send file')
#     a = input()
#     if a == '1':
#         data = b'Cert request'
#         sk.sendall(data)
#         cert_data = b''
#         while True:
#             part = sk.recv(1024)
#             cert_data += part
#             if len(part) < 1024:
#                 break
#         f = open('cert.pem', 'wb+')
#         f.write(cert_data)
#         f.close()
#     elif a == '2':
#         data = b'filename:cert.pem'
#         sk.sendall(data)
#         f = open('cert.pem', 'rb')
#         data = f.read()
#         f.close()
#         sk.sendall(data)
#     # else:
#     # file = open('Facial_Animation_-_RimhammerDwarves.xml', 'rb')
#     # data = file.read()
#     # file.close()
