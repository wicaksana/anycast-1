# This script creates files in probes/ which contain all ping information per probe-instance pair.
# Output files are named as c-instance-probe, where instance is the identifier of the C-root instance and probe is the prb_id.

import base64
import json
from pprint import pprint
import os
import sys

inst_file = 'RIPE-Atlas-measurement-2048556.json'
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

