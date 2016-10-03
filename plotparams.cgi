#!/bin/sh
# to be sourced from other scripts

# retrieve last values as defaults
if [ $EMAIL != someone@somewhere ]; then
    if [ -n "$DIR" ]; then
        def=$DIR/prefs/$EMAIL.plotstations
    else
        def=./prefs/$EMAIL.plotstations
    fi
    if [ -s $def ]; then
        eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
    fi

    if [ "$FORM_var" = "sign" ]; then
        var_sign="checked"
    else
        var_val="checked"
    fi

    if [ "$FORM_value" = "on" ]; then
        value="checked"
    fi
    if [ "$FORM_code" = "on" ]; then
        code="checked"
    fi
    if [ "$FORM_name" = "on" ]; then
        name="checked"
    fi

    case "$FORM_col" in
        bw)         col_bw="checked";;
        flipbw)     col_flipbw="checked";;
        rb)         col_rb="checked";;
        br)         col_br="checked";;
        colour)     col_colour="checked";;
        flipcolour) col_flipcolour="checked";;
        color)      col_color="checked";;
        flipcolor)  col_flipcolor="checked";;
        *)          col_rb="checked";;
    esac

    case "$FORM_mproj" in
        latlon)    mproj_latlon="selected";;
        nps)       mproj_nps="selected";;
        sps)       mproj_sps="selected";;
        robinson)  mproj_robinson="selected";;
        mollweide) mproj_mollweide="selected";;
        lambert)   mproj_lambert="selected";;
        *)         mproj_default="selected";;
    esac

    if [ -n "$FORM_nocbar" ]; then
        nocbar_checked=checked
    fi
    if [ -n "$FORM_notitleonplot" ]; then
        notitleonplot_checked=checked
    fi
    if [ -n "$FORM_nogrid" ]; then
        nogrid_checked=checked
    fi
    if [ -n "$FORM_nopoli" ]; then
        nopoli_checked=checked
    fi
fi # nonimous user?

# generate form
cat <<EOF
<a name=\"plotoptions\"></a><div class="formheader">Plot options</div>
<div class="formbody">
<form action="plotstations.cgi" method="post">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="climate" value="$FORM_climate">
<input type="hidden" name="shortclimate" value="$FORM_shortclimate">
<input type="hidden" name="prog" value="$FORM_prog">
<input type="hidden" name="listname" value="$FORM_listname">
<input type="hidden" name="extraargs" value="$FORM_extraargs">
<input type="hidden" name="oper" value="$oper">
<table width="100%" cellpadding=0 cellspacing=0 border=0>
<tr>
<td>Title:</td><td><input type="text" class="forminput" name="title" size="45" value="$title"></td>
</tr><tr>
<td>Scale:</td><td><input type="text" class="forminput" name="scale" size="4"  value="${FORM_scale:-1}"></td>
</tr><tr>
<td>Plot:</td><td>
<input type="radio" class="formradio" name="var" value="val" $var_val>value
<input type="radio" class="formradio" name="var" value="sign" $var_sign>significance</td>
</tr><tr>
<td>Write:</td><td>
<input type="checkbox" class="formcheck" name="value" $value>value, 
<input type="checkbox" class="formcheck" name="code" $code>station code, 
<input type="checkbox" class="formcheck" name="name" $name>station name</td>
</tr><tr>
<td>Colour:</td><td>
<input type="radio" class="formradio" name="col" value="bw" $col_bw>black/white
<input type="radio" class="formradio" name="col" value="flipbw" $col_flipbw>white/black
</td></tr><tr><td>&nbsp;</td><td>
<input type="radio" class="formradio" name="col" value="rb" $col_rb>red/blue
<input type="radio" class="formradio" name="col" value="br" $col_br>blue/red
</td></tr><tr><td>&nbsp;</td><td>
<input type="radio" class="formradio" name="col" value="colour" $col_colour>rainbow (blue-red)
<input type="radio" class="formradio" name="col" value="flipcolour" $col_flipcolour>rainbow (red-blue)
Range: <!--input type="text" class="forminput" name="cmin" size="4" value="-0.6"-->
to <input type="text" class="forminput" name="cmax" size="4" value="${FORM_cmax:-0.6}">
</td></tr><tr><td>&nbsp;</td><td>
<input type="radio" class="formradio" name="col" value="color" $col_color>rainbow (blue-red without border)
<input type="radio" class="formradio" name="col" value="flipcolor" $col_flipcolor>rainbow (red-blue without border)
</td></tr><tr><td>&nbsp;</td><td>
make grey when P><input type="text" class="forminput" name="greycut" size="2" value="${FORM_greycut:-5}">%</td>
</tr><tr>
<td>Projection:</td><td>
<select class="forminput" name="mproj">
<option value="default" $mproj_default>default
<option value="latlon" $mproj_latlon>lat-lon
<option value="nps" $mproj_nps>North polar stereographic
<option value="sps" $mproj_sps>South polar stereographic
<option value="robinson" $mproj_robinson>Robinson
<option value="mollweide" $mproj_mollweide>Mollweide
<option value="lambert" $mproj_lambert>Lambert
</select> projection
<td><a href="javascript:pop_page('help/maptype.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Plot options:<td>
<input type="checkbox" class="formcheck" name="nocbar" $nocbar_checked>no legend,
<input type="checkbox" class="formcheck" name="notitleonplot" $notitleonplot_checked>no title on plot,
<input type="checkbox" class="formcheck" name="nogrid" $nogrid_checked>no grid,
<input type="checkbox" class="formcheck" name="nopoli" $nopoli_checked>no political boundaries
<td><a href="javascript:pop_page('help/plotoptions.shtml',284,450)"><img src="images/info-i.gif" alt="help" border=\"0\"></a>
</td></tr><tr><td></td><td>
label distance <input type="$number" class="forminput" name="xlint" value="$FORM_xlint" $textsize2>&times;<input type="$number" class="forminput" name="ylint" value="$FORM_ylint" $textsize2>&deg;
</td></tr><tr>
<!-- geoTIFF does not work
<td>Output:</td><td><input type="radio" class="formradio" name="mapformat" value="png" $mapformat_png>PNG/EPS/PDF
<input type="radio" class="formradio" name="mapformat" value="geotiff" $mapformat_geotiff>geoTIFF
-->
</td></tr><tr>
<td>Contents:</td><td>(can be edited)</td>
</tr></table>
<textarea name="list" rows="5" cols="40">
EOF
cat $plotlist
cat <<EOF
</textarea><br>
<input type="submit" class="formbutton" value="Plot it">
</form>
</div>
EOF

. ./myvinkfoot.cgi
