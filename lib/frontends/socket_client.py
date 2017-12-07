import socket
import struct
import time
import bflow_pb2 as pb

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 50001))
query = pb.MacTableQuery(switch='99')
m = query.SerializeToString()
# Check length of message
length = len(m)
# Serialize message length, >I means big endian unsigned int which is always 4 bytes long
packed = struct.pack('>I', length)
# Send the length over the connection
clientsocket.send(packed)
# Now, send the message
clientsocket.send(m)
# Close the damn socket
clientsocket.close()
