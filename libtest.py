#!/usr/bin/python
from lib.topology import topology

t = topology
n1 = str(1)
n2 = str(2)
t.add_link(1,2,1)
t.path.spf_links(n1,n2)
