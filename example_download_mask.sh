#!/bin/sh
email=insert_your_Climate_Explorer_email_address_here
scenario=rcp85
countries="countries you want to retrieve" # eg "France_metropolitan Faroe_Is. US_New_Hampshire", as in get_+index.cgi
models="ens" # this gives all CMIP5 ensemble members on a 2.5º grid.Otherwise eg "ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 ... NorESM1-M" gives all CMIP5 models (see Annex I "Atlas" for the fiull list)
vars="variables that you want to retrieve"
standardunits="standardunits" # "" or "standardunits"
intertype=nearest
# land/sea mask not yet implemented in this script.
if [ $email = insert_your_Climate_Explorer_email_address_here ]; then
	echo "Please modify this script by inserting your Climate Explorer id at the top of the script"
	exit -1
fi
case $intertype in
	nearest) in="n";;
	interpolate) in="i";;
	*) echo "$0: error: option intertype should be nearest or interpolate, not $intertype"; exit -1;;
esac
case $standardunits in
	"") su="";;
	standardunits) su="_su";;
	*) echo "$0: error: option intertype should be nearest or interpolate, not $intertype"; exit -1;;
esac
# load list of masks, using a random field name
curl https://climexp.knmi.nl/upload_mask.cgi\?id=${email}\&field=cmip5_tas_Amon_ACCESS1-0_historical\&set=countries > /dev/null

for model in $models
do
    for country in $countries
    do
        mask=data/mask$country.$email.poly
        for var in $vars
        do
            # this computes the series
            curl http://climexp.knmi.nl/get_index.cgi\?id=$email\&field=cmip5_${var}_Amon_${model}_$scenario\&maskmetadata=$mask\&standardunits=$standardunits
            i=0
            exist=true
            while [ $exist = true ]
            do
                ens=`printf %03i $i`
                # and this retrieves it
                file=icmip5_${var}_Amon_${model}_${scenario}_${country}_${su}_$ens.dat
                wget http://climexp.knmi.nl/data/$file
                if [ ! -s $file ]; then
                    exist=false
                fi
                i=$((i+1))
            done
        done
    done
done