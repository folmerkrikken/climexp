#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Scenario runs" "index,nofollow"
cat <<EOF
<div class="kalelink">
We acknowledge the international modeling groups for providing their data for analysis, the Program for Climate Model Diagnosis and Intercomparison (<a href="http://www-pcmdi.llnl.gov/ipcc/about_ipcc.php" target="_new">PCMDI</a>) for collecting and archiving the model data, the JSC/CLIVAR Working Group on Coupled Modelling (WGCM) and their Coupled Model Intercomparison Project (CMIP) and Climate Simulation Panel for organizing the model data analysis activity, and the <a href="http://www.ipcc.ch" target="_new">IPCC</a> WG1 TSU for technical support. The IPCC Data Archive at Lawrence Livermore National Laboratory is supported by the Office of Science, U.S. Department of Energy.</div>
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="13"><input type="submit" class="formbutton" value="Select field">
Choose a field and press this button</td></tr>
EOF

sed -e "s/EMAIL/$EMAIL/" ./selectfield_ipcc.html
echo '</table>'
###cat selectfield_co2.html
###sed -e "s/EMAIL/$EMAIL/" selectfield_challenge.html
###cat selectfield_rcp.html

. ./myvinkfoot.cgi
