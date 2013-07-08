#!/bin/sh
# more functions, these are only for the web version

function lookup_region {
	# in order to use the Atlas routine in the KNMI Atlas
	# a routine to translate the srex+ name into the Atlas region/subregion convention
	[ "$lwrite" = true ] && echo "lookup_region: input $FORM_srex<br>"
	case "$FORM_srex" in
		world) region=world; subregion=3;;
		worldland) region=world; subregion=1;;
		worldsea) region=world; subregion=2;;
		NAmerica|SAmerica|Europe|Africa|Asia|Australia) region=$FORM_srex; subregion=1;;
		Arcticland) region=arctic; subregion=1;;
		Arcticsea) region=arctic; subregion=2;;
		CGI) region=highlatitudes; subregion=1;;
		NAS) region=highlatitudes; subregion=2;;
		ALA) region=westnorthamerica; subregion=1;;
		WNA) region=westnorthamerica; subregion=2;;
		CNA) region=eastnorthamerica; subregion=1;;
		ENA) region=eastnorthamerica; subregion=2;;
		CAM) region=centralamerica; subregion=1;;
		Caribbean) region=centralamerica; subregion=2;;
		AMZ) region=northsouthamerica; subregion=1;;
		NEB) region=northsouthamerica; subregion=2;;
		WSA) region=southsouthamerica; subregion=1;;
		SSA) region=southsouthamerica; subregion=2;;
		NEU) region=northeurope; subregion=1;;
		CEU) region=northeurope; subregion=2;;
		MED) region=mediterranean; subregion=1;;
		SAH) region=mediterranean; subregion=2;;
		WAF) region=weafrica; subregion=1;;
		EAF) region=weafrica; subregion=2;;
		SAF) region=southafrica; subregion=1;;
		WIndian) region=southafrica; subregion=2;;
		WAS) region=centralasia; subregion=1;;
		CAS) region=centralasia; subregion=2;;
		TIB) region=eastasia; subregion=2;;
		EAS) region=eastasia; subregion=1;;
		SAS) region=southasia; subregion=1;;
		NIndian) region=southasia; subregion=2;;
		SEA) region=southeastasia; subregion=1;;
		SEAsia_sea) region=southeastasia; subregion=2;;
		NAU) region=australia; subregion=1;;
		SAU) region=australia; subregion=2;;
		NTPacific) region=pacific; subregion=1;;
		EQPacific) region=pacific; subregion=2;;
		STPacific) region=pacific; subregion=3;;
		Antarcticland) region=antarctica; subregion=1;;
		Antarcticsea) region=antarctica; subregion=2;;
		*) echo "lookup_region: error: cannot find input $FORM_srex"; exit -1;;
	esac
	[ "$lwrite" = true ] && echo "lookup_region: found region=$region, subregion=$subregion <br>"
}

function get_file_list {

	# output a list of files in $files and a directory to put the output $dir
	
	var=$FORM_var
	case $FORM_var in
		tas|tasmin|tasmax|pr|evspsbl|pme|huss|rsds|psl) type=Amon;;
		tos|sos|zos) type=Omon;;
		sic) type=OImon;;
		*) echo "error: unknown variable $FORM_var"
			. ./myvinkfoot.cgi
			exit;;
	esac

	if [ $FORM_output = map -o $FORM_region = mask ]; then
		# interpolated fields
		res=_144
	else
		res=""
	fi
	case $FORM_dataset in
		CMIP5) 
			if [ "$FORM_plotvar" = mean -a -n "$res" ]; then
				files=CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_modmean_${FORM_scenario_cmip5}_00.nc
			else
				# we know that p goes to 3...
				files="CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_*_${FORM_scenario_cmip5}_r*i1p1$res.nc \
					  CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_*_${FORM_scenario_cmip5}_r*i1p2$res.nc \
					  CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_*_${FORM_scenario_cmip5}_r*i1p3$res.nc"
			fi
			dir=$FORM_dataset/$FORM_scenario_cmip5;;
		CMIP5one) 
			if [ "$FORM_plotvar" = mean -a -n "$res" ]; then
				files=CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_onemean_${FORM_scenario_cmip5}_00.nc
			else
				# we know that p goes to 3...
				files="CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_[^E]*_${FORM_scenario_cmip5}_r1i1p1$res.nc \
					  CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_EC-EARTH_${FORM_scenario_cmip5}_r8i1p?$res.nc \
					  CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_[^E]*_${FORM_scenario_cmip5}_r1i1p2$res.nc \
					  CMIP5/monthly/${FORM_var}/${FORM_var}_${type}_[^E]*_${FORM_scenario_cmip5}_r1i1p3$res.nc"
			fi
			dir=$FORM_dataset/$FORM_scenario_cmip5;;
		CMIP3) 
			if [ "$FORM_plotvar" = mean -a -n "$res" ]; then
				files=IPCCData/$FORM_scenario_cmip3/${FORM_var}_cmip3_ave_mean$res.nc
			else
				files=""
				for model in $cmip3models; do
					FORM_field=${FORM_var}_${model}_${FORM_scenario_cmip3}
					file=""
					. ./queryfield.cgi
					[ -n "$file" ] && files="$files $file"
				done
			fi
			dir=$FORM_dataset/$FORM_scenario_cmip3;;
		RT2b)
			if [ "$FORM_plotvar" = mean ]; then
				files=ENSEMBLES_RCM/rt2b/rt2b_modmean_${FORM_scenario_rt2b}_25km_${FORM_var}_00.nc
			else
				files=ENSEMBLES_RCM/rt2b/rt2b_*_${FORM_scenario_rt2b}_25km_${FORM_var}_MM.nc
			fi
			dir=$FORM_dataset/$FORM_scenario_rt2b;;
		RT3)
			if [ "$FORM_plotvar" = mean ]; then
				files=ENSEMBLES_RCM/rt3/rt3_modmean_25km_${FORM_var}_00.nc
			else
				files=ENSEMBLES_RCM/rt3/rt3_*_25km_${FORM_var}_MM.nc
			fi
			dir=$FORM_dataset;;
		ERAi) FORM_field=erai_${FORM_var}; . ./queryfield.cgi; files=$file
			dir=$FORM_dataset;;
		20CR) FORM_field=c${FORM_var}; . ./queryfield.cgi; files=$file
			dir=$FORM_dataset;;
		obs) field_name=FORM_obs_$FORM_obs
			FORM_field=${!field_name}; . ./queryfield.cgi; files=$file
			dir=$FORM_dataset/$FORM_field;;
		*) echo "error: unknown dataset $FORM_dataset"; . ./myvinkfoot.cgi; exit;;
	esac

	firstfile=`ls $files | head -1`
	if [ ! -s $firstfile ]; then
		echo "error: cannot find file $firstfile"
		. ./myvinkfoot.cgi
		exit
	fi
}

