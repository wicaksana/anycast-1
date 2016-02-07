# This script goes through all the valid probes from probes/c_prb_id_traceroute
# and determines how many AS-level hops for each line of files traceroute_probe/c-INSTANCE-PROBE
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
#inst = [ 'bts','fra','iad','jfk','lax','mad','ord','par' ]
#inst = [ 'bts' ]

# Load the list of probe - ASN relation
#prb_as = {}
#with open("prb_as") as f:
#	for line in f:
#		line_pieces = line.split(' ')
#		idx = int(line_pieces[0])
#		prb_as[idx] = line_pieces[1].strip()
#f.close()
#print "loaded %d probe to AS" % len(prb_as)

# Load the list of probe IDs
#idx_prb_id = -1;
#prb_id = {}
#with open("prb_id_list") as f:
#	for prb_id_line in f:
#		idx_prb_id += 1
#		prb_id[idx_prb_id] = int(prb_id_line)
#f.close()
#print "loaded %d probe IDs" % len(prb_id)

# Load the block_to_as file
#block = {}
#count = 0
#with open("block_to_as_summary") as f:
#	for block_line in f:
#		count += 1
#		block_pieces = block_line.split(' ')
#		block_prefix = str(block_pieces[0])
#		if block_pieces[1] == "NA\n":
#			block[block_prefix] = 0
#		else:
#			block[block_prefix] = int(block_pieces[1])
#f.close()
#print "loaded %d blocks" % count, "into %d positions" % len(block)


# Loop through probes
count = 0
progress_probe = 0
progress_bar = 1.0
hop_list_list = []
id_count = -1

#traceroute_file = "traceroute_probe/" + str(prb_id[idx_prb_id])
traceroute_file = "as-path-reverse"

hop_list = []

# Open the file traceroute_probe/c-INST-PROBE
with open(traceroute_file) as f:
	line_count = 0
	for line in f:
		hop_list = []
		ip_list = line.split(' ')
		for idx,hop in enumerate(ip_list):
			if idx == 0:
#					hop_list.append(int(prb_as[int(hop)]))
#					return_line = prb_as[int(hop)]
				hop_list.append(hop.strip())
			else:
				hop_list.append(hop.strip())
#					if (hop != '*') and ('.' in hop):
#						hop_octets = hop.split('.')
#						hop_prefix = hop_octets[0] + '.' + hop_octets[1] + '.' + hop_octets[2] + '.0'
#						if (hop_prefix in block):
#							if (block[hop_prefix] not in hop_list and block[hop_prefix] != 0):
#								hop_list.append(block[hop_prefix])
#								return_line += ' ' + str(block[hop_prefix])
#								prev_as = block[hop_prefix]
		if len(hop_list) > 1:
#				print return_line + " [ " + str(len(hop_list)) + " ]"
			hop_list_list.append(hop_list)
		line_count += 1
#		if (line_count == 10):
#			break
#print json.dumps(hop_list_list)
stuff = {}

rootlist = []
for aslist in hop_list_list:
#	aslist.reverse()
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


print MyEncoder().encode(rootlist)

quit()


	# Open the file traceroute_probe/c-INST-PROBE
#	with open(traceroute_file) as f:
#		hop_list = []
#		for line in f:
#
#			hop_count = 0
#			prev_prefix = ""
#			skip = 1
#			ip_list = line.split(' ')
#			for hop in ip_list:
#				if skip == 0:
#					if (hop != '*') and ('.' in hop):
#						hop_octets = hop.split('.')
#						hop_prefix = hop_octets[0] + '.' + hop_octets[1] + '.' + hop_octets[2] + '.0'
#						if hop_prefix in block:
#							if prev_prefix == "":
#								prev_prefix = block[hop_prefix]
#								#print hop_prefix, block[hop_prefix]
#							elif prev_prefix != block[hop_prefix]:
#								#print hop_prefix, block[hop_prefix]
#								prev_prefix = block[hop_prefix]
#								hop_count += 1
#				else:
#					skip = 0 # skips the first column because it is the probe ID
#
#			hop_list.append(hop_count)
#
#		output_file = traceroute_file + "-hops"
#		f = open(output_file, 'w')
#		for item_hop_list in hop_list:
#			print >> f, item_hop_list
#		#print hop_list, len(hop_list), output_file
#
#
#	progress_probe += 1
#	print progress_probe, tot_probe
#
#quit()







if len(sys.argv) != 2:
  print 'ERROR: Argument missing for calculating ping metrics.'
  print 'Arguments: [instance ID]'
  quit()

inst_id = sys.argv[1]
inst_file = '../files/traceroute/' + inst_id + '1a.c.root-servers.org_batch1'
output_file = 'traceroute/c-' + inst_id + '-prb-TEMP'

f = open(output_file, 'a+')

with open(inst_file) as json_data:
  data = json.load(json_data)
  json_data.close()

index = -1
for res in data:
	index += 1
	if 'result' in data[index]:
		print >> f, str(data[index]['prb_id'])

f.close()

#	if index == 5:
#		quit()

