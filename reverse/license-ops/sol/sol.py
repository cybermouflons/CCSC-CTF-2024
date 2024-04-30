#!/usr/bin/python

import random
import os
from pwn import *

os.chdir('../setup')

elf = context.binary = ELF("license", checksec=False)
context.terminal = ['kitty', '@', 'launch', '--cwd', 'current', '--location', 'hsplit', '--title', 'DEBUG']
gs = '''
init-pwndbg
c
'''

# wrapper functrns
def sl(x): r.sendline(x)
def sla(x, y): r.sendlineafter(x, y)
def se(x): r.send(x)
def sa(x, y): r.sendafter(x, y)
def ru(x): return r.recvuntil(x)
def rl(): return r.recvline()
def cl(): return r.clean()
def uu64(x): return u64(x.ljust(8, b'\x00'))
def uuu(x): return unhex(x[2:])

def run():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        HOST = args.R.split(':')[0]
        PORT = args.R.split(':')[1]
        return remote(HOST, PORT)
    else:
        return process(elf.path)

def is_valid_license(license_key):
    prefix, suffix = license_key.split('_')
    
    invalid_prefixes = ['333', '444', '555', '666', '777', '888', '999']
    if prefix in invalid_prefixes:
        return False
    
    if sum(int(digit) for digit in suffix) % 7 != 0:
        return False
    
    return True

def num_digits(num):
    ct = 0
    while num > 0:
        ct += 1
        num //= 10
    return ct

def sum_of_digits(num):
    sm = 0
    while num > 0:
        rem = num % 10
        sm += rem
        num //= 10
    return sm

def cd_key_gen():
    x1 = random.randint(0, 1000)
    while x1 % 111 == 0:
        x1 = random.randint(0, 1000)
    x1str = ""
    if x1 > 100:
        x1str = str(x1)
    if 10 < x1 < 100:
        x1str = "0" + str(x1)
    if x1 < 10:
        x1str = "00" + str(x1)
    x2 = 1
    while sum_of_digits(x2) % 7 != 0:
        x2 = random.randint(0, 10000000)
        while x2 % 10 == 0 or x2 % 10 == 8 or x2 % 10 == 9:
            x2 = random.randint(0, 10000000)
    length = num_digits(x2)
    x2str = ""
    for i in range(0, 7 - length):
        x2str += "0"
    x2str += str(x2)
    return x1str + "_" + x2str

# =-=-= Solution =-=-==- 
r = run()
## Generate valid license and send
#license = cd_key_gen()
# assert(is_valid_license(license)) == True

# send known good license
license = b'716_8206741'

log.info(f'Valid License found: {license}')

sla(b'Enter a Windows 95 product key: ', license)

# Send null-terminated password to bypass strcmp
# add newline to terminate read()
sla(b'Enter password: ', b'OrionProtc0l!!!\x00\n')

log.success(r.recvall())

# run multiple times for valid license key generator
# 716_8206741
# 396_4332063
# 513_0358586
