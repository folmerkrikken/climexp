#!/bin/sh
. ./init.cgi
# to be sourced from other scripts
# common options for lots of plots

if [ "$EMAIL" != somene@somewhere ]; then
  if [ -n "$DIR" ]; then
    def=$DIR/prefs/$EMAIL.plotoptions
  else
    def=prefs/$EMAIL.plotoptions
  fi
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
  fi
fi

case "$FORM_mproj" in
latlon)    mproj_latlon="selected";;
nps)       mproj_nps="selected";;
sps)       mproj_sps="selected";;
robinson)  mproj_robinson="selected";;
mollweide) mproj_mollweide="selected";;
lambert)   mproj_lambert="selected";;
*)         mproj_default="selected";;
esac

case "$FORM_maskout" in
light)   light_selected="selected";;
lighter) lighter_selected="selected";;
*)       mask_selected="selected";;
esac

case "$FORM_colourscale" in
0) colourscale_0="selected";;
1) colourscale_1="selected";;
3) colourscale_3="selected";;
2) colourscale_2="selected";;
9) colourscale_9="selected";;
8) colourscale_8="selected";;
11) colourscale_11="selected";;
13) colourscale_13="selected";;
12) colourscale_12="selected";;
19) colourscale_19="selected";;
18) colourscale_18="selected";;
*) colourscale_10="selected";;
esac

case "$FORM_shadingtype" in
contour) shadingtype_contour="checked";;
grfill)  shadingtype_grfill="checked";;
shadedcontour)       shadingtype_shadedcontour="checked";;
*)  shadingtype_shaded="checked";;
esac

case "$FORM_intertype" in
high)intertype_high="checked";;
low) intertype_low="checked";;
1)   intertype_1="checked";;
2)   intertype_2="checked";;
*)   intertype_high="checked";;
esac

if [ -n "$FORM_yflip" ]; then
  yflip_checked=checked
fi
if [ -n "$FORM_nocbar" ]; then
  nocbar_checked=checked
fi
if [ -n "$FORM_notitleonplot" ]; then
  notitleonplot_checked=checked
fi
if [ -n "$FORM_nogrid" ]; then
  nogrid_checked=checked
fi
if [ -n "$FORM_nolab" ]; then
  nolab_checked=checked
fi

case ${FORM_masktype:-all} in
5lan) hlan_checked="checked";;
5sea) hsea_checked="checked";;
land) land_checked="checked";;
sea)  sea_checked="checked";;
notl) notl_checked="checked";;
nots) nots_checked="checked";;
*)    all_checked="checked";;
esac

if [ -n "$FORM_standardunits" -o -z "$FORM_var" ]; then
  standardunits_checked="checked"
else
  standardunits_unchecked="checked"
fi

echo '<tr><td>Map type:<td>'
cat <<EOF
<select class="forminput" name="mproj">
<option value="default" $mproj_default>default
<option value="latlon" $mproj_latlon>lat-lon
<option value="nps" $mproj_nps>North polar stereographic
<option value="sps" $mproj_sps>South polar stereographic
<option value="robinson" $mproj_robinson>Robinson
<option value="mollweide" $mproj_mollweide>Mollweide
<option value="lambert" $mproj_lambert>Lambert
</select> projection
EOF
echo "<td><a href=\"javascript:pop_page('help/maptype.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
if [ -z "$tworegions" ]; then
    echo '<tr valign="baseline"><td>Region:<td>'
else
    echo '<tr valign="baseline"><td>Region first field:<td>'
fi
if [ -z "$NX" -a -z "$NY" -a -z "$NY" ]; then
  eval `bin/getunits.sh $file | egrep v 'warning|error|getfileunits'`
fi
if [ -z "$NY" -o "${NY:-0}" -gt 1 ]; then
cat <<EOF
<input type="$number" step=any class="forminput" name="lat1" value="$FORM_lat1" $textsize4>&deg;N 
to
<input type="$number" step=any class="forminput" name="lat2" value="$FORM_lat2" $textsize4>&deg;N, 
EOF
fi
if [ -z "$NX" -o "${NX:-0}" -gt 1 ]; then
cat <<EOF
<input type="$number" step=any class="forminput" name="lon1" value="$FORM_lon1" $textsize4>&deg;E 
to
<input type="$number" step=any class="forminput" name="lon2" value="$FORM_lon2" $textsize4>&deg;E
EOF
fi
if [ "${NZ:-1}" -gt 1 ]; then
cat <<EOF
, level <input type="$number" step=any class="forminput" name="lev1" value="$FORM_lev1" $textsize4> 
to
<input type="$number" step=any class="forminput" name="lev2" value="$FORM_lev2" $textsize4>,<br>
<input type="checkbox" class="formcheck" name="yflip" $yflip_checked>flip Z-axis
EOF
fi
if [ -n "$tworegions" ]; then
    cat <<EOF
