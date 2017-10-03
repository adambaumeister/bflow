from ryu.lib.packet import packet, ethernet, arp
"""
SENDER Class
Sets up everything we need to send packets through an openflow switch
"""
class sender:
    # Requires a datapath (switch) to send stuff too 
    def __init__(self,dp):
        # SETUP DEFAULTS
        self.dp = dp
        self.ofp = dp.ofproto 
        self.parser = dp.ofproto_parser
        # Default to flood output
        self.out_port = self.ofp.OFPP_FLOOD
        # Setup default action, which is to flood the packet out all ports
        self.action = [self.parser.OFPActionOutput(self.out_port, 0)]
        self.buffer_id = self.ofp.OFP_NO_BUFFER
        self.in_port = self.ofp.OFPP_CONTROLLER
        self.packet = None
    # Configure the data - requires a packet.packet instance 
    def set_data(self,packet):
        self.packet = packet 
    # Send a test packet
    def test_packet(self): 
        print "sending test packet out all ports"
        e = ethernet.ethernet(src='12:34:56:ab:cd:ef',dst='00:11:22:33:44:55',ethertype=2048)
        p = packet.Packet() 
        p.add_protocol(e)
        req = self.parser.OFPPacketOut(self.dp,self.buffer_id,self.in_port,self.action,p)
        self.dp.send_msg(req)
    def send(self):
        p = self.packet 
        req = self.parser.OFPPacketOut(self.dp,self.buffer_id,self.in_port,self.action,p)
        self.dp.send_msg(req)
