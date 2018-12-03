#!/bin/bash
. ./init.cgi
export PATH=$PATH:/usr/local/bin
# average an ensemble of fields
echo "Content-type: text/html"
echo

export DIR=`pwd`
. ./getargs.cgi
. ./queryfield.cgi
. ./myvinkhead.cgi "Annual cycle" "$kindname $climfield" "nofollow,index"

infile=$file
file=${infile%.nc}
file=${file%.ctl}_annualcycle.nc
file=data/`basename $file`

if [ ${infile%.ctl} != "$infile" ]; then
    ncfile=data/`basename $infile .ctl`.nc
    bin/grads2nc $infile $ncfile
    infile=$ncfile
fi

iens=0
echo "$EMAIL ($REMOTE_ADDR) cdo ydaymean $infile $file" >> log/log
if [ -z "$ENSEMBLE" ]; then
    if [ -s $file -a $file -nt $infile ]; then
        echo "Using cached data<p>"
    else
        echo "Computing annual cycle using <a href="https://code.zmaw.de/projects/cdo">cdo</a> ...<p>"
        cdo ydaymean $infile $file.$$
        mv $file.$$ $file
    fi
else
    iens=0
    ens=00
    ensinfile=`echo $infile | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
    ensfile=`echo $file | sed -e "s:\+\+:$ens:g" -e "s:\%\%:$ens:g"`
    echo "Computing annual cycle using <a href=\"https://code.zmaw.de/projects/cdo\" target=_new>cdo</a> ...<p>"
    while [ -s $ensinfile ]; do
        if [ -s $ensfile -a $ensfile -nt $ensinfile ]; then
            echo "Using cached data<p>"
        else
            echo "cdo ydaymean $ensinfile $ensfile"
            cdo ydaymean $ensinfile $ensfile.$$
            mv $ensfile.$$ $ensfile
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
kindname="annual cycle $kindname"
FORM_field=data/`basename $file .nc`.$EMAIL.info
cat > $FORM_field <<EOF
$file
NPERYEAR=$NPERYEAR
UNITS=$UNITS
$kindname
$climfield
EOF

. ./select.cgi
