#!/bin/bash
echo "Content-Type: text/html"
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "Atlantic Multidecadal Oscillation indices" ""

cat <<EOF
The Atlantic Multidecadal Oscillation (AMO) is characterised by an
average over SST in the northern Atlantic.  As global warming also
affects SST, a way must be found to separate the effects of global
warming from those of the natural oscillation or variability &mdash;
the observed record is too short to decide whether there is a
well-defined period.

<p>The first solution to this was to subtract a linear trend.
However, global warming has not been linear over the last 130
years, so this unphysical procedure tended to mix effects of global
warming and effects of the AMO.  If you really want it, you can
construct the index yourself by averaging SST over an area in the
North Atlantic, and subtracting a regression against time.

<p><a href="http://www.agu.org/pubs/crossref/2006/2006GL026894.shtml">Trenberth and Shea (2006)</a> proposed to use the region EQ-60&deg;N,
0&deg;-80&deg;W and subtract the global rise of SST 60&deg;S-60&deg;N
to obtain a measure of the internal variability, arguing that the effect of
external forcing on the North Atlantic should be similar to the effect on the
other oceans.

<div class="bijschrift">The AMO index as defined as the SST averaged over 0&deg;-60&deg;N, 0&deg;-80&deg;W minus SST averaged over 60&deg;S-60&deg;N. The green line denotes a 10-yr running mean.</div>
<center><img src="tsiamo_ersst_tsyr0.png" alt="annual values of AMO index" border=0 class=realimage hspace=0 vspace=0></center>

<p><a
href="http://www.ocean-sci.net/5/293/2009/os-5-293-2009.html">Van
Oldenborgh et al 2009</a> chose to leave out the tropical region, as
this region is also influenced by ENSO.  Guided by model experiments that
show a low correlation between global mean temperature and variability
  in the overturning circulation (AMOC),
they proposed to force the AMO index to be orthogonal to Tgobal by
definition, lading to the second definition included here.

<div class="bijschrift">The AMO index as defined as the SST averaged over 25&deg;-60&deg;N, 7&deg;-70&deg;W minus the regression on global mean temperature. The green line denotes a 10-yr running mean.</div>
<center><img src="tsiamo_ersstyr0.png" alt="annual values of AMO index" border=0 class=realimage hspace=0 vspace=0></center>
</div>

<p>The indices differ on the monhly and interannua time scales, but agree very well on longer time scales.

<p>If you would like to add another definition, please contact <a href="mailto:oldenborgh@knmi.nl">me</a>.
EOF

. ./myvinkfoot.cgi

