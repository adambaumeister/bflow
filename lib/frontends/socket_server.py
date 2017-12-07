import socket
import struct

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 50001))
serversocket.listen(5)
connection, address = serversocket.accept()

while True:
    print "Listening for messages"
    # Read, from the first message, the total length of the message we are expecting in serialized format
    message_length_packed = connection.recv(4)
    if len(message_length_packed) > 0:
        # Unpack that into the actual message length
        message_length = struct.unpack('>I', message_length_packed)[0]
        # Now take the message now that we know how long the dang ol' thing is man
        message = connection.recv(message_length)
        print message
    else:
        print "bad message, socket closed, or socket error."
        break



