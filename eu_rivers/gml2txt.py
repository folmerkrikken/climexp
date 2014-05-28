#!/usr/bin/python

from xml.dom import minidom
import cgi
import sys
import os
from unidecode import unidecode

Basinnames = {}
usenames = True
region = sys.argv[1]
region = region[0:2]

def getText(nodelist):
    rc = [ u'' ]
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return u''.join(rc)

def handleBasins(dom):
    Basins = dom.getElementsByTagName('ogr:' + root) 
    for Basin in Basins:
        handleBasin(Basin)

def handleBasin(Basin):
    # I assume there is only one polygon here per featuremember
    names = Basin.getElementsByTagName('ogr:NAME_ENGL') 
    Basinname = 'unknown'
    for name in names:
        Basinname = getText(name.childNodes)
    countries = Basin.getElementsByTagName('ogr:CTY_ID')
    countryname = '__' # default, some fields do not have the CTY_ID
    for country in countries:
        countryname = getText(country.childNodes)
    legals = Basin.getElementsByTagName('ogr:LGE_ID')
    legalname = '__'
    for legal in legals:
        legalname = getText(legal.childNodes)
    orgnames = Basin.getElementsByTagName('ogr:NAME')
    for orgname in orgnames:
        fullname = getText(orgname.childNodes)
    filename = countryname + "_" + legalname + "_" + unidecode(Basinname.replace(" ","_")) + ".txt"
    filename = filename.replace("/","_") # :-(
    # there are duplicate names...
    i = 0
    while os.path.exists(filename):
        i = i + 1
        filename = filename.split('.')[0] + ".%i.txt" % i
    print filename
    file = open(filename,"w")
    file.write("# RBD_F1v3.0 river basin " + countryname + " " + legalname + " " + \
        Basinname.encode('ascii', 'xmlcharrefreplace') + \
        " (" + fullname.encode('ascii', 'xmlcharrefreplace') + ")\n")
    file.write('# data from <a href="http://www.eea.europa.eu/data-and-maps/data/wise-Basin-basin-districts-rbds">EEA</a>\n')
    latlons = handlePolygon(Basin)
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

handleBasins(dom)
