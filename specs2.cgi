#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo
. ./getargs.cgi
. ./myvinkhead.cgi "SPECS empirical seasonal forecasts" ""

cat <<EOF
<p>Past observations are used to deduce significant correlations between the weather 
in the last three months (up to the beginning of the month) and the weather over the next season (from the end of the month). The main predictors are El Ni&ntilde;o / La Ni&ntilde;a and the trends due to global warming. Overfitting is avoided as much as possible. The system has been documented in <a href="http://www.geosci-model-dev.net/8/3947/2015/" target="_new">Eden et al, 2015</a>.

<!--
<p>This web page is under construction. Please give feedback if it does not work properly.
-->

EOF

#<iframe src="http://127.0.0.1/myapp/kprep_sop:8050" width=700 height=600>
cat <<EOF
<iframe src="http://127.0.0.1/myapp/kprep_sop" style="width:100%;height:1000;border:none">
EOF

