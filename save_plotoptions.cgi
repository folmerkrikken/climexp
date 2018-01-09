#!/bin/sh
if [ "$FORM_EMAIL" != someone@somewhere ]; then
# remember plotoptions for next plot
###echo "saving preferences in ./prefs/$FORM_EMAIL.plotoptions"
cat > ./prefs/$FORM_EMAIL.plotoptions <<EOF
FORM_mproj=$FORM_mproj;
FORM_lat1=$FORM_lat1;
FORM_lat2=$FORM_lat2;
FORM_lon1=$FORM_lon1;
FORM_lon2=$FORM_lon2;
FORM_lev1=$FORM_lev1;
FORM_lev2=$FORM_lev2;
FORM_altlat1=$FORM_altlat1;
FORM_altlat2=$FORM_altlat2;
FORM_altlon1=$FORM_altlon1;
FORM_altlon2=$FORM_altlon2;
FORM_plottype=$FORM_plottype;
FORM_cmin=$FORM_cmin;
FORM_cmax=$FORM_cmax;
FORM_maskout=$FORM_maskout;
FORM_pmin=$FORM_pmin;
FORM_colourscale=$FORM_colourscale;
FORM_shadingtype=$FORM_shadingtype;
FORM_yflip=$FORM_yflip;
FORM_notitleonplot=$FORM_notitleonplot;
FORM_nogrid=$FORM_nogrid;
FORM_nopoli=$FORM_nopoli;
FORM_nolab=$FORM_nolab;
FORM_nocbar=$FORM_nocbar;
FORM_xlint=$FORM_xlint;
FORM_ylint=$FORM_ylint;
FORM_intertype=$FORM_intertype;
FORM_masktype=$FORM_masktype;
FORM_standardunits=$FORM_standardunits;
FORM_log=$FORM_log;
EOF
fi
