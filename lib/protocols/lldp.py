"""
LLDP Protocol module
    Given a switch object, periodically sends LLDP messages
"""
import time
from ryu.lib.packet import packet, ethernet, lldp 
class LLDP: 
    def __init__(self,switch): 
        self.switch = switch
        e = ethernet.ethernet(src='12:34:56:ab:cd:ef',dst='00:11:22:33:44:55',ethertype=35020)
        lldp_ch = lldp.ChassisID(subtype=7,chassis_id=str(switch.id)) 
        lldp_port = lldp.PortID(subtype=7,port_id='Openflow')
        lldp_ttl  = lldp.TTL(ttl=1024)   
        lldp_end = lldp.End()   
        l = lldp.lldp([lldp_ch,lldp_port,lldp_ttl,lldp_end])
        p = packet.Packet()
        p.add_protocol(e)
        p.add_protocol(l)
        self.packet = p 
    # Start up LLDP sender
    def start(self):
        time.sleep(5) 
        print "Started LLDP thread"
        while True:
            self.switch.send_func.set_data(self.packet)
            self.switch.send_func.send()  
            time.sleep(2)
    # Parse incoming LLDP packet and return chassis_Id
    def get_id(self,l): 
        for tlv in l.tlvs:
            if "chassis_id" in tlv.__dict__: 
                return tlv.chassis_id  
                 
