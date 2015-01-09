#!/bin/sh
. ./init.cgi
export PATH=$PATH:/usr/local/bin
# compute anomalies of a field
echo "Content-type: text/html"
echo

export DIR=`pwd`
. ./getargs.cgi
. ./queryfield.cgi
. ./myvinkhead.cgi "Anomalies" "$kindname $climfield" "nofollow,index"

if [ "$EMAIL" != someone@somewhere ]; then
    prefs=prefs/$EMAIL.anomalies
    cat > $prefs <<EOF
FORM_climyear1=$FORM_climyear1;
FORM_climyear2=$FORM_climyear2;
EOF
fi    

infile=$file
file=${infile%.nc}
file=${file%.ctl}_${FORM_climyear1}_${FORM_climyear2}_anom.nc
file=data/`basename $file`

if [ ${infile%.ctl} != "$infile" ]; then
    ncfile=/tmp/`basename $infile .ctl`.nc
    bin/grads2nc $infile $ncfile
    infile=$ncfile
fi

iens=0
echo "$EMAIL ($REMOTE_ADDR) cdo fieldanomalies $infile $file" >> log/log
if [ -z "$ENSEMBLE" ]; then
    if [ -s $file -a $file -nt $infile ]; then
        echo "Using cached data<p>"
    else
        echo "Computing anomalies using <a href="https://code.zmaw.de/projects/cdo">cdo</a> ...<p>"
        climfile=${file%_anom.nc}_clim.nc
        tmpfile=${file%_anom.nc}_tmp.nc
        cdo seldate,${FORM_climyear1}-01-01,${FORM_climyear2}-12-31 $infile $tmpfile
        cdo ymonavg $tmpfile $climfile
        cdo ymonsub $infile $climfile $file
        rm $tmpfile $climfile
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
            echo "not yet ready $ensinfile $ensfile"
            climfile=${file%_anom.nc}_clim.nc
            tmpfile=${file%_anom.nc}_tmp.nc
            cdo seldate,${FORM_climyear1}-01-01,${FORM_climyear2}-12-31 $ensinfile $tmpfile
            cdo ymonavg $tmpfile $climfile
            cdo ymonsub $ensinfile $climfile $ensfile
            rm $tmpfile $climfile
            if [ ! -s $ensfile ]; then
                echo "Something went wrong in the anomaly routine."
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
kindname="${FORM_climyear1}-${FORM_climyear2} anomalies $kindname"
FORM_field=data/`basename $file .nc`.info
cat > $FORM_field <<EOF
$file
NPERYEAR=$NPERYEAR
UNITS=$UNITS
$kindname
$climfield
EOF

. ./select.cgi
