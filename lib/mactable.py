import pprint
# MAC Table class
# Represents a mac address table, stored in memory on this controller
class mac_table:
    def __init__(self):
        self.table = {}
        self.ports = {}  
        self.flooded = {}
        self.broadcast_enabled = {}

    def add(self, entry):
        if entry.mac not in self.table: 
            self.table[entry.mac] = entry
            if entry.port in self.ports:    
                self.ports[entry.port].append(entry)
            else:
                self.ports[entry.port] = [entry]
            return True
        return False

    def delete_mac(self,mac): 
        if mac in self.table:
            entry = self.table[mac]
            print "Debug: " + entry.mac 
            self.table.pop(mac,None)
            return entry

    def dump(self):
        print "dumping MAC table..."
        for key,e in self.table.iteritems(): 
            print "{0} : {1}".format(e.mac,e.port)

    def get_ports(self):
        return self.ports.keys()

    def get_entries(self): 
        return self.table

    def enable_broadcast(self, port):
        self.broadcast_enabled[port] = True

    def is_broadcast_enabled(self, port):
        if port in self.broadcast_enabled:
            return True

    def get_local_entries(self):
        entries = []
        for mac, entry in self.table.items():
            if not entry.remote:
                entries.append(entry)
        return entries

    def get_host_ports(self):
        ports = []
        for port in self.ports.keys():
            if len(self.ports[port]) == 1:
                ports.append(port)
                print "Port {0} is host port!"
        return ports

    def drop_port(self,port):
        # Hack below: ovs sends duplicate port down messages?
        removed = [] 
        if port in self.ports:
            for entry in self.ports[port]:  
                self.table.pop(entry.mac, None)
                print "Dropped : " + entry.mac 
                self.dump() 
                removed.append(entry)  
            self.ports.pop(port, None)
        return removed

    # MAC table entry
    class entry:
        # Create a table entry
        def __init__(self, mac, port):
            self.installed = False 
            self.mac = mac
            self.port = port
            self.cookie = 0
            self.remote = False

        # Set installed flag
        def install(self): 
            self.installed = True


