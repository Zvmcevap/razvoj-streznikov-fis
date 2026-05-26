"""
Naloga 1: posebej preizkusi RSA in AES enkripcijo.

Zagon:
    python main.py

Potrebna knjiznica:
    python -m pip install pycryptodome

Kaj prikaze:
    1. RSA:
       - ustvari par kljucev
       - enkriptira z javnim kljucem
       - dekriptira z zasebnim kljucem

    2. AES:
       - ustvari simetricni session key
       - enkriptira sporocilo
       - dekriptira sporocilo z istim kljucem
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes


def test_rsa():
    print("=== RSA TEST ===")

    # RSA je asimetricna enkripcija.
    # To pomeni, da imamo dva kljuca:
    # - public key: za enkripcijo
    # - private key: za dekripcijo
    key_pair = RSA.generate(2048)
    private_key = key_pair
    public_key = key_pair.publickey()

    message = b"Pozdrav iz RSA testa."

    # PKCS1_OAEP je priporocen nacin za RSA enkripcijo.
    encryptor = PKCS1_OAEP.new(public_key)
    ciphertext = encryptor.encrypt(message)

    decryptor = PKCS1_OAEP.new(private_key)
    plaintext = decryptor.decrypt(ciphertext)

    print("Original :", message.decode("utf-8"))
    print("Encrypted:", ciphertext.hex())
    print("Decrypted:", plaintext.decode("utf-8"))
    print()


def test_aes():
    print("=== AES TEST ===")

    # AES je simetricna enkripcija.
    # Isti kljuc se uporablja za enkripcijo in dekripcijo.
    session_key = get_random_bytes(16)  # 16 bajtov = AES-128
    message = b"Pozdrav iz AES testa."

    # AES.MODE_EAX poleg enkripcije omogoca tudi preverjanje integritete.
    encryptor = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = encryptor.encrypt_and_digest(message)
    nonce = encryptor.nonce

    # Za dekripcijo potrebujemo:
    # - isti session_key
    # - nonce
    # - tag
    decryptor = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    plaintext = decryptor.decrypt_and_verify(ciphertext, tag)

    print("Original :", message.decode("utf-8"))
    print("Key      :", session_key.hex())
    print("Nonce    :", nonce.hex())
    print("Tag      :", tag.hex())
    print("Encrypted:", ciphertext.hex())
    print("Decrypted:", plaintext.decode("utf-8"))
    print()


if __name__ == "__main__":
    test_rsa()
    test_aes()
