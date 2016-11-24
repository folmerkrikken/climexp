#!/bin/sh
if [ -n "$EMAIL" ]; then
if [ -n "$field2" ]; then
echo "<div class=\"menukopje\">Investigate $kindname $climfield</div>"
else
echo "<div class=\"menukopje\">Investigate this field</div>"
fi
###echo "<div class=\"menulink\"><a href=\"select.cgi?id=$EMAIL&field=$FORM_field\">Information, time series, download</a></div>"
if [ -z "$ENSEMBLE" ]; then
  echo "<div class=\"menulink\"><a href=\"plotform.cgi?id=$EMAIL&field=$FORM_field\">Plot this field</a></div>"
fi
cat <<EOF
<div class="menulink"><a href="difffieldform.cgi?id=$EMAIL&field=$FORM_field">Plot difference with a field</a></div>
<div class="menulink"><a href="getmomentsfieldform.cgi?id=$EMAIL&field=$FORM_field">Compute mean, s.d. or extremes</a></div>
<div class="menulink"><a href="attributeform.cgi?id=$EMAIL&field=$FORM_field">Trends in extremes</a></div>
<div class="menulink"><a href="eofform.cgi?id=$EMAIL&field=$FORM_field">Make EOFs</a></div>
<div class="menulink"><a href="fieldcorrseries.cgi?id=$EMAIL&field=$FORM_field">Correlate with a time series</a></div>
<div class="menulink"><a href="fieldcorrfield.cgi?id=$EMAIL&field=$FORM_field">Pointwise correlations with a field</a>
<div class="menulink"><a href="fieldcorrfield_obs.cgi?id=$EMAIL&field=$FORM_field">only observations</a></div>
<div class="menulink"><a href="fieldcorrfield_rea.cgi?id=$EMAIL&field=$FORM_field">only reanalyses</a></div>
<div class="menulink"><a href="fieldcorrfield_sea.cgi?id=$EMAIL&field=$FORM_field">only seasonal hindcasts</a></div>
<div class="menulink"><a href="fieldcorrfield_dec.cgi?id=$EMAIL&field=$FORM_field">only decadal hindcasts</a></div>
<div class="menulink"><a href="fieldcorrfield_cmip5.cgi?id=$EMAIL&field=$FORM_field">only CMIP5 scenario runs</a></div>
<div class="menulink"><a href="fieldcorrfield_use.cgi?id=$EMAIL&field=$FORM_field">only user-defined fields</a></div>
</div>
<div class="menulink"><a href="fieldcorrfield1.cgi?id=$EMAIL&field=$FORM_field">Spatial correlations with a field</a>
<div class="menulink"><a href="fieldcorrfield1_obs.cgi?id=$EMAIL&field=$FORM_field">only observations</a></div>
<div class="menulink"><a href="fieldcorrfield1_rea.cgi?id=$EMAIL&field=$FORM_field">only reanalyses</a></div>
<div class="menulink"><a href="fieldcorrfield1_sea.cgi?id=$EMAIL&field=$FORM_field">only seasonal hindcasts</a></div>
<div class="menulink"><a href="fieldcorrfield1_dec.cgi?id=$EMAIL&field=$FORM_field">only decadal hindcasts</a></div>
<div class="menulink"><a href="fieldcorrfield1_cmip5.cgi?id=$EMAIL&field=$FORM_field">only CMIP5 scenario runs</a></div>
<div class="menulink"><a href="fieldcorrfield1_use.cgi?id=$EMAIL&field=$FORM_field">only user-defined fields</a></div>
</div>
<div class="menulink"><a href="svdform.cgi?id=$EMAIL&field=$FORM_field">SVD</a>
<div class="menulink"><a href="svdform_obs.cgi?id=$EMAIL&field=$FORM_field">only observations</a></div>
<div class="menulink"><a href="svdform_rea.cgi?id=$EMAIL&field=$FORM_field">only reanalyses</a></div>
<div class="menulink"><a href="svdform_sea.cgi?id=$EMAIL&field=$FORM_field">only seasonal hindcasts</a></div>
<div class="menulink"><a href="svdform_cmip5.cgi?id=$EMAIL&field=$FORM_field">only CMIP5 scenario runs</a></div>
<div class="menulink"><a href="svdform_use.cgi?id=$EMAIL&field=$FORM_field">only user-defined fields</a></div>
</div>
<div class="menulink"><a href="regionverificationform.cgi?id=$EMAIL&field=$FORM_field">Verify field against observations</a></div>
EOF
if [ -n "$NX" -a -n "$NY" ]; then
    if [ $((NX*NY)) -le 1000 ]; then
        cat <<EOF
<div class="menulink"><a href="attributeform.cgi?id=$EMAIL&field=${FORM_field}&TYPE=gridpoints&NPERYEAR=${NPERYEAR}">Trends in return times of extremes of all grid points</a></div>
EOF
    fi
fi
cat <<EOF
</ul>
EOF
fi

