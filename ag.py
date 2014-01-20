import zlib
import os

def show(sha1):
    prefix = sha1[0:2]
    suffix = sha1[2:]

    # First find the file path 
    dirPath = os.path.join(r'.git\objects', prefix)
    files = os.listdir(dirPath)
    files = filter(lambda f: f.startswith(suffix), files)
    if len(files) == 0:
        print 'Could not find {0}'.format(sha1)
        return
    if len(files) > 1:
        print 'Multiple possible matches for {0}'.format(sha1)
        return

    filePath = os.path.join(dirPath, files[0])
    with open(filePath) as f:
        bytes = f.read()
        data = zlib.decompress(bytes)

    print data

