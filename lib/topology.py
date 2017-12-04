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
        self.root_bridge = ''

    # Add a switch to the layer 2 topology, requires a lib.switch object
    def add_switch(self,switch):
        # if switch exists re-init it
        if switch.id in self.switches:
            print "Switch reinit: deleted {0}".format(switch.id)
        # No smart root bridge election - just pick the one
        if self.root_bridge == '':
            self.root_bridge = switch.id
        self.switches[switch.id] = switch
        print "added switch " + str(switch.id)

    # Retrieve switch object    
    def get_switch(self,id):
        id = int(id) 
        return self.switches[id]

    # Add a link between devices
    # Updates the link_ref database
    def add_link(self,local_switch_id,peer_switch_id,local_port):
        local_switch_id = str(local_switch_id)
        peer_switch_id = str(peer_switch_id)
        l = Link(local_switch_id,peer_switch_id,local_port)
        # If the peer switch already has at least one link associated with it
        if peer_switch_id in self.link_ref:
            # If this link hasn't been created already
            if local_switch_id not in self.link_ref[peer_switch_id]:
                l = Link(local_switch_id, peer_switch_id, local_port)
                self.path.add_link(l)
                self.link_ref[local_switch_id][peer_switch_id] = l
            # Otherwise, grab the link object and add this switch as the other port on the other side
            else:
                l = self.link_ref[peer_switch_id][local_switch_id]
                l.add_port(local_switch_id, local_port)
                if local_switch_id not in self.link_ref:
                    self.link_ref[local_switch_id] = {}
                self.link_ref[local_switch_id][peer_switch_id] = l
        # Otherwise, must be the first link for the remote node
        else:
            if local_switch_id not in self.link_ref:
                self.link_ref[local_switch_id] = {}

            l = Link(local_switch_id, peer_switch_id, local_port)
            self.path.add_link(l)
            self.link_ref[local_switch_id][peer_switch_id] = l

        switch = self.get_switch(local_switch_id)
        # Only redo l2 forwarding if we've added a new peer link
        if switch.add_peer_link(l, local_port):
            self.drop_peer_macs()
            self.calc_l2_forwarding()

    # Add a mac to the topology and learn it on the local switch
    def add_mac(self,id,mac,port):
        switch = self.get_switch(id)
        added = switch.learn_mac(mac,port)
        if added:
            switch.push_all_flows()

    # Link handler, can be a p2p port or an edge port
    def link_change(self, dp_id, msg):
        switch = self.get_switch(dp_id) 
        ofproto = switch.ofproto
        if msg.reason == ofproto.OFPPR_DELETE:
            print "Port deleted"
        elif msg.reason == ofproto.OFPPR_MODIFY:
            link_down = (msg.desc.state & ofproto.OFPPS_LINK_DOWN)
            link_up = (msg.desc.state & ofproto.OFPPS_LIVE)
            if link_down:
                if switch.port_is_peer(msg.desc.port_no):
                    # Drop all macs learnt on peer links
                    self.drop_peer_macs()
                    print "Peer link down, recalculate forwarding"
                    link = switch.link_from_port(msg.desc.port_no)
                    # Remove this link from the link table
                    local_id = str(switch.id)
                    remote_id = str(link.remote_id)
                    self.link_ref[local_id].pop(remote_id)
                    self.link_ref[remote_id].pop(local_id)
                    self.path.remove_link(link)
                    switch.del_peer_link(msg.desc.port_no)
                    self.calc_l2_forwarding()
                else:
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

    # unlearn all macs from all peer links
    def drop_peer_macs(self):
        for id, switch in self.switches.items():
            switch.drop_peer_link_macs()

    def dump(self):
        for id,switch in self.switches.items():
            print "Topology has : " + str(id)

    # Calculate the l2 forwarding tables
    # This needs a lot of work. Currently clears out all broadcasts before starting again.
    def calc_l2_forwarding(self):
        print "!!!  Calculating l2 forwarding"
        for id,switch in self.switches.items():
            for id2, switch2 in self.switches.items():
                if id != id2:
                    try:
                        link = self.path.next_hop(str(id), str(id2))
                        local_port = link.ports[str(id)]
                        switch.learn_table(switch2.mac_table, local_port)
                        print "DEBUG:  Next hop to {0} is {1}".format(str(id2), link.local_port)
                    # Below is a little dangerous as we catch any key error, it's just a shortcut for now
                    except KeyError as e:
                        print "No path between {0} and {1}!".format(id,id2)
                    switch.push_all_flows()

        # Calc the broadcast forwarding
        # Enable broadcast forwarding OUT hosts ports
        # Also delete the existing broadcast rules for each switch
        for id, switch in self.switches.items():
            switch.clear_broadcasts()
            for port in switch.mac_table.get_host_ports():
                if not switch.port_is_peer(port):
                    switch.forward_broadcast(port)

        # Install broadcast forwarding rules for p2p links
        for id, switch in self.switches.items():
            link = self.path.next_hop(str(id),str(self.root_bridge))
            if link:
                local_switch_id = link.local_id
                local_switch = self.get_switch(local_switch_id)
                local_port = link.ports[str(local_switch_id)]

                remote_switch_id = link.remote_id
                remote_port = link.get_port_id(remote_switch_id)
                if remote_port:
                    remote_switch = self.get_switch(remote_switch_id)
                    local_switch.enable_broadcast(local_port)
                    remote_switch.enable_broadcast(remote_port)
                    print "Enabling broadcasts on {0} port {1} -> {2} port {3}".format(local_switch_id,local_port,remote_switch_id,remote_port)
            else:
                print "No path for broadcasts!"

        # Install broadcast forwarding rules for forwarding broadcast IN host ports
        for id, switch in self.switches.items():
            for port in switch.mac_table.get_host_ports():
                # Host port id is shitty at the moment so this may not always work!!
                if not switch.port_is_peer(port):
                    switch.enable_broadcast(port)
                    print "enabling broadcasts on host port {0} on {1}".format(switch.id, port)


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

    def get_port_id(self, id):
        if id in self.ports:
            return self.ports[id]
