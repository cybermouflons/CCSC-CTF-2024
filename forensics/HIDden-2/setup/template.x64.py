# File used to create / deug shellcode
# taken from: https://github.com/nobodyisnobody/docs/tree/main/modern.templates.for.shellcoding

context.log_level = 'error'
from pwn import *
context.terminal = ['kitty', '@', 'launch', '--cwd', 'current', '--location', 'hsplit', '--title', 'DEBUG']
context.update(arch="amd64", os="linux")

if (len(sys.argv) < 1):
  print('%s [RUN or GDB or EXE]' % (sys.argv[0]))
  exit(1)

def dumpit(shellc):
  print('shellcode length: {:d} bytes'.format(len(shellc)))
  # dump as hex number array
  print('\n\"\\x{}\"'.format('\\x'.join([format(b, '02x') for b in bytearray(shellc)])))
  # dump as C array
  print("\nunsigned char shellc[] = {{{}}};".format(", ".join([format(b, '#02x') for b in bytearray(shellc)])))
  # dump as hex array
  print('\npossibly problematic values are highlighted (00,0a,20)...\n')
  print(hexdump(shellc, highlight=b'\x0a\x20\x00'))

# put your shellcode here
shellc = asm('''
  /* Check GID and exit */           
  mov rax, 104
  mov rdi, 0
  syscall
  cmp eax, 0xdeadbeef                      
  jne exit
             
  /* push ctx */
  push 0x30
  mov rax, 0x6e595c687b446667
  push rax
  mov rax, 0x4c53635b767f4c52
  push rax
  mov rax, 0x516867077d592774
  push rax
  mov rax, 0x3e435a4c50645074
  push rax

  /* Read key */
  sub rsp, 8   
  mov rax, 0     
  mov rdi, 0     
  lea rsi, [rsp] 
  mov rdx, 8    
  syscall        

  lea rbx, [rsp]
  mov rbx, [rbx]

  add rsp, 8
               
  /* xor(0x13371337, 'rsp', 0x20) */
  xor rax, rax
  push 0x20
  pop rsi
  mov rdi, rsp
  add rsi, rdi
             
start_6:  
  mov rcx, [rdi]
  xor ecx, ebx
  mov rdx, 0xcafebabe
  add rdi, 4
  cmp rdi, rsi
  jb  start_6
             
  /* push Try Harder */
  push 0x1010101 ^ 0x7265
  xor dword ptr [rsp], 0x1010101
  mov rax, 0x6472614820797254
  push rax
  pop rcx
  xor rax, rax
  xor rbx, rbx
  xor rdx, rdx
  jmp exit

exit:
  mov rax, 60
  mov rdi, 0
  syscall
''')

dumpit(shellc)

if args.WRITE:
  with open('sc.bin', 'wb') as f:
    f.write(shellc)

if args.EXE:
  ELF.from_bytes(shellc).save('binary')

if args.RUN:
  p = run_shellcode(shellc)
  p.interactive()
elif args.GDB:
  p = debug_shellcode(shellc, gdbscript='''
    # set your pwndbg path here
    init-pwndbg
    b *0x401010
    b *0x401066
    c            
    set $rax=0xdeadbeef
    c                      
  ''')
  p.send(p64(0x13371337))
  p.interactive()
  
# =-=- Xor stuff =-=-=

# flag = b'CCSC{It-C4nn0t_Be_Helpd_Push_On}
# ctx = b"tPdPLZC>t'Y}\aghQRL\177v[cSLgfD{h\\Yn0"
# key = 0x13371337

# =-=-=- ELF stuff =-=-=-=
# Final ELF was created after writing shellcode to disk, encoding with shikata ga nai and then creating ELF using pwntools from python REPL:

# =-=-= Encode and build =-=-=-
# shikata gai nai: https://github.com/EgeBalci/sgn

# python template.x64.py WRITE
# shikata-ga-nai/sgn -i sc.bin -o sc.sgn -a 64 -v

# (Python REPL) : with open('sc.sgn', 'rb') as f:
#.            ..:     ELF.from_bytes(f.read()).save('flag3.exe')