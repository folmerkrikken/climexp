#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

# script to produce maps and time series analogous to the IPCC WG1 AR5 Annex I "Atlas"
# but much more general.
# The follwoing choices have to be made by the user
# 1) region: a rectangle or a predefined (uploaded?) mask
# 2) season: starting month, number of months
# 3) dataset: CMIP5, CMIP3, ENSEMBLES RCM, ...; maybe observational as well
# 4) variable (list depends on the above)
# 5) map or time series
# map:
# 6m) scenario (if model)
# 7m) measure of change, time period(s)
# 8m) measure of PDF
# 9m) measure of natural variability
# time series:
# 6t) time period
# 7t) scenario(s)
# 8t) include observations, which ones

DIR=`pwd`
. ./getargs.cgi
. ./init.cgi
[ -z "$EMAIL" ] && EMAIL=someone@somewhere
# check email address
. ./checkemail.cgi

if [ $EMAIL = oldenbor@knmi.nl ]; then
	export lwrite=true # false # true
fi

. ./myvinkhead.cgi "KNMI Atlas <font color="#ff2222">WORK IN PROGRESS</font>" "Choose parameters" ""

# if the script does not call itself load saved values
###echo "EMAIL=$EMAIL, FORM_resubmitted=$FORM_resubmitted<br>"
if [ $EMAIL != someone@somewhere ]; then
	if [ "$FORM_resubmitted" != true ]; then
  		def=prefs/$EMAIL.plot_atlas.$NPERYEAR
  		if [ -f $def ]; then
    		eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
  		fi
  	else
  		. ./plot_atlas_defaults_write.cgi
	fi
fi

echo `date` "$EMAIL ($REMOTE_ADDR) plot_atlas_form $FORM_dataset $FORM_var $FORM_output" >> log/log
. ./myvinkhead.cgi "Plot $FORM_dataset $FORM_var $FORM_graphtype" ""

# defaults for choice that entail other choices
[ -z "$FORM_region" ] && FORM_region=srex
[ -z "$FORM_dataset" ] && FORM_dataset=CMIP5
[ -z "$FORM_var" ] && FORM_var=tas
[ -z "$FORM_measure" ] && FORM_measure=diff
[ -z "$FORM_output" ] && FORM_output=map

# begin form
cat <<EOF
<div class="kalelink">
<form action="plot_atlas_form.cgi" method="POST">
<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>
EOF

# 1) region

case $FORM_region in
	srex) srex_checked=checked;;
	point) point_checked=checked;;
	box) box_checked=checked;;
	mask) mask_checked=checked;;
esac

case ${FORM_masktype:-all} in
5lan) land_checked="checked";;
5sea)  sea_checked="checked";;
*)    all_checked="checked";;
esac

# select a region - standard or custom
# except the top few the same as the AR5 Atlas


cat <<EOF
<tr><th colspan="3">Select a region</th></tr>
<tr><td>
Type:
</td><td>
<input type=hidden name=id value="$EMAIL">
<input type=hidden name=resubmitted value="true">
<input type=hidden name=region_old value="$FORM_region">
<input class=formradio type=radio name=region value=srex $srex_checked onchange=this.form.submit();>predefined
<input class=formradio type=radio name=region value=point $point_checked onchange=this.form.submit();>place
<input class=formradio type=radio name=region value=box $box_checked onchange=this.form.submit();>box
<input class=formradio type=radio name=region value=mask $mask_checked onchange=this.form.submit();>mask
EOF

if [ "$FORM_region" = srex ]; then
	case ${FORM_srex:-world} in
