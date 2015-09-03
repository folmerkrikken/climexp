#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Contact" ""

cat <<EOF
The support team of the KNMI Climate Explorer consists of <a href="http://www.knmi.nl/over-het-knmi/onze-mensen/geert-jan-van-oldenborgh">one research scientist</a>, next to my day job writing <a href="https://scholar.google.nl/citations?hl=nl&user=q9wj1loAAAAJ&view_op=list_works&sortby=pubdate">research papers</a>, in practice I spent about a day per week on the Climate Explorer and related <a href="/monthly_overview_world_weather/">projects</a>. This also means that I rely on the users to report bugs, please <a href="mailto:oldenborgh@knmi.nl">mail me</a> when something does not work as advertised.
EOF

. ./myvinkfoot.cgi

