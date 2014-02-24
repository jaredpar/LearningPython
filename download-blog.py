import urllib2
import os
""" 
This script is used to download the contents of my blog at 
http://blogs.msdn.com/b/jaredpar
"""

os.mkdir("_posts")
#mkdir "_posts"

def url_to_name(url):
    """
    The format of URL is 
    
        b/jaredpar/archive/2014/01/06/interviewing-college-candidates.aspx

    """

    target = "archive/"
    startIndex = url.find(target) + len(target)
    name = url[startIndex:]
    return name.replace('/','-')


def download_post(url):

    print "Processing {0}".format(url)
    fullUrl = 'http://blogs.msdn.com/'  + url
    response = urllib2.urlopen(fullUrl)
    html = response.read()

    header = '<div class="post-content user-defined-markup">'
    startIndex = html.find(header) + len(header)
    endIndex = html.find('<div class="post-attachment-viewer">', startIndex)
    text = html[startIndex:endIndex]

    name = url_to_name(url)
    fullName = "_posts/{0}".format(name)
    with open(fullName, 'w') as f:
        f.write(text)

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
            nextIndex = endIndex + 1
            download_post(link)

