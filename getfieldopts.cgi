#!/bin/bash
if [ -n "$FORM_minfac" ]; then
  corrargs="$corrargs minfac $FORM_minfac"
fi
if [ -n "$FORM_minfacsum" ]; then
  corrargs="$corrargs minfacsum $FORM_minfacsum"
fi
if [ -n "$FORM_intertype" ]; then
  corrargs="$corrargs interpolate $FORM_intertype"
fi
if [ -z "$FORM_mapformat" ]; then
    FORM_mapformat=png
fi
if [ "$FORM_mapformat" = png ]; then
    if [ -n "$FORM_mproj" -a "$FORM_mproj" != "default" ]; then
	map="$map
set mproj $FORM_mproj"
	if [ "$FORM_mproj" = "robinson" ];then
	    map="set lat -90 90
$map"
	elif [ "$FORM_mproj" = "nps" ]; then
	    map="set lat 20 90
$map"
	elif [ "$FORM_mproj" = "sps" ]; then
	    map="set lat -90 -20
$map"
	fi
    fi
else
    map="$map
set mproj latlon"
fi

if [ "$FORM_plottype" = "time-lon" ]; then
  if [ -z "$FORM_lat1" ]; then
    echo "Error: please fill out the latitude of the time-lon plot"
    echo "</body></html>"
    exit
  else
    map="$map
set lat $FORM_lat1"
    if [ -n "$FORM_lat2" ]; then
      FORM_var="ave($FORM_var,lat=$FORM_lat1,lat=$FORM_lat2)"
    fi
  fi
else
  if [ -n "$FORM_lat1" ]; then
    if [ -n "$FORM_lat2" ]; then
      if [ "${FORM_lat1%.*}" -lt "${FORM_lat2%.*}" ]; then
        map="$map
set lat $FORM_lat1 $FORM_lat2"
      else
        map="$map
set lat $FORM_lat2 $FORM_lat1"
      fi
    else
      map="$map
set lat $FORM_lat1 $FORM_lat1"
    fi
  elif [ -n "$FORM_lat2" ]; then
    map="$map
set lat $FORM_lat2 $FORM_lat2"
  fi
fi

if [ "$FORM_plottype" = "time-lat" ]; then
  if [ -z "$FORM_lon1" ]; then
    echo "Error: please fill out the longitude of the time-lat plot"
    echo "</body></html>"
    exit
  else
    map="$map
set lon $FORM_lon1"
    if [ -n "$FORM_lon2" ]; then
      FORM_var="ave($FORM_var,lon=$FORM_lon1,lon=$FORM_lon2)"
    fi
  fi
else
  if [ -n "$FORM_lon1" ]; then
    if [ -n "$FORM_lon2" ]; then
      map="$map
set lon $FORM_lon1 $FORM_lon2"
    else
      map="$map
set lon $FORM_lon1 $FORM_lon1"
    fi
  elif [ -n "$FORM_lon2" ]; then
    map="$map
set lon $FORM_lon2 $FORM_lon2"
  fi
fi

if [ -n "$FORM_lev1" ]; then
  map="$map
set lev $FORM_lev1 $FORM_lev2
set parea 1.5 10.5 1 7.5"
fi
   