world) world_selected=selected;; #World
worldland) worldland_selected=selected;; #World (land)
worldsea) worldsea_selected=selected;; #World (sea)
NAmerica) NAmerica_selected=selected;; #North America
SAmerica) SAmerica_selected=selected;; #South America
Europe) Europe_selected=selected;; #Europe
Africa) Africa_selected=selected;; #Africa
Asia) Asia_selected=selected;; #Asia
Australia) Australia_selected=selected;; #Australia
Arcticland) Arcticland_selected=selected;; #Arctic (land)
Arcticsea) Arcticsea_selected=selected;; #Arctic (sea)
CGI) CGI_selected=selected;; #SREX Canada/Greenland/Iceland
NAS) NAS_selected=selected;; #SREX North Asia
ALA) ALA_selected=selected;; #SREX Alaska
WNA) WNA_selected=selected;; #SREX West North America
CNA) CNA_selected=selected;; #SREX Central North America
ENA) ENA_selected=selected;; #SREX Eastern North America
CAM) CAM_selected=selected;; #SREX Central America
Caribbean) Caribbean_selected=selected;; #Caribbean
AMZ) AMZ_selected=selected;; #SREX Amazon
NEB) NEB_selected=selected;; #SREX North-East Brazil
WSA) WSA_selected=selected;; #SREX West Coast South America
SSA) SSA_selected=selected;; #SREX Southeastern South America
NEU) NEU_selected=selected;; #SREX North Europe
CEU) CEU_selected=selected;; #SREX Central Europe
MED) MED_selected=selected;; #SREX South Europe/Mediterranean
SAH) SAH_selected=selected;; #SREX Sahara
WAF) WAF_selected=selected;; #SREX west Africa
EAF) EAF_selected=selected;; #SREX East Africa
SAF) SAF_selected=selected;; #SREX Southern Africa
WIndian) WIndian_selected=selected;; #West Indian Ocean
WAS) WAS_selected=selected;; #SREX West Asia
CAS) CAS_selected=selected;; #SREX Central Asia
TIB) TIB_selected=selected;; #SREX Tibetan Plateau
EAS) EAS_selected=selected;; #SREX Eastern Asia
SAS) SAS_selected=selected;; #SREX South Asia
NIndian) NIndian_selected=selected;; #North Indian Ocean
SEA) SEA_selected=selected;; #SREX Southeast Asia (land)
SEAsia_sea) SEAsia_sea_selected=selected;; #Southeast Asia (sea)
NAU) NAU_selected=selected;; #SREX North Australia
SAU) SAU_selected=selected;; #SREX South Australia/New Zealand
NTPacific) NTPacific_selected=selected;; #Northern Tropical Pacific
EQPacific) EQPacific_selected=selected;; #Equatorial Pacific
STPacific) STPacific_selected=selected;; #Southern Tropical Pacific
Antarcticland) Antarcticland_selected=selected;; #Antarctic (land)
Antarcticsea) Antarcticsea_selected=selected;; #Antarctic (sea)
	esac

	cat <<EOF
</td></tr><tr><td>
Predefined:
</td><td>
<select class=forminput name=srex>
<option value=world $world_selected>World
<option value=worldland $worldland_selected>World (land)
<option value=worldsea $worldsea_selected>World (sea)
<option value=NAmerica $NAmerica_selected>North America
<option value=SAmerica $SAmerica_selected>South America
<option value=Europe $Europe_selected>Europe
<option value=Africa $Africa_selected>Africa
<option value=Asia $Asia_selected>Asia
<option value=Australia $Australia_selected>Australia
<option value=Arcticland $Arcticland_selected>Arctic (land)
<option value=Arcticsea $Arcticsea_selected>Arctic (sea)
<option value=CGI $CGI_selected>SREX Canada/Greenland/Iceland
<option value=NAS $NAS_selected>SREX North Asia
<option value=ALA $ALA_selected>SREX Alaska
<option value=WNA $WNA_selected>SREX West North America
<option value=CNA $CNA_selected>SREX Central North America
<option value=ENA $ENA_selected>SREX Eastern North America
<option value=CAM $CAM_selected>SREX Central America
<option value=Caribbean $Caribbean_selected>Caribbean
<option value=AMZ $AMZ_selected>SREX Amazon
<option value=NEB $NEB_selected>SREX North-East Brazil
<option value=WSA $WSA_selected>SREX West Coast South America
<option value=SSA $SSA_selected>SREX Southeastern South America
<option value=NEU $NEU_selected>SREX North Europe
<option value=CEU $CEU_selected>SREX Central Europe
<option value=MED $MED_selected>SREX South Europe/Mediterranean
<option value=SAH $SAH_selected>SREX Sahara
<option value=WAF $WAF_selected>SREX west Africa
<option value=EAF $EAF_selected>SREX East Africa
<option value=SAF $SAF_selected>SREX Southern Africa
<option value=WIndian $WIndian_selected>West Indian Ocean
<option value=WAS $WAS_selected>SREX West Asia
<option value=CAS $CAS_selected>SREX Central Asia
<option value=TIB $TIB_selected>SREX Tibetan Plateau
<option value=EAS $EAS_selected>SREX Eastern Asia
<option value=SAS $SAS_selected>SREX South Asia
<option value=NIndian $NIndian_selected>North Indian Ocean
<option value=SEA $SEA_selected>SREX Southeast Asia (land)
<option value=SEAsia_sea $SEAsia_sea_selected>Southeast Asia (sea)
<option value=NAU $NAU_selected>SREX North Australia
<option value=SAU $SAU_selected>SREX South Australia/New Zealand
<option value=NTPacific $NTPacific_selected>Northern Tropical Pacific
<option value=EQPacific $EQPacific_selected>Equatorial Pacific
<option value=STPacific $STPacific_selected>Southern Tropical Pacific
<option value=Antarcticland $Antarcticland_selected>Antarctic (land)
<option value=Antarcticsea $Antarcticsea_selected>Antarctic (sea)
</select>
</td><td align="right"><a href="javascript:pop_page('help/chooseareas.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a>
EOF
else
	# save the variable in a hidden variable
	cat <<EOF
