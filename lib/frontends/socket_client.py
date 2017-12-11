import socket
import struct
import time
import bflow_pb2 as pb

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 50001))
query = pb.MacTableQuery(function='GetMacTable', switch='1', QueryType='NORMAL')
m = query.SerializeToString()
# Check length of message
length = len(m)
# Serialize message length, >I means big endian unsigned int which is always 4 bytes long
packed = struct.pack('>I', length)
# Send the length over the connection
clientsocket.send(packed)
# Now, send the message
clientsocket.send(m)
# Get the responses...
message_length = 1

while message_length > 0:
    message_length_packed = clientsocket.recv(4)
    if len(message_length_packed) > 0:
        # Unpack that into the actual message length
        message_length = struct.unpack('>I', message_length_packed)[0]
        print message_length
        if message_length > 0:
            # Now take the message now that we know how long the dang ol' thing is man
            # This is also the last block of this program
            message = clientsocket.recv(message_length)
            query = pb.MacTableEntry()
            query.ParseFromString(message)
            print query.mac
    else:
        message_length = 0



# Close the damn socket
clientsocket.close()
