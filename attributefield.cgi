#!/bin/sh

. ./myvinkhead.cgi "Trends in extremes" "$kindname $climfield" "noindex,nofollow"

if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=true
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
outfile=data/trends_`basename ${FORM_field} .info`_$$.nc
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
root=attributefield`date "+%Y%m%d_%H%M"`_${$}

# plot trend parameter
FORM_var=alpha
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

# plot return time in the current climate
FORM_var=rt$FORM_year
if [ -n "$FORM_cmin" ]; then
    cmin_was_set="$FORM_cmin"
    FORM_cmin=""
fi
if [ -n "$FORM_cmax" ]; then
    cmax_was_set="$FORM_cmax"
    FORM_cmax=""
fi
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

# plot return time in a previous climate
FORM_var=rt$FORM_begin2
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and onger

[ -n "$cmin_was_set ] && FORM_cmin="$cmin_was_set"
[ -n "$cmax_was_set ] && FORM_cmax="$cmax_was_set"

# plot ratio of return times.
# note that this variable includes ±1e20 for "infinite" which should be plotted as defined
# but try not to let this set the scale of the colourbar
FORM_var=ratio
if [ -z "$FORM_cmin" ]; then
    cmin_was_nil=true
    FORM_cmin="-100"
fi
if [ -z "$FORM_cmax" ]; then
    cmax_was_nil=true
    FORM_cmax="100"
fi
id=${root}_$FORM_var
. ./grads.cgi
dano="" # otherwise it just gets longer and longer

[ -n "$cmin_was_nil" ] && FORM_cmin=""
[ -n "$cmax_was_nil" ] && FORM_cmax=""

# and finally plot the FAR due to the trend
insideloop=
FORM_var="1-1/ratio"
if [ -z "$FORM_cmin" ]; then
    cmin_was_nil=true
    FORM_cmin="0"
fi
if [ -z "$FORM_cmax" ]; then
    cmax_was_nil=true
    FORM_cmax="1"
fi
id=${root}_far
. ./grads.cgi
dano="" # otherwise it just gets longer and onger


cat <<EOF
Download the <a href="$outfile">netcdf file</a> with all results.
EOF

. ./myvinkfoot.cgi
