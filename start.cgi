#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

[ "$REMOTE_ADDR" = "134.17.128.149" ] && exit
[ "$REMOTE_ADDR" = "134.17.132.13" ] && exit
[ "$REMOTE_ADDR" = "81.94.205.66" ] && exit
. ./getargs.cgi
. ./init.cgi
# in order not to break bookmarks to this entry point allow QUERY_STRING (with some checking)
# do not allow / in email address
. ./searchengine.cgi
if [ -z "$EMAIL" ]; then
  . ./myvinkhead.cgi "No email address given" "" "noindex,nofollow"
  echo "Please <a href=\"registerform.cgi\">register or log in</a> or use the Climate Explorer <a href=\"/start.cgi?id=someone@somewhere\">anonymously</a> (with restrictions)"
  EMAIL=someone@somewhere
  . ./myvinkfoot.cgi
  exit
fi
c=`fgrep -c "^$EMAIL " ./log/list`
if [ $c = 0 ]; then
  . ./myvinkhead.cgi "User $EMAIL unknown" "" "noindex,follow"
  echo "Please <a href=\"registerform.cgi\">register or log in</a> or use the Climate Explorer <a href=\"/start.cgi?id=someone@somewhere\">anonymously</a> (with restrictions)"
  EMAIL=someone@somewhere
  . ./myvinkfoot.cgi
else
  FORM_username=`fgrep "$EMAIL" ./log/list|cut -f 2 -d ' '|tail -1|sed -e 's/+/ /g'`
  FORM_institute=`fgrep "$EMAIL" ./log/list|cut -f 3 -d ' '|tail -1|sed -e 's/+/ /g'`
  . ./myvinkhead.cgi "Starting point" "" "index,follow"

if [ "$EMAIL" != someone@somewhere ]; then
  echo "<div class=\"alineakop\">Welcome, $FORM_username from $FORM_institute</div>"
  ###echo "This page can be added to your bookmarks/favorites to avoid logging in.<p>"
  if [ -s data/randomimage.png ]
  then
    randomimage=data/randomimage.png
  else
    tmpfile=/tmp/start$$.txt
    list=`ls -t data/ | fgrep .png | egrep '(^[ghR])|(*corr*)' | egrep -v 'kml|tmp' `
    for file in $list
    do
      if [ -z "$randomimage" -a -s data/$file ]
      then
        randomimage=data/$file
      fi
    done
  fi
else
  echo "<div class=\"alineakop\">Welcome, anonymous user</div>"
  randomimage=imageoftheweek.png # pa61223.png

        cat <<EOF
Please enter the KNMI Climate Explorer, a research tool to investigate the climate.  This web site collects a lot of climate data and analysis tools.  Please verify yourself that the data you use is good enough for your purpose, and report errors back.  In publications the original data source should be cited, a link to a web page describing the data is always provided.

<p>Start by selecting a class of climate data from the right-hand menu.  After you have selected the time series or fields of interest, you will be able to investigate it, correlate it to other data, and generate derived data from it.

<p>If you are new it may be helpful to study the examples.

<p>Share and enjoy!
EOF
fi

if [ "$EMAIL" = someone@somewhere ]; then
  echo "<p>Some restrictions are in force, notably the possibility to define your own indices, to upload data into the Climate Explorer and to handle large datasets.  If you want to use these features please <a href="registerform.cgi">log in or register</a>."
fi

. ./check_ie.cgi

if [ ${REMOTE_ADDR#145.23} != $REMOTE_ADDR -a ${REMOTE_ADDR#145.23.248} = $REMOTE_ADDR -a $HTTP_HOST = climexp.knmi.nl ]; then
        echo "<p><font color=\"#FF0000\">KNMI users are advised to use the URL <a href=\"http://bhlclim.knmi.nl/start.cgi?id=$EMAIL\">bhlclim.knmi.nl</a></font>"
fi

if [ "$EMAIL" != someone@somewhere ]; then
        ###. ./headlines.cgi
        touch ./prefs/$EMAIL.news
fi

pngfile=$randomimage
getpngwidth
cat <<EOF
<div class="bijschrift"></div>
<center>
<img src="$randomimage" alt="random image" border=0 class="realimage" hspace=0 vspace=0 width=$halfwidth>
</center>
EOF

echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
echo '<tr><th colspan="2">News</th></tr>'
head -6 news.html
echo "<tr><td><a href=\"news.cgi?id=$EMAIL&all=all\">more...</a></td><td>&nbsp;</td></tr></table>"

. ./myvinkfoot.cgi
fi