#!/bin/sh
# write defaults file for the plot_atlas_form.cgi script
# co-ordinate the values with that.
###echo "writing defaults file<br>"
if [ $EMAIL != someone@somewhere ]; then
	def=prefs/$EMAIL.plot_atlas.$NPERYEAR
	cat << EOF > $def
FORM_region=$FORM_region;
FORM_srex=$FORM_srex;
FORM_lon1=$FORM_lon1;
FORM_lon2=$FORM_lon2;
FORM_lat1=$FORM_lat1;
FORM_lat2=$FORM_lat2;
FORM_masktype=$FORM_masktype;
FORM_mon=$FORM_mon;
FORM_sum=$FORM_sum;
FORM_dataset=$FORM_dataset;
FORM_var=$FORM_var;
FORM_normsd=$FORM_normsd;
FORM_output=$FORM_output;
FORM_scenario_cmip5=$FORM_scenario_cmip5;
FORM_scenario_cmip3=$FORM_scenario_cmip3;
FORM_scenario_rt2b=$FORM_scenario_rt2b;
FORM_measure=$FORM_measure;
FORM_begin=$FORM_begin;
FORM_end=$FORM_end;
FORM_begin2=$FORM_begin2;
FORM_end2=$FORM_end2;
FORM_regr=$FORM_regr;
FORM_plotvar=$FORM_plotvar;
FORM_obs_tas=$FORM_obs_tas;
FORM_obs_pr=$FORM_obs_pr;
FORM_obs_psl=$FORM_obs_psl;
FORM_rcp26=$FORM_rcp26;
FORM_rcp45=$FORM_rcp45;
FORM_rcp60=$FORM_rcp60;
FORM_rcp85=$FORM_rcp85;
FORM_anomaly=$FORM_anomaly;
FORM_anom1=$FORM_anom1;
FORM_anom2=$FORM_anom2;
EOF
fi