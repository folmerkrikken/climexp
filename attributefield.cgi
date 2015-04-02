#!/bin/sh

. ./myvinkhead.cgi "Trends in extremes" "$kindname $climfield" "noindex,nofollow"

if [ "$FORM_assume" != 'both' ]; then
    if [ "$FORM_fit" = "gpd" -a $NPERYEAR -gt 12 ]; then
        echo '<font color=#ff2222>The GPD(T) still has bugs for daily data. Please cross-check the results with other methods.</font><p>'
    else
        echo '<font color=#ff2222>I think it works now, please report problems.</font><p>'
    fi
else
    echo '<font color=#ff2222>Fitting position and scale independently is unfinished and untested. Use at own risk.</font><p>'
fi

startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
outfile=data/trends_${FORM_field}_$$.nc
corrargs="$corrargs $outfile"
echo `date` "$EMAIL ($REMOTE_ADDR) attributefield $corrargs" >> log/log
echo "Computing trend in extremes in each grid box.  This will take (quite) a while...<br>"
echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the job)</small><p>"
# generate GrADS data file
cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
attributefield $corrargs
@
EOF
export SCRIPTPID=$$
export FORM_EMAIL=$EMAIL

[ "$lwrite" = true ] && echo bin/attribute $corrargs
./bin/attributefield $corrargs 2>&1

if [ ! -s $outfile ]; then
    echo "Something went wrong"
    . ./myvinkfoot.cgi
    exit
fi
file=$outfile
FORM_var=alpha # trend
. ./grads.cgi

FORM_var=rt$FORM_end2
. ./grads.cgi

FORM_var=rt$FORM_begin2
. ./grads.cgi

FORM_var=ratio
. ./grads.cgi


echo "REST NOT YET READY"

. ./myvinkfoot.cgi
