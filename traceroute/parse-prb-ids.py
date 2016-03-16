import json

"""
Sunday Feb 17, 2016

BGP Hackathon, CAIDA, San Diego-CA, USA

This script has been written by the Anycast #1 team of the BGP hackathon.

Input:
JSON file with traceroute measurements from RIPE Atlas.
Note that the filename is hardcoded at this point and has to be changed by hand.

Output:
A file containing the list of all probe IDs used in the JSON traceroute measurement.
"""

with open('20160101.json') as json_data:
    data = json.load(json_data)
    json_data.close()

# Total of objects in the JSON file
pr = len(data)

c_hit = 0
c_err = 0
for index in range(0, pr):
    print(data[index]['prb_id'])