#

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

    def remove_link(self, link):
        try:
            self.graph.remove_edge(link.local_id, link.remote_id)
        except nx.NetworkXError as e:
            print "edge between {0} and {1} does not exist!".format(link.local_id, link.remote_id)

    # Run the spf algorithm and return all the links in the path
    def spf_links(self,start,end):
        links = []
        index = 0
        start = str(start)
        end = str(end)
        try:
            nodes = nx.dijkstra_path(self.graph,start,end)
        except nx.NetworkXNoPath as e:
            print e.message
            return
        for node in nodes: 
            index += 1
            if index < len(nodes): 
                peer = nodes[index]
                obj = self.graph.get_edge_data(node, peer)
                links.append(obj['object'])
        return links

    # Calculate the single "loop free" path through the network
    def loop_free_path(self):
        G = nx.path_graph(self.graph)
        pairs = nx.all_pairs_dijkstra_path(G)
        lf_path = []
        lf_path_links = []
        longest_path = 0
        pprint.pprint(pairs)
        for start_node in pairs.keys():
            for end_node in pairs[start_node].keys():
                path_length = len(pairs[start_node][end_node])
                if path_length > longest_path:
                    lf_path = pairs[start_node][end_node]
                    longest_path = path_length
                elif len(pairs[start_node]) == 1:
                    obj = self.graph.get_edge_data(start_node, end_node)
                    lf_path_links.append(obj)
        return lf_path

    def test_nx(self):
        G = nx.path_graph(self.graph)
        pairs = nx.all_pairs_dijkstra_path(G)
        longest_path = 0
        longest = []
        # NEARLY THERE!!!
        for node, paths in sorted(pairs):
            for peer, path in paths.items():
                path_length = len(path)
                if path_length > longest_path:
                    longest = path
                    print node + peer + str(longest)
                    longest_path = path_length
        return longest

    # Run the SPF algorithm but just return the next hop link
    def next_hop(self,start,end):
        links = self.spf_links(start, end)
        if links:
            if len(links) > 0:
                return links[0]
