#!/bin/bash

. ./getargs.cgi
WMO="$FORM_wmo"
wmo=`basename $WMO .dat | tr '%' '+'`
station="$FORM_station"
type="$FORM_type"
nperyear="$FORM_nperyear"
cat << EOF
Content-Type: text/html


EOF

. ./myvinkhead.cgi "Ensemble members" "Time series" "nofollow,noindex"

cat <<EOF
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th>number<th>ascii<th>netcdf<th>analyse separately
EOF
list=`cat data/$type$wmo.dat | tr '#' ' '`
i=0
for file in $list
do
	if [ -f "$file" ]; then
		name=${station}_$i
		wmo=`basename $file .dat | cut -b 2- | tr '+' '%'`
		cat << EOF
<tr><td>$i
<td><a href="$file"><img src="images/download.gif" border=0 alt="ascii data $name"></a>
<td><a href="dat2nc.cgi?datafile=$file&type=i&station=ensemble_member_$i&id=$EMAIL"><img src="images/download.gif" border=0 alt="netcdf data $name"></a>
<td><a href="getindices.cgi?WMO=$wmo&STATION=$name&TYPE=$type&id=$EMAIL&NPERYEAR=$nperyear"><img src="images/go_pijl.gif" border=0 alt="analyse $name"></a>
EOF
		i=$(($i + 1))
	fi
done
echo "</table>"

. ./myvinkfoot.cgi
