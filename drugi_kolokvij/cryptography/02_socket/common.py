"""
Skupne pomocne funkcije za posiljanje paketov po socketu.

Problem:
    TCP je stream, ne paketni protokol.
    Ce samo naredimo sock.recv(1024), ni nujno, da dobimo celo sporocilo.

Resitev:
    Pred vsakim sporocilom posljemo 4 bajte dolzine.
    Nato posljemo se podatke.
"""

import struct


def send_packet(sock, data: bytes):
    """
    Poslje paket:
        1. 4 bajti: dolzina podatkov
        2. podatki
    """
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)


def recv_exact(sock, n: int) -> bytes:
    """
    Prebere tocno n bajtov.
    Ce se povezava zapre, sprozi ConnectionError.
    """
    data = b""

    while len(data) < n:
        chunk = sock.recv(n - len(data))

        if not chunk:
            raise ConnectionError("Povezava je bila zaprta.")

        data += chunk

    return data


def recv_packet(sock) -> bytes:
    """
    Prebere paket, ki je bil poslan s send_packet().
    """
    raw_len = recv_exact(sock, 4)
    packet_len = struct.unpack("!I", raw_len)[0]

    return recv_exact(sock, packet_len)
