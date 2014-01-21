import zlib
import os
import struct
import sys
from collections import namedtuple

class Expando():
    pass

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
    packPath = r'C:\Users\jaredpar\Documents\GitHub\VsVim\.git\objects\pack\pack-1e4dcc41b28289effa674569532d4074f2c226ef.pack'

    def parsePackEntry(f):
        c = struct.unpack('b', f.read(1))[0]
        type = (c >> 4) & 7
        size = c & 15
        shift = 4
        while (c & 0x80) != 0:
            if shift >= 32:
                print 'Bad shift value'
                return

            c = struct.unpack('b', f.read(1))[0]
            increment = (c & 0x7f) << shift
            size += increment
            shift += 7
            print 'size {0}'.format(size)
        print 'type {0} size {1}'.format(type, size)

        bytes = f.read(size)
        if type == 1 or type == 2 or type == 3: 
            data = zlib.decompress(bytes)
            print data
        else:
            print 'not analyzing data'

    with open(packPath, 'rb') as f:

        # Magic number 
        f.read(4) 

        # Version number
        f.read(4)

        bytes = f.read(4)
        number = struct.unpack('>i', bytes)[0]
        print 'Number of items {0}'.format(number)

        for i in range(0, 4):
            parsePackEntry(f)

def printPackIndex():
    # The test pack index we are working with for now 
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

        # Read in all of the SHA1 values 
        entryList = []
        for x in range(0, total):
            name = f.read(20)
            sha1 = ''
            for b in name:
                sha1 += b.encode('hex')
            entry = Expando()
            entry.sha1 = sha1
            entry.offset = ''
            entry.crc32 = ''
            entryList.append(entry)

        # Read in all of the CRC32 values
        for x in range(0, total): 
            bytes = f.read(4)
            number = struct.unpack('>i', bytes)[0]
            entryList[x].crc32 = number

        # Read in all of the offsets
        for x in range(0, total):
            bytes = f.read(4)
            number = struct.unpack('>i', bytes)[0]
            entryList[x].offset = number

        # TODO: Need to read the 8 byte offset table if any of the high bits were
        # set in the offset table

        # Closing SHA1 signature pairs
        f.read(40)

        entryList.sort(key=lambda x: x.offset)
        for entry in entryList:
            print '{0} - {1} - {2}'.format(entry.sha1, entry.offset, entry.crc32)

        remaining = f.read()
        if remaining == '':
            print 'Hit the end of the file'
        else:
            print 'Didn\'t hit the end of the file'
            print '{0} bytes remaining'.format(len(remaining))
            print remaining

            
