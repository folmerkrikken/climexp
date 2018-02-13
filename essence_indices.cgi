#!/bin/sh

. ./init.cgi
. ./getargs.cgi
. ./searchengine.cgi
. ./checkemail.cgi

cat <<EOF
Content-Type: text/html

EOF
. ./myvinkhead.cgi "Time series" "ESSENCE climate experiment indices" "index,nofollow"

cat <<EOF
<ul>
<li><a href="getindices.cgi?WMO=ESSENCE/temp2_a1b_%%_global&STATION=Essence_Tglobal&TYPE=i&id=$EMAIL">Global mean temperature</a>, <a href="getindices.cgi?WMO=ESSENCE/temp2_a1b_ave_global&STATION=Essence_Tglobal&TYPE=i&id=$EMAIL">ensemble mean</a>
<li><a href="getindices.cgi?WMO=ESSENCE/OTATL_a1b_%%_new_max&STATION=Essence_max_Atlantic_ot35&TYPE=i&id=$EMAIL">Maximum Atlantic overturning at 35&deg;N</a>
<li><a href="getindices.cgi?WMO=ESSENCE/OTATL_hosing_%%_max&STATION=Essence_max_Atlantic_ot35_hosing&TYPE=i&id=$EMAIL">Maximum Atlantic overturning at 35&deg;N in the hosing experiments</a>
<li><a href="getindices.cgi?WMO=ESSENCE/nino12_tsw_a1b_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino12</a>, <a href="getindices.cgi?WMO=ESSENCE/nino3_tsw_a1b_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino3</a>, <a href="getindices.cgi?WMO=ESSENCE/nino3.4_tsw_a1b_%%&STATION=Essence_Nino3.4&TYPE=i&id=$EMAIL">Nino3.4</a>, <a href="getindices.cgi?WMO=ESSENCE/nino4_tsw_a1b_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino4</a> temperatures in the standard runs
<li><a href="getindices.cgi?WMO=ESSENCE/nino12_tsw_hosing_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino12</a>, <a href="getindices.cgi?WMO=ESSENCE/nino3_tsw_hosing_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino3</a>, <a href="getindices.cgi?WMO=ESSENCE/nino3.4_tsw_hosing_%%&STATION=Essence_Nino3.4&TYPE=i&id=$EMAIL">Nino3.4</a>, <a href="getindices.cgi?WMO=ESSENCE/nino4_tsw_hosing_%%&STATION=Essence_Nino3&TYPE=i&id=$EMAIL">Nino4</a> temperatures in the hosing experiments
<li><a href="getindices.cgi?WMO=ESSENCE/essence_nao_%%&STATION=Essence_NAO&TYPE=i&id=$EMAIL">NAO index</a> from the DJF averaged pattern in 1961-2000
<li>The same NAO index <a href="getindices.cgi?WMO=ESSENCE/essence_hosing_nao_%%&STATION=Essence_hosing_NAO&TYPE=i&id=$EMAIL">in the hosing experiments</a>.
<li><a href="getindices.cgi?WMO=ESSENCE/amo_tsw_a1b_%%&STATION=Essence_AMO&TYPE=i&id=$EMAIL">AMO index</a> (SST over 0&deg;-60&deg;N, 75&deg;-7.5&deg;W, no detrending) in the standard runs
<li><a href="getindices.cgi?WMO=ESSENCE/amo_tsw_hosing_%%&STATION=Essence_AMO&TYPE=i&id=$EMAIL">AMO index</a> (SST over 0&deg;-60&deg;N, 75&deg;-7.5&deg;W, no detrending) in the hosing runs
<li><a href="getindices.cgi?WMO=ESSENCE/heat750_a1b_%%_global&STATION=Essence_heat750&TYPE=i&id=$EMAIL">Ocean heat contant up to 750m</a>, <a href="getindices.cgi?WMO=ESSENCE/heat700_essence_%%&STATION=Essence_heat700&TYPE=i&id=$EMAIL&NPERYEAR=1">700m</a> in the standard runs
<li><a href="getindices.cgi?WMO=ESSENCE/rad0_a1b_%%_global&STATION=Essence_Q_toa&TYPE=i&id=$EMAIL">Net global TOA flux</a> in the standard runs, <a href="getindices.cgi?WMO=ESSENCE/trad0_a1b_%%_global&STATION=Essence_Qlw_toa&TYPE=i&id=$EMAIL">long-wave</a>,  <a href="getindices.cgi?WMO=ESSENCE/srad0_a1b_%%_global&STATION=Essence_Qsw_toa&TYPE=i&id=$EMAIL">short-wave</a>
</ul>
EOF

. ./myvinkfoot.cgi
