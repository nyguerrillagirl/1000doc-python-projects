import socket
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(5)

client, addr = server.accept()
data = client.recv(1024)

first, last, age, gender, occupation, weight = struct.unpack("10s 10s i s 15s f", data)

print(f"First name: {first.decode().strip(chr(0))}")
print(f"Last name: {last.decode().strip(chr(0))}")
print(f"Age: {age}")
print(f"Gender: {gender.decode().strip(chr(0))}")
print(f"Occupation: {occupation.decode().strip(chr(0))}")
print(f"Weight: {weight}")