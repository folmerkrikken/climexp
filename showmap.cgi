#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Select a time series" "Choose coordinates"

echo "Click on the map to have the coordinates filled out"
echo "<p><a href=\"click_s.cgi?id=$FORM_id&scale=$FORM_timescale&latlon=\"><img src=\"worldmap_s.jpeg\" alt=\"world map\" ismap></a>"

. ./myvinkfoot.cgi