<input type=hidden name=srex value="$FORM_srex">
EOF
fi

if [ "$FORM_region" = box ]; then
	cat <<EOF
</td></tr><tr><td>
Box:</td><td>
<input type="$number" step=any class="forminput" name="lat1" $textsize4 value="$FORM_lat1">&deg;N - 
<input type="$number" step=any class="forminput" name="lat2" $textsize4 value="$FORM_lat2">&deg;N,
<input type="$number" step=any class="forminput" name="lon1" $textsize4 value="$FORM_lon1">&deg;E -
<input type="$number" step=any class="forminput" name="lon2" $textsize4 value="$FORM_lon2">&deg;E
</td></tr><tr><td>
Land/sea mask:
</td><td>
<input type="radio" class="formradio" name="masktype" value="all" $all_checked>everything
<input type="radio" class="formradio" name="masktype" value="5lan" $land_checked>only land points
<input type="radio" class="formradio" name="masktype" value="5sea" $sea_checked>only sea points<br>
</td><td align="right"><a href="javascript:pop_page('help/landseamask.shtml',284,450)"><img src="images/info-i.gif" alt="help" border="0"></a></td></tr>
EOF
else
	# save the variables
	cat <<EOF
<input type=hidden name=lon1 value="$FORM_lon1">
<input type=hidden name=lon2 value="$FORM_lon2">
<input type=hidden name=lat1 value="$FORM_lat1">
<input type=hidden name=lat2 value="$FORM_lat2">
<input type=hidden name=masktype value="$FORM_masktype">
EOF
fi

if [ "$FORM_region" = point ]; then
	cat <<EOF
</td></tr><tr><td>
Place:
</td><td>
<input type="$number" step=any class="forminput" name="lat" $textsize4 value="$FORM_lat">&deg;N - 
<input type="$number" step=any class="forminput" name="lon" $textsize4 value="$FORM_lon">&deg;E
EOF
else
	cat <<EOF
<input type=hidden name=lon value="$FORM_lon">
<input type=hidden name=lat value="$FORM_lat">
EOF
fi

if [ "$FORM_region" = mask ]; then
	cat <<EOF
</td></tr><tr><td>
Mask file:
</td><td>
<input type="file" class="formbutton" name="mask" value="mask.nc">
<br>(netcdf file on 2.5&deg; grid starting at 1.25&deg;E/88.75&deg;S)
EOF
fi # nothing to save...

# season

case ${FORM_mon:--1} in
1) month_1_selected="selected";;
2) month_2_selected="selected";;
3) month_3_selected="selected";;
4) month_4_selected="selected";;
5) month_5_selected="selected";;
6) month_6_selected="selected";;
7) month_7_selected="selected";;
8) month_8_selected="selected";;
9) month_9_selected="selected";;
10) month_10_selected="selected";;
11) month_11_selected="selected";;
12) month_12_selected="selected";;
1:12) month_all_selected="selected";;
0) month_0_selected="selected";;
*) month_1_selected="selected";;
esac

case ${FORM_sum:-12} in
1) sum_1_selected=selected;;
2) sum_2_selected=selected;;
3) sum_3_selected=selected;;
4) sum_4_selected=selected;;
5) sum_5_selected=selected;;
6) sum_6_selected=selected;;
7) sum_7_selected=selected;;
8) sum_8_selected=selected;;
9) sum_9_selected=selected;;
10) sum_10_selected=selected;;
11) sum_11_selected=selected;;
*) sum_12_selected=selected;;
esac  

