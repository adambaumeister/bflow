from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp,lldp 
from lib.topology import topology
from lib.switch import switch 
from lib.protocols.lldp import LLDP
import lib.frontends.query as query
import pprint

# Define your class which is a RYU application
class ofnetwork(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        # Super instantiates this class as a child of "RyuApp" 
        super(ofnetwork, self).__init__(*args, **kwargs)
        # init topoloy
        self.topo = topology('testing')
        # Enable GRPC query responder
        query_responder = query.QueryResponder()
        query_responder.serve(self.topo)

    # Decorator, passes switch_featues_handler to set_ev_cls as EventOFPSwitchFeatures
    # CONFIG_DISPATCHER references the phase of negotiation with the Openflow switch
    # In the below case we are registering switch_features_handler to be enacted during the CONFIG_DISPATCHER phase
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # Datapath is very important: describes the switch that SENT this message
        # ie you can specify ev.msg.datapath.sendmsg to send a message to this specific switch
        datapath = ev.msg.datapath
        # init switch matching this one
        s = switch(datapath,ev.msg.datapath_id)
        # Enable protocols 
        self.proto_lldp = s.protocol_enable(LLDP) 
        self.topo.add_switch(s)



    # Handle port status changes
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev): 
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto 
        #switch = self.topo.get_switch(dp.id)
        #switch.port_change(msg)
        self.topo.link_change(dp.id,msg)

    # Send each packet through the processors we have 
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def dispatch(self, ev):
        self.layer2(ev)

    # Layer 2 handling
    def layer2(self, ev):
        mac = self.get_src_mac(ev)
        port = self.get_in_port(ev)
        dp = ev.msg.datapath
        switch = self.topo.get_switch(dp.id) 
        p = packet.Packet(ev.msg.data)
        l = p.get_protocol(lldp.lldp)
        # Process received LLDP packets
        if l:
            chassis_id = self.proto_lldp.get_id(l)
            self.topo.add_link(switch.id,chassis_id,port)
            return  
        self.topo.add_mac(switch.id,mac,port)

    # Retreive the source mac from a packet
    def get_src_mac(self, ev):
        # Parse the packet from the raw data
        p = packet.Packet(ev.msg.data)
        # Get the header from the packet by passing it the header class
        # Might need to extend these classes...
        eth = p.get_protocol(ethernet.ethernet)
        return eth.src

    # Retrieve the input port from a packetin event
    def get_in_port(self, ev): 
        match = ev.msg.match
        port = match.get("in_port")
        return port

    # Handle arp requests
    def arp(self ,ev):
        dp = ev.msg.datapath
        p = packet.Packet(ev.msg.data)
        a = p.get_protocol(arp.arp)
        if a: 
            in_port = self.get_in_port(ev)
            switch = self.topo.get_switch(dp.id)
            switch.flood(in_port)
