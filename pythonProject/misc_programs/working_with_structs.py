import struct

# Send the numbers 10 20 30 <- send as a byte stream over a network
byte_stream = struct.pack("iii", 10, 20, 30)
#print(byte_stream)
# Output: b'\n\x00\x00\x00\x14\x00\x00\x00\x1e\x00\x00\x00'
# Each i ==> 4 bytes. Stored as little-endian. 0a 00 00 00 => \n\x00\x00\x00
# But Python prints non‑printable bytes using escape sequences, not ASCII characters.

#print(f"Size of integer: {struct.calcsize('i')} bytes")

# use short (2 bytes instead)
byte_stream = struct.pack("hhh", 10, 20, 30)
#print(f"byte_stream using short ints: {byte_stream}")

# Use unsigned short (allows numbers from 0 to 65,535)
byte_stream = struct.pack("HHH", 10, 20, 30)
a, b , c = struct.unpack("HHH", byte_stream)
#print(a)
#print(b)
#print(c)

company = b"BrainyCode"
day, month, year = 10, 10, 1970
awesome = True

byte_stream = struct.pack("10s 3i ?", company, day, month, year, awesome)
print(byte_stream)
print(struct.unpack("10s 3i ?", byte_stream))