cat <<EOF
</td></tr><tr><th colspan=3>Select a season
</th></tr><tr><td>
Sesason:</td><td>
First month
<select class="forminput" name="mon">
<option value="1" $month_1_selected>Jan
<option value="2" $month_2_selected>Feb
<option value="3" $month_3_selected>Mar
<option value="4" $month_4_selected>Apr
<option value="5" $month_5_selected>May
<option value="6" $month_6_selected>Jun
<option value="7" $month_7_selected>Jul
<option value="8" $month_8_selected>Aug
<option value="9" $month_9_selected>Sep
<option value="10" $month_10_selected>Oct
<option value="11" $month_11_selected>Nov
<option value="12" $month_12_selected>Dec
</select>, 
length 
<select class="forminput" name="sum">
<option $sum_1_selected>1
<option $sum_2_selected>2
<option $sum_3_selected>3
<option $sum_4_selected>4
<option $sum_5_selected>5
<option $sum_6_selected>6
<option $sum_7_selected>7
<option $sum_8_selected>8
<option $sum_9_selected>9
<option $sum_10_selected>10
<option $sum_11_selected>11
<option $sum_12_selected>12
</select> months
</td><td><a href="javascript:pop_page('help/selectseason12.shtml',568,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
EOF

# dataset

case ${FORM_dataset:-CMIP5} in
CMIP5) CMIP5_selected=selected;;
CMIP5one) CMIP5one_selected=selected;;
CMIP3) CMIP3_selected=selected;;
RT2b)  RT2b_selected=selected;;
RT3)   RT3_selected=selected;;
ERAi)  ERAi_selected=selected;;
20CR)  CR_selected=selected;;
obs)   obs_selected=selected;;
esac

cat <<EOF
</td></tr><tr><th colspan=3>
Select a dataset and variable
</th></tr><tr><td>
Dataset:
</td><td>
<input type=hidden name=dataset_old value=$FORM_dataset>
<select class=forminput name=dataset onchange=this.form.submit();>
<option value=CMIP5 $CMIP5_selected>GCM: CMIP5 (full set)
<option value=CMIP5one $CMIP5one_selected>GCM: CMIP5 (one member per model)
<option value=CMIP3 $CMIP3_selected>GCM: CMIP3
<option value=RT2b $RT2b_selected>RCM: ENSEMBLES (Europe) GCM-driven
<option value=RT3 $RT3_selected>RCM: ENSEMBLES (Europe) ERA40-driven
<option value=ERAi $ERAi_selected>ERA-interim reanalysis
<option value=20CR $CR_selected>20C reanalysis
<option value=obs $obs_selected>Observations
</select> 
EOF

# variable

case ${FORM_var:-tas} in
tas) tas_selected=selected;;
tasmin) tasmin_selected=selected;;
tasmax) tasmax_selected=selected;;
pr)  pr_selected=selected;;
evspsbl) evspsbl_selected=selected;;
pme) pme_selected=selected;;
huss) huss_selected=selected;;
rsds) rsds_selected=selected;;
psl) psl_selected=selected;;
esac

if [ -n "$FORM_normsd" ]; then
	normsd_checked=checked
else
	normsd_unchecked=checked
fi

cat <<EOF
</td></tr><tr><td>
Variable:
</td><td>
<input type=hidden name=var_old value="$FORM_var">
<select class=forminput name=var onchange=this.form.submit();>
<option value=tas $tas_selected>near-surface temperature
<option value=tasmin $tasmin_selected>minimum near-surface temperature
<option value=tasmin $tasmax_selected>maximum near-surface temperature
<option value=pr $pr_selected>precipitation
<option value=evspsbl $evspsbl_selected>evaporation, transpiration, sublimation
<option value=pme $pme_selected>P-E, net water flux
<option value=huss $huss_selected>specific humidity near the surface
<option value=rsds $rsds_selected>downward solar radiation at the surface
<option value=psl $psl_selected>air pressure at sea-level
</select>
</td></tr><tr><td>
&nbsp;
</td><td>
<input type=radio class="formradio" name="normsd" value="" $normsd_unchecked>absolute
<input type=radio class="formradio" name="normsd" value="normsd" $normsd_checked>relative
</select> changes are shown
EOF

# map or time series

case ${FORM_output:-map} in
map) map_checked=checked;;
series) series_checked=checked;;
histogram) histogram_checked=checked;;
scatter) scatter_checked=checked;;
esac

