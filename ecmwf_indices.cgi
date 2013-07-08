#!/bin/sh

. ./getargs.cgi
. ./searchengine.cgi

cat <<EOF
Content-Type: text/html

EOF
. ./myvinkhead.cgi "Time series" "GCMs seasonal forecast indices" "index,nofollow"
cat <<EOF
<div class="alineakop">NINO indices</div>

<table class="realtable" width=451 border='0' cellpadding='0' cellspacing='0'>
<tr>
<th colspan="19">ECMWF System-3 ensemble mean</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jan_ensm&STATION=ECMWF3_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_feb_ensm&STATION=ECMWF3_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_mar_ensm&STATION=ECMWF3_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_apr_ensm&STATION=ECMWF3_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_may_ensm&STATION=ECMWF3_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jun_ensm&STATION=ECMWF3_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jul_ensm&STATION=ECMWF3_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_aug_ensm&STATION=ECMWF3_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_sep_ensm&STATION=ECMWF3_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_oct_ensm&STATION=ECMWF3_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_nov_ensm&STATION=ECMWF3_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_dec_ensm&STATION=ECMWF3_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jan_ensm&STATION=ECMWF3_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_feb_ensm&STATION=ECMWF3_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_mar_ensm&STATION=ECMWF3_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_apr_ensm&STATION=ECMWF3_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_may_ensm&STATION=ECMWF3_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jun_ensm&STATION=ECMWF3_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jul_ensm&STATION=ECMWF3_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_aug_ensm&STATION=ECMWF3_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_sep_ensm&STATION=ECMWF3_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_oct_ensm&STATION=ECMWF3_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_nov_ensm&STATION=ECMWF3_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_dec_ensm&STATION=ECMWF3_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jan_ensm&STATION=ECMWF3_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_feb_ensm&STATION=ECMWF3_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_mar_ensm&STATION=ECMWF3_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_apr_ensm&STATION=ECMWF3_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_may_ensm&STATION=ECMWF3_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jun_ensm&STATION=ECMWF3_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jul_ensm&STATION=ECMWF3_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_aug_ensm&STATION=ECMWF3_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_sep_ensm&STATION=ECMWF3_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_oct_ensm&STATION=ECMWF3_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_nov_ensm&STATION=ECMWF3_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_dec_ensm&STATION=ECMWF3_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jan_ensm&STATION=ECMWF3_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_feb_ensm&STATION=ECMWF3_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_mar_ensm&STATION=ECMWF3_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_apr_ensm&STATION=ECMWF3_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_may_ensm&STATION=ECMWF3_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jun_ensm&STATION=ECMWF3_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jul_ensm&STATION=ECMWF3_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_aug_ensm&STATION=ECMWF3_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_sep_ensm&STATION=ECMWF3_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_oct_ensm&STATION=ECMWF3_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_nov_ensm&STATION=ECMWF3_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_dec_ensm&STATION=ECMWF3_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">ECMWF System-2 ensemble mean</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jan_ensm&STATION=ECMWF2_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_feb_ensm&STATION=ECMWF2_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_mar_ensm&STATION=ECMWF2_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_apr_ensm&STATION=ECMWF2_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_may_ensm&STATION=ECMWF2_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jun_ensm&STATION=ECMWF2_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jul_ensm&STATION=ECMWF2_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_aug_ensm&STATION=ECMWF2_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_sep_ensm&STATION=ECMWF2_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_oct_ensm&STATION=ECMWF2_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_nov_ensm&STATION=ECMWF2_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_dec_ensm&STATION=ECMWF2_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jan_ensm&STATION=ECMWF2_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_feb_ensm&STATION=ECMWF2_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_mar_ensm&STATION=ECMWF2_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_apr_ensm&STATION=ECMWF2_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_may_ensm&STATION=ECMWF2_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jun_ensm&STATION=ECMWF2_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jul_ensm&STATION=ECMWF2_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_aug_ensm&STATION=ECMWF2_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_sep_ensm&STATION=ECMWF2_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_oct_ensm&STATION=ECMWF2_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_nov_ensm&STATION=ECMWF2_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_dec_ensm&STATION=ECMWF2_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jan_ensm&STATION=ECMWF2_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_feb_ensm&STATION=ECMWF2_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_mar_ensm&STATION=ECMWF2_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_apr_ensm&STATION=ECMWF2_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_may_ensm&STATION=ECMWF2_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jun_ensm&STATION=ECMWF2_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jul_ensm&STATION=ECMWF2_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_aug_ensm&STATION=ECMWF2_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_sep_ensm&STATION=ECMWF2_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_oct_ensm&STATION=ECMWF2_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_nov_ensm&STATION=ECMWF2_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_dec_ensm&STATION=ECMWF2_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jan_ensm&STATION=ECMWF2_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_feb_ensm&STATION=ECMWF2_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_mar_ensm&STATION=ECMWF2_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_apr_ensm&STATION=ECMWF2_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_may_ensm&STATION=ECMWF2_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jun_ensm&STATION=ECMWF2_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jul_ensm&STATION=ECMWF2_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_aug_ensm&STATION=ECMWF2_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_sep_ensm&STATION=ECMWF2_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_oct_ensm&STATION=ECMWF2_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_nov_ensm&STATION=ECMWF2_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_dec_ensm&STATION=ECMWF2_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">UKMO ensemble mean</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jan_ensm&STATION=UKMO_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_feb_ensm&STATION=UKMO_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_mar_ensm&STATION=UKMO_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_apr_ensm&STATION=UKMO_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_may_ensm&STATION=UKMO_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jun_ensm&STATION=UKMO_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jul_ensm&STATION=UKMO_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_aug_ensm&STATION=UKMO_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_sep_ensm&STATION=UKMO_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_oct_ensm&STATION=UKMO_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_nov_ensm&STATION=UKMO_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_dec_ensm&STATION=UKMO_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jan_ensm&STATION=UKMO_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_feb_ensm&STATION=UKMO_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_mar_ensm&STATION=UKMO_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_apr_ensm&STATION=UKMO_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_may_ensm&STATION=UKMO_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jun_ensm&STATION=UKMO_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jul_ensm&STATION=UKMO_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_aug_ensm&STATION=UKMO_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_sep_ensm&STATION=UKMO_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_oct_ensm&STATION=UKMO_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_nov_ensm&STATION=UKMO_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_dec_ensm&STATION=UKMO_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jan_ensm&STATION=UKMO_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_feb_ensm&STATION=UKMO_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_mar_ensm&STATION=UKMO_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_apr_ensm&STATION=UKMO_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_may_ensm&STATION=UKMO_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jun_ensm&STATION=UKMO_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jul_ensm&STATION=UKMO_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_aug_ensm&STATION=UKMO_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_sep_ensm&STATION=UKMO_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_oct_ensm&STATION=UKMO_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_nov_ensm&STATION=UKMO_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_dec_ensm&STATION=UKMO_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jan_ensm&STATION=UKMO_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_feb_ensm&STATION=UKMO_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_mar_ensm&STATION=UKMO_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_apr_ensm&STATION=UKMO_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_may_ensm&STATION=UKMO_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jun_ensm&STATION=UKMO_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jul_ensm&STATION=UKMO_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_aug_ensm&STATION=UKMO_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_sep_ensm&STATION=UKMO_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_oct_ensm&STATION=UKMO_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_nov_ensm&STATION=UKMO_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_dec_ensm&STATION=UKMO_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">NCEP-CFS ensemble mean</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jan_ensm&STATION=CFS_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_feb_ensm&STATION=CFS_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_mar_ensm&STATION=CFS_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_apr_ensm&STATION=CFS_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_may_ensm&STATION=CFS_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jun_ensm&STATION=CFS_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jul_ensm&STATION=CFS_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_aug_ensm&STATION=CFS_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_sep_ensm&STATION=CFS_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_oct_ensm&STATION=CFS_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_nov_ensm&STATION=CFS_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_dec_ensm&STATION=CFS_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jan_ensm&STATION=CFS_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_feb_ensm&STATION=CFS_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_mar_ensm&STATION=CFS_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_apr_ensm&STATION=CFS_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_may_ensm&STATION=CFS_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jun_ensm&STATION=CFS_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jul_ensm&STATION=CFS_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_aug_ensm&STATION=CFS_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_sep_ensm&STATION=CFS_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_oct_ensm&STATION=CFS_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_nov_ensm&STATION=CFS_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_dec_ensm&STATION=CFS_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jan_ensm&STATION=CFS_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_feb_ensm&STATION=CFS_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_mar_ensm&STATION=CFS_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_apr_ensm&STATION=CFS_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_may_ensm&STATION=CFS_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jun_ensm&STATION=CFS_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jul_ensm&STATION=CFS_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_aug_ensm&STATION=CFS_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_sep_ensm&STATION=CFS_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_oct_ensm&STATION=CFS_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_nov_ensm&STATION=CFS_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_dec_ensm&STATION=CFS_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jan_ensm&STATION=CFS_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_feb_ensm&STATION=CFS_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_mar_ensm&STATION=CFS_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_apr_ensm&STATION=CFS_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_may_ensm&STATION=CFS_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jun_ensm&STATION=CFS_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jul_ensm&STATION=CFS_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_aug_ensm&STATION=CFS_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_sep_ensm&STATION=CFS_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_oct_ensm&STATION=CFS_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_nov_ensm&STATION=CFS_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_dec_ensm&STATION=CFS_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">ECHAM4.5 ensemble mean</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jan_ensm&STATION=ECHAM5_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_feb_ensm&STATION=ECHAM5_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_mar_ensm&STATION=ECHAM5_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_apr_ensm&STATION=ECHAM5_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_may_ensm&STATION=ECHAM5_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jun_ensm&STATION=ECHAM5_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jul_ensm&STATION=ECHAM5_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_aug_ensm&STATION=ECHAM5_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_sep_ensm&STATION=ECHAM5_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_oct_ensm&STATION=ECHAM5_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_nov_ensm&STATION=ECHAM5_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_dec_ensm&STATION=ECHAM5_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jan_ensm&STATION=ECHAM5_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_feb_ensm&STATION=ECHAM5_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_mar_ensm&STATION=ECHAM5_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_apr_ensm&STATION=ECHAM5_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_may_ensm&STATION=ECHAM5_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jun_ensm&STATION=ECHAM5_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jul_ensm&STATION=ECHAM5_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_aug_ensm&STATION=ECHAM5_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_sep_ensm&STATION=ECHAM5_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_oct_ensm&STATION=ECHAM5_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_nov_ensm&STATION=ECHAM5_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_dec_ensm&STATION=ECHAM5_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jan_ensm&STATION=ECHAM5_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_feb_ensm&STATION=ECHAM5_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_mar_ensm&STATION=ECHAM5_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_apr_ensm&STATION=ECHAM5_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_may_ensm&STATION=ECHAM5_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jun_ensm&STATION=ECHAM5_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jul_ensm&STATION=ECHAM5_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_aug_ensm&STATION=ECHAM5_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_sep_ensm&STATION=ECHAM5_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_oct_ensm&STATION=ECHAM5_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_nov_ensm&STATION=ECHAM5_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_dec_ensm&STATION=ECHAM5_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jan_ensm&STATION=ECHAM5_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_feb_ensm&STATION=ECHAM5_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_mar_ensm&STATION=ECHAM5_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_apr_ensm&STATION=ECHAM5_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_may_ensm&STATION=ECHAM5_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jun_ensm&STATION=ECHAM5_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jul_ensm&STATION=ECHAM5_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_aug_ensm&STATION=ECHAM5_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_sep_ensm&STATION=ECHAM5_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_oct_ensm&STATION=ECHAM5_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_nov_ensm&STATION=ECHAM5_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_dec_ensm&STATION=ECHAM5_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">ECMWF System-3 full ensembles</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jan_m%%&STATION=ECMWF3_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_feb_m%%&STATION=ECMWF3_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_mar_m%%&STATION=ECMWF3_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_apr_m%%&STATION=ECMWF3_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_may_m%%&STATION=ECMWF3_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jun_m%%&STATION=ECMWF3_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_jul_m%%&STATION=ECMWF3_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_aug_m%%&STATION=ECMWF3_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_sep_m%%&STATION=ECMWF3_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_oct_m%%&STATION=ECMWF3_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_nov_m%%&STATION=ECMWF3_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino12a_dec_m%%&STATION=ECMWF3_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jan_m%%&STATION=ECMWF3_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_feb_m%%&STATION=ECMWF3_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_mar_m%%&STATION=ECMWF3_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_apr_m%%&STATION=ECMWF3_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_may_m%%&STATION=ECMWF3_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jun_m%%&STATION=ECMWF3_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_jul_m%%&STATION=ECMWF3_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_aug_m%%&STATION=ECMWF3_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_sep_m%%&STATION=ECMWF3_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_oct_m%%&STATION=ECMWF3_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_nov_m%%&STATION=ECMWF3_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3a_dec_m%%&STATION=ECMWF3_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jan_m%%&STATION=ECMWF3_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_feb_m%%&STATION=ECMWF3_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_mar_m%%&STATION=ECMWF3_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_apr_m%%&STATION=ECMWF3_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_may_m%%&STATION=ECMWF3_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jun_m%%&STATION=ECMWF3_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_jul_m%%&STATION=ECMWF3_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_aug_m%%&STATION=ECMWF3_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_sep_m%%&STATION=ECMWF3_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_oct_m%%&STATION=ECMWF3_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_nov_m%%&STATION=ECMWF3_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino3.4a_dec_m%%&STATION=ECMWF3_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jan_m%%&STATION=ECMWF3_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_feb_m%%&STATION=ECMWF3_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_mar_m%%&STATION=ECMWF3_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_apr_m%%&STATION=ECMWF3_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_may_m%%&STATION=ECMWF3_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jun_m%%&STATION=ECMWF3_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_jul_m%%&STATION=ECMWF3_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_aug_m%%&STATION=ECMWF3_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_sep_m%%&STATION=ECMWF3_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_oct_m%%&STATION=ECMWF3_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_nov_m%%&STATION=ECMWF3_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf3_nino4a_dec_m%%&STATION=ECMWF3_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">ECMWF System-2 full ensembles</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jan_m%%&STATION=ECMWF2_jan_nino12_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_feb_m%%&STATION=ECMWF2_feb_nino12_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_mar_m%%&STATION=ECMWF2_mar_nino12_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_apr_m%%&STATION=ECMWF2_apr_nino12_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_may_m%%&STATION=ECMWF2_may_nino12_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jun_m%%&STATION=ECMWF2_jun_nino12_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_jul_m%%&STATION=ECMWF2_jul_nino12_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_aug_m%%&STATION=ECMWF2_aug_nino12_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_sep_m%%&STATION=ECMWF2_sep_nino12_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_oct_m%%&STATION=ECMWF2_oct_nino12_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_nov_m%%&STATION=ECMWF2_nov_nino12_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino12a_dec_m%%&STATION=ECMWF2_dec_nino12_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jan_m%%&STATION=ECMWF2_jan_nino3_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_feb_m%%&STATION=ECMWF2_feb_nino3_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_mar_m%%&STATION=ECMWF2_mar_nino3_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_apr_m%%&STATION=ECMWF2_apr_nino3_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_may_m%%&STATION=ECMWF2_may_nino3_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jun_m%%&STATION=ECMWF2_jun_nino3_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_jul_m%%&STATION=ECMWF2_jul_nino3_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_aug_m%%&STATION=ECMWF2_aug_nino3_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_sep_m%%&STATION=ECMWF2_sep_nino3_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_oct_m%%&STATION=ECMWF2_oct_nino3_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_nov_m%%&STATION=ECMWF2_nov_nino3_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3a_dec_m%%&STATION=ECMWF2_dec_nino3_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jan_m%%&STATION=ECMWF2_jan_nino3.4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_feb_m%%&STATION=ECMWF2_feb_nino3.4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_mar_m%%&STATION=ECMWF2_mar_nino3.4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_apr_m%%&STATION=ECMWF2_apr_nino3.4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_may_m%%&STATION=ECMWF2_may_nino3.4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jun_m%%&STATION=ECMWF2_jun_nino3.4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_jul_m%%&STATION=ECMWF2_jul_nino3.4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_aug_m%%&STATION=ECMWF2_aug_nino3.4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_sep_m%%&STATION=ECMWF2_sep_nino3.4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_oct_m%%&STATION=ECMWF2_oct_nino3.4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_nov_m%%&STATION=ECMWF2_nov_nino3.4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino3.4a_dec_m%%&STATION=ECMWF2_dec_nino3.4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jan_m%%&STATION=ECMWF2_jan_nino4_ensm&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_feb_m%%&STATION=ECMWF2_feb_nino4_ensm&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_mar_m%%&STATION=ECMWF2_mar_nino4_ensm&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_apr_m%%&STATION=ECMWF2_apr_nino4_ensm&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_may_m%%&STATION=ECMWF2_may_nino4_ensm&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jun_m%%&STATION=ECMWF2_jun_nino4_ensm&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_jul_m%%&STATION=ECMWF2_jul_nino4_ensm&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_aug_m%%&STATION=ECMWF2_aug_nino4_ensm&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_sep_m%%&STATION=ECMWF2_sep_nino4_ensm&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_oct_m%%&STATION=ECMWF2_oct_nino4_ensm&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_nov_m%%&STATION=ECMWF2_nov_nino4_ensm&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ecmwf2_nino4a_dec_m%%&STATION=ECMWF2_dec_nino4_ensm&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">UKMO full ensembles</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jan_m%%&STATION=UKMO_jan_nino12_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_feb_m%%&STATION=UKMO_feb_nino12_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_mar_m%%&STATION=UKMO_mar_nino12_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_apr_m%%&STATION=UKMO_apr_nino12_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_may_m%%&STATION=UKMO_may_nino12_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jun_m%%&STATION=UKMO_jun_nino12_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_jul_m%%&STATION=UKMO_jul_nino12_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_aug_m%%&STATION=UKMO_aug_nino12_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_sep_m%%&STATION=UKMO_sep_nino12_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_oct_m%%&STATION=UKMO_oct_nino12_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_nov_m%%&STATION=UKMO_nov_nino12_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino12_dec_m%%&STATION=UKMO_dec_nino12_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jan_m%%&STATION=UKMO_jan_nino3_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_feb_m%%&STATION=UKMO_feb_nino3_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_mar_m%%&STATION=UKMO_mar_nino3_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_apr_m%%&STATION=UKMO_apr_nino3_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_may_m%%&STATION=UKMO_may_nino3_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jun_m%%&STATION=UKMO_jun_nino3_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_jul_m%%&STATION=UKMO_jul_nino3_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_aug_m%%&STATION=UKMO_aug_nino3_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_sep_m%%&STATION=UKMO_sep_nino3_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_oct_m%%&STATION=UKMO_oct_nino3_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_nov_m%%&STATION=UKMO_nov_nino3_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3_dec_m%%&STATION=UKMO_dec_nino3_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jan_m%%&STATION=UKMO_jan_nino3.4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_feb_m%%&STATION=UKMO_feb_nino3.4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_mar_m%%&STATION=UKMO_mar_nino3.4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_apr_m%%&STATION=UKMO_apr_nino3.4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_may_m%%&STATION=UKMO_may_nino3.4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jun_m%%&STATION=UKMO_jun_nino3.4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_jul_m%%&STATION=UKMO_jul_nino3.4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_aug_m%%&STATION=UKMO_aug_nino3.4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_sep_m%%&STATION=UKMO_sep_nino3.4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_oct_m%%&STATION=UKMO_oct_nino3.4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_nov_m%%&STATION=UKMO_nov_nino3.4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino3.4_dec_m%%&STATION=UKMO_dec_nino3.4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jan_m%%&STATION=UKMO_jan_nino4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_feb_m%%&STATION=UKMO_feb_nino4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_mar_m%%&STATION=UKMO_mar_nino4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_apr_m%%&STATION=UKMO_apr_nino4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_may_m%%&STATION=UKMO_may_nino4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jun_m%%&STATION=UKMO_jun_nino4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_jul_m%%&STATION=UKMO_jul_nino4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_aug_m%%&STATION=UKMO_aug_nino4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_sep_m%%&STATION=UKMO_sep_nino4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_oct_m%%&STATION=UKMO_oct_nino4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_nov_m%%&STATION=UKMO_nov_nino4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/ukmo_nino4_dec_m%%&STATION=UKMO_dec_nino4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">NCEP-CFS full ensembles</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jan_m%%&STATION=CFS_jan_nino12_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_feb_m%%&STATION=CFS_feb_nino12_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_mar_m%%&STATION=CFS_mar_nino12_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_apr_m%%&STATION=CFS_apr_nino12_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_may_m%%&STATION=CFS_may_nino12_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jun_m%%&STATION=CFS_jun_nino12_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_jul_m%%&STATION=CFS_jul_nino12_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_aug_m%%&STATION=CFS_aug_nino12_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_sep_m%%&STATION=CFS_sep_nino12_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_oct_m%%&STATION=CFS_oct_nino12_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_nov_m%%&STATION=CFS_nov_nino12_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino12_dec_m%%&STATION=CFS_dec_nino12_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jan_m%%&STATION=CFS_jan_nino3_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_feb_m%%&STATION=CFS_feb_nino3_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_mar_m%%&STATION=CFS_mar_nino3_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_apr_m%%&STATION=CFS_apr_nino3_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_may_m%%&STATION=CFS_may_nino3_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jun_m%%&STATION=CFS_jun_nino3_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_jul_m%%&STATION=CFS_jul_nino3_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_aug_m%%&STATION=CFS_aug_nino3_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_sep_m%%&STATION=CFS_sep_nino3_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_oct_m%%&STATION=CFS_oct_nino3_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_nov_m%%&STATION=CFS_nov_nino3_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3_dec_m%%&STATION=CFS_dec_nino3_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jan_m%%&STATION=CFS_jan_nino3.4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_feb_m%%&STATION=CFS_feb_nino3.4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_mar_m%%&STATION=CFS_mar_nino3.4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_apr_m%%&STATION=CFS_apr_nino3.4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_may_m%%&STATION=CFS_may_nino3.4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jun_m%%&STATION=CFS_jun_nino3.4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_jul_m%%&STATION=CFS_jul_nino3.4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_aug_m%%&STATION=CFS_aug_nino3.4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_sep_m%%&STATION=CFS_sep_nino3.4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_oct_m%%&STATION=CFS_oct_nino3.4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_nov_m%%&STATION=CFS_nov_nino3.4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino3.4_dec_m%%&STATION=CFS_dec_nino3.4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jan_m%%&STATION=CFS_jan_nino4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_feb_m%%&STATION=CFS_feb_nino4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_mar_m%%&STATION=CFS_mar_nino4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_apr_m%%&STATION=CFS_apr_nino4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_may_m%%&STATION=CFS_may_nino4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jun_m%%&STATION=CFS_jun_nino4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_jul_m%%&STATION=CFS_jul_nino4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_aug_m%%&STATION=CFS_aug_nino4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_sep_m%%&STATION=CFS_sep_nino4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_oct_m%%&STATION=CFS_oct_nino4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_nov_m%%&STATION=CFS_nov_nino4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/cfs_nino4_dec_m%%&STATION=CFS_dec_nino4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">ECHAM4.5 full ensembles</th>
</tr><tr>
<td>NINO12</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jan_m%%&STATION=ECHAM5_jan_nino12_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_feb_m%%&STATION=ECHAM5_feb_nino12_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_mar_m%%&STATION=ECHAM5_mar_nino12_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_apr_m%%&STATION=ECHAM5_apr_nino12_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_may_m%%&STATION=ECHAM5_may_nino12_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jun_m%%&STATION=ECHAM5_jun_nino12_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_jul_m%%&STATION=ECHAM5_jul_nino12_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_aug_m%%&STATION=ECHAM5_aug_nino12_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_sep_m%%&STATION=ECHAM5_sep_nino12_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_oct_m%%&STATION=ECHAM5_oct_nino12_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_nov_m%%&STATION=ECHAM5_nov_nino12_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino12_dec_m%%&STATION=ECHAM5_dec_nino12_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jan_m%%&STATION=ECHAM5_jan_nino3_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_feb_m%%&STATION=ECHAM5_feb_nino3_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_mar_m%%&STATION=ECHAM5_mar_nino3_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_apr_m%%&STATION=ECHAM5_apr_nino3_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_may_m%%&STATION=ECHAM5_may_nino3_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jun_m%%&STATION=ECHAM5_jun_nino3_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_jul_m%%&STATION=ECHAM5_jul_nino3_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_aug_m%%&STATION=ECHAM5_aug_nino3_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_sep_m%%&STATION=ECHAM5_sep_nino3_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_oct_m%%&STATION=ECHAM5_oct_nino3_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_nov_m%%&STATION=ECHAM5_nov_nino3_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3_dec_m%%&STATION=ECHAM5_dec_nino3_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO3.4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jan_m%%&STATION=ECHAM5_jan_nino3.4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_feb_m%%&STATION=ECHAM5_feb_nino3.4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_mar_m%%&STATION=ECHAM5_mar_nino3.4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_apr_m%%&STATION=ECHAM5_apr_nino3.4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_may_m%%&STATION=ECHAM5_may_nino3.4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jun_m%%&STATION=ECHAM5_jun_nino3.4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_jul_m%%&STATION=ECHAM5_jul_nino3.4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_aug_m%%&STATION=ECHAM5_aug_nino3.4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_sep_m%%&STATION=ECHAM5_sep_nino3.4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_oct_m%%&STATION=ECHAM5_oct_nino3.4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_nov_m%%&STATION=ECHAM5_nov_nino3.4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino3.4_dec_m%%&STATION=ECHAM5_dec_nino3.4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>NINO4</td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jan_m%%&STATION=ECHAM5_jan_nino4_ensembles&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_feb_m%%&STATION=ECHAM5_feb_nino4_ensembles&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_mar_m%%&STATION=ECHAM5_mar_nino4_ensembles&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_apr_m%%&STATION=ECHAM5_apr_nino4_ensembles&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_may_m%%&STATION=ECHAM5_may_nino4_ensembles&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jun_m%%&STATION=ECHAM5_jun_nino4_ensembles&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_jul_m%%&STATION=ECHAM5_jul_nino4_ensembles&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_aug_m%%&STATION=ECHAM5_aug_nino4_ensembles&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_sep_m%%&STATION=ECHAM5_sep_nino4_ensembles&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_oct_m%%&STATION=ECHAM5_oct_nino4_ensembles&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_nov_m%%&STATION=ECHAM5_nov_nino4_ensembles&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ENSOIndices/echam5_nino4_dec_m%%&STATION=ECHAM5_dec_nino4_ensembles&TYPE=i&id=$EMAIL">dec</a></td>
</tr>
</table>

