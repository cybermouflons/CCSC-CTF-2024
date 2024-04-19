#!/usr/bin/env python3
import json
import os

from telnetlib import Telnet

from encoder import Encoder

PART_1 = b"In the\x98\xa8\x90o\x90-li\xd0\xc0d\xc0p\xf9s\xb0\xe8f\x90\xb1\xd0\xe9ig\x88\xb8al\xb8\xc8xp\xa8ns\xa8,\xc0wh\xa0r\x88\xa8t\xa9\n\xc9isp\xe1\x98\xe0of\x90anc\xe0\xd0\x98t\xb8my\x98hs\xa8\xd0\xc9\xe0r\x90w\xb1\xa8\xd0\xa1\xb8h\xa0\x91\xc1\x90um\x98of\x91v\xd0rcl\xa8\x90k\xb0d\xd8p\xc8\xb9\xb0s\x80\xa0\xb0\x90,\na\xe8\xd0l\x98nd\xf1ti\xa8\xa0\xd9\xd0\xe0\x80\xa0\xb0\xa8ho\xf9\xb0t\xa8r\xb0ug\xa0\xba\xe0\x98cyb\xa0\xe8n\x90\xd0i\xc0\xd0\xa0\xf9\xd1.\xb0You,\xa0a\x88skil\x80\xf8d\xb8h\xd0c\xc8\xb0r,\nf\xf0n\xe1you\xd0s\xe8l\xd8\xc0th\xb8\xc8\xc0\xa0\xb0in\x98o\xdae\x98cla\xd0d\xb0s\xd0i\xa8\xd9wor\xe8\xd8\xa8\xa0f\x90\xe8h\xe1An\xd0\xe8\xd0m\xb8\xa0a\xc8I\xc8it\x88\xb0\x91v\xe0,\n\xa8\xb8sk\xb0d w\xe0\xc0h\xa0\xb0\xa0\xd8m\xf0n\xc0l\xb0\x98g\xd8\xf1e\x98\xe8\xc1\x88\x98\xc0\xb8r\xc0P\x90oj\xb0c\xc8\xb8E\x98h\xc0\xa0d\xc8vis\x98\xa8\xb8by\x90t\xf0\xb8\x98omn\xf0p\xa0\xc8\xc0\xa8\x90\nOr\xc8\xc0\xb0T\xc8ch. Am\xd0dst\xb0\x88\xd0\xe8\x98\xb0prawl\xf0ng\xc8v\xa0\xc8tu\xd8\xd0\xb8\x88\x98\xe0dsc\xa0pe\xa0\xd0of\x90Cy\xc0ru\xc8,\xb8wh\xf8\xb8\x88\xa8t\xa9\n\x88c\xa0o\x98s\xd0\x98f\x90\xb8i\xb0t\xb0ry\xb8c\xa0l\x80\xd0de\xb8w\xa0\xf0h\xe1\xf8b\xc8rpunk\xc8\xa8\xb8\xc9l\x80io\xd0,\xd0y\xa0u\xe8\xa0k\xe8\xb0b\xb8a\xb8d\xc0\xa8\xc0c\xb8m\x98s\n\xd8\xc8w\xa8\x98p\xd0n\xb0\x90f\x90ch\xa0i\x98\xe8,\xb8\xf8\xe8d\x98y\xd0ur\xa0w\xf0t\xe1\x88f\xd0\xc8m\xc0d\xb8ble\xd0sh\xc0\xa0\xb0\xd0\xb0\xd8g\x88\xb8n\xd8t\xb8\x88\xf0\xe8\x98\x88\xc0cro\xf0\x98\xc8i\xb8g\nd\xb8\xd0k\xb0es\x80. A\x98\x90you\x98\xe0avig\x98te\xc0\x90h\x9ar\x98\xd0c\xb9\xa8ous\xd8l\xc8by\xc0int\xf0\xc8\xe8f\x90e\xb8c\xd8\xe8p\xd8\xb0d\xc8m\xb0s\xb1\xd8i\x90\xa8\nan\xe9fo\xd0g\xd0\xa8u\xc8lik\xb0\x98y\xc0a\x98\xc1\x98\xe0c\xd0s\xc8w\xb8th\xa0rogu\xd8\xa8AI\xf0,\xa0\xe9\xc1lin\xa1b\x90\xd0w\x90\x80\xc0\xb8fr\xe8\xa9d\xb0a\x99\xd1o\xc8\nblurs\xc8i\xe8\x90th\xa0\xb9\x99g\x90-\xb0\xd0ake\xd9\x88\xc8\xb0dow\xb0\x88\xa8r.\xa0T\xd8e\x98f\xc0t\xa1o\xa8\x90gl\xa0b\xd0\x98\xb0\x90u\xf0\xb8n\x88my\xc0h\xc8\xb0gs\xa8i\xa0\n\xf8\xc8e\xb0b\xe0l\xf1c\xb8,\xc0\xa9d\x98th\xc0\x98\xb0\x90\xa8work\xb8puls\xd0\x88\xb0\xd8i\xf0h\xa0an\xa0\xb0c\x88p\xb0\xa9o\xc8\xe0f\x98r\x98\xc0he\x98l\x90g\x88\xe8da\xe0y\xc8\xa0\xb8\x80\x90s\nth\xd8\x90\xd0\x90w\x88i\xa8.\xb0Ok\x90\xf4\xd8s\x90enoug\xd8,\xb8\x90\xc0r\x88\xfbt\xc0\xb1f\xb8\xd8\xc0\xb8\xa8pa\xa8\xa1o\xd8\x90\xa0he\x98\xa8l\xe0g.\xa8'c\x80s\x88{\x88on\xd8r\xf0t\xc8\xf8he\xb0\x88\xa0i\xb9\xd8\x88'"

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
    return (
        bytes.fromhex(res["nonce"]),
        bytes.fromhex(res["enc_backup"]),
        bytes.fromhex(res["tag"]),
    )


