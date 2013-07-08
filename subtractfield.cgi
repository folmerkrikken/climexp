#!/bin/sh
# subtract the influence of an index on a field, returning the new field
# Geert Jan van Oldenborgh, KNMI, 29-dec-2004
lwrite=false

echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
###echo '<pre>'
###set | fgrep FORM_
###echo '</pre>'
###exit
. ./queryfield.cgi
outfile=data/s$$.ctl

. ./myvinkhead.cgi "Generate field" "$kindname $climfield minus the influence of $FORM_station" ""

echo "One moment...<p>"
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) subtractfield $file $corrargs" | sed -e "s:$DIR/::g" >> log/log
echo $DIR/bin/correlatefield $file $FORM_corrargs subtract $outfile > /tmp/s$$.log
($DIR/bin/correlatefield $file $FORM_corrargs subtract $outfile >> /tmp/s$$.log) 2>&1
if [ ! -s data/s$$.ctl ]; then
  echo "Something went wrong...<pre>"
  echo $DIR/bin/correlatefield $file $FORM_corrargs subtract $outfile
  cat /tmp/s$$.log
  . ./myvinkfoot.cgi
  exit
else
  if [ "$lwrite" = true ]; then
    cat /tmp/s$$.log | sed -e 's/$/<br>/'
  fi
  rm /tmp/s$$.log
fi
infofile=data/s$$.$EMAIL.info
cat > $infofile << EOF
data/s$$.ctl
NPERYEAR=$NPERYEAR
LSMASK=$LSMASK
$kindname
$climfield - $FORM_station
EOF
cat << EOF
Field generated succesfully
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$FORM_EMAIL">
<input type="hidden" name="field" value="$infofile">
<input type="submit" class=formbutton value="Continue">
</form>
EOF
. ./myvinkfoot.cgi
