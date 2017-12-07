"""
Query Module

gRPC responder for bFlow queries
Used to retrieve information about the bFlow tables
"""
import time

import grpc
from concurrent import futures

import bflow_pb2
import bflow_pb2_grpc
from ryu.lib import hub
"""
Serves queries for topology information
"""
class QueryResponder:
    def __init__(self, topology):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        bflow_pb2_grpc.add_TableQueryServicer_to_server(
            TableQueryServicer(topology), server
        )
        server.add_insecure_port('[::]:50001')
        self.server = server

    def serve(self):
        self.server.start()
        print "Started"
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            self.server.stop(0)

    def start(self):
        hub.spawn(self.serve)
        return


class TableQueryServicer(bflow_pb2_grpc.TableQueryServicer):
    def __init__(self, topology):
        self.topology = topology

    def GetMacTable(self, request, context):
        for id, switch in self.topology.switches.items():
            for e in switch.mac_table.get_local_entries():
                entry = bflow_pb2.MacTableEntry()
                entry.port = str(e.port)
                entry.mac = str(e.mac)

