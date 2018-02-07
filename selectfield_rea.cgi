#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi

. ./myvinkhead.cgi "Select a monthly field" "Reanalyses" "index,nofollow"
cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="8"><input type="submit" class="formbutton" value="Select field"> Open a section, select a field and press this button</th></tr>
EOF

if [ -n "$ROBOT" ]; then
    hiddenstyle_erainterim=""
    hiddenstyle_era5=""
    hiddenstyle_merra=""
    hiddenstyle_cfsr=""
    hiddenstyle_jra=""
    hiddenstyle_ncepncar=""
    hiddenstyle_ncepdoe=""
    hiddenstyle_20c=""
    hiddenstyle_era20c=""
else
    hiddenstyle_erainterim="style=\"display: none;\""
    hiddenstyle_era5="style=\"display: none;\""
    hiddenstyle_merra="style=\"display: none;\""
    hiddenstyle_cfsr="style=\"display: none;\""
    hiddenstyle_jra="style=\"display: none;\""
    hiddenstyle_ncepncar="style=\"display: none;\""
    hiddenstyle_ncepdoe="style=\"display: none;\""
    hiddenstyle_20c="style=\"display: none;\""
    hiddenstyle_era20c="style=\"display: none;\""
fi
if [ -s prefs/$EMAIL.field.12 ]; then
    eval `egrep '^FORM_field=[-_a-zA-Z0-9]*;$' ./prefs/$EMAIL.field.12`
    if [ -n "$FORM_field" ]; then
	. ./queryfield.cgi
	case $kindname in
	    ERA-int) hiddenstyle_erainterim="";;
	    ERA5) hiddenstyle_era5="";;
	    MERRA) hiddenstyle_merra="";;
	    CFSR) hiddenstyle_cfsr="";;
	    JRA) hiddenstyle_jra="";;
	    NCEP/NCAR) hiddenstyle_ncepncar="";;
	    NCEP/DOE) hiddenstyle_ncepdoe="";;
	    20C) hiddenstyle_20c="";;
	    ERA-20C) hiddenstyle_era20c="";;
	esac
    fi
fi

sed -e "s/hiddenstyle_erainterim/$hiddenstyle_erainterim/" \
    -e "s/hiddenstyle_era5/$hiddenstyle_era5/" \
    -e "s/hiddenstyle_merra/$hiddenstyle_merra/" \
    -e "s/hiddenstyle_cfsr/$hiddenstyle_cfsr/" \
    -e "s/hiddenstyle_jra/$hiddenstyle_jra/" \
    -e "s/hiddenstyle_ncepncar/$hiddenstyle_ncepncar/" \
    -e "s/hiddenstyle_ncepdoe/$hiddenstyle_ncepdoe/" \
    -e "s/hiddenstyle_20c/$hiddenstyle_20c/" \
    -e "s/hiddenstyle_era20c/$hiddenstyle_era20c/" \
    -e "s/value=\"$FORM_field\"/value=\"$FORM_field\" checked/" \
    ./selectfield_rea.html

cat <<EOF
</table>
EOF

. ./myvinkfoot.cgi
