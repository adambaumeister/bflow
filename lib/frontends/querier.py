"""
Quierier library

Handles the lower level communication between client apps and the bflow protobuf interface
"""
import socket
import struct

class Querier:
    def __init__(self, **kwargs):
        self.remote_addr = kwargs['remote_addr']
        self.remote_port = kwargs['remote_port']

    def connect(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.remote_addr, self.remote_port))

    def send(self, query):
        m = query.SerializeToString()
        # Check length of message
        length = len(m)
        # Serialize message length, >I means big endian unsigned int which is always 4 bytes long
        packed = struct.pack('>I', length)
        # Send the length over the connection
        self.clientsocket.send(packed)
        # Now, send the message
        self.clientsocket.send(m)
        # Get the responses...
        message_length = 1

        responses = []
        while message_length > 0:
            message_length_packed = self.clientsocket.recv(4)
            if len(message_length_packed) > 0:
                # Unpack that into the actual message length
                message_length = struct.unpack('>I', message_length_packed)[0]
                if message_length > 0:
                    # Now take the message now that we know how long the dang ol' thing is man
                    # This is also the last block of this program
                    message = self.clientsocket.recv(message_length)
                    responses.append(message)
            else:
                message_length = 0

        return responses

    def disconnect(self):
        self.clientsocket.close()