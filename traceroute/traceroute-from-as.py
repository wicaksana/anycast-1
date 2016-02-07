##
#	Sunday Feb 17, 2016
#
#	BGP Hackathon, CAIDA, San Diego-CA, USA
#
#	This script has been written by the Anycast #1 team of the BGP hackathon.
#
#	Input:
#		A text file containing the traceroute AS hops (ASN) separated by a blank space.
#
#	Output:
#		A JSON file containing D3 format data for a plot mapping the AS-level from multiple sources to
#		a single destination.
#

import base64
import json
from json import JSONEncoder
from pprint import pprint
import os
import sys

nodeidcounter = 0

class Node:
	def __init__(self):
		self.children = []
		self.name = ""
		global nodeidcounter
		self.nodeid = nodeidcounter
		nodeidcounter += 1
	def add_child(self, child):
		node = None
		matching_nodes = [x for x in self.children if x.name == child.name]
		if len(matching_nodes) > 0:
			node = matching_nodes[0]
		if node is None:
			self.children.append(child)
			node = child
		return node
	
	def __repr__(self):
		return str(self.name) + ' -> ' + str(self.children)

if len(sys.argv) < 2:
	print "please inform the file to be processed"
	quit()
else:
	traceroute_file = sys.argv[1]

count = 0
hop_list_list = []
id_count = -1

hop_list = []

with open(traceroute_file) as f:
	line_count = 0
	for line in f:
		hop_list = []
		hop_list.append(" ")
		ip_list = line.split(' ')
		for idx,hop in enumerate(ip_list):
			if idx == 0:
				hop_list.append(hop.strip())
			else:
				hop_list.append(hop.strip())
		if len(hop_list) > 1:
			hop_list_list.append(hop_list)
		line_count += 1

rootlist = []
for aslist in hop_list_list:
	level = 0
	cur_node = None
	for asn in aslist:
		if level == 0:
			node = None
			matching_nodes = [x for x in rootlist if x.name == str(asn)]
			if len(matching_nodes) > 0:
				node = matching_nodes[0]
			if node is None:
				node = Node()
				node.name = str(asn)
				rootlist.append(node)
			cur_node = node
		else:
			node = Node()
			node.name = str(asn)
			cur_node = cur_node.add_child(node)
		level += 1

class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

print "var astree=" + MyEncoder().encode(rootlist)[1:-1] + ";"

