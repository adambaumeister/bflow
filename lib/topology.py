"""
Topology
Represents a full Openflow network topology 
Handles forwarding between switches, and the provisioning of routed services
"""
import networkx as nx
import pprint
class topology: 
    def __init__(self,name):
        self.name = name
        self.switches = {}
        self.link_switch_map = {}
        self.link_ref = {}
        self.l2_neighbors = {}
        self.path = Path()

    # Add a switch to the layer 2 topology, requires a lib.switch object
    def add_switch(self,switch):
        # if switch exists re-init it
        if switch.id in self.switches:
            print "Switch reinit: deleted {0}".format(switch.id)  
        self.switches[switch.id] = switch
        print "added switch " + str(switch.id)

    # Retrieve switch object    
    def get_switch(self,id):
        id = int(id) 
        return self.switches[id]

    # Add a link between devices
    def add_link(self,local_switch_id,peer_switch_id,local_port):
        pprint.pprint(self.link_ref)
        l = Link(local_switch_id,peer_switch_id,local_port)
        # If the peer switch already has at least one link associated with it
        if peer_switch_id in self.link_ref:
            print "Existing entry for {0} ({1})".format(local_switch_id, peer_switch_id)
            # If this link hasn't been created already
            if local_switch_id not in self.link_ref[peer_switch_id]:
                l = Link(local_switch_id, peer_switch_id, local_port)
                self.path.add_link(l)
                self.link_ref[local_switch_id][peer_switch_id] = l
            # Otherwise, grab the link object and add this switch as the other port on the other side
            else:
                l = self.link_ref[peer_switch_id][local_switch_id]
                l.add_port(local_switch_id, local_port)
        # Otherwise, must be the first link for the remote node
        else:
            print "No existing entry for {0} {1}".format(local_switch_id,peer_switch_id)
            if local_switch_id not in self.link_ref:
                self.link_ref[local_switch_id] = {}

            l = Link(local_switch_id, peer_switch_id, local_port)
            self.path.add_link(l)
            self.link_ref[local_switch_id][peer_switch_id] = l
            #self.calc_l2_forwarding()

    # Add a mac to the topology and learn it on the local switch
    def add_mac(self,id,mac,port): 
        switch = self.get_switch(id)
        added = switch.learn_mac(mac,port)
        if added: 
            #self.calc_l2_forwarding()
            print "Do nothing with learned mac, temporary, we have to wait for links to come up"

    # Link handler, can be a p2p port or an edge port
    def link_change(self,dp_id,msg): 
        switch = self.get_switch(dp_id) 
        ofproto = switch.ofproto
        if msg.reason == ofproto.OFPPR_DELETE:
            print "Port deleted"
        elif msg.reason == ofproto.OFPPR_MODIFY:
            link_down = (msg.desc.state & ofproto.OFPPS_LINK_DOWN)
            link_up = (msg.desc.state & ofproto.OFPPS_LIVE)
            if link_down:
                # Delete flows from the local switch
                dropped_macs = switch.port_down(msg.desc.port_no)
                # Delete this mac from the topology 
                self.drop_macs(dropped_macs)
            if link_up:
                print "Link came up!"
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
        for id,switch in self.switches.items():
            for id2, switch2 in self.switches.items():
                if id != id2:
                    try:
                        link = self.path.next_hop(str(id), str(id2))
                    except KeyError as e:
                        print "No path between {0} and {1}!".format(id,id2)
                        print e.message


"""
Link
    An absract link object, contains contains information specific to the link and other details 
"""


class Link:
    def __init__(self,local_id,remote_id,local_port,**kwargs):
        self.link_id = 'l{0}{1}{2}'.format(local_id, remote_id, local_port)
        self.speed = 1000
        self.local_id = str(local_id)
        self.remote_id = str(remote_id)
        self.ports = {}
        self.ports[local_id] = local_port
        self.local_port = local_port
        for k,v in kwargs.items():
            self.__dict__[k] = v

    """
    Add an id -> port mapping to this link object
    """
    def add_port(self, local_id, port):
        self.ports[local_id] = port


"""
Path
    An abstract object representing a path (list of node ids seperated by Link objects) between two endpoints 
"""


class Path:
    def __init__(self):
        self.links = {}
        g = nx.Graph()  
        self.graph = g

    def add_link(self,link):
        if link.link_id in self.links:
            return
        self.links[link.link_id] = link
        edge_object = {}
        self.graph.add_edge(link.local_id, link.remote_id, object=link)
        print "added edge: {0}{1}".format(link.local_id, link.remote_id)

    # Run the spf algorithm and return all the links in the path
    def spf_links(self,start,end):
        links = []
        index = 0
        try:
            nodes = nx.dijkstra_path(self.graph,start,end)
        except nx.NetworkXNoPath as e:
            print e.message
            return
        for node in nodes: 
            index += 1
            if index < len(nodes): 
                peer = nodes[index]
                print "{0} {1}".format(node,peer)
                obj = self.graph.get_edge_data(node,peer)
                links.append(obj['object'])
        return links

    # Run the SPF algorithm but just return the next hop link
    def next_hop(self,start,end):
        links = self.spf_links(start, end)
        return links[0]
