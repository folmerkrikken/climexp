#!/bin/sh

echo "Content-Type:text/html"
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi

# check email address
. ./checkemail.cgi

. ./myvinkhead.cgi "Plot statistical properties" "$timescale $extraname$climate stations" "noindex,nofollow"

cat <<EOF
<form action="correlatebox.cgi" method="POST">
<input type="hidden" name="email" value="$email">
<input type="hidden" name="climate" value="$timescale $extraname$climate">
<input type="hidden" name="prog" value="$prog">
<input type="hidden" name="extraargs" value="$extraargs">
<input type="hidden" name="listname" value="$listname">
<input type="hidden" name="type" value="histogram">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">

<div class="formheader">Plot options</div>
<div class="formbody">
<input type="radio" name="var" value="hime" checked>mean<br>
<input type="radio" name="var" value="hisd">standard deviation<br>
<input type="radio" name="var" value="hisk">skewness<br>
&chi;<sup>2</sup> of a fit to a 
<input type="radio" name="var" value="higa">Gaussian<br>
return time of year <input type="text" class="forminput" name="year" size="4">, <input type="$number" class="forminput" name="threshold" textsize2 value="${FORM_threshold:-90}">%, <input type="radio" class="formradio" name="changesign" value="" $upper_checked>upper <input type="radio" class="formradio" name="changesign" value="on" $lower_checked>lower tail, fitted with a
<ul>
<li><input type="radio" name="var" value="higr">Gaussian (<input type="radio" name="var" value="higR">2.5% lower limit)<br>
<li><input type="radio" name="var" value="hipr">GPD with threshold <input type="text" class="forminput" name="dgt" size="4">%, <select class="forminput" name="restrain"><option value="0" $select00>do not constrain shape<option value="0.6" $select06>constrain shape to &plusmn;0.6<option value="0.4" $select04>constrain shape to &plusmn;0.4</select> (<input type="radio" name="var" value="hipR">2.5% lower limit)
</ul>
<br>Only show stations with at least
<input type="text" name="minnum" size="3"> valid years/months
</div>
<p><div class="formheader">Common options</div>
<div class="formbody">
EOF

cat $DIR/common1options.html

cat << EOF
<input type="submit" class="formbutton" value="Submit">
</div>
EOF

. ./myvinkfoot.cgi