cat <<EOF
</td></tr><tr><td>
Output:
</td><td>
<input type=hidden name=output_old value=$FORM_output>
<input type=radio class="formradio" name="output" value="map" $map_checked onchange=this.form.submit();>map, 
<input type=radio class="formradio" name="output" value="series" $series_checked onchange=this.form.submit();>time series 
<input type=radio class="formradio" name="output" value="histogram" $histogram_checked onchange=this.form.submit();>histogram
<!--<input type=radio class="formradio" name="output" value="scatter" $scatter_checked onchange=this.form.submit();>scatter plots-->
EOF

thisyear=`date -d "1 months ago" +%Y`

dumptypes="0"
endhistory=%thisyear
if [ $FORM_dataset = CMIP5 -o $FORM_dataset = CMIP5one ]; then
	yr1=1861
	yr2=2100
	dumptypes="0 1"
	endhistory=2005
elif [ $FORM_dataset = CMIP3 ]; then
	yr1=1900
	yr2=2099
	dumptypes="0 1"
	endhistory=2000
elif [ $FORM_dataset = RT2b ]; then
	yr1=1950
	yr2=2100
	dumptypes="0 1"
	endhistory=2000
elif [ $FORM_dataset = RT3 ]; then
	yr1=1960
	yr2=2000
elif [ $FORM_dataset = 20CR ]; then
	yr1=1878
	yr2=2010
elif [ $FORM_dataset = obs ]; then
	if [ $FORM_var = tas ]; then
		yr1=1880
	else
		yr1=1901
	fi
	yr2=$thisyear
fi
[ -z "$FORM_begin" ] && FORM_begin=$yr1
[ -z "$FORM_end" ] && FORM_end=2005
[ -z "$FORM_begin2" ] && FORM_begin2=2006
[ -z "$FORM_end2" ] && FORM_end=$yr2
if [ $FORM_end -gt $yr2 ]; then
	FORM_begin=$((yr2-FORM_end+FORM_begin))
	[ $FORM_begin -lt $yr1 ] && FORM_begin=$yr1
	FORM_end=$yr2
fi
if [ $FORM_begin -lt $yr1 ]; then
	FORM_end=$((yr1+FORM_end-FORM_begin))
	[ $FORM_end -gt $yr2 ] && FORM_end=$yr2
	FORM_begin=$yr1
fi
if [ $FORM_end2 -gt $yr2 ]; then
	FORM_begin2=$((yr2-FORM_end2+FORM_begin2))
	[ $FORM_begin2 -lt $yr1 ] && FORM_begin2=$yr1
	FORM_end2=$yr2
fi
if [ $FORM_begin2 -le $FORM_end ]; then
	FORM_end2=$((FORM_end+1+FORM_end2-FORM_begin2))
	[ $FORM_end2 -gt $yr2 ] && FORM_end2=$yr2
	FORM_begin2=$((FORM_end+1))
fi	

if [ "${FORM_output:-map}" = map -o "$FORM_output" = histogram ]; then

	# map & histogram options

	cat <<EOF
</td></tr><tr><th colspan=3>
Map options
</th></tr><tr><td>
EOF
	if [ $FORM_dataset = CMIP5 -o $FORM_dataset = CMIP5one -o $FORM_dataset = CMIP3 -o $FORM_dataset = RT2b ]; then
		echo "Scenario:"
	else
		echo "(Re)analysis:"
	fi
	if [ $FORM_dataset = CMIP5 -o $FORM_dataset = CMIP5one ]; then
		case ${FORM_scenario_cmip5:-rcp45} in
			rcp26) rcp26_selected=selected;;
			rcp45) rcp45_selected=selected;;
			rcp60) rcp60_selected=selected;;
			rcp85) rcp85_selected=selected;;
		esac
		cat <<EOF
</td><td>
<select class=forminput name=scenario_cmip5>
<option value=rcp26 $rcp26_selected>Historical + RCP2.6
<option value=rcp45 $rcp45_selected>Historical + RCP4.5
<option value=rcp60 $rcp60_selected>Historical + RCP6.0
<option value=rcp85 $rcp85_selected>Historical + RCP8.5
</select>
EOF
	else
		cat <<EOF
<input type=hidden name=scenario_cmip5 value=$FORM_scenario_cmip5>
EOF
	fi
	if [ $FORM_dataset = CMIP3 ]; then
		case $FORM_scenario_cmip3 in
			sresa1b) sresa1b_selected=selected
		esac
		cat <<EOF
