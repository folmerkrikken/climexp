#!/bin/bash
cat <<EOF
Content-Type: text/html



EOF

. ./init.cgi
. ./getargs.cgi
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
. ./save_averagefieldspace.cgi

. ./queryfield.cgi

. ./myvinkhead.cgi "Computing derived field" "$kindname $climfield" "noindex,nofollow"

# prevent abuse...
if [ "FORM_avex" = 1 -a "$FORM_avey" = "1" ]; then
   echo "The data is already at this spatial resolution.  Nothing to do, nothing done."
   . ./myvinkfoot.cgi
   exit
fi

kindname="${FORM_avex}x${FORM_avey} average of $kindname"
corrargs="$file $FORM_avex $FORM_avey"
outfile=data/`basename ${FORM_field}_${FORM_avex}_${FORM_avey}`
testfile=`echo "$outfile" | tr '%' '0'`
if [ ! -s $testfile.nc -o $testfile.nc -ot $file ]; then
    [ "$lwrite" = true ] && echo "averagefieldspace.sh $corrargs $outfile.nc"
    echo `date` "$EMAIL ($REMOTE_ADDR) averagefieldspace.sh $corrargs $outfile.nc" >> log/log
    (./bin/averagefieldspace.sh $corrargs $outfile.nc) 2>&1
fi
if [ -n "$LSMASK" ]; then
    maskfile=data/lsmask_`basename $outfile`
    corrargs="$LSMASK $FORM_avex $FORM_avey"
    if [ ! -s $maskfile.nc ]; then
        [ "$lwrite" = true ] && echo "averagefieldspace.sh $corrargs $maskfile.nc"
        (./bin/averagefieldspace $corrargs $maskfile.nc) 2>&1
    fi
    LSMASK=$maskfile.nc
fi

infofile=$outfile.$EMAIL.info
###echo "cat > $infofile <<EOF"
cat > $infofile <<EOF
$outfile.nc
NPERYEAR=$NPERYEAR
LSMASK=$LSMASK
$kindname
$climfield
EOF

# rest is standard
FORM_field=$infofile
. ./select.cgi
