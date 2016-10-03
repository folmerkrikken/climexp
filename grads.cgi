#!/bin/sh
. ./init.cgi
# to be sourced from various scripts.
if [ $EMAIL = oldenborgh@knmi.nl ]; then
	lwrite=false # true
	if [ "$lwrite" = true ]; then
		echo "Turned on debug printing<p>"
		###set -x
	fi
fi
hiresmap=true
if [ "$hiresmap" = true ]; then
	doublesize="x1804 y1394"
else
	doublesize="x902 y697"
fi
grads=$DIR/bin/grads
config=`$grads -b -l -c quit| fgrep Config`
c=`echo $config | fgrep -c v2.0`
[ -z "$FORM_mapformat" ] && FORM_mapformat=png
if [ $c -gt 0 ]; then
	grads20=true
	gradsver=2.0
else
	gradsver=1.8
	if [ "$FORM_mapformat" = geotiff ]; then
		echo "geotiff export is not supported by GrADS 1.8"
		exit
	fi
fi
# expects variables: ...
#
# to find netpbm on MacOS X
export PATH=/sw/bin:/usr/local/bin:$PATH
if [ -z "$alreadyprinted" ]
then
	echo "<p>Plotting with <a href=\"http://grads.iges.org/grads/\" target=_top>GrADS $gradsver</a>..."
fi

. ./save_plotoptions.cgi

# generate unique number if not already set
if [ -z "$id" ]; then
	id=`date "+%Y%m%d_%H%M"`_$$
fi
# check
if [ -z "$NZ" ]; then
	if [ "$lwrite" = true ]; then
		echo '<pre>'
		bin/getunits.sh $file
		echo '</pre>'
	fi
	NPERYEAROLD=$NPERYEAR
	eval `bin/getunits.sh $file | egrep -v 'error|warning|getfileunits'`
# changed 28-apr-2009 to make work again with verification plots, which have
# NPERYEAR=1 but refer to monthly data...
	if [ -n "$NPERYEAROLD" ]; then
		NPERYEAR=$NPERYEAROLD
	fi