def read_all(tn: Telnet):
    request = {
        "command": "read_all",
    }
    json_send(tn, request)
    res = json_recv(tn)
    return bytes.fromhex(res["title"]), bytes.fromhex(res["data"])


def restore_backup(tn: Telnet, nonce: bytes, enc_backup: bytes, tag: bytes):
    request = {
        "command": "restore_backup",
        "tag": tag.hex(),
        "nonce": nonce.hex(),
        "enc_backup": enc_backup.hex(),
    }
    json_send(tn, request)
    res = json_recv(tn)
    return res["res"]


def attack(tn: Telnet):
    WINDOW_SIZE = 16
    LENGTH_SIZE = 8
    username = "ccsc"
    password = "ccsc"
    dummy_block = b"\x00" * WINDOW_SIZE

    _ = register(tn, username, password)
    _ = login(tn, username, password)

    guess_seq = b""
    for _ in range(LENGTH_SIZE):
        ctxt_min_len = None
        byte_min_len = None
        for b in range(1, 128):
            edit_title(tn, dummy_block + (guess_seq + bytes([b])) * 3)
            _, ctxt, _ = get_encrypted_backup(tn)
            if ctxt_min_len is None or len(ctxt) < ctxt_min_len:
                ctxt_min_len = len(ctxt)
                byte_min_len = bytes([b])
        guess_seq += byte_min_len

    flag_len = guess_seq[0]

    guess_seq_back = b""
    for _ in range(flag_len - (LENGTH_SIZE - 1)):
        ctxt_min_len = None
        byte_min_len = None
        for b in range(1, 128):
            new_data = (bytes([b]) + guess_seq_back) * 3 + dummy_block
            insert_data(tn, 0, new_data)
            _, ctxt, _ = get_encrypted_backup(tn)
            if ctxt_min_len is None or len(ctxt) < ctxt_min_len:
                ctxt_min_len = len(ctxt)
                byte_min_len = bytes([b])
            delete_data(tn, 0, len(new_data) - 1)
        guess_seq_back = byte_min_len + guess_seq_back

    flag_part_2 = guess_seq[1:] + guess_seq_back
    
    flag_part_1 = Encoder.decode(PART_1)[-25:-1]
    print(flag_part_1 + flag_part_2)


if __name__ == "__main__":
    if "REMOTE" in os.environ:
        HOSTNAME = ""
    else:
        HOSTNAME = "localhost"
    PORT = 1337
    with Telnet(HOSTNAME, PORT) as tn:
        attack(tn)
