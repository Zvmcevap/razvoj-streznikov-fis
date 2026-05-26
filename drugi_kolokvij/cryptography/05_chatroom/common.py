"""
Pomocne funkcije za socket pakete.

Ta verzija pri zaprti povezavi vrne None,
kar je prirocno pri serverju z vec clienti.
"""

import struct


def send_packet(sock, data: bytes):
    """
    Poslje paket:
        - 4 bajte dolzine
        - nato podatke
    """
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)


def recv_exact_or_none(sock, n: int):
    """
    Prebere tocno n bajtov.
    Ce je povezava zaprta, vrne None.
    """
    data = b""

    while len(data) < n:
        chunk = sock.recv(n - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def recv_packet_or_none(sock):
    """
    Prebere en cel paket.
    Ce je povezava zaprta, vrne None.
    """
    raw_len = recv_exact_or_none(sock, 4)

    if raw_len is None:
        return None

    packet_len = struct.unpack("!I", raw_len)[0]

    return recv_exact_or_none(sock, packet_len)