<tr><td>Region second field:<td>
<input type="$number" step=any class="forminput" name="altlat1" value="$FORM_altlat1" $textsize4>&deg;N 
to
<input type="$number" step=any class="forminput" name="altlat2" value="$FORM_altlat2" $textsize4>&deg;N, 
<input type="$number" step=any class="forminput" name="altlon1" value="$FORM_altlon1" $textsize4>&deg;E 
to
<input type="$number" step=any class="forminput" name="altlon2" value="$FORM_altlon2" $textsize4>&deg;E
EOF
fi
if [ -z "$latlononly" -a "${NZ:-1}" -le 1 ]; then
cat <<EOF
in a <select class="forminput" name="plottype">
<option>lat-lon
<option>time-lon
<option>time-lat
</select> plot
EOF
fi
echo "<td><a href=\"javascript:pop_page('help/region.shtml',568,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
echo '<tr><td>Contours:<td>'
cat <<EOF
<input type="$number" step=any class="forminput" name="cmin" value="$FORM_cmin" $textsize6>
to
<input type="$number" step=any class="forminput" name="cmax" value="$FORM_cmax" $textsize6>
EOF
if [ -n "$probmask" ]; then
echo "<select class=forminput name=maskout><option value=mask $mask_selected>mask out<option value=light $light_selected>make light<option value=lighter $lighter_selected>make lighter</select>: p&gt;<input type=\"$number\" step=any class=\"forminput\" name=\"pmin\" value="${FORM_pmin:-10}" $textsize3>%"
fi
echo "<td><a href=\"javascript:pop_page('help/contour.shtml',852,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
echo '<tr><td>Colours:<td>' 
cat <<EOF
<select class="forminput" name="colourscale">
<option value="10" $colourscale_10>blue-grey-red
<option value="11" $colourscale_11>red-grey-blue
<option value="13" $colourscale_13>grey-red
<option value="12" $colourscale_12>grey-blue
<option value="14" $colourscale_14>grey-blue-red
<option value="18" $colourscale_18>red-grey
<option value="19" $colourscale_19>blue-grey
<option value="0" $colourscale_0>old blue-grey-red
<option value="1" $colourscale_1>old red-grey-blue
<option value="3" $colourscale_3>old grey-blue-red
<option value="2" $colourscale_2>old grey-red-blue
<option value="9" $colourscale_9>old blue-red-grey
<option value="8" $colourscale_8>old red-blue-grey
</select>
EOF
echo "<td><a href=\"javascript:pop_page('help/colours.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
echo '<tr><td>Shading:<td>'
cat <<EOF
<input type="radio" class="formradio" name="shadingtype" value="shadedcontour" $shadingtype_shadedcontour>shading and contours
<input type="radio" class="formradio" name="shadingtype" value="shaded" $shadingtype_shaded>shading
<input type="radio" class="formradio" name="shadingtype" value="contour" $shadingtype_contour>contours
<input type="radio" class="formradio" name="shadingtype" value="grfill" $shadingtype_grfill>grid boxes
EOF
echo "<td><a href=\"javascript:pop_page('help/shading.shtml',568,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
echo '<tr><td>Plot options:<td>'
cat <<EOF
<input type="checkbox" class="formcheck" name="nocbar" $nocbar_checked>no color bar&nbsp;&nbsp;
<input type="checkbox" class="formcheck" name="notitleonplot" $notitleonplot_checked>no title on plot,&nbsp;&nbsp;
<input type="checkbox" class="formcheck" name="nogrid" $nogrid_checked>no grid
EOF
echo "<td><a href=\"javascript:pop_page('help/plotoptions.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
echo '<tr><td><td>'
cat <<EOF
label distance <input type="$number" step=any class="forminput" name="xlint" value="$FORM_xlint" $textsize2>&times;<input type="$number" step=any class="forminput" name="ylint" value="$FORM_ylint" $textsize2>&deg; or <input type="checkbox" class="formcheck" name="nolab" $nolab_checked>no labels
EOF
echo '<tr><td>Output to:<td>'
cat <<EOF
<input type="radio" class="formradio" name="mapformat" value="png" checked>browser <!--(png/eps/pdf)-->
<input type="radio" class="formradio" name="mapformat" value="kml">Google Earth (kml)
<input type="radio" class="formradio" name="mapformat" value="geotiff">GIS (geotiff)
EOF
echo "<td><a href=\"javascript:pop_page('help/plotoutput.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"

if [ "$interpolate" = "true" ]; then
  echo '<tr><td>Interpolate:<td>'
  cat << EOF
<select class="forminput" name="intertype">
<option value="high" $intertype_high>finest
<option value="low" $intertype_low>coarsest
<option value="1" $intertype_1>first
<option value="2" $intertype_2>second
</select> grid
EOF
echo "<td><a href=\"javascript:pop_page('help/interpolate.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi

if [ -n "$LSMASK" -a "$lsmask" = yes ]; then
  echo '<tr><td>Show:<td>'
  cat <<EOF
<input type="radio" class="formradio" name ="masktype" value="all" $all_checked>everything
<input type="radio" class="formradio" name ="masktype" value="5lan" $hlan_checked>only land points
<input type="radio" class="formradio" name ="masktype" value="5sea" $hsea_checked>only sea points
EOF
echo "<td><a href=\"javascript:pop_page('help/labdsea.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi
if [ -z "$replot" ]; then
  if [ -n "$NEWUNITS" ]; then
    if [ "$UNITS" != "$NEWUNITS" ]; then
      echo '<tr><td>Units:<td>'
      cat <<EOF
<input type="radio" class="formradio" name ="standardunits" value="standardunits" $standardunits_checked>convert to $NEWUNITS
<input type="radio" class="formradio" name ="standardunits" value="" $standardunits_unchecked>leave in $UNITS
EOF
      echo "<td><a href=\"javascript:pop_page('help/convertunits.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
    fi
  else
    echo '<tr><td>Units:<td>'
    cat <<EOF
<input type="radio" class="formradio" name ="standardunits" value="standardunits" $standardunits_checked>convert to standard units
<input type="radio" class="formradio" name ="standardunits" value="" $standardunits_unchecked>use original units
EOF
    echo "<td><a href=\"javascript:pop_page('help/convertunits.shtml',284,450)\"><img src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
  fi
fi
