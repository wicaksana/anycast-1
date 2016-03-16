import requests
import json

response = requests.get('https://stat.ripe.net/data/looking-glass/data.json?resource=184.164.241.0')
html = response.text
print(html)

data = json.loads(html)
for rrc in data['data']['rrcs']:
    print("the rrc: ".format(rrc))
    for entry in data['data']['rrcs'][rrc]['entries']:
        out = entry['as_path'].split(' ')
        out.reverse()
        out = ' '.join(out)
        print(out)
    # print(entry['as_path'])

