##
#	Sunday Feb 17, 2016
#
#	BGP Hackathon, CAIDA, San Diego-CA, USA
#
#	This script has been written by the Anycast #1 team of the BGP hackathon.
#
#	Input:
#		A JSON file from RIPE Atlas containing results of a traceroute measurement.
#
#	Output:
#		Individual files per probe in the traceroute measurement. These files contain in each line all the hops in a traceroute run.
#

import base64
import json
from pprint import pprint
import os
import sys

inst_file = '20160101.json'

with open(inst_file) as json_data:
  data = json.load(json_data)
  json_data.close()

index = -1
for res in data:
	index += 1
	output_str = ""
	if 'result' in data[index]:
		for idx_hop in range(0,len(data[index]['result'])):
			if 'result' in data[index]['result'][idx_hop]:
				found_hop = 0
				for idx_try in data[index]['result'][idx_hop]['result']:
					if idx_try.get('from'):
						found_hop = 1
						output_str = output_str + ' ' + idx_try['from']
						break
				if found_hop == 0:
					output_str = output_str + ' *'

	if output_str != "":
		output_file = 'traceroute_probe/' + str(data[index]['prb_id'])
		output_str = str(data[index]['prb_id']) + output_str
		f = open(output_file, 'a+')
		print >> f, output_str
		f.close()

