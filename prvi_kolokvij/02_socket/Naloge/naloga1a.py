import socket
import sys

HOST, PORT = "149.62.71.186", 1234

# Ustvarimo socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Povežemo se

    # Pošljemo sporočilo

    # Sprejmemo sporočilo


print("Sent:     {}".format(sent))
print("Received: {}".format(received))
