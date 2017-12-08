"""
Query Module

Socket-based responder for bFlow queries
Used to retrieve information about the bFlow tables

Wondering why this doesn't use gRPC? gRPC threading isn't supported within green threads.
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
        # Supported functions
        self.function_map = {
            'GetMacTable': self.get_mac_table
        }

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
                # Parse the message using the generic parser
                query = pb.MessageParser()
                query.ParseFromString(message)
                # Route to Correct function and return the response object and length
                messages = self.function_map[query.function](message)
                self.send_response(connection, messages)

            else:
                print "bad message, socket closed, or socket error."
                break

    def start(self):
        hub.spawn(self.serve)
        return

    def get_mac_table(self, message):
        entry = pb.MacTableEntry()
        entry.mac = "ss:pp:aa:gh:et"
        entry.port = "99"
        entry.switch = "1"
        messages = [entry, entry]
        return messages

    def send_response(self, connection, messages):
        for message in messages:
            m = message.SerializeToString()
            length = len(m)
            # Serialize message length, >I means big endian unsigned int which is always 4 bytes long
            packed = struct.pack('>I', length)
            # Send the length over the connection
            connection.send(packed)
            # Now, send the actual message
            connection.send(m)
        # Send the EOF message as a 0 byte
        packed = struct.pack('>I', 0)
        connection.send(packed)
