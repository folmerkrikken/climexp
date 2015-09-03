#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Contact" ""

cat <<EOF
The support team of the KNMI Climate Explorer consists of <a href="mailto:oldenborgh@knmi.nl">one research scientist</a>, next to my day job writing <a href="mailto:oldenborgh@knmi.nlpublished.html">research papers</a>, in practice I spent about a day per week on the Climate Explorer and related <a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/">projects</a>. This also means that I rely on the users to report bugs, please <a href="mailto:oldenborgh@knmi.nl">mail me</a> when something does not work as advertised.
EOF

. ./myvinkfoot.cgi

