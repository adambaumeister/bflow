"""
bflow_cli

An interface into the bflow application.
Uses protocol buffers on the backend to present a CLI to the user.
"""
import cmd
import lib.frontends.bflow_pb2 as pb
import sys
from lib.frontends.querier import Querier


class Bflow(cmd.Cmd):
    prompt = 'bflow: '

    def do_get(self, *args):
        if len(args) > 0:
            query = pb.GenericQuery(function='ConnectionInfo')
            responses = querier.send(query)
            for message in responses:
                query_response = pb.GenericResponse()
                query_response.ParseFromString(message)
                print query_response.data
        return

    def do_EOF(self, line):
        return True

    def do_quit(self, line):
        querier.disconnect()
        exit()


querier = Querier(remote_addr='localhost', remote_port=2222)
querier.connect()
Bflow().cmdloop()