<div class="alineakop">NAO indices</div>

<table class="realtable" width=451 border='0' cellpadding='0' cellspacing='0'>
<tr>
<th colspan="19">System-1 ensemble mean</th>
</tr><tr>
<td>Iceland-Azores</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%0&STATION=ECMWF_%0_NAO&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%1&STATION=ECMWF_%1_NAO&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%2&STATION=ECMWF_%2_NAO&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%3&STATION=ECMWF_%3_NAO&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%4&STATION=ECMWF_%4_NAO&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%5&STATION=ECMWF_%5_NAO&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jan&STATION=ECMWF_jan_NAO&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_feb&STATION=ECMWF_feb_NAO&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_mar&STATION=ECMWF_mar_NAO&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_apr&STATION=ECMWF_apr_NAO&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_may&STATION=ECMWF_may_NAO&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jun&STATION=ECMWF_jun_NAO&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jul&STATION=ECMWF_jul_NAO&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_aug&STATION=ECMWF_aug_NAO&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_sep&STATION=ECMWF_sep_NAO&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_oct&STATION=ECMWF_oct_NAO&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_nov&STATION=ECMWF_nov_NAO&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_dec&STATION=ECMWF_dec_NAO&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Iceland-Gibraltar</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%0&STATION=ECMWF_%0_NAO_Gib&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%1&STATION=ECMWF_%1_NAO_Gib&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%2&STATION=ECMWF_%2_NAO_Gib&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%3&STATION=ECMWF_%3_NAO_Gib&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%4&STATION=ECMWF_%4_NAO_Gib&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%5&STATION=ECMWF_%5_NAO_Gib&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jan&STATION=ECMWF_jan_NAO_Gib&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_feb&STATION=ECMWF_feb_NAO_Gib&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_mar&STATION=ECMWF_mar_NAO_Gib&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_apr&STATION=ECMWF_apr_NAO_Gib&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_may&STATION=ECMWF_may_NAO_Gib&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jun&STATION=ECMWF_jun_NAO_Gib&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jul&STATION=ECMWF_jul_NAO_Gib&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_aug&STATION=ECMWF_aug_NAO_Gib&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_sep&STATION=ECMWF_sep_NAO_Gib&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_oct&STATION=ECMWF_oct_NAO_Gib&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_nov&STATION=ECMWF_nov_NAO_Gib&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_dec&STATION=ECMWF_dec_NAO_Gib&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Pattern-based</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%0&STATION=ECMWF_%0_NAO_pat&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%1&STATION=ECMWF_%1_NAO_pat&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%2&STATION=ECMWF_%2_NAO_pat&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%3&STATION=ECMWF_%3_NAO_pat&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%4&STATION=ECMWF_%4_NAO_pat&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%5&STATION=ECMWF_%5_NAO_pat&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jan&STATION=ECMWF_jan_NAO_pat&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_feb&STATION=ECMWF_feb_NAO_pat&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_mar&STATION=ECMWF_mar_NAO_pat&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_apr&STATION=ECMWF_apr_NAO_pat&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_may&STATION=ECMWF_may_NAO_pat&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jun&STATION=ECMWF_jun_NAO_pat&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jul&STATION=ECMWF_jul_NAO_pat&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_aug&STATION=ECMWF_aug_NAO_pat&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_sep&STATION=ECMWF_sep_NAO_pat&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_oct&STATION=ECMWF_oct_NAO_pat&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_nov&STATION=ECMWF_nov_NAO_pat&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_dec&STATION=ECMWF_dec_NAO_pat&TYPE=i&id=$EMAIL">dec</a></td>

