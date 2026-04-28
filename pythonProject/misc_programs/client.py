import socket
import struct

# data to send via the socket
first_name = b"John"
last_name = b"Smith"
age = 35
gender = b"m"
occupation = b"Programmer"
weight = 87.52

# 10s 10s i s 15s f <- our template for what will be sent

data = struct.pack("10s 10s i s 15s f", first_name, last_name, age, gender, occupation, weight)
#print(data)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
client.send(data)
client.close()
