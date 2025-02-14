#!/usr/bin/env python3

payload = ['\0'] * 64 # Create an empty 64-byte payload

# Setting the expected characters at the correct indexes

flag_chars = {
    0x22: '4', 0x14: '3', 0x24: 'r', 1: 'T', 0x15: 'v', 6: '0', 0x27: '}', 0x26: 'd',
    0x1f: 'r', 0x1d: '3', 8: '3', 0x16: 'e', 0x23: '1', 5: 'r', 0: 'H', 0x20: '3',
    0x12: '.', 0xd: '4', 3: '{', 10: '_', 0x10: '.', 4: 'b', 7: 'k', 0xf: 't',
    0xe: 'r', 0x13: 'n', 0x19: 't', 0x11: '.', 9: 'n', 0x1e: '_', 0x1a: '0',
    0x18: '_', 0xc: 'p', 0x17: 'r', 0x1c: 'b', 0x21: 'p', 2: 'B', 0x1b: '_',
    0xb: '4', 0x25: '3'
}

# Fill in the flag in the correct positions
for index, char in flag_chars.items():
    # print(char, end='')
    payload[index] = char


print(''.join(payload))

