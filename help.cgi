#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Help overview" "" "index,follow"

cat <<EOF
I am building a help system for the Climate Explorer.
New users are adviced to study the <a href="examp.cgi?id=$EMAIL">examples</a>.  There is also a <a href="http://www.knmi.nl/publications/fulltexts/the_climate_explorer.pdf">presentation</a> available that gives an overview of the system. <a href="http://www.knmi.nl/publications/showAbstract.php?id=9861" target=_new>Trouet and van Oldenborgh</a> (TRR, 2013) gives a useful overview and manual for paleo-climatologists and others who try to understand the influence of climate on their time series.

<p>In the Climate Explorer pages, the <a href="help.cgi?id=$EMAIL"><img src="images/info-i.gif" alt="help" border="0"></a> symbol indicates a help pop-up.  Below an alphabetical list of these pop-ups is given.  Please contact <a href="http://www.knmi.nl/~oldenbor/">me</a> if the help text is confusing, or missing in a place where it is needed.

<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="2">Available help topics</a>
EOF

tmpfile=/tmp/help$$.html
touch $tmpfile
for file in help/*.shtml
do
  if [ $file != help/template.shtml ]; then
    titel=`fgrep alineakop $file | head -1 | sed -e 's/^[^>]*>//' -e 's/<.*$//'`
    echo "<tr><td><div class=\"kalelink\"><!--$titel--><a href=\"$file\" target=\"_new\">$titel</a></div><td><a href=\"javascript:pop_page('$file',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>" >> $tmpfile
  fi
done
sort $tmpfile
rm $tmpfile

cat <<EOF
</table>
EOF

. ./myvinkfoot.cgi

 
