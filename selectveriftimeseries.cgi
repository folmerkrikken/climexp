#!/bin/bash

cat <<EOF
<div class="formheader">Time series to verify against</div>
<div class="formbody">
If the series is not in the list, select it first.<br>
EOF

forbidden='!`;&|'
i=0
for file in $DIR/data/*$NPERYEAR.$EMAIL.inf
do
# if no match it loops once with the unexpanded *.inf...
if [ -f "$file" ]; then
  c=`echo $file | egrep -c '\+|%'`
  if [ $c = 0 ]; then
    let i=$i+1
    datfile=`head -1 $file | tr $forbidden '?'`
    st=`head -2 $file | tail -1 | tr '_' ' '`
    wm=`tail -1 $file`
    ty=`basename $datfile .dat`
    ty=`basename $ty $wm`
# this is wrong ... if someone adds an index between this script and the next
# the wrong file will be selected.
    echo " <input type=\"radio\" class=\"formradio\" name=\"timeseries\" value=\"$file\">$st ($ty$wm)<br>"
  fi
fi
done
if [ "$ENSEMBLE" = true ]; then
  echo " <input type=\"radio\" class=\"formradio\" name=\"timeseries\" value=\"perfectmodel\">perfect model<br>"
fi

echo '</div'
