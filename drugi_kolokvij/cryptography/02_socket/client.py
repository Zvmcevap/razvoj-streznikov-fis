"""
Naloga 2(a) - CLIENT

Client:
    - od serverja prejme RSA public key
    - ustvari AES session key
    - z RSA zakodira AES key
    - z AES zakodira sporocilo
    - vse potrebno poslje serverju

Zagon:
    python client.py
"""

import json
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

from common import send_packet, recv_packet


HOST = "127.0.0.1"
PORT = 5001


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    with sock:
        # 1. Prejmi public RSA key od serverja.
        public_key_bytes = recv_packet(sock)
        public_key = RSA.import_key(public_key_bytes)

        # 2. Ustvari AES session key.
        session_key = get_random_bytes(16)

        # 3. AES session key zakodiraj z RSA public key-em.
        rsa_encryptor = PKCS1_OAEP.new(public_key)
        encrypted_session_key = rsa_encryptor.encrypt(session_key)

        # 4. Sporocilo zakodiraj z AES.
        message = input("Vnesi sporocilo: ").encode("utf-8")

        aes_encryptor = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = aes_encryptor.encrypt_and_digest(message)

        # 5. Poslji vse, kar server potrebuje za dekripcijo.
        packet = {
            "encrypted_session_key": encrypted_session_key.hex(),
            "nonce": aes_encryptor.nonce.hex(),
            "tag": tag.hex(),
            "ciphertext": ciphertext.hex(),
        }

        send_packet(sock, json.dumps(packet).encode("utf-8"))

        print("Sporocilo poslano.")


if __name__ == "__main__":
    main()
