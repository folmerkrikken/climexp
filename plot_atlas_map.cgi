#!/bin/sh
# to be sourced from plot_atlas_form.cgi, all input has already been processed and the top of the page drawn.
# note that the hatching is not yet implemented, this should be done by doing the same exercise
# for lots of time steps in the control run and computing the s.d. of these as in make_control.sh
# and make_derived_control.sh .  
. ./define_functions_atlas.cgi
. ./more_functions_atlas.cgi

echo "<font color=#ff2222>plot_atlas_map: UNDER CONSTRUCTION</font>"
echo "Hatching of regions where the change is small compared to natural variability is not yet ready<br>"

# First find files

get_file_list

# Next compute difference / regression data

season=mon${FORM_mon}_ave${FORM_sum}
get_season_name
nfiles=0
for file in $files
do
	nfiles=$((nfiles+1))
done
outfiles=""
if [ "$FORM_database" = CMIP5one ]; then
	one=one
else
	one=""
fi
if [ -n "$FORM_normsd" ]; then
	rel=rel
else
	rel=""
fi
quantroot=atlas/regr/$dir/quant$one
[ ! -d $quantroot ] && mkdir -p $quantroot

if [ "$FORM_measure" = diff ]; then
	root=atlas/diff/$dir/$season
	[ ! -d $root ] && mkdir -p $root
	ifiles=0
	for file in $files
	do
		if [ $FORM_end -lt $FORM_begin ]; then
			echo "error: end $FORM_end year less then begin year $FORM_begin"
			. ./myvinkfoot.cgi
			exit
		fi
		if [ $FORM_end2 -lt $FORM_begin2 ]; then
			echo "error: end $FORM_end2 year less then begin year $FORM_begin2"
			. ./myvinkfoot.cgi
			exit
		fi
		difffile=$root/${rel}diff_`basename $file .nc`_${FORM_begin2}-${FORM_end2}_minus_${FORM_begin}-${FORM_end}_$season.nc
		outfiles="$outfiles $difffile"
		ifiles=$((ifiles+1))
		if [ ! -s $difffile -o $difffile -ot $file ]; then
			echo "computing difference field $ifiles/$nfiles ...<br>"
			[ "$lwrite" = true ] && echo "difffield $file $file mon $FORM_mon ave $FORM_sum begin2 $FORM_begin end2 $FORM_end begin $FORM_begin2 end $FORM_end2 $FORM_normsd $difffile<br>"
			difffield $file $file mon $FORM_mon ave $FORM_sum begin2 $FORM_begin end2 $FORM_end begin $FORM_begin2 end $FORM_end2 $FORM_normsd $difffile
			[ "$lwrite" = true ] && ls -l $difffile
		fi
	done
	quantfile=$quantroot/quant_diff_${FORM_var}_${type}_${FORM_begin2}-${FORM_end2}_minus_${FORM_begin}-${FORM_end}_$season.nc
	xvar=${rel}diff
elif [ "$FORM_measure" = regr ]; then
	root=atlas/regr/$dir/$season
	[ ! -d $root ] && mkdir -p $root
	case $FORM_regr in
		time) reffile=KNMIData/time12.dat;;
		co2eq) reffile=CDIACData/RCP45_CO2EQ.dat;;
		obstglobal) reffile=NASAData/giss_al_gl_m_4yrlo.dat;;
		modtglobal) echo "reference modtglobal not yet implemented"; . ./myvinkfoot.cgi; exit;;
		*) echo "unknown reference $FORM_regr"; . ./myvinkfoot.cgi; exit;;
	esac
	if [ $FORM_end2 -lt $FORM_begin ]; then
		echo "error: end $FORM_end2 year less then begin year $FORM_begin"
		. ./myvinkfoot.cgi
		exit
	fi
	if [ $FORM_refr != modtglobal ]; then
		if [ ! -s $reffile ]; then
			echo "error: cannot find reference series $reffile"
			. ./myvinkfoot.cgi
			exit
		fi
	fi
	ifiles=0
	for file in $files
	do
		regrfile=$root/regr_`basename $file .nc`_${FORM_regr}_${FORM_begin}-${FORM_end2}_$season.nc
		outfiles="$outfiles $regrfile"
		ifiles=$((ifiles+1))
		if [ ! -s $regrfile -o $regrfile -ot $file ]; then
			echo "computing regression of field $ifiles/$nfiles ...<br>"
			correlatefield $file $reffile mon $FORM_mon ave $FORM_sum begin $FORM_begin end $FORM_end2 $regrfile > /dev/null
		fi
	done
	quantfile=$quantroot/quant_regr_${FORM_var}_${type}_${FORM_regr}_${FORM_begin}-${FORM_end2}_$season.nc
	xvar=${rel}regr
