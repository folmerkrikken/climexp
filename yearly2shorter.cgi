#!/bin/sh
# make a time series with a shorter time scale than the original

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

if [ -z "$FORM_field" ]; then
    # time series
    STATION=$FORM_STATION
    WMO=$FORM_WMO
    TYPE=$FORM_TYPE
    NAME=$FORM_NAME
    NPERYEAR="$FORM_NPERNEW"

    corrargs="$DIR/data/$TYPE$WMO.dat $NPERYEAR mon $FORM_mon $FORM_oper $FORM_sum"
    WMO=${WMO}_$FORM_oper$NPERYEAR

    PROG="yearly2shorter $corrargs"

    . ./getdata.cgi

else
    # field
    echo "Content-Type: text/html"
    echo
    # check email address
    . ./checkemail.cgi
    if [ "$EMAIL" = "someone@somewhere" ]; then
      echo "Anonymous users cannot use this function as it stores new data on the server. Please <a href=\"registerform.cgi\">register or log in</a>"
      . ./myvinkfoot.cgi
      exit
    fi
    if [ $EMAIL = oldenborgh@knmi.nl ]; then
        lwrite=false # true
    fi

    . ./queryfield.cgi
    NAME="$climfield"

    . ./myvinkhead.cgi "Computing derived field" "$kindname $climfield" "noindex,nofollow"
    if [ "$NPERYEAR" = "$FORM_nperyearnew" ]; then
        echo "The data is already at this time resolution.  Nothing to do, nothing done."
        . ./myvinkfoot.cgi
        exit
    fi
    field=${FORM_field%.${id}.info}
    outfile=data/`basename ${field}_${FORM_NPERNEW}_${FORM_mon}_${FORM_oper}`
    corrargs="$file $FORM_NPERNEW mon $FORM_mon $FORM_oper $FORM_sum"
    PROG="./bin/yearly2shorterfield $corrargs"
    [ "$lwrite" = true ] && echo "$PROG $outfile.nc"
    echo `date` "$EMAIL ($REMOTE_ADDR) $PROG $outfile.nc" >> log/log
    ($PROG $outfile.nc) 2>&1

    infofile=$outfile.$EMAIL.info
###echo "cat > $infofile <<EOF"
    cat > $infofile <<EOF
$outfile.nc
NPERYEAR=$FORM_nperyearnew
LSMASK=$LSMASK
$kindname
$NAME
EOF

    FORM_field=$infofile
    . ./select.cgi

fi