"""
Topology
Represents a full Openflow network topology 
Handles forwarding between switches, and the provisioning of routed services
"""
import networkx as nx
class topology: 
    def __init__(self,name):
        self.name = name
        self.switches = {}
        self.links = {}
        self.link_switch_map = {}
        self.l2_neighbors = {}  
    # Add a switch to the layer 2 topology, requires a lib.switch object
    def add_switch(self,switch):
        # if switch exists re-init it
        if switch.id in self.switches:
            #for link_id in self.link_switch_map[switch.id]:
            print "Switch reinit: deleted {0}".format(switch.id)  
        self.switches[switch.id] = switch
        print "added switch " + str(switch.id)
    # Retrieve switch object    
    def get_switch(self,id):
        id = int(id) 
        return self.switches[id]
    # Add a link between devices 
    def add_link(self,local_switch_id,peer_switch_id,local_port):
        link_id = 'l{0}{1}{2}'.format(local_switch_id,peer_switch_id,local_port)
        # Don't add links that have already been added, silly
        if link_id in self.links:
            return  
        local_switch = self.get_switch(local_switch_id)
        peer_switch = self.get_switch(peer_switch_id)
        l = Link(local_switch_id,peer_switch_id,local_port)
        self.links[link_id] = l
        self.calc_l2_forwarding()
    # Add a mac to the topology and learn it on the local switch
    def add_mac(self,id,mac,port): 
        switch = self.get_switch(id)
        added = switch.learn_mac(mac,port)
        if added: 
            self.calc_l2_forwarding()  
    # Linkhandler, can be a p2p port or an edge port
    def link_change(self,dp_id,msg): 
        switch = self.get_switch(dp_id) 
        ofproto = switch.ofproto
        if msg.reason == ofproto.OFPPR_DELETE:
            print "Port deleted"
        elif msg.reason == ofproto.OFPPR_MODIFY:
            link_down = (msg.desc.state & ofproto.OFPPS_LINK_DOWN)
            if link_down:
                # Delete flows from the local switch
                dropped_macs = switch.port_down(msg.desc.port_no)
                # Delete this mac from the topology 
                self.drop_macs(dropped_macs)
        elif msg.reason == ofproto.OFPPR_ADD:
            print "Port Add"
    # Unlearn mac(s) from the topology
    def drop_macs(self,macs):
        for mac in macs: 
            for id,switch in self.switches.items(): 
                switch.unlearn_mac(mac)  
    def dump(self):
        for id,switch in self.switches.items():
            print "Topology has : " + str(id)
    # Calculate the l2 forwarding tables
    def calc_l2_forwarding(self):
        print "not yet implemented..." 
"""
Link
    An absract link object, contains contains information specific to the link and other details 
"""
class Link:
    def __init__(self,local_id,remote_id,local_port,**kwargs):
        self.speed = 1000
        self.local_id = local_id
        self.remote_id = remote_id
        self.local_port = local_port
        for k,v in kwargs.items():
            self.__dict__[k] = v 
"""
Path
    An abstract object representing a path (list of node ids seperated by Link objects) between two endpoints 
"""
class Path:
    def __init__(self,links): 
        self.links = links 
        g = nx.Graph()  
        for link in self.links:
            g.add_edge(link.local_id,link.remote_id, object=link)
        self.graph = g
    # Run the spf algorithm and return all the links in the path  
    def spf_links(self,start,end):
        #print  nx.dijkstra_path_length(self.graph, start, end, 'speed')
        #print  nx.dijkstra_path(self.graph, start, end, 'speed')
        index = 0
        nodes = nx.dijkstra_path(self.graph,start,end) 
        for node in nodes: 
            index += 1
            if index < len(nodes): 
                peer = nodes[index]
                print "{0} {1}".format(node,peer)  
                obj = self.graph.get_edge_data(node,peer) 
                print obj['object'].local_port
