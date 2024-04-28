import math
import os
import string
from functools import cache
from itertools import cycle
from typing import Tuple

from banner import banner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from secret import FLAG

BLOCK_SIZE = 16
KEY = os.urandom(32)


@cache
def get_random_blocks(n: int, block_size: int = BLOCK_SIZE) -> bytes:
    if n > 1:
        return get_random_blocks(n - 1) + os.urandom(block_size)
    elif n == 1:
        return os.urandom(block_size)
    else:
        return b""


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, cycle(key)))


def encrypt(input_data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
    iv = os.urandom(BLOCK_SIZE)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(input_data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data, iv


def decrypt(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data


def start_new_session(key: bytes) -> tuple[bytes, bytes]:
    user = input("Please enter a username: ")
    user = "".join(c for c in user if c in string.ascii_lowercase)
    session = f"user={user}&flag={FLAG}".encode()
    enc_session, session_iv = encrypt(session, key)
    return enc_session, session_iv


def use_existing_session() -> bytes:
    session_hex = input("Please enter an existing session (hex): ")
    return bytes.fromhex(session_hex)


def show_masked_flag(session: bytes, iv: bytes, key: bytes) -> None:
    dec_cookie = decrypt(session, key, iv)
    flag = dec_cookie.split(b"=")[-1]
    flag_enc = xor(
        flag,
        get_random_blocks(math.ceil(len(flag) / BLOCK_SIZE)),
    )
    print("Masked flag:", flag_enc.hex())


if __name__ == "__main__":
    print(banner)
    session, session_iv = None, None
    while True:
        try:
            print("Please select one of the following options")
            if session is None:
                print("1. Start new session")
                print("2. Use an existing encrypted session state")
            else:
                print("Current session:", session.hex())
                print("1. Exit session")
                print("2. Show masked flag")

            option = input(">>> ")
            if option not in ["1", "2"]:
                print("Invalid option")
                exit(1)

            if session is None:
                if option == "1":
                    session, session_iv = start_new_session(KEY)
                elif option == "2":
                    session = use_existing_session()
            else:
                if option == "1":
                    session = None
                elif option == "2":
                    show_masked_flag(session, session_iv, KEY)
        except ValueError as e:
            print("Invalid input", e)
        except Exception as e:
            print("An error occurred during decryption:", e)
