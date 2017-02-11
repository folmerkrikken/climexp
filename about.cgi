#!/bin/sh
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "About the Climate Explorer" ""

cat <<EOF
The KNMI Climate Explorer is a web application to analysis climate data statistically.  It started in late 1999 as a <a href="history/">sinple web page</a> to analyse ENSO teleconnections and has grown over the years to more than 10 TB of climate data and dozens of analysis tools.  It is now part of the WMO Regional Climate Centre at KNMI, together with <a href="http://www.ecad.eu">ECA&amp;D</a>.

<p>This is scientific tool. Please verify yourself that the data you use is good enough for your purpose, and <a href="contact.cgi?id=$EMAIL">report errors back</a>. In publications the original data source should be cited, a link to a web page describing the data is always provided.

<p>The KNMI Climate Exoplorer is not operational: if it breaks down it will be fixed during Dutch office hours. Over the last few years the availability has been pretty good, although sometimes a few users slow down the system by doing large computations simultaneously. The <a href="forecast_verification.cgi?id=$EMAIL">seasonal forecast verification</a> page was supported by the EU project <a href="http://ensembles-eu.metoffice.com/" target="_new">ENSEMBLES</a>, the Atlas by another EU project <a href="http://www.specs-fp7.eu/SPECS/Home.html" target=_new>SPECS<a>, the <a href="http://www.climatecentre.org" target="_new">Red Cross / Red Crescent Climate Centre</a> and he Dutch Ministry of Infrastructure and Environment. The rest is an informal project. We are working on a new version of the software that will become an operational part of KNMI.

<p>The support team consists of <a href="http://www.knmi.nl/over-het-knmi/onze-mensen/geert-jan-van-oldenborgh">one research scientist</a>, next to my day job writing <a href="https://scholar.google.nl/citations?hl=nl&user=q9wj1loAAAAJ&view_op=list_works&sortby=pubdate">research papers</a>, in practice I spent about a day per week on the Climate Explorer and related projects.

<p>Much of the observational data is updated monthly.  Other data is updated when needed.  More and more data is pulled from external sites on request, see the link <a href="selectfield_external.cgi?id=$EMAIL">external data</a>.  If you have an interesting dataset that you want to publish on the Climate Explorer please send me the URL of a <a href="http://cf-pcmdi.llnl.gov/" target="_new">CF-compliant netcdf file</a> and a short description.

<p>The code of the Climate Explorer itself is freely available.  Due to its humble origins it consists of a set of shell scripts and Fortran programs and runs under linux and Mac OS X.
EOF

. ./myvinkfoot.cgi

