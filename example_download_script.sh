#!/bin/bash
email=insert_your_Climate_Explorer_email_address_here
lats="latitudes where you want the data"
lons="longitudes where you want the data"
vars="variables that you want to retrieve"
intertype=nearest # "nearest" grid point, or "interpolate".
standardunits="" # "" or "standardunits"
# land/sea mask not yet implemented in this script.
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
	
for lat in $lats
do
	for lon in $lons
	do
		for var in $vars
		do
			curl http://climexp.knmi.nl/get_index.cgi\?id=$email\&field=cmip5_${var}_Amon_ens_rcp85\&lat1=$lat\&lon1=$lon\&intertype=$intertype\&standardunits=$standardunits
			i=0
			exist=true
			while [ $exist = true ]
			do
				if [ $i -lt 10 ]; then
					ens=0$i
				else
					ens=$i
				fi
				file=icmip5_${var}_Amon_ens_rcp85_${lon}E_${lat}N_${in}_${su}_$ens.dat
				wget http://climexp.knmi.nl/data/$file
				if [ ! -s $file ]; then
					exist=false
				fi
				i=$((i+1))
			done
		done
	done
done
