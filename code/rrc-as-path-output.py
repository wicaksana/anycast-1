#!/usr/bin/env python 

import urllib2
import json
from pprint import pprint
response = urllib2.urlopen('https://stat.ripe.net/data/looking-glass/data.json?resource=184.164.241.0')
html = response.read()


data=json.loads(html)
for rrc in data['data']['rrcs']:
 for entry in data['data']['rrcs'][rrc]['entries']:
   out =  entry['as_path'].split(' ')
   out.reverse()
   out = ' '.join(out)
   print out 
   #print entry['as_path'] 