else
	echo "unknown measure $FORM_measure"
	. ./myvinkfoot.cgi
	exit
fi

# compute quantiles if needed

if [ "$FORM_plotvar" != mean ]; then
	infiles=""
	doit=false
	if [ ! -s $quantfile ]; then
		doit=true
	else
		for outfile in $outfiles
		do
			if [ $quantfile -ot $outfile ]; then
				doit=true
			fi
		done
	fi
	if [ $doit = true -o "$lwrite" = true ]; then # (re)generate $quantfile	
		for outfile in $outfiles
		do
			infile=/tmp/${xvar}_`basename $outfile`
			if [ ! -s $infile -o $infile -ot $outfile ]; then
				if [ ! -s $outfile ]; then
					echo "$0: error: cannot find $outfile"; exit
				fi
				ncks -O -v $xvar $outfile $infile
			fi
			infiles="$infiles $infile"
		done
		echo "generating quantiles ..."
		###echo "./bin/quantiles_field $infiles $quantfile"
		./bin/quantiles_field $infiles $quantfile | sed -e 's/$/<br>/'
		if [ $? != 0 -o ! -s $quantfile ]; then
			echo "$0: error: something went wrong"
			exit
		fi
		rm $infiles
	fi
	plotfile=$quantfile
else
	if [ $nfiles != 1 ]; then
		echo "error: expecting only one file, not $files"
		. ./myvinkfoot.cgi
		exit
	fi
	plotfile=${outfiles# *}
fi
[ "$lwrite" = true ] && echo "plotfile=$plotfile<br>"

# add sd from pre-industrial runs
# for the time being just set to zero...
q=`basename $plotfile`
if [ "$FORM_plotvar" != mean ]; then
	cdo delname,sd,sdsd $plotfile /tmp/$q
	# temporarily set sd to zero
	cdo selname,sd,sdsd $plotfile /tmp/sd_$q
else
	cp $plotfile /tmp/$q
	cdo selname,prob $plotfile /tmp/sd2_$q
	cdo setname,sd /tmp/sd2_$q /tmp/sd_$q
	rm /tmp/sd2_$q
fi
cdo mulc,0 /tmp/sd_$q /tmp/sd2_$q
rm /tmp/sd_$q
mv $plotfile $plotfile.bak
cdo merge /tmp/sd2_$q /tmp/$q $plotfile
if [ ! -s $plotfile ]; then
	echo "Something went wrong in"
	echo "cdo merge /tmp/sd_$q /tmp/$q $plotfile"
	exit -1
fi
rm $plotfile.bak


# Finally plot map

lonoverlap=10
latoverlap=5
if [ "$FORM_region" = srex ]; then
	[ "$lwrite" = true ] && echo "calling lookup_region with FORM_srex=$FORM_srex<br>"
	lookup_region
	define_region
	# check
	if [ "$FORM_srex" != "${abbr[$subregion]}" -a "$FORM_srex" != "${shortname[$subregion]}" ]; then
		echo "error: inconsistency in lookup_region: $FORM_srex gives $region $subregion"
		echo "but abbr = ${abbr[$subregion]} and shortname = ${shortname[$subregion]}"
		. ./myvinkfoot.cgi
		exit
	fi
	# make the map larger than the area over which the time series are defined
	if [ -z "${lon1[$subregion]}" ]; then # polygon region
		if [ ! -s SREX/$FORM_srex.txt ]; then
			echo "internal error: cannot find file SREX/$FORM_srex.txt"
			echo "region=$region, subregion=$subregion, lon1[$subregion]=${lon1[$subregion]}"
			exit -1
		fi
		eval `bin/polygon2box SREX/$FORM_srex.txt | tr -d ' '`
		lon1[$subregion]=$xmin # we assume the region have been encoded sensibly with no wrapping longitudes
		lon2[$subregion]=$xmax
		lat1[$subregion]=$ymin
		lat2[$subregion]=$ymax
	fi
elif [ "$FORM_region" = box ]; then
	subregion=1
	lon1[$subregion]=$FORM_lon1
	lon2[$subregion]=$FORM_lon2
	lat1[$subregion]=$FORM_lat1
	lat2[$subregion]=$FORM_lat2
elif [ "$FORM_region" = point ]; then
	subregion=1
	lon1[$subregion]=$FORM_lon
	lon2[$subregion]=$FORM_lon
	lat1[$subregion]=$FORM_lat
	lat2[$subregion]=$FORM_lat
elif [ "$FORM_region" = mask ]; then
	echo "cannot handle maps with masks yet"
	exit -1
else
	echo "error: unknown region $FORM_region"; exit -1
fi
if [ "$lwrite" = true ]; then
	echo "lon1[$subregion] = ${lon1[$subregion]}<br>"
	echo "lon2[$subregion] = ${lon2[$subregion]}<br>"
	echo "lat1[$subregion] = ${lat1[$subregion]}<br>"
	echo "lat2[$subregion] = ${lat2[$subregion]}<br>"
fi
if [ ${lon1[$subregion]} != -170 -o ${lon2[$subregion]} != 190 ]; then
	plotlon1=`echo "${lon1[$subregion]} - $lonoverlap" | bc -l`
	plotlon2=`echo "${lon2[$subregion]} + $lonoverlap" | bc -l`
else
	plotlon1=${lon1[$subregion]}
	plotlon2=${lon2[$subregion]}
fi
if [ ${lat1[$subregion]} != -90 ]; then
	plotlat1=`echo "${lat1[$subregion]} - $latoverlap" | bc -l`
else
	plotlat1=${lat1[$subregion]}
fi
if [ ${lat2[$subregion]} !=	90 ]; then
	plotlat2=`echo "${lat2[$subregion]} + $latoverlap" | bc -l`
else
	plotlat2=${lat2[$subregion]}
fi
[ "$lwrite" = true ] && echo "plotlon1,plotlon2=$plotlon1,$plotlon2<br>"
[ "$lwrite" = true ] && echo "plotlat1,plotlat2=$plotlat1,$plotlat2<br>"
# variable
c=`file $plotfile | fgrep -c NetCDF`
[ $c != 1 ] && echo "$0: error: cannot find $plotfile" && exit -1
[ ! -d atlas/maps/$dir ] && mkdir -p atlas/maps/$dir
root=atlas/maps/$dir/`basename $plotfile .nc`
get_region_extension
root=${root}_${region_extension}
var="$FORM_var"
define_var
if [ -n "$FORM_normsd" ]; then
	plotvarunits="%"
else
	plotvarunits=${units#\[}
	plotvarunits=${plotvarunits%\]}
fi
[ "$lwrite" = true ] && echo "plotvarunits=$plotvarunits<br>"
if [ "$FORM_measure" = diff ]; then
	titlebegin="${varname} ${FORM_begin2}-${FORM_end2} minus ${FORM_begin}-${FORM_end} $sname"
elif [ "$FORM_measure"=regr ]; then
	titlebegin="regression ${varname} on $FORM_regr ${FORM_begin}-${FORM_end2} $sname"
	case "$FORM_regr" in
		time) plotvarunits="$plotvarunits/yr";;
		co2eq) plotvarunits="$plotvarunits/ppm";;
		*global) plotvarunits="$plotvarunits/K";;
		*) echo "internal error: unknow value for FORM_regr=$FORM_regr"; exit -1;;
	esac
