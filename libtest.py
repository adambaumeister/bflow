#!/usr/bin/python
from lib.topology import topology

t = topology("spaghett")
n1 = str(1)
n2 = str(2)
n3 = str(3)
n4 = str(4)
t.add_link(n1, n2, 1)
t.add_link(n2, n3, 2)
t.add_link(n4, n2, 3)
t.path.spf_links(n1,n2)
