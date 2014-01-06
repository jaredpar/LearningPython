import urllib2

""" 
This script is used to download the contents of my blog at 
http://blogs.msdn.com/b/jaredpar
"""

for i in range(1, 13):
    print ('Page {0}'.format(i))

    url = 'http://blogs.msdn.com/b/jaredpar/default.aspx?PageIndex={0}'.format(i)
    response = urllib2.urlopen(url)
    html = response.read()

    header = '<a class="internal-link view-post" href="'
    headerLength = len(header)
    done = False
    nextIndex = 0
    while not done:
        startIndex = html.find(header, nextIndex) + headerLength + 1
        if startIndex <= 0 or startIndex < nextIndex:
            done = True
        else:
            endIndex = html.find('"', startIndex)
            link = html[startIndex:endIndex]
            print link
            nextIndex = endIndex + 1

