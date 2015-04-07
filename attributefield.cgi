#!/bin/sh

. ./myvinkhead.cgi "Trends in extremes" "$kindname $climfield" "noindex,nofollow"

if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false # true
fi

if [ "$FORM_assume" != 'both' ]; then
    if [ "$FORM_fit" = "gpd" -a $NPERYEAR -gt 12 ]; then
        echo '<font color=#ff2222>The GPD(T) still has bugs for daily data. Please cross-check the results with other methods.</font><p>'
    else
        echo '<font color=#ff2222>I think it works now, please report problems.</font><p>'
    fi
else
    echo '<font color=#ff2222>Fitting position and scale independently is unfinished and untested. Use at own risk.</font><p>'
fi

[ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
[ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
[ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
[ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"

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

[ "$lwrite" = true ] && echo bin/attributefield $corrargs
./bin/attributefield $corrargs 2>&1

if [ ! -s $outfile ]; then
    echo "Something went wrong"
    . ./myvinkfoot.cgi
    exit
fi
file=$outfile
insideloop=true
FORM_var=alpha # trend
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

FORM_var=rt$FORM_year
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

FORM_var=rt$FORM_begin2
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

insideloop=
FORM_var=ratio
id=${root}_$FORM_var
. ./grads.cgi


echo "REST NOT YET READY"

. ./myvinkfoot.cgi