<input type=hidden name=scenario_cmip3 value=sresa1b>
</td><td>SRES A1B
EOF
	else
		cat <<EOF
<input type=hidden name=scenario_cmip3 value=sresa1b>
EOF
	fi
	if [ $FORM_dataset = RT2b ]; then
		case $FORM_scenario_rt2b in
			sresa1b) sresa1b_selected=selected
		esac
		cat <<EOF
<input type=hidden name=scenario_rt2b value=A1B>
</td><td>SRES A1B
EOF
	else
		cat <<EOF
<input type=hidden name=scenario_rt2b value=A1B>
EOF
	fi
	if [ $FORM_dataset = RT3 ]; then
		cat <<EOF
</td><td>ERA-40 boundary conditions
EOF
	fi
	if [ $FORM_dataset = ERAi ]; then
		yr1=1979
		yr2=$thisyear
		cat <<EOF
</td><td>ERA-interim reanalysis
EOF
	fi
	if [ $FORM_dataset = 20CR ]; then
		cat <<EOF
</td><td>Reanalysis of the twentieth century
EOF
	fi
	if [ $FORM_dataset = obs ]; then
		dataset_ok=true
		var_ok=
		if [ $FORM_var = tas ]; then 
			var_ok=true
			case ${FORM_obs_tas:-giss_temp_1200} in
				giss_temp_1200) giss_temp_1200_selected=selected;;
				ncdc_temp) ncdc_temp_selected=selected;;
				hadcrut4110) hadcrut4110_selected=selected;;
			esac
			cat <<EOF
</td><td>
<select class=forminput name=obs_tas>
<option value=giss_temp_1200 $giss_temp_1200_selected>GISTEMP 1200
<option value=ncdc_temp $ncdc_temp_selected>NCDC MOST
<option value=hadcrut4110 $hadcrut4110_selected>HadCRUT4.1.1.0
</select>
EOF
		else
			cat <<EOF
<input type=hidden name=obs_tas value=$FORM_obs_tas>
EOF
		fi
		if [ $FORM_var = pr ]; then
			var_ok=true
			case ${FORM_obs_pr:-hadcrut4110} in
				gpcc_25) gpcc_25_selected=selected;;
				prca) prca_selected=selected;;
				cru311_pre_25) cru311_pre_25_selected=selected;;
			esac
			cat <<EOF
</td><td>
<select class=forminput name=obs_pr>
<option value=gpcc_25 $gpcc_25_selected>GPCC v6
<option value=prca $prca_selected>NCDC anomalies
<option value=cru311_pre_25 $cru311_pre_25_selected>CRU TS 3.10.01
</select>
EOF
		else
			cat <<EOF
<input type=hidden name=obs_pr value=$FORM_obs_pr>
EOF
		fi
		if [ $FORM_var = psl ]; then
			var_ok=true
			case ${FORM_obs_psl:-hadlslp2r} in
				trenberthslp) trenberthslp_selected=selected;;
				hadslp2r) hadslp2r_selected=selected;;
			esac
			cat <<EOF
</td><td>
<select class=forminput name=obs_psl>
<option value=trenberthslp $trenberthslp_selected>UCAR ds010 (NH only)
<option value=hadslp2r $hadslp2r_selected>HadSLP2r
</select>
EOF
		else
			cat <<EOF
<input type=hidden name=obs_pr value=$FORM_obs_pr>
EOF
		fi
		if [ $var_ok !+ true ]; then
			echo "Sorry, cannot handle variable $FORM_var in dataset observations yet"
			echo "</td></tr></table</form></div>"
			. ./myvinkfoot.cgi
		fi		
	fi
	
	case ${FORM_measure:-diff} in
		diff) diff_selected=selected;;
		regr) regr_selected=selected;;
	esac
	cat <<EOF
</th></tr><tr><td>
Measure:
</td><td>
<input type=hidden name=measure_old value=$FORM_measure>
<select class=forminput name=measure onchange=this.form.submit();>
<option value=diff $diff_selected>Difference of two periods
<option value=regr $regr_selected>Linear or non-linear trend
</select>
EOF
    if [ "${FORM_measure:-diff}" = diff ]; then
		cat <<EOF
