#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

# check if a search engine, if so set user to anonymous
. ./getargs.cgi

. ./searchengine.cgi

. ./myvinkhead.cgi "Select or upload a time series" "User-defined time series"

###cat news.html
cat <<EOF
These are the time series you are working with, they will be erased 3 days after last use.

<p><table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
EOF
if [ "$EMAIL" != "someone@somewhere" ]; then
# generate list of user-defined indices
  forbidden='!`;'
  for NPERYEAR in 1464 366 365 360 73 36 12 4 1
  do
	started=false
	for file in data/*$NPERYEAR.$EMAIL.inf
	do
	  ###echo "NPERYEAR,file = $NPERYEAR,$file<br>"
	  if [ -f $file ]; then
		if [ $started = false ]
		then
		  started=true
		  . ./nperyear2timescale.cgi
		  echo "<tr><th>${timescale}timeseries"
		  case $NPERYEAR in
			  365) echo "(365-day calendar)";;
			  360) echo "(360-day calendar)";;
		  esac
		fi
		datfile=`cat "$file"|head -1|		 tr "+$forbidden" '%?'`
		wmo=`	 cat "$file"|tail -1|		 tr "+$forbidden" '%?'`
		type=`	 basename $datfile .dat`
		type=`	 basename $type $wmo`
		wmo=${wmo##$type}
		STATION=`cat "$file"|head -2|tail -1|tr "+$forbidden" '%?'`
		station=`echo $STATION | tr '_%' ' +'`
		echo "<tr><td><div class=\"kalelink\"><a href=\"getindices.cgi?WMO=data/$type${wmo}&STATION=${STATION}&TYPE=${type}&id=${EMAIL}&NPERYEAR=$NPERYEAR\">$station</a> ($type$wmo)</div>"
	  fi
	done
  done
else
  echo "<tr><th>Anonymous users cannot use user-defined indices"
fi
echo '</table>'

. ./uploadform.cgi


