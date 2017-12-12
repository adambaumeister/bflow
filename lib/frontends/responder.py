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
            'ConnectionInfo': self.conn_info,
            'GetMacTable': self.get_mac_table
        }
        self.port = 2222
        self.bind_addr = 'localhost'

    def serve(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.bind_addr, self.port))
        serversocket.listen(5)
        while True:
            # First block is here - we're waiting for a connection.
            connection, address = serversocket.accept()
            # When someone connects, dispatch to handler
            self.dispatch(connection, address)

    def dispatch(self, connection, address):
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
                print "bad message, socket closed, or socket error from {0}".format(address)
                return

    def start(self):
        hub.spawn(self.serve)
        return

    def conn_info(self, message):
        generic = pb.GenericResponse()
        conn_info = 'Hi! You are connected to the bflow server running on {0}:{1}. Thanks!'.format(self.bind_addr,
                                                                                                   self.port)
        generic.data = conn_info
        messages = [generic]
        return messages

    def get_mac_table(self, message):
        query = pb.MacTableQuery()
        query.ParseFromString(message)
        switch_id = query.switch
        switch = self.topology.get_switch(switch_id)
        messages = []
        for e in switch.mac_table.get_local_entries():
            entry = pb.MacTableEntry()
            entry.mac = e.mac
            entry.port = str(e.port)
            entry.switch = str(switch_id)
            messages.append(entry)
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
