#!/bin/sh
. ./init.cgi
export PATH=$PATH:/usr/local/bin
# average an ensemble of fields
echo "Content-type: text/html"
echo

export DIR=`pwd`
. ./getargs.cgi
. ./queryfield.cgi
. ./myvinkhead.cgi "Zonal mean" "$kindname $climfield" "nofollow,index"

infile=$file
file=${infile%.nc}
file=${file%.ctl}_zonalmean.nc
file=data/`basename $file`

if [ ${infile%.ctl} != "$infile" ]; then
    ncfile=/tmp/`basename $infile .ctl`.nc
    bin/grads2nc $infile $ncfile -q
    infile=$ncfile
fi
if [ -n "$FORM_lon1" -a "$FORM_lon1" != 0 -o -n "$FORM_lon2" -a "$FORM_lon2" != 360 ]; then
    echo "Sorry, cannot average over ${FORM_lon1}&deg;E to ${FORM_lon2}&deg; yet."
    . ./myvinkfoot.cgi
    exit
fi

iens=0
echo "$EMAIL ($REMOTE_ADDR) cdo zonmean $infile $file" >> log/log
if [ -z "$ENSEMBLE" ]; then
    if [ -s $file -a $file -nt $infile ]; then
	echo "Using cached data<p>"
    else
	echo "Computing zonal mean using <a href="https://code.zmaw.de/projects/cdo">cdo</a> ...<p>"
	cdo zonmean $infile $file
    fi
else
    iens=0
    ens=00
    ensinfile=`echo $infile | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
    ensfile=`echo $file | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
    echo "Computing zonal mean using <a href=\"https://code.zmaw.de/projects/cdo\" target=_new>cdo</a> ...<p>"
    while [ -s $ensinfile ]; do
	if [ -s $ensfile -a $ensfile -nt $ensinfile ]; then
	    echo "Using cached data<p>"
	else
	    echo "cdo zonmean $ensinfile $ensfile"
	    cdo zonmean $ensinfile $ensfile
	    if [ ! -s $ensfile ]; then
		echo "Something went wrong in the averaging routine."
		. ./myvinkfoot.cgi
		exit
	    fi
	fi
	iens=$((iens+1))
	if [ $iens -lt 10 ]; then
	    ens=0$iens
	else
	    ens=$iens
	fi
	ensinfile=`echo $infile | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
	ensfile=`echo $file | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
    done
fi

eval `bin/getunits.sh $file`
ENSEMBLE=""
kindname="zonal mean $kindname"
FORM_field=data/`basename $file .nc`.info
cat > $FORM_field <<EOF
$file
NPERYEAR=$NPERYEAR
UNITS=$UNITS
$kindname
$climfield
EOF

. ./select.cgi
