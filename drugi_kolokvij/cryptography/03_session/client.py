"""
Naloga 2(b) - CLIENT

Client:
    - najprej poslje AES session key, zakodiran z RSA
    - nato v zanki posilja vec AES-zakodiranih sporocil
    - isti session key se uporablja do konca povezave

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
PORT = 5002


def encrypt_message(session_key: bytes, text: str) -> dict:
    """
    Zakodira eno sporocilo z AES.
    Pomembno:
        Za vsako sporocilo ustvarimo nov nonce.
    """
    encryptor = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = encryptor.encrypt_and_digest(text.encode("utf-8"))

    return {
        "nonce": encryptor.nonce.hex(),
        "tag": tag.hex(),
        "ciphertext": ciphertext.hex(),
    }


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    with sock:
        # 1. Prejmi RSA public key.
        public_key = RSA.import_key(recv_packet(sock))

        # 2. Ustvari en AES session key za celo povezavo.
        session_key = get_random_bytes(16)

        # 3. Session key zakodiraj z RSA in ga poslji serverju.
        rsa_encryptor = PKCS1_OAEP.new(public_key)
        encrypted_session_key = rsa_encryptor.encrypt(session_key)

        send_packet(sock, encrypted_session_key)

        print("Session key poslan.")
        print("Vnasaj sporocila. Za konec napisi /exit.")

        # 4. Posiljaj vec sporocil z istim session key-em.
        while True:
            text = input("> ")

            packet = encrypt_message(session_key, text)
            send_packet(sock, json.dumps(packet).encode("utf-8"))

            if text == "/exit":
                break


if __name__ == "__main__":
    main()
