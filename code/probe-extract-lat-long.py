import json
import csv


data_file = "../data/RIPE-Atlas-measurement-2048556.json"
prob_geo = "../data/meta-latest.out"

with open(prob_geo) as data_file:
    data = json.load(data_file)

geolocation_probes = [(item['address_v4'],
                       item['latitude'],
                       item['longitude'],
                       item['asn_v4'])
                      for item in data['objects'] if item['address_v4']]


with open('../data/probes-lat-long-asn.csv', 'wb') as testfile:
    csv_writer = csv.writer(testfile)
    for y in geolocation_probes:
        csv_writer.writerow(y)
