#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

. ./myvinkhead.cgi "Select a 6-hourly field" "" "index,follow"

cat <<EOF
<div class="alineakop">Observations</div>
<form action="select.cgi" method="POST">
<div class="kalelink">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>
<!--<tr><td colspan="11"><input type="submit" value="Select field"></td></tr>-->
<tr>
<th colspan="11"><a href="Ad">ERS reprocessed scattermometer</a> 0.5&deg;&times;0.5&deg;</th>
EOF
for var in header u v tx ty speed
do
  case $var in
  header) name="&nbsp;";;
  u) name=$var;;
  v) name=$var;;
  tx) name="&tau;<sub>x</sub>";;
  ty) name="&tau;<sub>y</sub>";;
  speed) name="|u|";;
  *) name="unknown";;
  esac
  echo "</tr><tr><td>$name</td>"
  yr=1992
  while [ $yr -lt 2002 ]
  do
    if [ $var = header ]; then
      echo "<td>$yr</td>"
    else
      echo "<td><input type=\"radio\" class=\"formradio\" name=\"field\" value=\"sos_${yr}_${var}\"></td>"
    fi
    yr=$(($yr + 1))
  done
done
cat <<EOF
</tr><tr><td colspan="11"><input type="submit" class="formbutton" value="Select field"></td>
</tr>
</table>
</div>
</form>
EOF

. ./myvinkfoot.cgi
