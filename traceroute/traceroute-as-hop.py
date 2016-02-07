##
#	Sunday Feb 17, 2016
#
#	BGP Hackathon, CAIDA, San Diego-CA, USA
#
#	This script has been written by the Anycast #1 team of the BGP hackathon.
#
#	Input:
#		Text files containing the traceroute AS hops (ASN) separated by a blank space. These files are created by processing JSON files from RIPE Atlas measurements.
#
#	BEFORE running:
#		Before running this script, you have to parse the traceroute JSON files from RIPE Atlas. To do so:
#			$ python peel-traceroute.py
#		Note that the JSON input file for peel-traceroute.py is hardcoded and have to be changed by hand at this point.
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

if len(sys.argv) < 2:
	print "please inform the PEERING ASN to be the root of the plot"
	quit()
else:
	peering_asn = str(sys.argv[1])

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

# Load the list of probe - ASN relation
prb_as = {}
with open("prb_as") as f:
	for line in f:
		line_pieces = line.split(' ')
		idx = int(line_pieces[0])
		prb_as[idx] = line_pieces[1].strip()
f.close()

# Load the list of probe IDs
idx_prb_id = -1;
prb_id = {}
with open("prb_id_list") as f:
	for prb_id_line in f:
		idx_prb_id += 1
		prb_id[idx_prb_id] = int(prb_id_line)
f.close()

# Load the block_to_as file
block = {}
count = 0
with open("block_to_as_summary") as f:
	for block_line in f:
		count += 1
		block_pieces = block_line.split(' ')
		block_prefix = str(block_pieces[0])
		if block_pieces[1] == "NA\n":
			block[block_prefix] = 0
		else:
			block[block_prefix] = int(block_pieces[1])
f.close()

# Loop through probes
count = 0
progress_probe = 0
progress_bar = 1.0
tot_probe = len(prb_id)
hop_list_list = []
id_count = -1
for idx_prb_id in range(len(prb_id)):

	traceroute_file = "traceroute_probe/" + str(prb_id[idx_prb_id])

	hop_list = []

	# Open the file traceroute_probe/c-INST-PROBE
	with open(traceroute_file) as f:
		for line in f:
			ip_list = line.split(' ')
			for idx,hop in enumerate(ip_list):
				if idx == 0:
					hop_list.append(int(prb_as[int(hop)]))
					return_line = prb_as[int(hop)]
				else:
					if (hop != '*') and ('.' in hop):
						hop_octets = hop.split('.')
						hop_prefix = hop_octets[0] + '.' + hop_octets[1] + '.' + hop_octets[2] + '.0'
						if (hop_prefix in block):
							if (block[hop_prefix] not in hop_list and block[hop_prefix] != 0):
								hop_list.append(block[hop_prefix])
								return_line += ' ' + str(block[hop_prefix])
								prev_as = block[hop_prefix]
			if len(hop_list) > 1:
				hop_list_list.append(hop_list)
			hop_list.append(str(peering_asn))
			hop_list.append(" ")
			break

stuff = {}

rootlist = []
for aslist in hop_list_list:
	aslist.reverse()
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

