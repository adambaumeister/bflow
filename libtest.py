#!/usr/bin/python
from lib.topology import topology, Link, Path

t = topology("spaghett")
p = Path()
l1 = Link("n1", "n2", 1)
l2 = Link("n2", "n3", 2)
l3 = Link("n3", "n4", 3)
p.add_link(l1)
p.add_link(l2)
p.add_link(l3)
p.test_nx()
#links = p.loop_free_path()
#for link in links:
 #   print "{0} - {1}".format(link.local_id, link.remote_id)
