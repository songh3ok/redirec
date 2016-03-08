import json
import urllib
import struct
import csv
import requests


response = requests.get('http://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP949.TXT', stream=True)

map = {}
for line in csv.reader(response.raw, delimiter='\t'):
    if len(line) != 3:
        continue

    cp949_str, utf8_str, comment = line
    if cp949_str.strip() and utf8_str.strip():
        utf8 = unichr(int(utf8_str, 0)).encode('utf8')
        cp949 = urllib.quote(struct.pack(">H", int(cp949_str, 0)))
        map[utf8] = cp949


var = 'var charTable = %s;' % json.dumps(map)
commonScript = open('src.js').read()

js_file = open('build.js', 'w+')
js_file.write(var + commonScript)
