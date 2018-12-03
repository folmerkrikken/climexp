#!/bin/bash
# I should not include this as argument
case $file in
    IPCCData*) url="http://www-pcmdi.llnl.gov/ipcc/about_ipcc.php";;
    ESSENCE*)  url="http://www.knmi.nl/~sterl/Essence/";;
    ERA*)      url="http://www.ecmwf.int/en/research/climate-reanalysis";;
    Demeter*)  url="http://data.ecmwf.int/data";;
    ECMWF*)    url="http://www.ecmwf.int";;
    NCEPNCAR*) url="http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml";;
    CMIP5_yr*) url="http://www.cccma.ec.gc.ca/data/climdex/climdex.shtml";;
    CMIP5*)    url="showmetadata.cgi?EMAIL=$EMAIL&field=$FORM_field";;
    data*)     url="";;
    *)         url=`fgrep \"${FORM_field}\" selectfield_obs.html selectfield_rapid.html selectdailyfield*.html | sed -e 's/^.*href=\"//'  -e 's/\".*$//' -e "s/EMAIL/$EMAIL/"`;;
esac
