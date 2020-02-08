from pwn import *

payload = b""

payload += b""

print(payload)
with open("in.txt","wb") as f:
    f.write(payload)
