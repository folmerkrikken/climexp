#!/bin/sh
. ./init.cgi
. ./getargs.cgi
echo 'Content-Type: text/html'
echo
echo
# in order not to break bookmarks to this entry point allow QUERY_STRING (with some checking)
# do not allow / in email address
. ./searchengine.cgi
. ./checkemail.cgi
. ./myvinkhead.cgi "Starting point" "" "index,follow"

if [ "$EMAIL" != someone@somewhere ]; then
    FORM_username=`fgrep "$EMAIL" ./log/newlist | cut -f 2 -d ' ' | tail -1 | sed -e 's/+/ /g'`
    FORM_institute=`fgrep "$EMAIL" ./log/newlist | cut -f 3 -d ' ' | tail -1 | sed -e 's/+/ /g'`
    echo "<div class=\"alineakop\">Welcome, $FORM_username from $FORM_institute</div>"
    if [ -s data/randomimage.png ]; then
        randomimage=data/randomimage.png
    else
        tmpfile=/tmp/start$$.txt
        list=`ls -t data/ | fgrep .png | egrep '(^[dghR])|(.*corr.*)' | egrep -v 'kml|tmp' `
        for file in $list; do
            if [ -z "$randomimage" -a -s data/$file ]; then
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

if [ "$EMAIL" != someone@somewhere ]; then
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

echo '<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>'
echo '<tr><th colspan="2">News</th></tr>'
head -6 news.html | sed -e "s/FORM_EMAIL/$EMAIL/"
echo "<tr><td><a href=\"news.cgi?id=$EMAIL&all=all\">more...</a></td><td>&nbsp;</td></tr></table>"

. ./myvinkfoot.cgi