"""
Naloga 4 - SERVER

Chatroom z enkriptiranimi sporocili:
    - vsak client ima svoj AES session key s serverjem
    - client poslje enkriptirano sporocilo serverju
    - server ga dekriptira
    - server ga ponovno enkriptira za vsakega drugega clienta
    - vsak client prejme sporocila ostalih

Pomembno:
    To ni end-to-end enkripcija.
    Server vidi plaintext, ker mora sporocila preposiljati drugim clientom.

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
PORT = 5004


def encrypt_text(session_key: bytes, text: str) -> dict:
    """
    Enkriptira tekst za enega clienta.
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
    Dekriptira AES paket od clienta.
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


def broadcast(sender_socket, sockets, session_keys, usernames, text):
    """
    Poslje sporocilo vsem clientom razen posiljatelju.
    Za vsakega prejemnika uporabi njegov AES session key.
    """
    sender_name = usernames.get(sender_socket, "unknown")
    outgoing_text = f"{sender_name}: {text}"

    for client_socket in list(session_keys.keys()):
        if client_socket is sender_socket:
            continue

        try:
            packet = encrypt_text(session_keys[client_socket], outgoing_text)
            send_packet(client_socket, json.dumps(packet).encode("utf-8"))

        except Exception:
            # Ce clientu ne moremo poslati, ga odstranimo.
            if client_socket in sockets:
                sockets.remove(client_socket)

            session_keys.pop(client_socket, None)
            usernames.pop(client_socket, None)
            client_socket.close()


def main():
    private_key = RSA.generate(2048)
    public_key_bytes = private_key.publickey().export_key()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    sockets = [server_socket]

    # client_socket -> AES session key
    session_keys = {}

    # client_socket -> username
    usernames = {}

    print(f"Encrypted chat server poslusa na {HOST}:{PORT}")

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [])

            for sock in readable:
                if sock is server_socket:
                    # Nov client.
                    client_socket, addr = server_socket.accept()
                    print("Nov client:", addr)

                    # 1. Poslji public RSA key.
                    send_packet(client_socket, public_key_bytes)

                    # 2. Prejmi init paket:
                    #    - RSA-zakodiran AES session key
                    #    - AES-zakodiran username
                    init_data = recv_packet_or_none(client_socket)

                    if init_data is None:
                        client_socket.close()
                        continue

                    init_packet = json.loads(init_data.decode("utf-8"))

                    rsa_decryptor = PKCS1_OAEP.new(private_key)
                    session_key = rsa_decryptor.decrypt(
                        bytes.fromhex(init_packet["encrypted_session_key"])
                    )

                    username = decrypt_packet(
                        session_key,
                        init_packet["username_packet"]
                    )

                    sockets.append(client_socket)
                    session_keys[client_socket] = session_key
                    usernames[client_socket] = username

                    print(f"{username} se je povezal.")

                    # Ostalim sporoci, da je prisel nov uporabnik.
                    broadcast(
                        client_socket,
                        sockets,
                        session_keys,
                        usernames,
                        "se je povezal."
                    )

                else:
                    # Sporocilo od obstojecega clienta.
                    data = recv_packet_or_none(sock)

                    if data is None:
                        username = usernames.get(sock, "unknown")
                        print(f"{username} se je odklopil.")

                        sockets.remove(sock)
                        session_keys.pop(sock, None)
                        usernames.pop(sock, None)
                        sock.close()
                        continue

                    try:
                        packet = json.loads(data.decode("utf-8"))
                        message = decrypt_packet(session_keys[sock], packet)

                        if message == "/exit":
                            username = usernames.get(sock, "unknown")
                            print(f"{username} je zapustil chat.")

                            sockets.remove(sock)
                            session_keys.pop(sock, None)
                            usernames.pop(sock, None)
                            sock.close()
                            continue

                        print(f"{usernames[sock]}: {message}")

                        # Preposlji vsem ostalim.
                        broadcast(sock, sockets, session_keys, usernames, message)

                    except Exception as e:
                        print("Napaka pri clientu:", e)

                        if sock in sockets:
                            sockets.remove(sock)

                        session_keys.pop(sock, None)
                        usernames.pop(sock, None)
                        sock.close()

    finally:
        for sock in sockets:
            sock.close()


if __name__ == "__main__":
    main()
