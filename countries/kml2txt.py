#!/usr/bin/python

from xml.dom import minidom
import cgi

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleCountries(dom):
    countries = dom.getElementsByTagName('Placemark') 
    for country in countries:
        handleCountry(country)

def handleCountry(country):
    name = country.getElementsByTagName('name') 
    countryname = getText(name.item(0).childNodes)
    countryname = countryname.replace(u'\ufffd','c')
    print countryname
    filename = countryname.replace(" ","_") + '.txt'
    file = open(filename,"w")
    file.write("# " + countryname + "\n")
    file.write("# from http://www.rjruss.info/2010/12/free-countries-of-world-in-polygon-kml.html\n")
    polygons = country.getElementsByTagName('Polygon')
    for polygon in polygons:
        latlons = handlePolygon(polygon)
        for latlon in latlons:
            file.write(latlon.replace(","," ") + "\n")
        file.write("\n")

def handlePolygon(polygon):
    coordinates = polygon.getElementsByTagName('coordinates')
    returnlist = []
    for coordinate in coordinates:
        latlons = getText(coordinate.childNodes)
        latlons = latlons.split(" ")
        returnlist += latlons
    return returnlist

dom = minidom.parse('countries_world.kml')
handleCountries(dom)

###countrylist = xmldoc.getElementsByTagName('name') 
###print len(countrylist)
###for country in countrylist:
###    for node in country.childNodes:
###        if node.nodeType == node.TEXT_NODE:
###            print node.data
