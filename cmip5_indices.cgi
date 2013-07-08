#!/bin/sh

. ./getargs.cgi

. ./searchengine.cgi
. ./checkemail.cgi

cat <<EOF
Content-Type: text/html

EOF
. ./myvinkhead.cgi "Time series" "CMIP5 climate experiment indices" "index,nofollow"

echo "<div class=kalelink>"
cat CMIP5_disclaimer.html
cat <<EOF
The following indices are available at this moment:

<div class="alineakop">Global mean temperature</div
<ul>
<li>RCP2.6:
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_modmean_rcp26_000&STATION=CMIP5_RCP26_Tglobal&TYPE=i&id=$EMAIL">multi-model mean</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_mod_rcp26_%%%&STATION=CMIP5_RCP26_models_Tglobal&TYPE=i&id=$EMAIL">models</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_ens_rcp26_%%%&STATION=CMIP5_RCP26_members_Tglobal&TYPE=i&id=$EMAIL">members</a>
<li>RCP4.5:
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_modmean_rcp45_000&STATION=CMIP5_RCP45_Tglobal&TYPE=i&id=$EMAIL">multi-model mean</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_mod_rcp45_%%%&STATION=CMIP5_RCP45_models_Tglobal&TYPE=i&id=$EMAIL">models</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_ens_rcp45_%%%&STATION=CMIP5_RCP45_members_Tglobal&TYPE=i&id=$EMAIL">members</a>
<li>RCP6.0:
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_modmean_rcp60_000&STATION=CMIP5_RCP60_Tglobal&TYPE=i&id=$EMAIL">multi-model mean</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_mod_rcp60_%%%&STATION=CMIP5_RCP60_models_Tglobal&TYPE=i&id=$EMAIL">models</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_ens_rcp60_%%%&STATION=CMIP5_RCP60_members_Tglobal&TYPE=i&id=$EMAIL">members</a>
<li>RCP8.5:
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_modmean_rcp85_000&STATION=CMIP5_RCP85_Tglobal&TYPE=i&id=$EMAIL">multi-model mean</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_mod_rcp85_%%%&STATION=CMIP5_RCP85_models_Tglobal&TYPE=i&id=$EMAIL">models</a>,
<a href="getindices.cgi?WMO=CMIP5/Tglobal/global_tas_Amon_ens_rcp85_%%%&STATION=CMIP5_RCP85_members_Tglobal&TYPE=i&id=$EMAIL">members</a>
</ul>
<br>(<a href="CMIP5/Tglobal/index.cgi?email=$EMAIL">download all files</a>)
</div>
EOF


. ./myvinkfoot.cgi
