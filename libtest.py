#!/usr/bin/python
from lib.topology import topology, Link, Path

t = topology("spaghett")
l1 = Link("n1", "n2", 1)
l2 = Link("n2", "n3", 2)
l3 = Link("n2", "n4", 3)
t.path.spf_links(n1,n2)
