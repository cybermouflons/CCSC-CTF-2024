#!/usr/bin/env python3
import socketserver
import json
import sys
import secrets

from datetime import datetime
from pytz import timezone
tz = datetime.now(timezone("EET"))
tZ = datetime.now(timezone("CET"))

from base64 import b64encode

from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Cipher import AES

from secret import FLAG


PORT = 1337

def blockify(msg: bytes, block_size: int):
    block = [msg[i : i + block_size] for i in range(0, len(msg), block_size)]
    return block


def xor(X: bytes, Y: bytes):
    return bytes(x ^ y for (x, y) in zip(X, Y))


class SE:

    def __init__(self, key_enc=None, key_mac=None):
        self.key_enc = key_enc
        self.key_mac = key_mac
        if self.key_enc is None:
            self.key_enc = secrets.token_bytes(16)

        if self.key_mac is None:
            self.key_mac = secrets.token_bytes(16)

    def encrypt(self, ptxt: bytes, iv=None):
        prev_c = iv
        prev_p = bytes([0]) * AES.block_size
        if prev_c is None:
            prev_c = secrets.token_bytes(AES.block_size)

        ptxt_padded = pad(ptxt, AES.block_size, style="x923")
        blocks = blockify(ptxt_padded, AES.block_size)
        cipher = AES.new(self.key_enc, AES.MODE_ECB)

        ctxt = prev_c
        for block in blocks:
            mask = xor(prev_p, prev_c)
            interm = xor(mask, block)
            prev_c = cipher.encrypt(interm)
            ctxt += prev_c
            prev_p = block

        mac = HMAC.new(self.key_mac, digestmod=SHA256)
        mac.update(ctxt)

        return ctxt + mac.digest()

    def decrypt(self, ctxt: bytes):
        if (len(ctxt) <= AES.block_size + SHA256.digest_size) and (
            len(ctxt) % AES.block_size != 0
        ):
            raise ValueError("Decryption failed.")
        iv = ctxt[: AES.block_size]
        blocks = blockify(ctxt[AES.block_size : -SHA256.digest_size], AES.block_size)
        cipher = AES.new(self.key_enc, AES.MODE_ECB)
        tag = ctxt[-SHA256.digest_size :]

        prev_c = iv
        prev_p = bytes([0]) * AES.block_size

        ptxt_padded = b""
        for block in blocks:
            interm = cipher.decrypt(block)
            mask = xor(prev_p, prev_c)
            prev_p = xor(mask, interm)
            ptxt_padded += prev_p
            prev_c = block

        ptxt = unpad(ptxt_padded, AES.block_size, style="x923")

        mac = HMAC.new(self.key_mac, digestmod=SHA256)
        mac.update(ctxt[: -SHA256.digest_size])
        verified = True
        try:
            mac.verify(tag)
        except ValueError:
            verified = False

        return ptxt, verified


class Server:
    def __init__(self, flag, stdin=sys.stdin.buffer, stdout=sys.stdout.buffer):
        self.stdin = stdin
        self.stdout = stdout

        self.flag = flag

        self.registered_users = {}
        self.current_user = None

        self.version = b"v2.0.0 Andromeda"
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
        user["key_enc"] = secrets.token_bytes(16)
        user["key_mac"] = secrets.token_bytes(16)
        user.update(
            {
                "version": self.version,
                "flag": self.flag,
                "title": b"Placeholder",
                "data": b"",
            }
        )

        self.send_message(
            {
                "res": f"Your registration was succesful. You will soon receive the AES and MAC keys by post. Please be patient, the mail will soon dispatch from Andromeda. In the meantime, you can edit the title and the data in your free storage."
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

        flag_len = len(user["flag"])
        title_len = len(user["title"])
        serialized_backup = (
            user["version"]
            + flag_len.to_bytes(1, "big")
            + user["flag"]
            + title_len.to_bytes(1, "big")
            + user["title"]
            + user["data"]
        )

        cipher = SE(user["key_enc"], user["key_mac"])
        ctxt = cipher.encrypt(serialized_backup)
        self.send_message(
            {
                "enc_backup": ctxt.hex(),
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

        enc_backup = bytes.fromhex(msg["enc_backup"])

        user = self.registered_users[self.current_user]
        cipher = SE(user["key_enc"], user["key_mac"])
        try:
            serialized_backup, verified = cipher.decrypt(enc_backup)
            if not verified:
                self.send_message({"res": f"Decryption failed ({tz.strftime('%d-%m-%y %H:%M')})"})
                return
        except:
            self.send_message({"res": f"Decryption failed ({tZ.strftime('%d-%m-%y %H:%M')})"})
            return

        pos = 0
        version = serialized_backup[pos : pos + 16]
        if version != self.version or len(version) != 16:
            self.send_message({"res": "Invalid format."})
            return
        pos += 16
        try:
            flag_len = serialized_backup[pos]
        except:
            self.send_message({"res": "Invalid format."})
            return
        pos += 1
        if len(serialized_backup[pos:]) < flag_len:
            self.send_message({"res": "Invalid format."})
            return
        flag = serialized_backup[pos : pos + flag_len]
        pos += flag_len
        try:
            title_len = serialized_backup[pos]
        except:
            self.send_message({"res": "Invalid format."})
            return
        pos += 1
        if len(serialized_backup[pos:]) < title_len:
            self.send_message({"res": "Invalid format."})
            return
        title = serialized_backup[pos : pos + title_len]
        pos += title_len
        data = serialized_backup[pos:]

        user["version"] = version
        user["flag"] = flag
        user["title"] = title
        user["data"] = data

        self.send_message({"res": "Backup restored."})


if __name__ == "__main__":

    class RequestHandler(socketserver.StreamRequestHandler):
        def handle(self):
            server = Server(flag=FLAG, stdin=self.rfile, stdout=self.wfile)
            server.main()

    class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    TCPServer(("0.0.0.0", PORT), RequestHandler).serve_forever()