fi
# check whether there is a variable "prob" in the file if masking out
if [ -n "$FORM_pmin" ]; then
	if [ ${FORM_pmin#-} = $FORM_pmin -a $FORM_pmin != 100 ]; then
		if [ `file $file | fgrep -i -c ascii` = 0 ]; then
			c=`ncdump -h $file | fgrep -c ' prob('`
		else
			c=`egrep -c '^prob' $file`
		fi
		if [ $c = 0 ]; then
			echo "No p-values found, ignoring request to mask out p<${FORM_pmin}%<br>"
			FORM_pmin="0"
		fi
	fi
fi
# watch colourbar variable - may be empty
if [ -n "$FORM_nocbar" -o "$FORM_mapformat" != png ]; then
	FORM_cbar="off"
else
	FORM_cbar="on"
fi
# for KML, make a latlon plot
if [ -n "$FORM_xlint" ]; then
	ylint=${FORM_xlint}:${FORM_ylint}
elif [ -n "$FORM_ylint" ]; then
	ylint=${FORM_ylint}
fi
if [ -n "$FORM_yflip" ]; then
	if [ -z $ylint ]; then
		ylint="yflip"
	else
		ylint="yflip":$ylint
	fi
fi
[ "$lwrite" = true ] && echo "FORM_yflip=$FORM_yflip<br>ylint=$ylint<br>"
# sum in GrADS?
var=$FORM_var
if [ -n "$FORM_plotsum" ]; then
	if [ "$FORM_plotsum" -gt 1 ]; then
		###sum="run sum ${FORM_var:-corr} $FORM_plotsum"
		FORM_var="ave(${FORM_var:-corr},t+0,t+$((FORM_plotsum-1)))"
		[ "$lwrite" = true ] && echo "FORM_var=$FORM_var<br>"
	fi
fi
# anomalies requested?
if [ -n "$FORM_plotanomaly" ]; then
	clim_file=${FORM_field}_clim$FORM_climyear1${FORM_climyear2}_${FORM_plotsum:-1}.ctl
	if [ ${clim_file#data} = $clim_file ]; then
		clim_file=data/$clim_file
	fi
	if [ ! -s $clim_file -o $clim_file -ot $file ]; then
		args="$file"
		[ -n "$FORM_climyear1" ] && args="$args begin $FORM_climyear1"
		[ -n "$FORM_climyear2" ] && args="$args end $FORM_climyear2"
		[ -n "$FORM_plotsum" ] && args="$args ave $FORM_plotsum"
		echo "<p>Computing climatology..."
		[ -f $clim_file ] && rm $clim_file
		bin/fieldclim $args $clim_file 2>&1
		if [ ! -s "$clim_file" ]; then
			echo "grads.cgi: error: failed to compute climatology<br>"
			echo "bin/fieldclim $args $clim_file"
			. ./myvinkfoot.cgi
			exit -1
		fi
		echo "<p><a href=grads2nc.cgi?file=$clim_file&id=$EMAIL>Climatology</a> is ready, calling Grads..."
    else
		echo "<p>Using <a href=grads2nc.cgi?file=$clim_file&id=$EMAIL>climatology</a>."
	fi
	clim="open $clim_file
run clim ${var:-corr} $NPERYEAR ${date:-$i} ${FORM_plotsum:-1} $FORM_climyear1 $FORM_climyear2"
	if [ -n "$FORM_climyear1" ]; then
	# this should be coordinated with clim.gs
		yy1=${FORM_climyear1#19}
		yy2=${FORM_climyear2#19}
		yy1=${yy1#20}
		yy2=${yy2#20}
	else
		yy1=""
		yy2=""
	fi
	climtime="${date%????}2000"
	if [ "$FORM_plotanomalykind" = "logrelative" ]; then
		FORM_var="log10(${FORM_var:-corr}/clim${yy1}${yy2}(time=$climtime))"
	elif [ "$FORM_plotanomalykind" = "relative" ]; then
		FORM_var="${FORM_var:-corr}/clim${yy1}${yy2}(time=$climtime)-1"
	else
		FORM_var="${FORM_var:-corr}-clim${yy1}${yy2}(time=$climtime)"
	fi
fi

# generate GrADS metadata file - should be doing this in perl...
firstmonth=`echo ${FORM_month:-1:12} | sed -e 's/\:.*//' | tr -d '\'`
lastmonth=`echo ${FORM_month:-1:12} | sed -e 's/.*\://' | tr -d '\'`
nperyear=${NPERYEAR#-}
if [ $lastmonth -gt $nperyear ]; then
	lastmonth=$nperyear
fi
firstlag=`echo ${FORM_lag:-0} | sed -e 's/\:.*//'`
lastlag=`echo ${FORM_lag:-0} | sed -e 's/.*\://'`
if [ -z "$FORM_plottype" -o "$FORM_plottype" = "lat-lon" ]; then
	mn=$((firstmonth-(lastlag)))
	nm=$((lastmonth-(firstlag)))
	l=$((nm-(mn)+1))
else
	l=1
fi
if [ "$lwrite" = true ]; then
	echo "<br>"
	echo "FORM_month,NPERYEAR=$FORM_month,$NPERYEAR<br>"
	echo "firstmonth=$firstmonth,lastmonth=$lastmonth<br>"
	echo "FORM_lag=$FORM_lag<br>"
	echo "firstlag=$firstlag,lastlag=$lastlag<br>"
	echo "mn=$mn, nm=$nm<br>"
	echo "l=$l<br>"
	echo "sumstring=$sumstring<br>"
fi

if [ $NPERYEAR = 1 ]; then
	month2string=./bin/annual2string
elif [ $NPERYEAR = 4 ]; then
	month2string=./bin/season2string
else
	month2string=./bin/month2string
fi

i=0
while [ $i -lt $l ]
do 
	i=$(($i+1))
	if [ "$firstmonth" = "$lastmonth" ]; then
		if [ "$FORM_fix" = "fix2" ]; then
			[ "$lwrite" = true ] && echo "$month2string "$firstmonth" "$sumstring" "$(($firstlag+$i-1))" "$FORM_operation" $FORM_fix"
			eval `$month2string "$firstmonth" "$sumstring" "$(($firstlag+$i-1))" "$FORM_operation" $FORM_fix`
		else
			[ "$lwrite" = true ] && echo "$month2string "$firstmonth" "$sumstring" "$(($lastlag-$i+1))" "$FORM_operation" $FORM_fix"
			eval `$month2string "$firstmonth" "$sumstring" "$(($lastlag-$i+1))" "$FORM_operation" $FORM_fix`
		fi
	else
		eval `$month2string "$((firstmonth+$i-1))" "$sumstring" "$FORM_lag" "$FORM_operation" $FORM_fix`
###	 echo $DIR/bin/month2string "$((firstmonth+$i-1))" "$sumstring" "$FORM_lag" "$FORM_operation" $FORM_fix
###	 $DIR/bin/month2string "$((firstmonth+$i-1))" "$sumstring" "$FORM_lag" "$FORM_operation" $FORM_fix
	fi
	if [ -n "$FORM_colourscale" ]; then
		flipcolor=$FORM_colourscale
	elif [ -n "$FORM_flipcolor" ]; then
		flipcolor=$FORM_flipcolor
	fi
	if [ -n "$FORM_cmin" -a -n "$FORM_cmax" ]; then
# bloody SGI bc does not accept leading +...
		echo ''
###	   FORM_cmax=`echo $FORM_cmax | tr '+' ' '`
###	   cint=`echo "($FORM_cmax-($FORM_cmin))/10" | bc -l`
###	   echo "cint = $cint"
	elif [ -n "$FORM_cmin" -o -n "$FORM_cmax" ]; then
		echo "Please specify both lower and upper bounds of contours</body></html>"
		exit
	fi
	
	if [ ${FORM_var:-corr} = mask ]; then
		###echo "maskname,FORM_maskname=$maskname,$FORM_maskname<br>"
		[ -z "$maskname" ] && maskname=$FORM_maskname
		FORM_var="mask ${maskname}"
		. ./title.cgi
		###FORM_var="maskout(mask,mask-0.01)" this gives a white plot as the calue is constant
		FORM_var="mask"
		FORM_shadingtype=grfill
		FORM_cbar=off
		FORM_cmin=-1
		FORM_cmax=1
	else
		. ./title.cgi
	fi
	[ "$lwrite" = true ] && echo "title=$title<br>
"
	echo "$title" | tr '\\' ' ' | sed -e 's/>/\&gt;/g' -e 's/</\&lt;/g' > /tmp/grads_title_$$_$i.txt
    if [ ${FORM_var#bo_} != ${FORM_var} ]; then
        echo "Negative values denote positive return times of negative extremes" >> /tmp/grads_title_$$_$i.txt
    fi
	if [ -n "$FORM_notitleonplot" ]; then
		drawtitle=""
	else
		drawtitle="draw title $title"
	fi
	if [ -n "$FORM_nogrid" ]; then
		grid="set grid off"
	else
		grid="set grid on"
	fi
	if [ -n "$FORM_nolab" ]; then
		grid="$grid
set xlab off
set ylab off"
	fi
    . ./setmap.cgi
	if [ -n "$FORM_nopoli" ]; then
		grid="$grid
set poli off"
	fi
	
	if [ "$FORM_movie" = "yes" ]; then
		
		dano="$dano
enable print data/g${id}_$i.gm
run danoloop ${FORM_var:-corr} $i$date $i2$date2 $FORM_shadingtype $flipcolor $FORM_cbar $FORM_cmin $FORM_cmax $cint
disable print
printim data/g${id}_$i.png white $doublesize"

	else
		if [ -n "$date2" ]; then
			date="${date}:$i${date2}"
			parea="set parea 1.5 10.5 1 7.5"
		fi
		if [ "$FORM_plottype" = "time-lat" -o "$FORM_plottype" = "time-lon" ]; then
			date="year "
			parea="set parea 1.5 10.5 1 7.5"
		fi
		c=`echo "$drawtitle" | tr '\\\\' '\\n' | wc -l`
		if [ "$c" -gt 2 -a -z "$parea" ]; then
			parea="set parea 1 9.5 1 7.5"
		fi
		if [ "$XWRAP" = true ]; then
			setlon="set lon -180 180"
		fi
		if [ ${NZ:-0} -gt 1 ]; then
			setlev="set z 1 $NZ"
		fi
		if [ -z "$FORM_maskout" -o "$FORM_maskout" = mask ]; then
			pminarg=${FORM_pmin:-100}
		else
			pminarg=${FORM_pmin:-100}:$FORM_maskout
		fi
		if [ "$FORM_mapformat" = png ]; then
			dano="$dano
run danoprob ${FORM_var:-corr} ${date:-$i} ${FORM_shadingtype:-shadedcontour} ${flipcolor:-0} ${FORM_cbar:-1} ${ylint:-0} $pminarg $FORM_cmin $FORM_cmax
$drawtitle"
			if [ -z "$grads20" ]; then
				dano="$dano
enable print data/g${id}_$i.gm
print
disable print
printim data/g${id}_$i.png white $doublesize
clear"
			else
				dano="$dano
print data/g${id}_$i.eps
printim data/g${id}_$i.png white $doublesize
clear"
			fi
		elif [ "$FORM_mapformat" = kml ]; then
			setlat="set lat -90 90"
			dano="set xlab off
set ylab off
set grid off
set mpdraw off
$dano
run danoprob ${FORM_var:-corr} ${date:-$i} ${FORM_shadingtype:-shadedcontour} ${flipcolor:-0} off ${ylint:-0} $pminarg $FORM_cmin $FORM_cmax
printim data/g${id}_${i}_tmp.png white x1584 y1020
cbarn
printim data/g${id}_${i}_tmp2.png white x1584 y1020
clear"
		else
			dano="set xlab off
set ylab off
set grid off
$dano
run danoprob ${FORM_var:-corr} ${date:-$i} geotiff:data/g${id}_$i ${flipcolor:-0} off ${ylint:-0} $pminarg $FORM_cmin $FORM_cmax
clear"
		fi
	fi
done

# do not allow shell escapes
forbidden='!`'
sum=`echo "$sum"   | tr $forbidden '?'`
clim=`echo "$clim" | tr $forbidden '?'`
map=`echo "$map"   | tr $forbidden '?'`
dano=`echo "$dano" | tr $forbidden '?'`
# run grads
cd $DIR
if [ `file $file | fgrep -i -c ascii` = 0 ]; then
	openfile="sdfopen $file"
else
	datfile=`dirname $file`/`head -1 $file | sed -e 's/^[^^]*\^//'`
	if [ ! -s $datfile ]; then
		[ "$lwrite" = true ] && echo "<br>$datfile does not exist"
		if [ -s $datfile.gz ]; then
			[ "$lwrite" = true ] && echo "<br>but $datfile.gz does"
			newdatfile=data/`basename $datfile`
			if [ ! -s $newdatfile -o $newdatfile -ot $datfile.gz ]; then
				[ "$lwrite" = true ] && echo "<br>gunzipping $datfile.gz to $newdatfile"
				gunzip -c $datfile.gz > $newdatfile
			fi
			newfile=data/`basename $file`
			if [ ! -s $newfile -o $newfile -ot $file ]; then
				[ "$lwrite" = true ] && echo "<br>copying $file to $newfile"
				cp $file data/
			fi
			file=$newfile
		else
			echo 'Cannot locate data file'
			. ./myvinkfoot.cgi
			exit
		fi
	fi
	if [ "${datfile%nc}" != "$datfile" ]; then
		openfile="xdfopen $file"
	else
		openfile="open $file"
	fi
fi
export GADDIR=$DIR/grads
export UDUNITS_PATH=$DIR/grads/udunits.dat
export HOME=/tmp
cat <<EOF > /tmp/grads$id.log
$openfile
set xlopts 1 4 0.15
set ylopts 1 4 0.15
$setlon
$setlat
$setlev
$parea
$map
$grid
$sum
$clim
$dano
quit
EOF
$grads -l -b << EOF >> /tmp/grads$id.log
$openfile
set xlopts 1 4 0.15
set ylopts 1 4 0.15
$setlon
$setlat
$setlev
$parea
$map
$grid
$sum
$clim
$dano
quit
EOF

if [ "$FORM_mapformat" = kml ]; then
	alreadyprinted=
	if [ -n "$map" ]; then
		mapfile=/tmp/map$$.txt
		echo "$map" > $mapfile
	fi
	eval `./bin/coordinates2kml ${FORM_lon1:-@} ${FORM_lon2:-@} ${FORM_lat1:-@} ${FORM_lat2:-@} $mapfile`
###	 echo "lwrap = $lwrap" 1>&2
	[ -n "$mapfile" ] && rm $mapfile
	# service to myself andf other customers
	if [ "$lwrap" = TRUE -a -z "$FORM_lon1" ]; then
		if [ ${EMAIL%nl} != $EMAIL ]; then
			lookat_lon=5
			lookat_lat=52
		elif [ ${EMAIL%uk} != $EMAIL ]; then
			lookat_lon=0
			lookat_lat=51.5
		elif [ ${EMAIL%int} != $EMAIL ]; then
			lookat_lon=-1
			lookat_lat=51.5
		elif [ ${EMAIL%de} != $EMAIL ]; then
			lookat_lon=10
			lookat_lat=50
		elif [ ${EMAIL%ch} != $EMAIL ]; then
			lookat_lon=8
			lookat_lat=47
		elif [ ${EMAIL%fr} != $EMAIL ]; then
			lookat_lon=2.4
			lookat_lat=48.75
		elif [ ${EMAIL%au} != $EMAIL ]; then
			lookat_lon=135
			lookat_lat=-25
		elif [ ${EMAIL%edu} != $EMAIL -o ${EMAIL%gov} != $EMAIL -o ${EMAIL%mil} != $EMAIL ]; then
			lookat_lon=260
			lookat_lat=40
		fi
	fi
	i=0
	[ "$lwrite" = true ] && echo "l=$l<br>"
	while [ $i -lt $l ]
	do
		i=$(($i+1))
		f=data/g${id}_$i
		if [ ! -s data/g${id}_${i}_tmp.png ]; then
			[ -f data/g${id}_${i}_tmp.png ] && rm data/g${id}_${i}_tmp.png
			echo "<html><body><pre>"
			echo "Something went wrong!"
			echo
			echo "$dano"
			echo
			cat /tmp/grads$id.log
			echo "</pre>"
			. ./myvinkfoot.cgi
		fi
		if [ "$lwrite" = true ]; then
			echo '<pre>'
			cat /tmp/grads$id.log
			echo '</pre>'
		fi
		rm /tmp/grads$id.log
		if [ -z "$alreadyprinted" ]; then
			alreadyprinted=true
			echo "<p>Converting to KML file for <a href=\"http://earth.google.com\" target=_new>Google Earth</a>, <a href=\"http://worldwind.arc.nasa.gov/\" target=_new>World Wind</a>, <a href=\"http://www.esri.com/software/arcgis/explorer/\" target=_new>ArcGIS explorer</a> or another visualisation application....<p>"
		fi
		if [ "$lwrap" = TRUE ]; then
			# left and right remove the whole frame if the whole earth is covered
			(pngtopnm data/g${id}_${i}_tmp.png | pnmcrop | pnmcut -left 2 -right -3 -top 1 -bottom -2 > /tmp/g${id}_${i}_m.pnm) 2> /dev/null
			pnmcut -right 0 /tmp/g${id}_${i}_m.pnm > /tmp/g${id}_${i}_l.pnm
			pnmcut -left -1 /tmp/g${id}_${i}_m.pnm > /tmp/g${id}_${i}_r.pnm
			pnmcat -leftright /tmp/g${id}_${i}_l.pnm /tmp/g${id}_${i}_m.pnm /tmp/g${id}_${i}_r.pnm | pnmtopng > data/g${id}_${i}_kml.png
		else
			# remove the white around the figure, and half the frame on top and bottom
			(pngtopnm data/g${id}_${i}_tmp.png | pnmcrop | pnmcut -left 1 -right -2 -top 1 -bottom -2 | pnmtopng > data/g${id}_${i}_kml.png) 2> /dev/null
		fi
		# extract colour bar - if someone knows a better way I'd love to hear it
		pnmfile=/tmp/g${id}_${i}_tmp.pnm
		cbfile=data/cb${id}_${i}_kml.png
		pngtopnm data/g${id}_${i}_tmp2.png | pnmcrop > $pnmfile
		string=`pamfile $pnmfile`
		hsize2=`echo $string | sed -e 's/^[^,]*, //' -e 's/ by.*$//'`
		vsize2=`echo $string | sed -e 's/^.*by //' -e 's/ maxval.*$//'`
		string=`file data/g${id}_${i}_kml.png`
		hsize1=`echo $string | sed -e 's/^[^,]*, //' -e 's/ x .*$//'`
		vsize1=`echo $string | sed -e 's/^.* x //' -e 's/,.*$//'`
		if [ $hsize2 = $(($hsize1 + 2)) ]; then
		# horizontal colour bar
			pnmcut -top $(($vsize1 + 2)) $pnmfile | pnmcrop | pnmpad -white -l10 -r10 -t10 -b10 | pnmtopng > $cbfile
			x1=0.5
			y1=0
			x2=0.5
			y2=0.025
			xsize=0.7
			ysize=0.05
		elif [ $vsize2 = $(($vsize1 + 2)) ]; then
			# vertical colour bar
			pnmcut -left $(($hsize1 + 2)) $pnmfile | pnmcrop | pnmpad -white -l10 -r10 -t10 -b10 | pnmtopng > $cbfile
			x1=0
			y1=0.5
			x2=0
			y2=0.5
			xsize=0.07
			ysize=0.6
		else
			echo "Error locating colour bar<br>"
			echo "size1 = $hsize1 x $vsize1<br>"
			echo "size2 = $hsize2 x $vsize2<br>"
			cbfile=""
		fi
		rm data/g${id}_${i}_tmp.png data/g${id}_${i}_tmp2.png $pnmfile
		kmlfile=data/g${id}_$i.kml
		kmlbase=$SERVER_NAME
		[ $SERVER_NAME = zuidzee.knmi.nl -o $SERVER_NAME = bhw080.knmi.nl ] && kmlbase="$kmlbase/~oldenbor/climexp"
		kmltitle=`echo "$title" | tr '\\\\' ' '`
		cat > $kmlfile <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Folder>
<description>$kmltitle</description>
<name>Climate Explorer map</name>
<LookAt>
  <longitude>$lookat_lon</longitude>
  <latitude>$lookat_lat</latitude>
  <range>$lookat_range</range>
</LookAt>
<GroundOverlay>
  <name>Climate Explorer map</name>
  <color>B0ffffff</color>
  <Icon>
	<href>g${id}_${i}_kml.png</href>
  </Icon>
  <LatLonBox>
	<north>$latlonbox_north</north>
	<south>$latlonbox_south</south>
	<east>$latlonbox_east</east>
	<west>$latlonbox_west</west>
	<rotation>0</rotation>
  </LatLonBox>
</GroundOverlay>
<ScreenOverlay>
  <name>Climate Explorer Colour bar</name>
  <Icon>
	<href>cb${id}_${i}_kml.png</href>
  </Icon>
  <overlayXY x="$x1" y="$y1" xunits="fraction" yunits="fraction"/>
  <screenXY x="$x2" y="$y2" xunits="fraction" yunits="fraction"/>
  <size x="$xsize" y="$ysize" xunits="fraction" yunits="fraction"/>
</ScreenOverlay>
</Folder>
</kml>
EOF
		( cd data; zip g${id}_$i.kmz g${id}_$i.kml g${id}_${i}_kml.png cb${id}_${i}_kml.png; rm g${id}_$i.kml g${id}_${i}_kml.png cb${id}_${i}_kml.png ) > /dev/null
		echo "<p>"
		echo "<a href=\"$f.kmz\">KML file</a> of "
		cat /tmp/grads_title_$$_$i.txt
		rm /tmp/grads_title_$$_$i.txt
	done

elif [ "$FORM_mapformat" = png ]; then
	# convert to EPS, scale PNG
	if [ -z "$alreadyprinted" ]
	then
		alreadyprinted="gedaan"
		if [ "$FORM_movie" != "yes" -a -z "$grads20" ]; then
			echo "Converting to postscript with <a href=\"http://www.bol.ucla.edu/~munnich/grads/gxeps.html\" target=_top>gxeps</a>...<p>"
		fi
	fi
	i=0
	[ "$lwrite" = true ] && echo "l=$l<br>"
	while [ $i -lt $l ]
	do
		i=$(($i+1))
		f=data/g${id}_$i
		if [ -z "$grads20" ]; then
			size=`wc -c $f.gm | sed -e 's/data.*//'`
		else
			size=`wc -c $f.eps | sed -e 's/data.*//'`
		fi
		if [ "$size" -lt 50 ];then
			echo "Something went wrong!"
			echo "<pre>"
			cat /tmp/grads$id.log
			rm /tmp/grads$id.log
			echo "</pre>"
		else
			if [ -f /tmp/grads$id.log ]; then
				if [ "$lwrite" = true ]; then
					echo '<pre>'
					echo "$dano"
					cat /tmp/grads$id.log
					echo '</pre>'
				fi
				rm /tmp/grads$id.log
			fi
		fi
		if [ "$FORM_movie" != "yes" ]; then
			if [ -s $f.png ]; then
				(pngtopnm $f.png | pnmscale 0.5 | pnmcrop | pnmtopng > $f.new.png) 2> /dev/null
				mv $f.new.png $f.png
			else
				[ -f $f.png ] && rm $f.png
			fi
			if [ -z "$grads20" ]; then
				$DIR/bin/gxeps -c -d -i $f.gm
				/bin/rm $f.gm
			fi
			gzip -f $f.eps &
			echo "<div class=\"bijschrift\">"
			cat /tmp/grads_title_$$_$i.txt
			rm /tmp/grads_title_$$_$i.txt
			echo "(<a href=\"$f.eps.gz\">eps</a>,"
			echo "<a href=\"ps2pdf.cgi?file=$f.eps.gz\">pdf</a>)</div>"
			if [ -s $f.png ]; then
				if [ "$hiresmap" = true ]; then
					pngfile=$f.png
					getpngwidth
					echo "<center><img src=\"$f.png\" alt=\"$title\" width=$halfwidth><br clear=all></center>"
				else
					echo "<center><img src=\"$f.png\" alt=\"$title\"><br clear=all></center>"
				fi
			fi
			if [ -x bin/fieldsignificance ]; then
				x=${FORM_var%[0-9][0-9][0-9][0-9]}
				if [ ${x%_rt_} != $x ]; then
				    if [ ${x#bo_} != $x ]; then
				        pmin=all_lo
				    else
    					pmin=all
    				fi
				else
					pmin=${FORM_pmin:-10}
				fi
				if [ "$lwrite" = true ]; then
					echo "FORM_var=$FORM_var<br>"
					echo "x=$x<br>"
					echo "pmin=$pmin<br>"
					echo "./bin/fieldsignificance $file $i $pmin lon1 ${FORM_lon1:--180} lon2 ${FORM_lon2:-180} lat1 ${FORM_lat1:--90} lat2 ${FORM_lat2:-90} > /tmp/fieldsignificance.log"
				fi
				[ $pmin = 'all_lo' ] && echo '<b>Low extremes:</b><br>'
				( ./bin/fieldsignificance $file $i $pmin lon1 ${FORM_lon1:--180} lon2 ${FORM_lon2:-180} lat1 ${FORM_lat1:--90} lat2 ${FORM_lat2:-90} > /tmp/fieldsignificance.log ) 2>&1 | fgrep -v error 
                if [ $pmin = 'all_lo' ]; then
				    echo '<b>High extremes:</b><br>'
                    pmin=all_hi
    				( ./bin/fieldsignificance $file $i $pmin lon1 ${FORM_lon1:--180} lon2 ${FORM_lon2:-180} lat1 ${FORM_lat1:--90} lat2 ${FORM_lat2:-90} > /tmp/fieldsignificance.log ) 2>&1 | fgrep -v error 
    			fi
			fi
		else
			cat <<EOF > data/movie$$.html
<html>
<head>
<title>KNMI Climate Explorer: Movie of ${FORM_var:-corr}</title>
</head>
<body bcolor="#ffffff">
<h2>Movie of ${FORM_var:-corr}</h2>
<img src="../$f.gif">
<a href="../$f.ps.gz">postscript</a>
</body>
</html>
EOF
			echo "<p>The animated gifs are made via a tortuous route.  If the web server gives up before it is finished the script will continue, and you can view the movie <a href=\"data/movie$$.html\">here</a> after a while.	Please let me know if you know of a quicker way."
			echo "<p>Converting to postscript with <a href="http://www.iges.org/grads/gadoc/gradutilgxps.html" target="_top">gxps</a>...<p>"
			$DIR/bin/gxps -c -i $f.gm -o $f.ps
			rm $f.gm
			echo "<p>Converting to png with <a href="http://www.cs.wisc.edu/~ghost/" target="_top">ghostscript</a>...<p>"
			gs -q -r100 -dNOPAUSE -sDEVICE=png256 -sOutputFile=${f}%04d.png $f.ps -c quit
			gzip -f $f.ps &
			echo "<p>Converting to gif with <a href="http://netpbm.sourceforge.net/" target="_top">netpbm</a>...<p>"
			for pngfile in ${f}*.png; do
				echo .
				pngtopnm $pngfile | pnmscale 0.5 | pnmrotate -90 | (ppmtogif > data/`basename $pngfile .png`.gif) 2> /dev/null
				rm $pngfile
			done
			echo "<p>Converting to animated gif with <a href="http://www.danbbs.dk/~dino/whirlgif/" target="_top">whirlgif</a>...<p>"
			$DIR/bin/whirlgif  -loop 0 -time 100 -minimize ${f}?*.gif > $f.gif
			rm ${f}????.gif
			echo "<p><img src=\"$f.gif\">"
			echo "<a href=\"$f.ps.gz\">postscript</a> ("
			ls -l $f.ps.gz | awk '{print $5/1048576}'
			echo "MB)"
			echo "<p><a href=\"data/movie$$.html\">view again</a>"
		fi
		if [ -n "$extra1" ]
		then
			echo $extra1$(($firstmonth+$i-1))$extra2
		fi
		if [ -n "$extra3" ]
		then
			echo $extra3$(($firstmonth+$i-1))$extra4
		fi
	done
	if [ -z "$insideloop" -a \( -z "$date" -o "$date" = "year " \) ];then
		
		if [ -n "$datafile" ]; then
#
# let the user download the raw data
#
			if [ -s $datafile.dat ]; then
				datfile=$datafile.dat
				gzip $datfile &
			elif [ -s $datafile.grd ]; then
				datfile=$datafile.grd
				gzip $datfile &
			elif [ -s $datafile.nc ]; then
				datfile=$datafile.nc
			fi
			dat=`date`
			nexttitle=`echo "$title" | tr '\\\\ \n' '_'`
			
			if [ $datfile = $datafile.nc ]; then
				cat <<EOF
<p>
Get the raw data as <a href="$datafile.nc">netcdf</a> file.
EOF
			else
				cat <<EOF
<p>
Get the raw data as GrADS <a href="$datafile.ctl">control</a>
and (gzipped) <a href="$datfile.gz">data</a> files,
or generate a <a href="grads2nc.cgi?file=$datafile.ctl&id=$EMAIL&title=$nexttitle">netCDF</a> file,
or download as <a href="grads2ascii.cgi?file=$datafile.ctl&id=$EMAIL&title=$nexttitle">ascii</a> (big).
EOF
			fi
		fi
#
# replot option
#
		cat <<EOF
<form action="replot.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="pagetitle" value="$pagetitle">
<input type="hidden" name="file" value="$file">
<input type="hidden" name="datafile" value="$datafile">
<input type="hidden" name="map" value="$map">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="month" value="$FORM_month">
<input type="hidden" name="lag" value="$FORM_lag">
<input type="hidden" name="sum" value="$FORM_sum">
<input type="hidden" name="sum2" value="$FORM_sum2">
<input type="hidden" name="fix" value="$FORM_fix">
<input type="hidden" name="operation" value="$FORM_operation">
<input type="hidden" name="sumstring" value="$sumstring">
<input type="hidden" name="log" value="$FORM_log">
<input type="hidden" name="sqrt" value="$FORM_sqrt">
<input type="hidden" name="ndiff" value="$FORM_ndiff">
<input type="hidden" name="diff" value="$FORM_diff">
<input type="hidden" name="subsum" value="$FORM_subsum">
<input type="hidden" name="detrend" value="$FORM_detrend">
<input type="hidden" name="yrstart" value="$yrstart">
<input type="hidden" name="yrstop" value="$yrstop">
<input type="hidden" name="end" value="$FORM_end">
<input type="hidden" name="begin" value="$FORM_begin">
<input type="hidden" name="end2" value="$FORM_end2">
<input type="hidden" name="begin2" value="$FORM_begin2">
<input type="hidden" name="dlt" value="$FORM_dlt">
<input type="hidden" name="dgt" value="$FORM_dgt">
<input type="hidden" name="lt" value="$FORM_lt">
<input type="hidden" name="gt" value="$FORM_gt">
<input type="hidden" name="ensanom" value="$FORM_ensanom">
<input type="hidden" name="STATION" value="$FORM_STATION">
<input type="hidden" name="station" value="$station">
<input type="hidden" name="maskname" value="$maskname">
<input type="hidden" name="kindname" value="$kindname">
<input type="hidden" name="climfield" value="$climfield">
<input type="hidden" name="RANK" value="$RANK">
<input type="hidden" name="CLIM" value="$CLIM">
<input type="hidden" name="field1" value="$field1">
<input type="hidden" name="kindname1" value="$kindname1">
<input type="hidden" name="climfield1" value="$climfield1">
<input type="hidden" name="field2" value="$field2">
<input type="hidden" name="kindname2" value="$kindname2">
<input type="hidden" name="climfield2" value="$climfield2">
<input type="hidden" name="ENSEMBLE" value="$ENSEMBLE">
<p>
<div class="formheader">Replot</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr valign="baseline">
<td>Variable:<td>
EOF
		if [ $FORM_var = "maskout(mask,mask-0.01)" ]; then
			FORM_var=mask
		fi
		if [ `file $file | fgrep -i -c ascii` = 0 ]; then
			if [ -x bin/nc2varlist ]; then
				# better way
				[ "$lwrite" = true ] && echo "bin/nc2varlist $file"
				bin/nc2varlist $file \
					| sed -e 's/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\([^>]*\)>\(.*\)$/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\1 checked>\2/'
			else
				# there must be a better way, including units, but for the time being...
				ncdump -h $file \
					| fgrep ':long_name = ' | egrep -v '[:space:]*(time|lon|lat|level):' \
					| sed -e 's/^[^a-zA-Z]*\([^:]*\):long_name = "*\(.*\)".*$/<input type="radio" class="formradio" name="var" value="\1">\2<br>/' \
					| sed -e 's/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\([^>]*\)>\(.*\)$/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\1 checked>\2/'
			fi
		else
			# do not try this at home!
				sed -e '1,/VARS/d' -e '/ENDVARS/d' -e 's/^.*=>//' -e 's/^\([^ ]*\)  *[-0-9][0-9]*  *[-0-9][0-9]*  *\(.*\)$/<input type="radio" class="formradio" name="var" value="\1">\2<br>/' $file \
					| sed -e 's/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\([^>]*\)>\(.*\)$/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\1 checked>\2/'
fi

		intable=true
		if [ -n "$FORM_pmin" ]; then
			probmask=true
		fi
		replot="yes"
		. $DIR/plotoptions.cgi
		
		cat <<EOF
<tr><td colspan="2">
<input type="submit" class="formbutton" value="Replot">
</table>
</div>
</form>
EOF
	fi
	if [ -n "$subtractform" ]; then
		cat << EOF
<form action="subtractfield.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<input type="hidden" name="station" value="$station">
<input type="hidden" name="corrargs" value="$corrargs">
<p><div class="formheader">
Generate a new field with the influence of $station subtracted linearly
</div><div class="formbody">
<input type="submit" class="formbutton" value="Submit">
</div>
</form>
EOF
	fi
elif [ "$FORM_mapformat" = geotiff ]; then
	i=0
	[ "$lwrite" = true ] && echo "l=$l<br>"
	while [ $i -lt $l ]
	do
		i=$(($i+1))
		f=data/g${id}_$i
		size=`wc -c $f.tif | sed -e 's/data.*//'`
		if [ "$size" -lt 50 ];then
			echo "Something went wrong!"
			echo "<pre>"
			cat /tmp/grads$id.log
			rm /tmp/grads$id.log
			echo "</pre>"
		else
			if [ -f /tmp/grads$id.log ]; then
				if [ "$lwrite" = true ]; then
					echo '<pre>'
					echo "$dano"
					cat /tmp/grads$id.log
					echo '</pre>'
				fi
				rm /tmp/grads$id.log
			fi
		fi
		echo "<p>"
		echo "<a href=\"$f.tif\">GeoTIFF</a> of"
		cat /tmp/grads_title_$$_$i.txt
		rm /tmp/grads_title_$$_$i.txt
		if [ -n "$extra1" ]
		then
			echo $extra1$(($firstmonth+$i-1))$extra2
		fi
		if [ -n "$extra3" ]
		then
			echo $extra3$(($firstmonth+$i-1))$extra4
		fi
	done
else
	echo "error: unknown mapformat $FORM_mapformat"
	. ./myvinkfoot.cgi
fi # mapformat
