#!/usr/bin/python
import pprint
aslistlist=[[1, 2, 3], [1,3,2], [1,5,6,7]]

class Node:
	def __init__(self):
		self.children = []
		self.asn = 0

	def add_child(self, child):
		node = None
		matching_nodes = [x for x in self.children if x.asn == child.asn]
		if len(matching_nodes) > 0:
			node = matching_node[0]
		if node is None:
			self.children.append(child)
			node = child
		return node
	
	def __repr__(self):
		return str(self.asn) + ' -> ' + str(self.children)
	def __unicode__(self):
		return str(self.asn)

rootlist = []
for aslist in aslistlist:
	level = 0
	cur_node = None
	for asn in aslist:
		if level == 0:
			node = None
			matching_nodes = [x for x in rootlist if x.asn == asn]
			if len(matching_nodes) > 0:
				node = matching_nodes[0]
			if node is None:
				node = Node()
				node.asn = asn
				rootlist.append(node)
			cur_node = node
		else:
			node = Node()
			node.asn = asn
			cur_node = cur_node.add_child(node)	 
		level += 1

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(aslistlist)
pp.pprint(rootlist)
