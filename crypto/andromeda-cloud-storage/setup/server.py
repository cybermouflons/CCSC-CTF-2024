#!/usr/bin/env python3
import socketserver
import json
import sys
import secrets

from base64 import b64encode

from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Cipher import AES

from encoder import Encoder
from secret import FLAG_PART_2


PORT = 1337


class Server:
    def __init__(self, flag, stdin=sys.stdin.buffer, stdout=sys.stdout.buffer):
        self.stdin = stdin
        self.stdout = stdout

        self.flag = flag

        self.registered_users = {}
        self.current_user = None

        self.MAX_TITLE_LEN = 2**8 - 1
        self.MAX_FLAG_LEN = 2**8 - 1

    def send_message(self, msg: dict):
        self.stdout.write(json.dumps(msg).encode() + b"\n")
        self.stdout.flush()

    def read_message(self) -> dict:
        return json.loads(self.stdin.readline())

    def main(self):
        try:
            while True:
                try:
                    self.handle_command()
                except (
                    TypeError,
                    KeyError,
                    ValueError,
                    json.decoder.JSONDecodeError,
                ) as e:
                    self.send_message(
                        {
                            "res": f"Failed to execute command: {type(e).__name__}: {str(e)}"
                        }
                    )
        except BrokenPipeError:
            pass

    def handle_command(self):
        msg = self.read_message()
        command = msg["command"]

        match command:
            case "register":
                self.register_handler(msg)
            case "login":
                self.login_handler(msg)
            case "logout":
                self.logout_handler()
            case "edit_title":
                self.edit_title_handler(msg)
            case "delete_data":
                self.delete_data_handler(msg)
            case "insert_data":
                self.insert_data_handler(msg)
            case "encrypted_backup":
                self.encrypted_backup_handler()
            case "read_all":
                self.read_all_handler()
            case "restore_backup":
                self.restore_backup_handler(msg)
            case _:
                raise ValueError("No such command")

    def register_handler(self, msg):
        username = msg["username"]
        password = msg["password"]

        if not isinstance(username, str) or not isinstance(password, str):
            self.send_message(
                {"res": "The provided username or password is not a string."}
            )
            return

        if username in self.registered_users:
            self.send_message({"res": "Registration failed."})
            return

        # Who cares about password policies.
        self.registered_users[username] = {}
        user = self.registered_users[username]
        user["hash"] = bcrypt(b64encode(SHA256.new(password.encode()).digest()), 12)
        user["key"] = secrets.token_bytes(16)
        user.update(
            {
                "version": b"v1.1.1 Andromeda",
                "title": b"Placeholder",
                "flag": FLAG_PART_2,
                "data": b"",
            }
        )

        self.send_message(
            {
                "res": f"Your registration was succesful. You will soon receive the AES key by post. Please be patient, the mail will soon dispatch from Andromeda. In the meantime, you can edit the title and the data in your free storage."
            }
        )

    def login_handler(self, msg):
        if self.current_user is not None:
            self.send_message({"res": "Logout first."})
            return

        username = msg["username"]
        password = msg["password"]

        if username not in self.registered_users:
            self.send_message({"res": "Login failed."})
            return

        b64pwd = b64encode(SHA256.new(password.encode()).digest())
        try:
            bcrypt_check(b64pwd, self.registered_users[username]["hash"])
        except ValueError:
            self.send_message({"res": "Login failed."})
            return

        self.current_user = username
        self.send_message(
            {"res": f"Welcome to our Andromeda Cloud Storage, {self.current_user}!"}
        )

    def logout_handler(self):
        if self.current_user is None:
            self.send_message({"res": "Already logged out."})
        else:
            self.current_user = None
            self.send_message({"res": "Succesfully logged out."})

    def edit_title_handler(self, msg):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        new_title = bytes.fromhex(msg["new_title"])
        if len(new_title) > self.MAX_TITLE_LEN:
            self.send_message(
                {"res": "Title is longer than the max allowed length (255)"}
            )
            return
        user = self.registered_users[self.current_user]
        user["title"] = new_title
        self.send_message({"res": "Title was succesfully updated."})

    def delete_data_handler(self, msg):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        start_idx = msg["start_idx"]
        end_idx = msg["end_idx"]
        user = self.registered_users[self.current_user]
        if not (0 <= start_idx <= end_idx):
            self.send_message({"res": "Please provide a valid range."})
            return

        user["data"] = user["data"][:start_idx] + user["data"][end_idx + 1 :]

        self.send_message({"res": "Data range was succesfully deleted."})

    def insert_data_handler(self, msg):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        insert_idx = msg["insert_idx"]
        new_data = bytes.fromhex(msg["new_data"])
        user = self.registered_users[self.current_user]
        if insert_idx < 0:
            self.send_message({"res": "Please provide a valid insertion point."})
            return

        user["data"] = user["data"][:insert_idx] + new_data + user["data"][insert_idx:]

        self.send_message({"res": "Data was succesfully inserted."})

    def encrypted_backup_handler(self):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        user = self.registered_users[self.current_user]

        title_len = len(user["title"])
        flag_len = len(user["flag"])
        serialized_backup = (
            user["version"]
            + title_len.to_bytes(1, "big")
            + user["title"]
            + flag_len.to_bytes(1, "big")
            + user["flag"]
            + user["data"]
        )
        encoded_backup = Encoder.encode(serialized_backup)

        cipher = AES.new(user["key"], AES.MODE_GCM)
        ctxt, tag = cipher.encrypt_and_digest(encoded_backup)
        nonce = cipher.nonce
        self.send_message(
            {
                "nonce": nonce.hex(),
                "enc_backup": ctxt.hex(),
                "tag": tag.hex(),
            }
        )

    def read_all_handler(self):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        user = self.registered_users[self.current_user]

        self.send_message(
            {
                "title": user["title"].hex(),
                "data": user["data"].hex(),
            }
        )

    def restore_backup_handler(self, msg):
        if self.current_user is None:
            self.send_message({"res": "Please login first."})
            return

        tag = bytes.fromhex(msg["tag"])
        nonce = bytes.fromhex(msg["nonce"])
        enc_backup = bytes.fromhex(msg["enc_backup"])

        user = self.registered_users[self.current_user]
        cipher = AES.new(user["key"], AES.MODE_GCM, nonce=nonce)
        try:
            encoded_backup = cipher.decrypt_and_verify(enc_backup, tag)
        except:
            self.send_message({"res": "Backup decryption failed."})
            return

        serialized_backup = Encoder.decode(encoded_backup)
        pos = 0
        version = serialized_backup[pos : pos + 16]
        pos += 16
        title_len = serialized_backup[pos]
        pos += 1
        if len(serialized_backup[pos:]) < title_len:
            self.send_message({"res": "Invalid format."})
            return
        title = serialized_backup[pos : pos + title_len]
        pos += title_len
        flag_len = serialized_backup[pos]
        pos += 1
        if len(serialized_backup[pos:]) < flag_len:
            self.send_message({"res": "Invalid format."})
            return
        flag = serialized_backup[pos : pos + flag_len]
        pos += flag_len
        data = serialized_backup[pos:]

        user["version"] = version
        user["title"] = title
        user["flag"] = flag
        user["data"] = data

        self.send_message({"res": "Backup restored."})


if __name__ == "__main__":

    class RequestHandler(socketserver.StreamRequestHandler):
        def handle(self):
            server = Server(flag=FLAG_PART_2, stdin=self.rfile, stdout=self.wfile)
            server.main()

    class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    TCPServer(("0.0.0.0", PORT), RequestHandler).serve_forever()
