#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Help overview" "" "index,follow"

cat | sed -e "s/FORM_EMAIL/$EMAIL/" <<EOF
I am building a help system for the Climate Explorer.
New users are adviced to study the <a href="examp.cgi?id=$EMAIL">examples</a>.  There is also an old <a href="/publications/the_climate_explorer.pdf">presentation</a> available that gives an overview of the system, and a more recent <a href="publications/Climexp_Brazil.mp4">video presentation</a> focussing mainly on the Atlas. <a href="http://www.bioone.org/doi/abs/10.3959/1536-1098-69.1.3" target=_new>Trouet and van Oldenborgh</a> (TRR, 2013) gives a useful overview and manual for paleo-climatologists and others who try to understand the influence of climate on their time series. Finally, some results are shown on the pages <a href="effects.cgi?id=FORM_EMAIL"</a>Effects of El Ni&ntilde;o on world weather</a>.

<p>In the Climate Explorer pages, the <a href="help.cgi?id=$EMAIL"><img src="images/info-i.gif" alt="help" border="0"></a> symbol indicates a help pop-up.  Below an alphabetical list of these pop-ups is given.  Please contact <a href="mailto:oldenborgh@knmi.nl">me</a> if the help text is confusing, or missing in a place where it is needed.

<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
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

 
