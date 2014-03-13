#!/bin/sh
# script to be able to use queryfield.cgi from python

. ./queryfield.cgi
echo "file=$file"
echo "climfield=$climfield"
echo "LSMASK=$LSMASK"
echo "NPERYEAR=$NPERYEAR"
echo "NOMISSING=$NOMISSING"
echo "map=$map"
