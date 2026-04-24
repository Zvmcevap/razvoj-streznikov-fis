import socket
import sys

HOST, PORT = "0.0.0.0", 1234
data = "Živjo!"

# Ustvarimo socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Povežemo se
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Sprejmemo
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))