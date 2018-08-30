#!/usr/bin/python

from xml.dom import minidom
import cgi
import sys
import os
from unidecode import unidecode

Subdivisionnames = {}
usenames = True
region = sys.argv[1]
region = region[0:2]

def getText(nodelist):
    rc = [ u'' ]
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return u''.join(rc)

def handleSubdivisions(dom):
    Subdivisions = dom.getElementsByTagName('ogr:' + root) 
    for Subdivision in Subdivisions:
        print Subdivision;
        handleSubdivision(Subdivision)

def handleSubdivision(Subdivision):
    # I assume there is only one polygon here per featuremember
    names = Subdivision.getElementsByTagName('ogr:ST_NM') 
    Subdivisionname = 'unknown'
    for name in names:
        Subdivisionname = getText(name.childNodes)
    filename = root + '.txt'
    print filename
    file = open(filename,"w")
    file.write("# India Subdivision " + Subdivisionname + "\n")
    latlons = handlePolygon(Subdivision)
    for latlon in latlons:
        file.write(latlon.replace(","," ") + "\n")
    file.write("\n")
    file.close()

def handlePolygon(polygon):
    coordinates = polygon.getElementsByTagName('gml:coordinates')
    returnlist = []
    for coordinate in coordinates:
        latlons = getText(coordinate.childNodes)
        latlons = latlons.split(" ")
        returnlist += latlons
    return returnlist

if len(sys.argv) <= 2:
    print "usage: " + sys.argv[0] + " infile.gml min_area"
    exit(-1)

root = sys.argv[1]
root = root.split(".")[0]
dom = minidom.parse(sys.argv[1])
min_area = float(sys.argv[2])

handleSubdivisions(dom)
