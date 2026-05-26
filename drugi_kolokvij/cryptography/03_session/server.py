"""
Naloga 2(b) - SERVER

Razlika od 2(a):
    - RSA handshake se naredi samo enkrat.
    - Server prejme en AES session key.
    - Nato z istim session key-em prejema vec sporocil.

Zagon:
    python server.py
"""

import json
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

from common import send_packet, recv_packet


HOST = "127.0.0.1"
PORT = 5002


def decrypt_message(session_key: bytes, packet: dict) -> str:
    """
    Dekodira eno AES sporocilo.
    Vsako sporocilo ima svoj nonce in tag.
    """
    nonce = bytes.fromhex(packet["nonce"])
    tag = bytes.fromhex(packet["tag"])
    ciphertext = bytes.fromhex(packet["ciphertext"])

    decryptor = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    plaintext = decryptor.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode("utf-8")


def main():
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

        # 1. Poslji public RSA key.
        send_packet(conn, public_key_bytes)

        # 2. Prejmi RSA-zakodiran AES session key.
        encrypted_session_key = recv_packet(conn)

        rsa_decryptor = PKCS1_OAEP.new(private_key)
        session_key = rsa_decryptor.decrypt(encrypted_session_key)

        print("Session key prejet.")
        print("Cakam sporocila...")

        # 3. Z istim session key-em prejemaj vec sporocil.
        while True:
            try:
                packet = json.loads(recv_packet(conn).decode("utf-8"))
                message = decrypt_message(session_key, packet)

                print("Client:", message)

                if message == "/exit":
                    print("Client je zakljucil.")
                    break

            except ConnectionError:
                print("Client je zaprl povezavo.")
                break
            except ValueError:
                print("Napaka: tag ni pravilen ali sporocilo ni veljavno.")
                break

    server_socket.close()


if __name__ == "__main__":
    main()
