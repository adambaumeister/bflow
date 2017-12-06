"""
GRPC Server for testing purposes
"""
import time

import grpc
from concurrent import futures

import bflow_pb2
import bflow_pb2_grpc


class TableQueryServicer(bflow_pb2_grpc.TableQueryServicer):
    def __init__(self):
        test_entry = bflow_pb2.MacTableEntry()
        test_entry.switch = '1'
        test_entry.port = '99'
        test_entry.mac = 'ahspaghett'
        self.entries = [test_entry]

    def GetMacTable(self, request, context):
        for entry in self.entries:
            yield entry

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bflow_pb2_grpc.add_TableQueryServicer_to_server(
        TableQueryServicer(), server
    )
    server.add_insecure_port('[::]:50001')
    server.start()
    print "Started"
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


serve()