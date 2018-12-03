#!/bin/bash
echo "Content-Type: text/html" ""
echo
echo

. ./getargs.cgi
. ./myvinkhead.cgi "ADVICE pressure data" ""

cat <<EOF
In April 2003, the ADVICE data set (station data and gridded) were not available or described elsewhere on the web.  The reference is 

<p>P. D. Jones, T. D. Davies, D. H. Lister, V. Slonosky, T. Jonsson,
L. Barring, P. Jonsson, P. Maheras, F. Kolyva-Machera, M. Barriendos,
J. Martin-Vide, R. Rodriquez, M. J. Alcoforado, H. Wanner, C. Pfister,
J. Luterbacher, R. Rickli, E. Schuepbach, E. Kaas, T. Schmith,
J. Jacobeit and C. Beck, Monthly mean Pressure reconstructions for
Europe for the 1780-1995 Period. Int. J. Climatol. 19: 347-364. (1999)
<a href="http://hdl.handle.net/doi:10.1002/(SICI)1097-0088(19990330)19:4<347::AID-JOC363>3.0.CO;2-S">doi:10.1002/(SICI)1097-0088(19990330)19:4<347::AID-JOC363>3.0.CO;2-S</a>
EOF

. ./myvinkfoot.cgi
