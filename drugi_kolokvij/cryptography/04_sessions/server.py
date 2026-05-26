"""
Naloga 3 - SERVER

Vec sessionov v enem programu:
    - server sprejme vec clientov
    - vsak client ima svoj AES session key
    - server uporablja select(), da spremlja vec socketov hkrati
    - sporocila samo prejema in dekriptira

Zagon:
    python server.py
"""

import json
import select
import socket

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

from common import send_packet, recv_packet_or_none


HOST = "127.0.0.1"
PORT = 5003


def decrypt_message(session_key: bytes, packet: dict) -> str:
    """
    Dekodira AES paket od posameznega clienta.
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


def main():
    private_key = RSA.generate(2048)
    public_key_bytes = private_key.publickey().export_key()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # V tem seznamu so server socket in vsi client socketi.
    sockets = [server_socket]

    # Slovar: client_socket -> AES session key
    session_keys = {}

    print(f"Server poslusa na {HOST}:{PORT}")

    try:
        while True:
            # select pove, kateri socketi imajo podatke za branje.
            readable, _, _ = select.select(sockets, [], [])

            for sock in readable:
                if sock is server_socket:
                    # Nov client.
                    client_socket, addr = server_socket.accept()
                    print("Nov client:", addr)

                    # 1. Poslji RSA public key.
                    send_packet(client_socket, public_key_bytes)

                    # 2. Prejmi RSA-zakodiran AES session key.
                    encrypted_session_key = recv_packet_or_none(client_socket)

                    if encrypted_session_key is None:
                        client_socket.close()
                        continue

                    rsa_decryptor = PKCS1_OAEP.new(private_key)
                    session_key = rsa_decryptor.decrypt(encrypted_session_key)

                    sockets.append(client_socket)
                    session_keys[client_socket] = session_key

                    print("Session key nastavljen za:", addr)

                else:
                    # Obstojeci client posilja sporocilo.
                    data = recv_packet_or_none(sock)

                    if data is None:
                        print("Client se je odklopil.")
                        sockets.remove(sock)
                        session_keys.pop(sock, None)
                        sock.close()
                        continue

                    try:
                        packet = json.loads(data.decode("utf-8"))
                        message = decrypt_message(session_keys[sock], packet)

                        print("Client:", message)

                        if message == "/exit":
                            print("Client je poslal /exit.")
                            sockets.remove(sock)
                            session_keys.pop(sock, None)
                            sock.close()

                    except Exception as e:
                        print("Napaka pri dekripciji:", e)
                        sockets.remove(sock)
                        session_keys.pop(sock, None)
                        sock.close()

    finally:
        for sock in sockets:
            sock.close()


if __name__ == "__main__":
    main()
