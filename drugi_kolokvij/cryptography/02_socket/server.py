"""
Naloga 2(a) - SERVER

Hibridna enkripcija preko socketa:
    - RSA se uporabi za prenos AES session key-a.
    - AES se uporabi za dejansko sporocilo.

Zagon:
    python server.py
"""

import json
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

from common import send_packet, recv_packet


HOST = "127.0.0.1"
PORT = 5001


def main():
    # Server ustvari RSA par kljucev.
    # Private key ostane na serverju.
    # Public key posljemo clientu.
    private_key = RSA.generate(2048)
    public_key_bytes = private_key.publickey().export_key()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server poslusa na {HOST}:{PORT}")

    conn, addr = server_socket.accept()

    with conn:
        print("Client povezan:", addr)

        # 1. Clientu poslji public RSA key.
        send_packet(conn, public_key_bytes)

        # 2. Prejmi JSON s hibridno zakodiranimi podatki.
        packet = json.loads(recv_packet(conn).decode("utf-8"))

        encrypted_session_key = bytes.fromhex(packet["encrypted_session_key"])
        nonce = bytes.fromhex(packet["nonce"])
        tag = bytes.fromhex(packet["tag"])
        ciphertext = bytes.fromhex(packet["ciphertext"])

        # 3. RSA private key odklene AES session key.
        rsa_decryptor = PKCS1_OAEP.new(private_key)
        session_key = rsa_decryptor.decrypt(encrypted_session_key)

        # 4. AES session key odklene sporocilo.
        aes_decryptor = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
        plaintext = aes_decryptor.decrypt_and_verify(ciphertext, tag)

        print("Dekodirano sporocilo:")
        print(plaintext.decode("utf-8"))

    server_socket.close()


if __name__ == "__main__":
    main()
