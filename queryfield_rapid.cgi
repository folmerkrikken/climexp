#!/bin/bash
# to be sourced from various scripts
# my database of field info, listing GrADS .ctl file or netCDF file, 
# full name, and special mappings or colour properties.
flipcolor=0
if [ -z "$FORM_field" ]; then
  echo;echo "Please select a field"
  exit
fi
NPERYEAR=12 # default
case $FORM_field in
Rapidluterbachertemp) file=RapidData/LuterbacherTemp.ctl;kindname="Luterbacher et al.";climfield="Temperature";NPERYEAR=4;map='set lat 35 70
set lon -25 40';;
Rapidluterbacherslp) file=RapidData/slp_1659-1999.ctl;kindname="Luterbacher et al.";climfield="Sea Level Pressure";NOMISSING=nomissing;NPERYEAR=12;map='set lat 30 70
set lon 330 400';;
Rapidluterbachergph) file=RapidData/500hpa_1659-1999.ctl;kindname="Luterbacher et al.";climfield="Geopotential Height";NOMISSING=nomissing;NPERYEAR=12;map='set lat 30 70
set lon 330 400';;
Rapidbriffatemp) file=RapidData/briffatemp.ctl;kindname="Briffa et al.";climfield="Temperature";NPERYEAR=1;;
Rapidbriffaslp) file=RapidData/briffaslp.ctl;kindname="Briffa et al.";climfield="Sea Level Pressure";NPERYEAR=1;;
Rapidpaulingprecip) file=RapidData/PaulingPrecip.ctl;kindname="Pauling et al.";climfield="Precipitation";NPERYEAR=4;map='set lat 30 71
set lon -30 40';;
Rapidcookpdsi) file=RapidData/NADAv2-2008_flipped.nc;kindname="NADA v2";climfield="PDSI";NPERYEAR=1;map='set lat 17.5 65
set lon -137.5 -52.5';;
RapidCook2010MADA) file=RapidData/MADApdsi_flipped.nc;kindname="MADA";climfield="PDSI";NPERYEAR=1;map='set lat -10 57.5
set lon 60 145';;
Rapidcook2015owda) file=RapidData/owda_hd_fix1_500_fixed.nc;kindname="OWDA";climfield="PDSI";NPERYEAR=1;map='set lat 25 75
set lon -15 45';;
data/*) 

esac
