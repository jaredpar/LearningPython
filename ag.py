import zlib
import os
import struct
import sys

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
        index = data.find('\0')
        if index < 0: 
            print 'invalid object format'
            return

        data = data[index + 1:]

    print data

def printPack():
    # The test pack we are working with for now 
    packIndexPath = r'C:\Users\jaredpar\Documents\GitHub\VsVim\.git\objects\pack\pack-1e4dcc41b28289effa674569532d4074f2c226ef.idx'

    # just assuming version 2 of the .idx format for now
    # https://www.kernel.org/pub/software/scm/git/docs/technical/pack-format.txt

    with open(packIndexPath, 'rb') as f:

        # Magic number 
        f.read(4) 

        # Version number
        f.read(4)

        total = 0
        for x in range(0, 256):
            bytes = f.read(4)
            number = struct.unpack('>i', bytes)[0]
            print "{0} - {1}".format(x, number)
            total = number

        # Print out all of the SHA1 values stored in the pack file 
        for x in range(0, total):
            name = f.read(20)
            for b in name:
                sys.stdout.write(b.encode('hex'))
            print ""


