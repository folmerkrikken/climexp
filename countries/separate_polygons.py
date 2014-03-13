#!/usr/bin/python
import sys

if len(sys.argv) < 6:
    print "usage: sys.argv[0] polygonfile lon1 lon2 lat1 lat2"
    sys.exit(-1)

file = sys.argv[1]
lon1 = float(sys.argv[2])
lon2 = float(sys.argv[3])
lat1 = float(sys.argv[4])
lat2 = float(sys.argv[5])

with open(file,'r') as f:
    newpolygon = True
    firstblank = True
    notprinted = False
    print "# only points in the box {lat1} - {lat2}N, {lon1} - {lon2}E".format(lat1=lat1,
        lat2=lat2,lon1=lon1,lon2=lon2)
    for line in f:
        line = line[:-1] # get rid of newline, should be done more elegantly
        if line[0:1] == '#':
            print line
        elif line == '':
            newpolygon = True
            notprinted = False
            if firstblank:
                print line
                firstblank = False
        else:
            words = line.split()
            lon = float(words[0])
            lat = float(words[1])
            if lon >= lon1 and lon <= lon2 and lat >= lat1 and lat <= lat2:
                if notprinted:
                    print >> sys.stderr, 'cutting polygon in half!\n'
                    print >> sys.stderr, line
                print line
                newpolygon = False
                firstblank = True
                notprinted = False
            else:
                notprinted = True
