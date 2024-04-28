from itertools import cycle

from pwn import *

host = "localhost"
port = 13373
conn = remote(host, port)
block_size = 16


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, cycle(key)))


def blockify(msg: bytes, block_size: int):
    block = [msg[i : i + block_size] for i in range(0, len(msg), block_size)]
    return block


conn.recvuntil(b">>> ")

conn.sendline(b"1")
conn.recvuntil(b"Please enter a username: ")
username = b"a" * (block_size - len("user=")) + b"b" * (
    block_size - len("&flag=")
)  # We want to fill first and second block
reconstructed_session = f"user={username.decode()}&flag=".encode()
assert len(reconstructed_session) // block_size == 2
reconstructed_session_blocks = blockify(reconstructed_session, block_size)

conn.sendline(username)
conn.recvuntil(b"Current session: ")
encrypted_session_hex = conn.recvline().strip().decode()
encrypted_session = bytes.fromhex(encrypted_session_hex)
encrypted_session_blocks = blockify(encrypted_session, block_size)

conn.sendline(b"2")
conn.recvuntil(b"Masked flag: ")
masked_flag_hex = conn.recvline().strip().decode()
masked_flag = bytes.fromhex(masked_flag_hex)

# CBC Bit Flipping
ct_mask = xor(reconstructed_session_blocks[1], b"=".ljust(block_size, b"0"))
flipped_session = b"".join(
    [xor(encrypted_session_blocks[0], ct_mask)] + encrypted_session_blocks[1:]
)
flipped_session_hex = flipped_session.hex()

conn.sendline(b"1")
conn.recvuntil(b">>> ")
conn.sendline(b"2")
conn.recvuntil(b"Please enter an existing session (hex): ")
conn.sendline(flipped_session_hex.encode())

conn.sendline(b"2")
conn.recvuntil(b"Masked flag: ")
flipped_masked_flag_hex = conn.recvline().strip().decode()
flipped_masked_flag = bytes.fromhex(flipped_masked_flag_hex)
xor_mask = xor(flipped_masked_flag, b"CCSC{".rjust(20, b"0"))
flag = xor(masked_flag, xor_mask)

print("FLAG:", flag)

conn.close()
