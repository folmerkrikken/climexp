#!/bin/bash
# usage: $0 < file_with_lats_lons.txt
email=insert_your_Climate_Explorer_email_address_here
vars="rr tx tg tn"
intertype=nearest # "nearest" grid point, or "interpolate".
standardunits="" # "" or "standardunits"
if [ $email = insert_your_Climate_Explorer_email_address_here ]; then
	echo "Please modify this script by inserting your Climate Explorer id at the top of the script"
	exit -1
fi
case $intertype in
	nearest) in="n";;
	interpolate) in="i";;
	*) echo "$0: error: option intertype should be nearest or interpolate, not $intertype"; exit -1;;
esac
case $standardunits in
	"") su="";;
	standardunits) su="_su";;
	*) echo "$0: error: option intertype should be nearest or interpolate, not $intertype"; exit -1;;
esac
	
for var in $vars
do
    lat=something
    while [ 1 ]
    do
        echo reading lat lon
        read lat lon
        if [ -z "$lat" -o -z "$lon" ]; then
            echo "no more lat/lon pairs in stdin"
            exit
        fi
        field=ensembles_05_${var}_mo
		file=i${field}_${lon}E_${lat}N_${in}${su}.dat
        if [ ! -s $file ]; then
    		curl http://climexp.knmi.nl/get_index.cgi\?id=$email\&field=$field\&lat1=$lat\&lon1=$lon\&intertype=$intertype\&standardunits=$standardunits
	    	wget http://climexp.knmi.nl/data/$file
		    if [ ! -s $file ]; then
			    echo "something went wrong downloading $file"
			    exit
			else
			    c=`file $file | fgrep -c HTML`
			    if [ $c != 0 ]; then
			       echo "something went wrong downloading $file"
                    rm $file
			        exit
			    fi  
		    fi
		fi
	done
done
