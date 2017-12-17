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
            i = Input(args)
            i.route()
        return

    def do_EOF(self, line):
        return True

    def do_quit(self, line):
        querier.disconnect()
        exit()

    def emptyline(self):
        return


class Input:
    def __init__(self, args):
        self.passed_args = args[0].split(" ")
        self.dispatcher = {
            'ConnectionInfo': self.connection_info,
            'GetMacTable': self.get_mac_table,
        }

    def route(self):
        command = self.passed_args[0]
        print command
        self.passed_args.pop(0)
        self.dispatcher[command]()

    def connection_info(self):
        query = pb.GenericQuery(function='ConnectionInfo')
        responses = querier.send(query)
        for message in responses:
            query_response = pb.GenericResponse()
            query_response.ParseFromString(message)
            print query_response.data

    def parse_args(self, required, optional, descriptions):
        required_length = len(optional)
        arg_length = len(self.passed_args)
        if arg_length >= required_length:
            print "Yep"


    def get_mac_table(self):
        required = [
            'switch'
        ]
        optional = [
            'type'
        ]
        descriptions = [
            'Switch OpenFlow ID',
            'Query type [NORMAL|DETAILED]'
        ]
        self.parse_args(required, optional, descriptions)

querier = Querier(remote_addr='localhost', remote_port=2222)
querier.connect()
Bflow().cmdloop()