#!/usr/bin/python3

import sys
import os
import crccheck
import platform
import ctypes

# Import lzss module via ctypes
LZSS_SO_EXT = "so" if platform.uname()[0] != "Darwin" else "dylib"
LZSS_SO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lzss." + LZSS_SO_EXT)
lzss_functions = ctypes.CDLL(LZSS_SO_FILE)
lzss_functions.encode_file.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

if len(sys.argv) != 4:
    print ("Usage: bin2ota.py BOARD sketch.bin sketch.ota")
    print ("  BOARD = [ MKR_WIFI_1010 | NANO_33_IOT | PORTENTA_H7_M7 | NANO_RP2040_CONNECT | NICLA_VISION | OPTA | GIGA | NANO_ESP32 | ESP32 | UNOR4WIFI]")
    sys.exit()

board = sys.argv[1]
ifile = sys.argv[2]
ofile = sys.argv[3]
lfile = ifile + '.lzss'

# Compress bin
ifile_encoded = ifile.encode('utf-8')
lfile_encoded = lfile.encode('utf-8')
lzss_functions.encode_file(ifile_encoded, lfile_encoded)

# Read the binary file
file = open(lfile, "rb")
data = bytearray(file.read())
file.close()

# Magic number (VID/PID)
if board == "MKR_WIFI_1010":
    magic_number = 0x23418054.to_bytes(4,byteorder='little')
elif board == "NANO_33_IOT":
    magic_number = 0x23418057.to_bytes(4,byteorder='little')
elif board == "PORTENTA_H7_M7":
    magic_number = 0x2341025B.to_bytes(4,byteorder='little')
elif board == "NANO_RP2040_CONNECT":
    magic_number = 0x2341005E.to_bytes(4,byteorder='little')
elif board == "NICLA_VISION":
    magic_number = 0x2341025F.to_bytes(4,byteorder='little')
elif board == "OPTA":
    magic_number = 0x23410064.to_bytes(4,byteorder='little')
elif board == "GIGA":
    magic_number = 0x23410266.to_bytes(4,byteorder='little')
elif board == "NANO_ESP32":
    magic_number = 0x23410070.to_bytes(4,byteorder='little')
# Magic number for all ESP32 boards not related to (VID/PID)
elif board == "ESP32":
    magic_number = 0x45535033.to_bytes(4,byteorder='little')
elif board == "UNOR4WIFI":
    magic_number = 0x23411002.to_bytes(4,byteorder='little')
else:
    print ("Error,", board, "is not a supported board type")
    sys.exit()

# Version field (byte array of size 8) - all 0 except the compression flag set.
version = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40])

# Prepend magic number and version field to payload
data_complete = magic_number + version + data

# Calculate length and CRC32
data_len = len(data_complete)
data_crc = crccheck.crc.Crc32.calc(data_complete)

# Write to outfile
out_file = open(ofile, "wb")
out_file.write((data_len).to_bytes(4, byteorder='little'))
out_file.write((data_crc).to_bytes(4, byteorder='little'))
out_file.write(data_complete)
out_file.close()
