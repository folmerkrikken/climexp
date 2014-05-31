#!/usr/bin/python

from xml.dom import minidom
import cgi
import sys

rivernames = {}
usenames = True
region = sys.argv[1]
region = region[0:2]

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleCountries(dom):
    countries = dom.getElementsByTagName('ogr:' + root) 
    for country in countries:
        handleCountry(country)

def handleCountry(country):
    global filenames
    # I assume there is only one polygon here per featuremember
    names = country.getElementsByTagName('ogr:AREA_SQKM') 
    for name in names:
        csqkm = getText(name.childNodes)
        sqkm = float(csqkm)
        if sqkm < min_area:
            return
    names = country.getElementsByTagName('ogr:BASIN_ID') 
    for name in names:
        countryname = getText(name.childNodes)
        if usenames:
            info = rivernames[countryname]
            countryname = info[0]
            othername = info[1]
        else:
            othername = countryname
        filename = countryname + ".txt"
        print filename
        file = open(filename,"w")
        file.write("# " + countryname + " (" + othername + ")\n")
        file.write('# data from <a href="http://hydrosheds.cr.usgs.gov/datadownload.php?reqdata=30bass">HydroSHEDS</a>\n')
        file.write("# area " + csqkm + " km2\n")
        latlons = handlePolygon(country)
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

handleCountries(dom)
