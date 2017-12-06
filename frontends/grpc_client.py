"""
GRPC Frontend using Protocol Buffers
"""
import bflow_pb2 as pb
import bflow_pb2_grpc
import grpc

channel = grpc.insecure_channel('localhost:50001')
stub = bflow_pb2_grpc.TableQueryStub(channel)
query = pb.MacTableQuery(switch='1')
for entry in stub.GetMacTable(query):
    print entry.port
