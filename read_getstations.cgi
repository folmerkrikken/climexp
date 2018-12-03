#!/bin/bash
# to be sourced from other scripts
# read getstation defaults from file and sets the appropriate variables
# for switches

def=./prefs/$EMAIL.getstations
if [ -s $def ]; then
  eval `egrep '^FORM_[A-Za-z0-9]*=[a-zA-Z_]*[-+0-9.]*;$' $def`
fi
FORM_name=`echo $FORM_NAME | tr '_' ' '`

case $FORM_climate in
precipitation) climate_precipitation="checked";;
precipitation_all) climate_precipitation_all="checked";;
temperature) climate_temperature="checked";;
temperature_all) climate_temperature_all="checked";;
min_temperature) climate_min_temperature="checked";;
min_temperature_all) climate_min_temperature_all="checked";;
max_temperature) climate_max_temperature="checked";;
max_temperature_all) climate_max_temperature_all="checked";;
sealevel_pressure) climate_sealevel_pressure="checked";;
sealevel) climate_sealevel="checked";;
sealev) climate_sealev="checked";;
runoff) climate_runoff="checked";;
streamflow) climate_streamflow="checked";;
streamflowdaily) climate_streamflowdaily="checked";;
ecaprcp) climate_ecaprcp="checked";;
ecatemp) climate_ecatemp="checked";;
ecatmin) climate_ecatmin="checked";;
ecatmax) climate_ecatmax="checked";;
ecapres) climate_ecapres="checked";;
ecasnow) climate_ecasnow="checked";;
ecaclou) climate_ecaclou="checked";;
becaprcp) climate_becaprcp="checked";;
becatemp) climate_becatemp="checked";;
becatmin) climate_becatmin="checked";;
becatmax) climate_becatmax="checked";;
becapres) climate_becapres="checked";;
becasnow) climate_becasnow="checked";;
becaclou) climate_becaclou="checked";;
gdcnprcp) climate_gdcnprcp="checked";;
gdcnprcpall) climate_gdcnprcp_all="checked";;
gdcntemp) climate_gdcntemp="checked";;
gdcntave) climate_gdcntave="checked";;
gdcntmin) climate_gdcntmin="checked";;
gdcntmax) climate_gdcntmax="checked";;
gdcnpres) climate_gdcnpres="checked";;
eu_sealevel_pressure) climate_eu_sealevel_pressure="checked";;
snow) climate_snow="checked";;
esac

case $FORM_sum in
1) sum_1="checked";;
2) sum_2="checked";;
3) sum_3="checked";;
4) sum_4="checked";;
*) sum_1="checked";;
esac

case $FORM_month in
0) month_0="checked";;
1) month_1="checked";;
2) month_2="checked";;
3) month_3="checked";;
4) month_4="checked";;
5) month_5="checked";;
6) month_6="checked";;
7) month_7="checked";;
8) month_8="checked";;
9) month_9="checked";;
10) month_10="checked";;
11) month_11="checked";;
12) month_12="checked";;
esac