</td></tr><tr><td>
Reference period:
</td><td>
<input type="text" min=$yr1 max=$yr2 step=1 name="begin" size=4 value="${FORM_begin:-1986}">-<input type="text" min=$yr1 max=$yr2 step=1 name="end" size=4 value="${FORM_end:-2005}">
</td></tr><tr><td>
Future period:
</td><td>
<input type="text" min=$yr1 max=$yr2 step=1 name="begin2" size=4 value="${FORM_begin2:-$((yr2-19))}">-<input type="text" min=$yr1 max=$yr2 step=1 name="end2" size=4 value="${FORM_end2:-$yr2}">
EOF
	else
		# these two are not used in the regression
		cat <<EOF
<input type=hidden name=end value=$FORM_end>
<input type=hidden name=begin2 value=$FORM_begin2>
EOF
	fi
	if [ "$FORM_measure" = regr ]; then
		case ${FORM_regr:-time} in
			time) time_selected=selected;;
			co2eq) co2eq_selected=selected;;
			obstglobal) obstglobal_selected=selected;;
			modtglobal) modtglobal_selected=selected;;
		esac
		[ $FORM_end -gt $yr2 ] && FORM_end=$yr2
		[ $FORM_begin -lt $yr1 ] && FORM_begin=$yr1
		cat <<EOF
</td></tr><tr><td>
Trend definition:
</td><td>
<select class=forminput name=regr>
<option value=time $time_selected>Linear trend in time
<option value=co2eq $co2eq_selected>Proportional to effective CO2 concentration
<option value=obstglobal $obstglobal_selected>Proportional to observed Tglobal
<option value=modtglobal $modtglobal_selected>Proportional to modelled Tglobal
</select>
</td></tr><tr><td>
Fit period:
</td><td>
<input type="text" min=$yr1 max=$yr2 step=1 name="begin" size=4 value="${FORM_begin:-1950}">-<input type="text" min=$yr1 max=$yr2 step=1 name="end2" size=4 value="${FORM_end:-2100}">
EOF
	else
		# these variables are not used in the difference definition
		cat <<EOF
<input type=hidden name=regr value=$FORM_regr>
EOF
	fi

	if [ $FORM_output = map ]; then

		# measure of PDF - coordinate with quantiles_field and getweightedquantile
	
		case $FORM_plotvar in
			mean) mean_selected=selected;;
			p025) p025_selected=selected;;
			p05) p05_selected=selected;;
			p10) p10_selected=selected;;
			p17) p17_selected=selected;;
			p25) p25_selected=selected;;
			p50) p50_selected=selected;;
			p75) p75_selected=selected;;
			p83) p83_selected=selected;;
			p90) p90_selected=selected;;
			p95) p95_selected=selected;;
			p975) p975_selected=selected;;
		esac
		cat <<EOF
</td></tr><tr><td>
Plot:
</td><td>
<select class=forminput name=plotvar>
<option value=mean $mean_selected>mean
<option value=p025 $p025_selected>2.5%
<option value=p05 $p05_selected>5%
<option value=p10 $p10_selected>10%
<option value=p17 $p17_selected>17%
<option value=p25 $p25_selected>25%
<option value=p50 $p50_selected>50%
<option value=p75 $p75_selected>75%
<option value=p83 $p83_selected>83%
<option value=p90 $p90_selected>90%
<option value=p95 $p95_selected>95%
<option value=p975 $p975_selected>97.5%
</select>
EOF

		# submit

		cat <<EOF
</td></tr><tr><td colspan=2>
<input type="submit" class="formbutton" value="Make map">
EOF

	else # histogram

		cat <<EOF
<input type=hidden name=plotvar value=$FORM_plotvar>
</td></tr><tr><td colspan=2>
<input type="submit" class="formbutton" value="Make histogram">
EOF

	fi
else
	# hidden versions of all parameters in map, histogram to save them
	FORM_measure_old=$FORM_measure
	cat <<EOF
<input type=hidden name=scenario_cmip5 value=$FORM_scenario_cmip5>
<input type=hidden name=scenario_cmip3 value=$FORM_scenario_cmip3>
<input type=hidden name=scenario_rt2b value=$FORM_scenario_rt2b>
<input type=hidden name=measure value=$FORM_measure>
<input type=hidden name=begin value=$FORM_begin>
<input type=hidden name=end2 value=$FORM_end2>
<input type=hidden name=regr value=$FORM_regr>
<input type=hidden name=plotvar value=$FORM_plotvar>
EOF
fi

