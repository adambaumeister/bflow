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
            'MacTable': self.get_mac_table,
        }
        self.command = ''

    def route(self):
        command = self.passed_args[0]
        self.passed_args.pop(0)
        if command not in self.dispatcher:
            print "Command not found '{0}'".format(command)
            return

        self.command = command
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

        dict = {}
        if arg_length > 0:
            if self.passed_args[0] == '?':
                self.command_help(required, optional)
                return
        else:
            self.command_help(required, optional)
            return

        # assign required arguments to dictionary
        i = 0
        if arg_length >= required_length:
            for arg in required:
                dict[arg] = self.passed_args[i]
                i += 1
        else:
            for arg in required:
                print "Missing required argument {0}".format(arg)

        # If there are still args left, assign them to optional attributes
        if i < arg_length:
            for arg in optional:
                dict[arg] = self.passed_args[i]

        return dict

    def command_help(self, required, optional):
        print "Usage: {0} [{1}] ({2})".format(self.command, ",".join(required), ",".join(optional))

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
        dict = self.parse_args(required, optional, descriptions)
        print dict['switch']
        query = pb.MacTableQuery(
            function='GetMacTable',
            switch=dict['switch'],
            QueryType='0'
        )
        responses = querier.send(query)
        for message in responses:
            query_response = pb.MacTableEntry()
            query_response.ParseFromString(message)
            switch = query_response.switch
            mac = query_response.mac
            port = query_response.port
            print "{0},{1},{2}".format(switch,mac,port)

querier = Querier(remote_addr='localhost', remote_port=2222)
querier.connect()
Bflow().cmdloop()