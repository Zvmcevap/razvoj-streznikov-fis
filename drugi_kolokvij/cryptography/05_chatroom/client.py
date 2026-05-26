"""
Naloga 4 - CLIENT

Encrypted chatroom client:
    - ustvari AES session key
    - ga poslje serverju, zakodiranega z RSA
    - posilja AES-zakodirana sporocila
    - v loceni niti sprejema AES-zakodirana sporocila drugih clientov

Zagon:
    python client.py
"""

import json
import socket
import threading

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

from common import send_packet, recv_packet_or_none


HOST = "127.0.0.1"
PORT = 5004


def encrypt_text(session_key: bytes, text: str) -> dict:
    """
    Enkriptira tekst z AES.
    """
    encryptor = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = encryptor.encrypt_and_digest(text.encode("utf-8"))

    return {
        "nonce": encryptor.nonce.hex(),
        "tag": tag.hex(),
        "ciphertext": ciphertext.hex(),
    }


def decrypt_packet(session_key: bytes, packet: dict) -> str:
    """
    Dekriptira AES paket.
    """
    decryptor = AES.new(
        session_key,
        AES.MODE_EAX,
        nonce=bytes.fromhex(packet["nonce"])
    )

    plaintext = decryptor.decrypt_and_verify(
        bytes.fromhex(packet["ciphertext"]),
        bytes.fromhex(packet["tag"])
    )

    return plaintext.decode("utf-8")


def listen_for_messages(sock, session_key):
    """
    Sprejema sporocila serverja.
    Tece v loceni niti, da lahko uporabnik hkrati pise.
    """
    while True:
        try:
            data = recv_packet_or_none(sock)

            if data is None:
                print("\nServer je zaprl povezavo.")
                break

            packet = json.loads(data.decode("utf-8"))
            message = decrypt_packet(session_key, packet)

            print("\n" + message)
            print("> ", end="", flush=True)

        except Exception:
            print("\nNapaka pri sprejemu sporocila.")
            break


def main():
    username = input("Username: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    try:
        # 1. Prejmi serverjev RSA public key.
        public_key = RSA.import_key(recv_packet_or_none(sock))

        # 2. Ustvari AES session key.
        session_key = get_random_bytes(16)

        # 3. Session key zakodiraj z RSA.
        rsa_encryptor = PKCS1_OAEP.new(public_key)
        encrypted_session_key = rsa_encryptor.encrypt(session_key)

        # 4. Username poslji enkriptiran z AES.
        username_packet = encrypt_text(session_key, username)

        init_packet = {
            "encrypted_session_key": encrypted_session_key.hex(),
            "username_packet": username_packet,
        }

        send_packet(sock, json.dumps(init_packet).encode("utf-8"))

        # 5. Locena nit za sprejemanje sporocil.
        listener = threading.Thread(
            target=listen_for_messages,
            args=(sock, session_key),
            daemon=True
        )
        listener.start()

        print("Povezan. Pisite sporocila. Za konec napisi /exit.")

        while True:
            text = input("> ")

            packet = encrypt_text(session_key, text)
            send_packet(sock, json.dumps(packet).encode("utf-8"))

            if text == "/exit":
                break

    finally:
        sock.close()


if __name__ == "__main__":
    main()
