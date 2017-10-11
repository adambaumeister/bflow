#!/usr/bin/python
from lib.topology import Path,Link
"""
"""
nodes = {
    'n1' : ['n2','n3'], 
    'n2' : ['n1','n3'],
    'n3' : ['n2','n1','n4','n5'],
    'n4' : ['n3'],
    'n5' : ['n3'],
}
"""
    n1===n2" 
    test
""" 
nodes2 = {
    'n1' : ['n2','n2'] 
}
l1 = Link('n1','n2',1)  
#l2 = Link('n2','n1',2) 
l3 = Link('n2','n3',1) 
#l4 = Link('n3','n2',2) 
#links = [l1,l2,l3,l4]  
links = [l1,l3]  
#for k,v in nodes.items(): 
#    print "{0} {1}".format(k,v) 
p = Path(links)
p.spf_links('n1','n3') 
