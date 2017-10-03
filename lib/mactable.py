import pprint
# MAC Table class
# Represents a mac address table, stored in memory on this controller
class mac_table:
    def __init__(self):
        self.table = {}
        self.ports = {}  
        self.flooded = {}  
    def add(self, entry):
        if entry.mac not in self.table: 
            self.table[entry.mac] = entry
            if entry.port in self.ports:    
                self.ports[entry.port].append(entry)
            else:
                self.ports[entry.port] = [entry]
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
    def drop_port(self,port):
        # Hack below: ovs sends duplicate port down messages?
        removed = [] 
        if port in  self.ports: 
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
        def __init__(self, mac,port):
            self.installed = False 
            self.mac = mac
            self.port = port
            self.cookie = 0 
        # Set installed flag
        def install(self): 
            self.installed = True   

