import json
import urllib2
import gzip
from StringIO import StringIO

tempUrl = 'http://api.stackexchange.com//2.1/users/23283/answers?fromdate=1389312000&order=desc&sort=activity&site=stackoverflow'
myUrl = 'http://api.stackexchange.com/2.1/users/23282/answers?site=stackoverflow'
response = urllib2.urlopen(tempUrl)

if response.info().get('Content-Encoding') == 'gzip':
    buffer = StringIO(response.read())
    f = gzip.GzipFile(fileobj=buffer)
    text = f.read()
else:
    text = f.read()

j = json.loads(text)
for e in j['items']:
    print e['answer_id']