function get_model {
	# get the model name back from the file name :-(
	# also set LSMASK while we are at it.
	[ -z "$var" ] && var=$FORM_var
	case $FORM_dataset in
		CMIP5*) 
			model=`basename $file .nc`
			model=${model#${var}_${type}_}
			model=${model%_${FORM_scenario_cmip5}*}
			if [ ${model%mean} != $model ]; then
				# coordinate qith quesryfield...
				if [ $var = sic -o $var = tos -o $var = sos ]; then
					LSMASK=CMIP5/monthly/lsmask_cmip3_288.nc
				else
					LSMASK=CMIP5/monthly/lsmask_cmip3_144.nc
				fi
			else
				if [ $type = Amon -o $type = Lmon ]; then
					case $model in
	           			HadGEM2*)  trylsmask=CMIP5/fixed/sftlf_fx_HadGEM2-ES_historical_r1i1p1.nc;;
						inmcm4)    trylsmask=CMIP5/fixed/sftlf_fx_${model}_rcp45_r0i0p0.nc;;
						*)         trylsmask=CMIP5/fixed/sftlf_fx_${model}_historical_r0i0p0.nc;;
					esac
				fi
				if [ -n "$trylsmask" -a \( -s "$trylsmask" -o -s $HOME/climexp/$trylsmask \) ]; then
					LSMASK=$trylsmask
				fi
			fi
			;;
		CMIP3) 
			model=`basename $file | sed -e 's/0[0-9]/%%/'`
			line=fgrep $model queryfield.cgi
			FORM_field=${line%\)*}
			model=${FORM_field#*_}
			LSMASK=${line#*LSMASK=}
			LSMASK=${LSMASK%;*}
			;;
		RT2b)
			model=`basename $file .nc`
			model=${model#rt2b_}
			model=${model%_${FORM_scenario_rt2b}*};;
		RT3)
			model=`basename $file .nc`
			model=${model#rt2b_}
			model=${model%_25km*};;
		ERAi) # from here on LSMASK has been set by the call to queryfield.cgi in get_file_list
			model=erai;;
		20CR) 
			model=20c;;
		obs) 
			model=$FORM_field;;
		*) echo "error: unknown dataset $FORM_dataset"; . ./myvinkfoot.cgi; exit;;
	esac
	if [ -z "$model" ]; then
		echo "something went wrong in get_model with dataset $FORM_datset and var $var"
		. ./myvinkfoot.cgi
		exit
	fi
	if [ -z "$LSMASK" ]; then
		echo "LSMASK is undefined with dataset $FORM_dataset and var $var"
		. ./myvinkfoot.cgi
		exit
	fi
	if [ ! -s "$LSMASK" ]; then
		echo "cannot find LSMASK $LSMASK"
		. ./myvinkfoot.cgi
		exit
	fi
}

function get_region_extension {
	case "$FORM_region" in
		srex) region_extension=$FORM_srex;;
		point) region_extension=${FORM_lat}N_${FORM_lon}E;;
		box|mask) region_extension=${FORM_lat1}-${FORM_la2}N_${FORM_lon1}-${FORM_lon2}E;;
		*) echo "error: unknown region $FORM_region"; exit -1;;
	esac
}
