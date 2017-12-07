"""
SWITCH Class
    A logical switch object
"""
from lib.mactable import mac_table
from lib.sender import sender
from ryu.lib import hub
import time
class switch:
    # Requires ev.msg.datapath to init and the datapath id 
    # controller.dp.id isn't initilized until MAIN_DISPATCHER so the user can pass it
    # This class can be started at any point but the best call is to do it during the switch features request message
    def __init__(self,dp,id=None):
        # DP so we can manipulate switch direct from this table 
        self.datapath = dp
        self.parser = dp.ofproto_parser
        self.ofproto = dp.ofproto
        self.flooded = {} 
        self.proto_enabled = {} 
        self.proto_available = {}
        self.peer_links = {}
        # Keep track of cookies
        self.cookie = 1 
        self.flowtable = {}
        # Configure defaults 
        # id represents the OF switch 64-bit identifier
        self.broadcast_flows = []
        self.broadcast_ports = []

        if dp.id:  
            self.id = dp.id
        else: 
            self.id = id
        # Mac table for the switch, currently only one is supported
        self.mac_table = mac_table()
        # Add default flow to switch, forwards unmatched packets to controller
        match = self.parser.OFPMatch() 
        actions = [self.parser.OFPActionOutput(self.ofproto.OFPP_CONTROLLER,
                                          self.ofproto.OFPCML_NO_BUFFER)]
        inst = [self.parser.OFPInstructionActions(self.ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = self.parser.OFPFlowMod(datapath=dp, priority=0,match=match, instructions=inst)
        dp.send_msg(mod)
        self.send_func = sender(self.datapath)
        # Configure switch to always forward LLDP packets to controller  
        match = self.parser.OFPMatch(
            eth_type=35020
        ) 
        actions = [self.parser.OFPActionOutput(self.ofproto.OFPP_CONTROLLER,
                                          self.ofproto.OFPCML_NO_BUFFER)]
        inst = [self.parser.OFPInstructionActions(self.ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = self.parser.OFPFlowMod(datapath=dp, priority=0,match=match, instructions=inst)
        dp.send_msg(mod)

    # Add a mac -> port mapping to this switchesMAC address table
    def learn_mac(self, mac, port, remote=False):
        table = self.mac_table 
        entry = table.entry(mac, port)
        # Flag this entry as not local to us
        if remote:
            entry.remote = True
        added = table.add(entry)
        return added

    # Delete all flows matching this mac address from this switch
    def unlearn_mac(self,mac):
        entry = self.mac_table.delete_mac(mac)
        if entry: 
            self.flow_delete(entry)

    # Delete all flows matching this mac address from this switch
    def unlearn_mac_entry(self, entry):
        self.flow_delete(entry)

    # Lean an entire table
    def learn_table(self,mac_table,port):
        #print "Learning table on port {0}".format(port)
        for entry in mac_table.get_local_entries():
            mac = entry.mac
            self.learn_mac(mac, port, remote=True)

    def push_all_flows(self): 
        self.macs_to_switch()

    def macs_to_switch(self):
        dp = self.datapath
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        for key,e in self.mac_table.get_entries().iteritems():
            if e.installed == False:
                match = parser.OFPMatch(
                    eth_dst = e.mac
                )
                actions = [parser.OFPActionOutput(e.port)]
                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                mod = parser.OFPFlowMod(datapath=dp, priority=1,match=match, instructions=inst,cookie=self.cookie,cookie_mask=255)
                #mod = parser.OFPFlowMod(datapath=dp, priority=1,match=match, instructions=inst)
                dp.send_msg(mod)
                e.install()
                e.cookie = self.cookie 
                self.cookie += 1 
                print "Added flow (cookie: {0}".format(str(self.cookie))

    # Flood the provided event packet to all ports (except the one it was received on) 
    def flood(self,passed_in_port):
        actions = []
        parser = self.parser
        ofproto = self.ofproto
        dp = self.datapath
        match = parser.OFPMatch(
            in_port = passed_in_port,
            eth_dst = 'ff:ff:ff:ff:ff:ff'
        )
        # Need to improve this, currently keeps track of connected hosts via mac table
        for port in self.mac_table.get_ports():
            # Only output to ports that have broadcasts enabled
            # Something wrong with this logic
            if port != passed_in_port and self.mac_table.is_broadcast_enabled(port):
                a = self.parser.OFPActionOutput(port)
                actions.append(a)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = parser.OFPFlowMod(datapath=dp, priority=1,match=match, instructions=inst, cookie=self.cookie, cookie_mask=255)
        dp.send_msg(mod)
        # Mark this port as having a flood rule configured already
        self.flooded[passed_in_port] = True
        self.cookie += 1
        self.broadcast_flows.append(self.cookie)

        # Forward broadcasts on the provided port
    def enable_broadcast(self, port):
        #print "Enabling port {0} on {1}".format(port,self.id)
        self.mac_table.enable_broadcast(port)
        self.flood(port)

    # Forward broadcasts out port
    def forward_broadcast(self, port):
        #print "Enabling forwarding of broadcasts port: {0} Switch: {1}".format(port,self.id)
        self.mac_table.enable_broadcast(port)
        self.broadcast_ports.append(port)

    # Remove all broadcast rules
    def clear_broadcasts(self):
        for c in self.broadcast_flows:
            self.flow_delete_cookie(c)
        self.broadcast_flows = []
        for port in self.broadcast_ports:
            self.mac_table.disable_broadcast(port)

    # Delete a flow
    def flow_delete(self,entry): 
        dp = self.datapath
        parser = self.parser
        inst = []
        match = self.parser.OFPMatch() 
        mod = parser.OFPFlowMod(datapath=dp, cookie=entry.cookie,cookie_mask=255,command=self.ofproto.OFPFC_DELETE
                                , instructions=inst,match=match, out_port=entry.port, out_group=self.ofproto.OFPG_ANY)
        dp.send_msg(mod)
        print "Deleted cookie: {0} port: {1} ".format(str(entry.cookie),str(entry.port))

    # Delete a flow matching a cookie
    def flow_delete_cookie(self, c):
        dp = self.datapath
        parser = self.parser
        inst = []
        match = self.parser.OFPMatch()
        mod = parser.OFPFlowMod(datapath=dp, cookie=c, cookie_mask=255, command=self.ofproto.OFPFC_DELETE
                                , instructions=inst, match=match, out_group=self.ofproto.OFPG_ANY)
        dp.send_msg(mod)
        print "Deleted flow cookie: {0}".format(str(c))

    # Mark a port down and remove all associated flows
    def port_down(self,port):
        print "Port down : " + str(port)
        dropped_macs = [] 
        dropped_entries = self.mac_table.drop_port(port)
        for entry in dropped_entries: 
            self.flow_delete(entry)
            # Return macs that are local to this switch only
            dropped_macs.append(entry.mac)
        return dropped_macs

    # Run protocols
    def protocol_enable(self, module):
        m = module(self)
        thread = hub.spawn(m.start)
        return m

    # Add a peer link (link to another switch...) to this switch
    def add_peer_link(self,Link,port):
        if port not in self.peer_links:
            self.peer_links[port] = Link
            return True

    # Remove a peer link
    def del_peer_link(self, port):
        if port in self.peer_links:
            self.peer_links.pop(port)
            return True

    # Check if port is a peer link
    def port_is_peer(self, port):
        if port in self.peer_links:
            return True
        else:
            return False

    # Return link object by Port
    def link_from_port(self, port):
        if port in self.peer_links:
            return self.peer_links[port]
        else:
            return False

    # Unlearn all macs pointing down peer links
    def drop_peer_link_macs(self):
        for port, link in self.peer_links.items():
            removed = self.mac_table.drop_port(port)
            for entry in removed:
                self.unlearn_mac_entry(entry)


    # Return links per peer
    def links_by_peer(self,peer_id):
        links = [] 
        for link in self.get_peer_links().values():
            if int(link.peer.id) == int(peer_id): 
                print "Debug: " + str(peer_id) + str(link.peer.id) 
                links.append(link)
        return links

    def get_peer_links(self):
        return self.peer_links
