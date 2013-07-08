#!/bin/sh
# to be sourced from plot_atlas_form.cgi, all input has already been processed and the top of the page drawn.
. ./define_functions_atlas.cgi
. ./more_functions_atlas.cgi

echo "<font color=#ff2222>plot_atlas_map: UNDER CONSTRUCTION</font><br>"
###echo "lwrite=$lwrite<br>"

# First find files

get_file_list

# Next compute monthly time series

get_region_extension
monthlydir=atlas/series/$dir/monthly/$region_extension
[ ! -d $monthlydir ] && mkdir -p $monthlydir
if [ -n "$FORM_anomaly" ]; then
	[ -z "${FORM_anom1}" ] && FORM_anom1=1986
	[ -z "${FORM_anom2}" ] && FORM_anom2=2005
	if [ $FORM_anom1 -gt $FORM_anom2 ]; then
		echo "error: anomalies from $FORM_anom1 to $FORM_anom2 are not defined"
		. ./myvinkfoot.cgi
		exit
	fi
	anomdir=atlas/series/$dir/monthly_anom_${FORM_anom1}_${FORM_anom2}/$region_extension
	[ ! -d $anomdir ] && mkdir -p $anomdir
fi
if [ -z "$FORM_anomaly" ]; then
	dump0dir=atlas/series/$dir/monthly_dump0/$region_extension
	dump1dir=atlas/series/$dir/monthly_dump1/$region_extension
else
	dump0dir=atlas/series/$dir/monthly_dump0_${FORM_anom1}_${FORM_anom2}/$region_extension
	dump1dir=atlas/series/$dir/monthly_dump1_${FORM_anom1}_${FORM_anom2}/$region_extension
fi
[ ! -d $dump0dir ] && mkdir -=p $dump0dir
[ ! -d $dump1dir ] && mkdir -=p $dump1dir

for file in $files
do
	get_model # deduce model from $file and get path to lsmask
	series=$monthlydir/time_`basename $file .nc`_${region_extension}.dat
	if [ ! -s $series -o $series -ot $file ]; then
		case $FORM_region in
			point)	args="$FORM_lon $FORM_lon $FORM_lat $FORM_lat interpolate";;
			box) 	if [ "$FORM_masktype" = all ]; then
						lsargs=""
					else
						lsargs="lsmask $LSMASK $FORM_masktype"
					fi
					args="$FORM_lon1 $FORM_lon2 $FORM_lat1 $FORM_lat2 $lsargs nearest"
					;;
			srex)	lookup_region
					define_region
					if [ -n "${abbr[$subregion]}" ]; then
						# the region is defined by a mask
						maskfile=${abbr[$subregion]}/mask_${model}_${abbr[$subregion]}.nc
						if [ ! -s $maskfile ]; then
							echo "error: cannot locate maskfile $maksfile"; exit -1
						fi
						args="mask $maksfile"
					else
						args="${lon1[$subregion]} ${lon2[$subregion]} ${lat1[$subregion]}  ${lat2[$subregion]} lsmask $LSMASK ${lsmask[$subregion]}"
					fi
					;;
			mask) 	save_uploaded_mask
					if [ ! -s $maskfile ]; then
						echo "error: cannot located uploaded maskfile $maksfile"; exit -1
					fi
					args="mask $maskfile"
					;;
			*) 		echo "error: unknown value for region: $FORM_region"; exit -1
					;;
		esac
		echo "averaging $model over $region_extension..."
		[ "$lwrite" = true ] && echo "get_index $file $args > $series"
		./bin/get_index $file $args > $series
		if [ ! -s $series ]; then
			echo "Something went wrong in $file $args > $series"
			. ./myvinkfoot.cgi
			exit
		fi
	else
		[ "$lwrite" = true ] && echo "$series is up-to-date"
	fi
	
	# take anomalies if requested
	
	if [ -z "$FORM_anomaly" ]; then
		aseries=$series
	else
		[ "$lwrite" = true ] && echo "Taking anomalies..."
		if [ -n "$FORM_normsd" ]; then
			rel="normsd ave $FORM_sum"
		else
			rel=""
		fi
		if [ -z "$FORM_normsd" ]; then
			aseries=$anomdir/`basename $series .dat`a.txt
		else
			aseries=$anomdir/`basename $series .dat`a_rel$FORM_sum.txt
		fi
		if [ ! -s $aseries -o $aseries -ot $series ]; then
			# ensanom here means "compute anomalies relative to the ensemble mean"
			# normsd here means "take relative anomalies"
			[ "$lwrite" = true ] && echo "plotdat anom $FORM_anom1 $FORM_anom2 ensanom $rel $series | fgrep -v repeat > $aseries"
			plotdat anom $FORM_anom1 $FORM_anom2 ensanom $rel $series | fgrep -v repeat > $aseries
			status=$?
			c=`cat $aseries | wc -l`
			if [ $status != 0 -o -z "$c" -o "$c" -lt 100 ]; then
				echo "something went wrong in making $aseries"
				cat $aseries
				rm $aseries
				. ./myvinkfoot.cgi
				exit -1
			fi
		fi # update needed?
	fi # anomalies requested ?
	
	# make plot files summing over the correct season
	
	for ext in $dumptypes
	do
		case $ext in
			0) times="end $endhistory";dumpdir=$dump0dir;;
			1) times="begin $((endhistory+1))";dumpdir=$dump1dir;;
			*) echo "$0: error: unknown ext $ext"; exit -1;;
		esac
		dumpfile=$dumpdir/`basename $series .dat`_m${FORM_month}_s$FORM_sum.txt
		# always plot standard units
		standardunits=standardunits
		
		if [ ! -s $dumpfile -o $dumpfile -ot $aseries ]; then
			[ "$lwrite" = true ] && echo "correlate $aseries file $regrfile mon $FORM_mon ave $FORM_sum $times dump $dumpfile"
			correlate $aseries time mon $FORM_mon ave $FORM_sum $times $standardunits dump $dumpfile
			status=$?
			c=`cat $dumpfile | wc -l`
			if [ $status != 0 -o $c -lt 80 ]; then
				echo "something went wrong in making $dumpfile"
				echo "status=$status, c=$c"
				cat $dumpfile
				rm $dumpfile
				. ./myvinkfoot.cgi
				exit -1
			fi
		fi
	done
	
done # files
