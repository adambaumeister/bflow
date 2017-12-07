import socket
import struct
import time

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 50001))
messages = ["spaghetti", "is", "life", "lololololololol6969696969696969696969696969"]
for m in messages:
    # Check length of message
    length = len(m)
    # Serialize message length, >I means big endian unsigned int which is always 4 bytes long
    packed = struct.pack('>I', length)
    # Send the length over the connection
    clientsocket.send(packed)
    # Now, send the message
    clientsocket.send(m)
time.sleep(10)
# Close the damn socket
clientsocket.close()
