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
    print countryname
    filename = "US_" + countryname.replace(" ","_") + '.txt'
    file = open(filename,"w")
    file.write("# " + countryname + "\n")
    file.write("# from https://developers.google.com/kml/documentation/us_states.kml\n")
    polygons = country.getElementsByTagName('Polygon')
    for polygon in polygons:
        latlons = handlePolygon(polygon)
        for latlon in latlons:
            file.write(latlon.replace(","," "))
        file.write("\n")

def handlePolygon(polygon):
    coordinates = polygon.getElementsByTagName('coordinates')
    returnlist = []
    for coordinate in coordinates:
        latlons = getText(coordinate.childNodes)
        latlons = latlons.split(" ")
        returnlist += latlons
    return returnlist

dom = minidom.parse('us_states.kml')
handleCountries(dom)