if [ "$FORM_output" = series ]; then

	# time series options
	
	cat <<EOF
</td></tr><tr><th colspan=3>
Time series options
</th></tr><tr><td>
Scenario(s):
</td><td>
EOF
	if [ $FORM_dataset = CMIP5 -o $FORM_dataset = CMIP5one ]; then
		[ -n "$FORM_rcp26" ] && rcp26_checked=checked
		[ -n "$FORM_rcp45" ] && rcp45_checked=checked
		[ -n "$FORM_rcp60" ] && rcp60_checked=checked
		[ -n "$FORM_rcp85" ] && rcp85_checked=checked
		cat <<EOF
<input type=checkbox class=formcheck name=rcp26 $rcp26_checked>RCP2.6
<input type=checkbox class=formcheck name=rcp45 $rcp45_checked>RCP4.5
<input type=checkbox class=formcheck name=rcp60 $rcp60_checked>RCP6.0
<input type=checkbox class=formcheck name=rcp85 $rcp85_checked>RCP8.5
EOF
	else
		cat <<EOF
<input type=hidden name=rcp26 value=$FORM_rcp26>
<input type=hidden name=rcp45 value=$FORM_rcp45>
<input type=hidden name=rcp60 value=$FORM_rcp60>
<input type=hidden name=rcp85 value=$FORM_rcp85>
EOF
	fi
	if [ $FORM_dataset = CMIP3 ]; then
		echo "$FORM+_scenario_cmip3"
	elif [ $FORM_dataset = RT2b ]; then
		echo "$FORM+_scenario_rt2b"
	elif [ ${FORM_dataset#CMIP5} = $FORM_dataset ]; then
		echo "approximation of real world"
	fi
	echo "FORM_anomaly=$FORM_anomaly<br>"
	[ -n "$FORM_anomaly" ] && anomaly_checked=checked
	cat <<EOF
</td></tr><tr><td>
Plot period:
</td><td>
<input type="text" min=$yr1 max=$yr2 step=1 name="begin" size=4 value="${FORM_begin:-$yr1}">-<input type="text" min=$yr1 max=$yr2 step=1 name="end2" size=4 value="${FORM_end2:-$yr2}">
</td></tr><tr><td>
Anomalies:
</td><td>
<input type=checkbox class=formcheck name=anomaly $anomaly_checked>Take anomalies wrt 
<input type="text" min=$yr1 max=$yr2 step=1 name="anom1" size=4 value="${FORM_anom1:-1986}">-<input type="text" min=$yr1 max=$yr2 step=1 name="anom2" size=4 value="${FORM_anom2:-2005}">
EOF

	# submit

	cat <<EOF
</td></tr><tr><td colspan=2>
<input type="submit" class="formbutton" value="Make time series">
EOF
else
	# hidden versions of all time series parameters
	cat <<EOF
<input type=hidden name=rcp26 value=$FORM_rcp26>
<input type=hidden name=rcp45 value=$FORM_rcp45>
<input type=hidden name=rcp60 value=$FORM_rcp60>
<input type=hidden name=rcp85 value=$FORM_rcp85>
<input type=hidden name=anomaly value=$FORM_anomaly>
<input type=hidden name=anom1 value=$FORM_anom1>
<input type=hidden name=anom2 value=$FORM_anom2>
EOF
fi

cat <<EOF
</td></tr>
</table>
</form>
</div>
EOF

if [ -n "$FORM_region" -a "$FORM_region" = "${FORM_region_old}" \
	-a -n "$FORM_dataset" -a "$FORM_dataset" = "$FORM_dataset_old" \
	-a -n "$FORM_var" -a "$FORM_var" = "$FORM_var_old" \
	-a -n "$FORM_measure" -a "$FORM_measure" = "$FORM_measure_old" \
	-a -n "$FORM_output" -a "$FORM_output" = "$FORM_output_old" ]; then
	if [ $FORM_output = map ]; then
		. ./plot_atlas_map.cgi
	elif [ $FORM_output = series ]; then
		. ./plot_atlas_series.cgi
	elif [ $FORM_output = histogram ]; then
		echo " A WONDERFUL TIME SERIES PLOT WILL APPEAR HERE"
	elif [ $FORM_output = scatter ]; then
		echo " A WONDERFUL TIME SCATTER PLOT WILL APPEAR HERE"
	else
		echo "Error: do not know how to make a $FORM_output plot"
	fi
fi

. ./myvinkfoot.cgi
