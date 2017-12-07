"""
Query Module

gRPC responder for bFlow queries
Used to retrieve information about the bFlow tables
"""
import time
import bflow_pb2 as pb
import socket
import struct
from ryu.lib import hub
"""
Serves queries for topology information
"""
class QueryResponder:
    def __init__(self, topology):
        self.topology = topology

    def serve(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('localhost', 50001))
        serversocket.listen(5)
        # First block is here - we're waiting for a connection.
        connection, address = serversocket.accept()

        while True:
            # Second block is below, we're waiting to receive data
            print "Listening for messages"
            # Read, from the first message, the total length of the message we are expecting in serialized format
            message_length_packed = connection.recv(4)
            if len(message_length_packed) > 0:
                # Unpack that into the actual message length
                message_length = struct.unpack('>I', message_length_packed)[0]
                # Now take the message now that we know how long the dang ol' thing is man
                # This is also the last block of this program
                message = connection.recv(message_length)
                query = pb.MacTableQuery()
                query.ParseFromString(message)
                print query.switch
            else:
                print "bad message, socket closed, or socket error."
                break

    def start(self):
        hub.spawn(self.serve)
        return