</tr><tr>
<th colspan="19">System-2 ensemble mean</th>
</tr><tr>
<td>Iceland-Azores</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%0&STATION=ECMWF2_%0_NAO&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%1&STATION=ECMWF2_%1_NAO&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%2&STATION=ECMWF2_%2_NAO&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%3&STATION=ECMWF2_%3_NAO&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%4&STATION=ECMWF2_%4_NAO&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%5&STATION=ECMWF2_%5_NAO&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jan&STATION=ECMWF2_jan_NAO&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_feb&STATION=ECMWF2_feb_NAO&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_mar&STATION=ECMWF2_mar_NAO&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_apr&STATION=ECMWF2_apr_NAO&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_may&STATION=ECMWF2_may_NAO&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jun&STATION=ECMWF2_jun_NAO&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jul&STATION=ECMWF2_jul_NAO&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_aug&STATION=ECMWF2_aug_NAO&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_sep&STATION=ECMWF2_sep_NAO&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_oct&STATION=ECMWF2_oct_NAO&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_nov&STATION=ECMWF2_nov_NAO&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_dec&STATION=ECMWF2_dec_NAO&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Iceland-Gibraltar</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%0&STATION=ECMWF2_%0_NAO_Gib&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%1&STATION=ECMWF2_%1_NAO_Gib&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%2&STATION=ECMWF2_%2_NAO_Gib&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%3&STATION=ECMWF2_%3_NAO_Gib&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%4&STATION=ECMWF2_%4_NAO_Gib&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%5&STATION=ECMWF2_%5_NAO_Gib&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jan&STATION=ECMWF2_jan_NAO_Gib&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_feb&STATION=ECMWF2_feb_NAO_Gib&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_mar&STATION=ECMWF2_mar_NAO_Gib&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_apr&STATION=ECMWF2_apr_NAO_Gib&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_may&STATION=ECMWF2_may_NAO_Gib&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jun&STATION=ECMWF2_jun_NAO_Gib&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jul&STATION=ECMWF2_jul_NAO_Gib&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_aug&STATION=ECMWF2_aug_NAO_Gib&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_sep&STATION=ECMWF2_sep_NAO_Gib&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_oct&STATION=ECMWF2_oct_NAO_Gib&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_nov&STATION=ECMWF2_nov_NAO_Gib&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_dec&STATION=ECMWF2_dec_NAO_Gib&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Pattern-based</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%0&STATION=ECMWF2_%0_NAO_pat&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%1&STATION=ECMWF2_%1_NAO_pat&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%2&STATION=ECMWF2_%2_NAO_pat&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%3&STATION=ECMWF2_%3_NAO_pat&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%4&STATION=ECMWF2_%4_NAO_pat&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%5&STATION=ECMWF2_%5_NAO_pat&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jan&STATION=ECMWF2_jan_NAO_pat&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_feb&STATION=ECMWF2_feb_NAO_pat&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_mar&STATION=ECMWF2_mar_NAO_pat&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_apr&STATION=ECMWF2_apr_NAO_pat&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_may&STATION=ECMWF2_may_NAO_pat&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jun&STATION=ECMWF2_jun_NAO_pat&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jul&STATION=ECMWF2_jul_NAO_pat&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_aug&STATION=ECMWF2_aug_NAO_pat&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_sep&STATION=ECMWF2_sep_NAO_pat&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_oct&STATION=ECMWF2_oct_NAO_pat&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_nov&STATION=ECMWF2_nov_NAO_pat&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_dec&STATION=ECMWF2_dec_NAO_pat&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<th colspan="19">System-1 full ensembles</th>
</tr><tr>
<td>Iceland-Azores</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%0_%%&STATION=ECMWF_%0_ensemble_NAO&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%1_%%&STATION=ECMWF_%1_ensemble_NAO&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%2_%%&STATION=ECMWF_%2_ensemble_NAO&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%3_%%&STATION=ECMWF_%3_ensemble_NAO&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%4_%%&STATION=ECMWF_%4_ensemble_NAO&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_%5_%%&STATION=ECMWF_%5_ensemble_NAO&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jan_%%&STATION=ECMWF_jan_ensemble_NAO&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_feb_%%&STATION=ECMWF_feb_ensemble_NAO&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_mar_%%&STATION=ECMWF_mar_ensemble_NAO&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_apr_%%&STATION=ECMWF_apr_ensemble_NAO&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_may_%%&STATION=ECMWF_may_ensemble_NAO&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jun_%%&STATION=ECMWF_jun_ensemble_NAO&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_jul_%%&STATION=ECMWF_jul_ensemble_NAO&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_aug_%%&STATION=ECMWF_aug_ensemble_NAO&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_sep_%%&STATION=ECMWF_sep_ensemble_NAO&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_oct_%%&STATION=ECMWF_oct_ensemble_NAO&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_nov_%%&STATION=ECMWF_nov_ensemble_NAO&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IA_dec_%%&STATION=ECMWF_dec_ensemble_NAO&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Iceland-Gibraltar</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%0_%%&STATION=ECMWF_%0_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%1_%%&STATION=ECMWF_%1_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%2_%%&STATION=ECMWF_%2_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%3_%%&STATION=ECMWF_%3_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%4_%%&STATION=ECMWF_%4_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_%5_%%&STATION=ECMWF_%5_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jan_%%&STATION=ECMWF_jan_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_feb_%%&STATION=ECMWF_feb_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_mar_%%&STATION=ECMWF_mar_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_apr_%%&STATION=ECMWF_apr_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_may_%%&STATION=ECMWF_may_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jun_%%&STATION=ECMWF_jun_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_jul_%%&STATION=ECMWF_jul_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_aug_%%&STATION=ECMWF_aug_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_sep_%%&STATION=ECMWF_sep_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_oct_%%&STATION=ECMWF_oct_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_nov_%%&STATION=ECMWF_nov_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_IG_dec_%%&STATION=ECMWF_dec_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Pattern-based</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%0_%%&STATION=ECMWF_%0_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%1_%%&STATION=ECMWF_%1_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%2_%%&STATION=ECMWF_%2_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%3_%%&STATION=ECMWF_%3_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%4_%%&STATION=ECMWF_%4_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_%5_%%&STATION=ECMWF_%5_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jan_%%&STATION=ECMWF_jan_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_feb_%%&STATION=ECMWF_feb_ensemble_NAO_pat&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_mar_%%&STATION=ECMWF_mar_ensemble_NAO_pat&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_apr_%%&STATION=ECMWF_apr_ensemble_NAO_pat&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_may_%%&STATION=ECMWF_may_ensemble_NAO_pat&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jun_%%&STATION=ECMWF_jun_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_jul_%%&STATION=ECMWF_jul_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_aug_%%&STATION=ECMWF_aug_ensemble_NAO_pat&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_sep_%%&STATION=ECMWF_sep_ensemble_NAO_pat&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_oct_%%&STATION=ECMWF_oct_ensemble_NAO_pat&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_nov_%%&STATION=ECMWF_nov_ensemble_NAO_pat&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf_nao_pat_dec_%%&STATION=ECMWF_dec_ensemble_NAO_pat&TYPE=i&id=$EMAIL">dec</a></td>
</tr>
<th colspan="19">System-2 full ensembles</th>
</tr><tr>
<td>Iceland-Azores</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%0_%%&STATION=ECMWF2_%0_ensemble_NAO&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%1_%%&STATION=ECMWF2_%1_ensemble_NAO&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%2_%%&STATION=ECMWF2_%2_ensemble_NAO&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%3_%%&STATION=ECMWF2_%3_ensemble_NAO&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%4_%%&STATION=ECMWF2_%4_ensemble_NAO&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_%5_%%&STATION=ECMWF2_%5_ensemble_NAO&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jan_%%&STATION=ECMWF2_jan_ensemble_NAO&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_feb_%%&STATION=ECMWF2_feb_ensemble_NAO&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_mar_%%&STATION=ECMWF2_mar_ensemble_NAO&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_apr_%%&STATION=ECMWF2_apr_ensemble_NAO&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_may_%%&STATION=ECMWF2_may_ensemble_NAO&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jun_%%&STATION=ECMWF2_jun_ensemble_NAO&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_jul_%%&STATION=ECMWF2_jul_ensemble_NAO&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_aug_%%&STATION=ECMWF2_aug_ensemble_NAO&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_sep_%%&STATION=ECMWF2_sep_ensemble_NAO&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_oct_%%&STATION=ECMWF2_oct_ensemble_NAO&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_nov_%%&STATION=ECMWF2_nov_ensemble_NAO&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IA_dec_%%&STATION=ECMWF2_dec_ensemble_NAO&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Icealnd-Gibraltar</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%0_%%&STATION=ECMWF2_%0_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%1_%%&STATION=ECMWF2_%1_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%2_%%&STATION=ECMWF2_%2_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%3_%%&STATION=ECMWF2_%3_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%4_%%&STATION=ECMWF2_%4_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_%5_%%&STATION=ECMWF2_%5_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jan_%%&STATION=ECMWF2_jan_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_feb_%%&STATION=ECMWF2_feb_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_mar_%%&STATION=ECMWF2_mar_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_apr_%%&STATION=ECMWF2_apr_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_may_%%&STATION=ECMWF2_may_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jun_%%&STATION=ECMWF2_jun_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_jul_%%&STATION=ECMWF2_jul_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_aug_%%&STATION=ECMWF2_aug_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_sep_%%&STATION=ECMWF2_sep_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_oct_%%&STATION=ECMWF2_oct_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_nov_%%&STATION=ECMWF2_nov_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_IG_dec_%%&STATION=ECMWF2_dec_ensemble_NAO_Gib&TYPE=i&id=$EMAIL">dec</a></td>
</tr><tr>
<td>Pattern-based</td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%0_%%&STATION=ECMWF2_%0_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+0</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%1_%%&STATION=ECMWF2_%1_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+1</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%2_%%&STATION=ECMWF2_%2_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+2</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%3_%%&STATION=ECMWF2_%3_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+3</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%4_%%&STATION=ECMWF2_%4_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+4</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_%5_%%&STATION=ECMWF2_%5_ensemble_NAO_pat&TYPE=i&id=$EMAIL">+5</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jan_%%&STATION=ECMWF2_jan_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jan</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_feb_%%&STATION=ECMWF2_feb_ensemble_NAO_pat&TYPE=i&id=$EMAIL">feb</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_mar_%%&STATION=ECMWF2_mar_ensemble_NAO_pat&TYPE=i&id=$EMAIL">mar</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_apr_%%&STATION=ECMWF2_apr_ensemble_NAO_pat&TYPE=i&id=$EMAIL">apr</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_may_%%&STATION=ECMWF2_may_ensemble_NAO_pat&TYPE=i&id=$EMAIL">may</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jun_%%&STATION=ECMWF2_jun_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jun</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_jul_%%&STATION=ECMWF2_jul_ensemble_NAO_pat&TYPE=i&id=$EMAIL">jul</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_aug_%%&STATION=ECMWF2_aug_ensemble_NAO_pat&TYPE=i&id=$EMAIL">aug</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_sep_%%&STATION=ECMWF2_sep_ensemble_NAO_pat&TYPE=i&id=$EMAIL">sep</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_oct_%%&STATION=ECMWF2_oct_ensemble_NAO_pat&TYPE=i&id=$EMAIL">oct</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_nov_%%&STATION=ECMWF2_nov_ensemble_NAO_pat&TYPE=i&id=$EMAIL">nov</a></td>
<td><a href="getindices.cgi?WMO=ECMWFData/ecmwf2_nao_pat_dec_%%&STATION=ECMWF2_dec_ensemble_NAO_pat&TYPE=i&id=$EMAIL">dec</a></td>
</tr>
</table>
EOF

. ./myvinkfoot.cgi
