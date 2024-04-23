#!/usr/bin/env python3
import json
import os

from telnetlib import Telnet
from datetime import datetime
from pytz import timezone

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def blockify(msg: bytes, block_size: int):
    block = [msg[i : i + block_size] for i in range(0, len(msg), block_size)]
    return block


def xor(X: bytes, Y: bytes):
    return bytes(x ^ y for (x, y) in zip(X, Y))


def readline(tn: Telnet):
    return tn.read_until(b"\n")


def json_recv(tn: Telnet):
    line = readline(tn)
    return json.loads(line.decode("utf-8"))


def json_send(tn: Telnet, req):
    request = json.dumps(req).encode("utf-8")
    tn.write(request + b"\n")


def register(tn: Telnet, username: str, password: str):
    request = {
        "command": "register",
        "username": username,
        "password": password,
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def login(tn: Telnet, username: str, password: str):
    request = {
        "command": "login",
        "username": username,
        "password": password,
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def logout(tn: Telnet):
    request = {
        "command": "logout",
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def edit_title(tn: Telnet, new_title: bytes):
    request = {
        "command": "edit_title",
        "new_title": new_title.hex(),
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def delete_data(tn: Telnet, start_idx: int, end_idx: int):
    request = {
        "command": "delete_data",
        "start_idx": start_idx,
        "end_idx": end_idx,
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def insert_data(tn: Telnet, insert_idx: int, new_data: bytes):
    request = {
        "command": "insert_data",
        "insert_idx": insert_idx,
        "new_data": new_data.hex(),
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def get_encrypted_backup(tn: Telnet):
    request = {
        "command": "encrypted_backup",
    }
    json_send(tn, request)
    res = json_recv(tn)
    return bytes.fromhex(res["enc_backup"])


def read_all(tn: Telnet):
    request = {
        "command": "read_all",
    }
    json_send(tn, request)
    res = json_recv(tn)
    return bytes.fromhex(res["title"]), bytes.fromhex(res["data"])


def restore_backup(tn: Telnet, enc_backup: bytes):
    request = {
        "command": "restore_backup",
        "enc_backup": enc_backup.hex(),
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def oracle_valid_padding(msg: str):
    hour = int(msg[-6:-4])
    tZ = datetime.now(timezone("CET"))
    padding_hour = tZ.hour
    if hour == padding_hour:
        return False
    else:
        return True


def attack(tn: Telnet):
    username = "ccsc"
    password = "ccsc"

    _ = register(tn, username, password)
    _ = login(tn, username, password)

    enc_backup = get_encrypted_backup(tn)

    iv = enc_backup[: AES.block_size]
    c_blocks = blockify(
        enc_backup[AES.block_size : -SHA256.digest_size], AES.block_size
    )
    tag = enc_backup[-SHA256.digest_size :]

    guess_blocks = []
    prev_c = iv
    prev_p = bytes([0]) * AES.block_size
    for current_c in c_blocks:
        p_guess = b""
        mask_rhs = b""
        # find the iv block that results into a valid padding of size AES.block_size
        for i in range(AES.block_size):
            mask_lhs = b"\x00" * (AES.block_size - i - 1)
            # find the byte that results into a valid padding of size i+1
            for b in range(256):
                last_mask_rhs = bytes([mask_rhs[-1] ^ i ^ (i + 1)]) if i > 0 else b""
                guess_mask = mask_lhs + bytes([b]) + mask_rhs[:-1] + last_mask_rhs
                guess_iv = xor(xor(prev_c, prev_p), guess_mask)
                res = restore_backup(tn, guess_iv + current_c + tag)
                if oracle_valid_padding(res):
                    # check for edge case when the second, (and third, and forth...)
                    # last byte(s) is/are the zero byte. It requires an additional
                    # padding oracle query that modifies the second last byte just
                    # to break a valid padding that occurs by chance.
                    if i == 0:
                        guess_mask = mask_lhs[:-1] + b"\x01" + bytes([b])
                        guess_iv = xor(xor(prev_c, prev_p), guess_mask)
                        res = restore_backup(tn, guess_iv + current_c + tag)
                        if not oracle_valid_padding(res):
                            continue
                        p_guess = bytes([b ^ (i + 1)]) + p_guess
                        mask_rhs = bytes([b])
                    elif i != 0:
                        p_guess = bytes([b]) + p_guess
                        mask_rhs = (
                            bytes([b])
                            + mask_rhs[:-1]
                            + bytes([mask_rhs[-1] ^ i ^ (i + 1)])
                        )
                    break
        prev_c = current_c
        prev_p = p_guess
        guess_blocks.append(p_guess)
    
    flag = b"".join(guess_blocks)[33:-18]
    print(flag)


if __name__ == "__main__":
    if "REMOTE" in os.environ:
        HOSTNAME = ""
    else:
        HOSTNAME = "localhost"
    PORT = 1337
    with Telnet(HOSTNAME, PORT) as tn:
        attack(tn)