else
	echo "internal error: unknown measure $FORM_measure"; exit -1
fi
case $FORM_dataset in
	CMIP5*) title="$FORM_dataset $FORM_scenario_cmip5 $titlebegin";; 
	CMIP3) title="$FORM_dataset $FORM_scenario_cmip3 $titlebegin";; 
	RT2b) title="$FORM_dataset $FORM_scenario_rt2b $titlebegin";;
	RT3|ERAi|20CR) title="$FORM_dataset $titlebegin";;
	obs) fieldname=FORM_obs_$FORM_var
		title="${!fieldname} $titlebegin";;
	*) echo "error: unknown dataset $FORM_dataset"; exit -1;;
esac
mycbar=True
nsd=1 # change < this number of standard deviations natural variability is hatched
if [ $FORM_plotvar != mean ]; then
	plotvar="$FORM_plotvar"
elif [ $FORM_measure = diff ]; then
	plotvar=${rel}diff
elif [ $FORM_measure = regr ]; then
	plotvar=${rel}regr
fi
pmin="5"
if [ $pmin != 5 ]; then
	echo "$0: sorry, can only handle pmin = 5 at the moment, not $pmin,$nsd"; exit -1
fi
if [ ${plotvar#p} != $plotvar ]; then
	plotvarname="${plotvar#p}%"
else
	plotvarname=$FORM_plotvar
fi
title="$plotvarname $title"
if [ $plotvar = sd ]; then
	uncert=0
else
	uncert=0 # no hatching for the time being1
fi
force=true # false
if [ $force=true -o ! -s $root.eps -o $root.eps -ot $plotfile ]; then
	cat > /tmp/nclinput$$.ncl <<EOF
 load "\$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
 load "\$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
 load "\$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
 load "\$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
 load "./danoprob.ncl"

begin

; READ DATA
  a = addfile("${plotfile}","r")
  plotvar = a->${plotvar}(0,0,:,:)
  plotvar = a->${plotvar}(0,0,:,:) * ${fac}
; danoprob cuts on this variable; this gives $pmin/100 when plotvar=$nsd * sd
  prob = ( $pmin / 100. )  * $nsd * a->sd(0,0,:,:) / (0.000001 + abs(a->${plotvar}(0,0,:,:)))
  copy_VarCoords(plotvar,prob)

; SETUP POSTSCRIPT
  p = new(6,graphic)
  wks = gsn_open_wks("eps","${root}")

; RESOURCES FOR PLOT
  res = True
  res@gsnDraw = False
  res@gsnFrame = False
  if ("$region".ne."world") then
   res@mpCenterLonF = ($plotlon1+$plotlon2)/2
  else
   res@mpCenterLonF = 10.
  end if

; COLORS
  rgbcbar = "$rgbcbar"
  plotvarunits="$plotvarunits"


; CONTOUR INTERVALS
  res@cnLevelSelectionMode = "ExplicitLevels"
  res@cnLevels = $cnlevels

; LABELS
  res@gsnLeftString = "$title"
  res@gsnRightString = ""
  res@lbLabelBarOn = $mycbar
  res@lbTitleString = "["+plotvarunits+"]"
  res@lbTitleFontHeightF = 0.012
  res@lbTitlePosition = "Right"
  res@lbTitleDirection = "Across"
  res@lbLabelAutoStride = True
  res@lbLabelFontHeightF = 0.012

; TO PREVENT AN UNPLOTTED HALF...
 if("$region".eq."pacific") then
   usefieldf = False
 else
   usefieldf = True
 end if

; CALL PLOT FUNCTION
  res@mpPerimOn = False
  if("$region".ne."arctic".and."$region".ne."highlatitudes".and."$region".ne."antarctica") then
   res@mpProjection = "Robinson"
   res@mpFillOn = False
   res@mpLimitMode = "LatLon"
   res@mpMinLonF = $plotlon1
   res@mpMaxLonF = $plotlon2
   res@mpMinLatF = $plotlat1
   res@mpMaxLatF = $plotlat2
   plot = danoprob(wks,res,plotvar,"shaded",$cbar,rgbcbar,0,$pmin,$cmin,$cmax,$cint,"latlon",$uncert,prob,usefieldf)
  end if
  if ("$region".eq."arctic".or."$region".eq."highlatitudes") then
   res@mpMinLatF = $plotlat1
   res@gsnTickMarksOn = False
   plot = danoprob(wks,res,plotvar,"shaded",$cbar,rgbcbar,0,$pmin,$cmin,$cmax,$cint,"NH",$uncert,prob,usefieldf)
  end if
  if ("$region".eq."antarctica") then
   res@mpMaxLatF = $plotlat2
   res@gsnTickMarksOn = False
   plot = danoprob(wks,res,plotvar,"shaded",$cbar,rgbcbar,0,$pmin,$cmin,$cmax,$cint,"SH",$uncert,prob,usefieldf)
  end if
  lres = True
EOF
	[ "$lwrite" = true ] && echo "FORM_region,FORM_srex = $FORM_region,$FORM_srex<br>"
	if [ $FORM_region != srex -o "$FORM_srex" != world ]; then
		i=$subregion
		if [ $FORM_region != srex -o -z "${abbr[$i]}" ]; then
			[ "$lwrite" = true ] && echo "using lon12,lat12<br>"
			cat >> /tmp/nclinput$$.ncl <<EOF
; ADD RECTANGLES
  xpts = (/${lon1[$i]},${lon1[$i]},${lon2[$i]},${lon2[$i]},${lon1[$i]}/)
  ypts = (/${lat1[$i]},${lat2[$i]},${lat2[$i]},${lat1[$i]},${lat1[$i]}/)
  do i = 0,3
   p(i) = gsn_add_polyline(wks,plot,xpts(i:i+1),ypts(i:i+1),lres)
  end do
  delete(xpts)
  delete(ypts)
EOF
		else # polygon
			[ "$lwrite" = true ] && echo "using SREX/${abbr[$i]}_kaal.txt<br>"
			cat >> /tmp/nclinput$$.ncl <<EOF

; ADD POLYGONS - the "kaal" version does not have comments and repeats the first line at the end
    lonlat = asciiread("SREX/${abbr[$i]}_kaal.txt",(/1+${npoly[$i]},2/),"float")
	do i = 0,$((npoly[$i]-1))
	 p(i) = gsn_add_polyline(wks,plot,lonlat(i:i+1,0),lonlat(i:i+1,1),lres)
	end do
    delete(lonlat)
EOF
		fi # box or polygon
	fi # not world
	cat >> /tmp/nclinput$$.ncl <<EOF
  draw(plot)
; ADD PERCENTILE LABEL
  ;txres = True
  ;txres@txFontHeightF = 0.017
  ;txres@txFontColor = 1 ; 0
  ;txres@txBackgroundFillColor = "white" ; "black"
  ;gsn_text_ndc(wks,"${plotvarname}",$labelx,$labely,txres)

  frame(wks)

end
EOF
	export NCARG_ROOT=./ncl
	./ncl/bin/ncl -Qn < /tmp/nclinput$$.ncl | fgrep -v EXPLICIT | sed -e 's/$/<br>/'
	status=$?
	size=`cat $root.eps | wc -c`
	[ "$lwrite" = true ] && echo "size=$size<br>"
	if [ $status != 0 -o $size -lt 10000 ]; then
		rm $root.eps
		[ $status != 0 ] && echo "ncl returned status $status. "
		[ $size -lt 10000 ] && echo "postscript file too small, $size bytes. "
		echo "<p>$0: something went wrong in the script:<p>"
		cat /tmp/nclinput$$.ncl | sed -e 's/$/<br>/'
		exit -1
	fi
	./bin/epstopdf $root.eps
	gs -q -r180 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -sDEVICE=ppmraw -sOutputFile=$root.pnm $root.eps -c quit
	pnmcrop $root.pnm | pnmtopng > $root.png
	rm $root.pnm
fi
pngfile=$root.png
getpngwidth
cat <<EOF
<div class="bijschrift">$title (<a href="$root.eps">eps</a>, <a href="$root.pdf">pdf</a>, <a href="$plotfile">netcdf</a>)</div>
<center><img src="$root.png" alt="$title" width=$halfwidth><br clear=all></center>
EOF
