#!/bin/sh

def=./prefs/$EMAIL.coordinates
if [ -s $def ]; then
  eval `egrep '^FORM_[a-z0-9]*=[-+.@/a-zA-Z0-9_]*;$' $def`
fi

[ "$FORM_lon1" = "$FORM_lon2" ] && FORM_lon2=""
[ "$FORM_lat1" = "$FORM_lat2" ] && FORM_lat2=""

case ${FORM_intertype:-nearest} in
interpolated) intertype_i="selected";;
*)            intertype_n="selected";;
esac

case ${FORM_masktype:-all} in
5lan) fivelan_checked="checked";lshidden=true;;
5sea) fivesea_checked="checked";lshidden=true;;
land) land_checked="checked";lshidden=false;;
sea)  sea_checked="checked";lshidden=false;;
notl) notl_checked="checked";lshidden=false;;
nots) nots_checked="checked";lshidden=false;;
*)    all_checked="checked";lshidden=true;;
esac

if [ -n "$ROBOT" -o $lshidden = false ]; then
	hiddenstyle_landsea=""
else
	hiddenstyle_landsea="\"display: none;\""
fi

case ${FORM_gridpoints:-average} in
max) max_checked="checked";;
min) min_checked="checked";;
true) gridpoints_checked="checked";;
field) outfield_checked="checked";;
*)    average_checked="checked";;
esac

case ${FORM_standardunits} in
standardunits) standardunits_checked="checked";;
"") oldunits_checked="checked";;
*) standardunits_checked="checked";;
esac

if [ "$SHOWMASK" = true ]; then
	cat << EOF
<tr><td>Mask:
</td><td><select name=maskmetadata>
<option value="">no mask</option>
EOF
	for maskmetadata in data/*.$EMAIL.poly
	do
		if [ -f $maskmetadata ]; then
			this=`head -1 $maskmetadata`
			name=`head -2 $maskmetadata | tail -n -1`
			if [ "$this" = "$maskfile" -o \( -z "$maskfile" -a "$maskmetadata" = "$FORM_maskmetadata" \) ]; then
				selected=selected
			else
				selected=""
			fi
			echo "<option value=\"$maskmetadata\" $selected>$name</option>"
		fi
	done
	cat <<EOF
	</select>
&nbsp <a href="upload_mask_form.cgi?id=$EMAIL&field=$FORM_field">add a mask to the list</a>
</td><td align="right"><a href="javascript:pop_page('help/mask.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
EOF
fi # SHOWMASK
cat << EOF
<tr><td>
Latitude:
</td><td>
<input type="$number" step=any class="forminput" name="lat1" $textsize4 value="$FORM_lat1">&deg;N - 
<input type="$number" step=any class="forminput" name="lat2" $textsize4 value="$FORM_lat2">&deg;N
</td><td align="right"><a href="javascript:pop_page('help/choosecoordinate.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td></tr><tr><td>
Longitude: 
</td><td>
<input type="$number" step=any class="forminput" name="lon1" $textsize4 value="$FORM_lon1">&deg;E -
<input type="$number" step=any class="forminput" name="lon2" $textsize4 value="$FORM_lon2">&deg;E
</td></tr><tr><td>
Boundaries:
</td><td>
<select class="forminput" name="intertype">
<option value="nearest" $intertype_n>halfway grid points</option>
<option value="interpolated" $intertype_i>interpolated</option>
</select>
</td></tr>
<tr><td>Make:</td>
<td>
<input type="radio" class="formradio" name="gridpoints" value="false" $average_checked>average
<input type="radio" class="formradio" name="gridpoints" value="max" $max_checked>max
<input type="radio" class="formradio" name="gridpoints" value="min" $min_checked>min
<input type="radio" class="formradio" name="gridpoints" value="true" $gridpoints_checked>set of grid points
<input type="radio" class="formradio" name="gridpoints" value="field" $outfield_checked>subset of the field
</td><td align="right"><a href="javascript:pop_page('help/gridpoints.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
EOF
if [ -z "$NOMISSING" ]; then
cat <<EOF
<tr><td>Demand at least:</td><td>
<input type="$number" class="forminput" name="minfac" value="${FORM_minfac:-30}" $textsize2>% valid points in this region
</td><td><a href="javascript:pop_page('help/validpoints.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
</td></tr><tr>
<!--
<td>Noise model:
</td><td>
<input type="radio" class="formradio" name ="noisemodel" value="1" 
checked>the same in all grid points or <input type="radio" class="formradio" name ="noisemodel" value="2">proportional to the variability (not yet implemented)
</td><td align="right"><a href="javascript:pop_page('help/noisemodel.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
-->
EOF
fi
if [ -n "$LSMASK" ]; then
	cat << EOF
<tr valign="baseline"><td>Considering:</td><td>
<input type="radio" class="formradio" name="masktype" value="all" $all_checked>everything
<input type="radio" class="formradio" name="masktype" value="5lan" $fivelan_checked>land points
<input type="radio" class="formradio" name="masktype" value="5sea" $fivesea_checked>sea points
<a href="javascript:hidden_info_switch('landsea');">show/hide more</a><br>
<div id="landsea" style=$hiddenstyle_landsea>
<input type="radio" class="formradio" name="masktype" value="land" $land_checked>only land points
<input type="radio" class="formradio" name="masktype" value="sea" $sea_checked>only sea points<br>
<input type="radio" class="formradio" name="masktype" value="notl" $notl_checked>not land points
<input type="radio" class="formradio" name="masktype" value="nots" $nots_checked>not sea points<br>
</div>
</td><td align="right"><a href="javascript:pop_page('help/landseamask.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
EOF
fi
if [ "$UNITS" != "$NEWUNITS" ]; then
  cat <<EOF
<tr><td>Units:</td><td>
<input type="radio" class="formradio" name="standardunits" value="standardunits" $standardunits_checked>convert to $NEWUNITS
<input type="radio" class="formradio" name="standardunits" value="" $oldunits_checked>leave in $UNITS
</td><td align="right"><a href="javascript:pop_page('help/convertunits.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td>
EOF
else
  cat <<EOF
<input type="hidden" name="standardunits" value="$FORM_standardunits">
EOF
fi
cat << EOF
<tr><td colspan="3"><input type="submit" class="formbutton" value="Make time series">
EOF
