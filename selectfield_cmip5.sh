#!/bin/sh
# constructs automatically but off-line the HTML file for the CMIP5 ensemble field selection.

# get the list of vars and models from concatenate_years.sh
vars1="tas tasmin tasmax pr evspsbl pme huss taz psl" # prw clwvi # no space
vars2="rlds rlus rlut rsds rsus rsdt rsut hfss hfls"
vars3="mrso mrro mrros sic tos z200 z500"
nvarmax=10
models="modmean onemean mod one ens ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CESM1-CAM5-1-FV2 CESM1-FASTCHEM CESM1-WACCM CMCC-CM CMCC-CMS CMCC-CESM CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H GISS-E2-H-CC GISS-E2-R GISS-E2-R-CC HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MPI-ESM-P MRI-CGCM3 MRI-ESM1 NorESM1-M NorESM1-ME"
exps="historical rcp26 rcp45 rcp60 rcp85"

for table in 1 2 3
do
    case $table in
        1) vars=$vars1;echo "<tr><th colspan=$((2+nvarmax))><a name=surface></a>Surface variables";;
        2) vars=$vars2;echo "<tr><th colspan=$((2+nvarmax))><a name=radiation></a>Radiation variables";;
        3) vars=$vars3;echo "<tr><th colspan=$((2+nvarmax))><a name=ocean></a>Land, Ocean, Sea Ice variables";;
    esac

    nmodel=-5
    for model in $models
    do
    	pmax_prescribed=1
        case $model in
            onemean) modelname="CMIP5 mean (one member per model)";;
            modmean) modelname="CMIP5 mean";;
            modmedian) modelname="CMIP5 median";;
            mod)     modelname="all models";;
            one)     modelname="one member per model";;
            ens)     modelname="all members";;
            GISS*)   pmax_prescribed=3;;
            *)       modelname=$model;;
        esac
        p=0
        while [ $p -lt $pmax_prescribed ]
        do
        	p=$((p+1))
			if [ ${model#GISS} != $model ]; then
				modelname="${model} p$p"
				modelp=${model}_p${p}
			else
				modelp=$model
			fi
	        nmodel=$((nmodel+1))
        	nthree=$(( (nmodel-1)/3 ))
    	    n=$(( nmodel - 3*nthree ))
			if [ $nmodel = -4 -o $n = 1 ]; then
				echo "<tr><th>model<th>exp"
				for var in $vars
				do
					case $var in
						tasmin)  varname="tas<br>min";;
						tasmax)  varname="tas<br>max";;
						evspsbl) varname="evsp<br>sbl";;
						*)       varname=$var;;
					esac
					case $var in
						tas|pr|psl|evspsbl|pme|tasmin|tasmax|taz|huss|r???|hf?s|z?00|tos) varname=$varname;;
						*) varname="<font color=#888888>$varname</font>";;
					esac
					echo "<th>$varname"
				done
			fi
			nexp=0
			for exp in $exps
			do
				hasdata=false
				for var in $vars; do
					case $var in
						?os) type=Omon;;
						mr*) type=Lmon;;
						sic) type=OImon;;
						*) type=Amon;;
					esac
					oldfile="CMIP5/monthly/$var/${var}_${type}_${modelp}_${exp}_00.nc"
					file="CMIP5/monthly/$var/${var}_${type}_${modelp}_${exp}_000.nc"
					if [ -e $file -o -L $file -o -s $oldfile -o -L $oldfile ]; then
						hasdata=true
					else
						if [ $p -gt 1 ]; then
							echo "<!-- cannot find CMIP5/monthly/$var/${var}_${type}_${modelp}_${exp}_000.nc -->"
						fi
					fi
				done
				if [ $hasdata = true ]; then
					nexp=$((nexp+1))
					if [ $nexp = 1 ]; then
						echo "<tr><td>$modelname"
					else
						echo "<tr><td>&nbsp;"
					fi
					echo "<td>$exp"
					for var in $vars
					do
						case $var in
							?os) type=Omon;;
							mr*) type=Lmon;;
							sic) type=OImon;;
							*) type=Amon;;
						esac
						oldfile=CMIP5/monthly/$var/${var}_${type}_${modelp}_${exp}_00.nc
						file=CMIP5/monthly/$var/${var}_${type}_${modelp}_${exp}_000.nc
						if [ -e $file -o -L $file -o -e $oldfile -o -L $oldfile ]; then
							if [ -e $file -o -L $file ]; then
								f=$file
							else
								f=$oldfile
							fi
							files=`echo $f | sed -e 's/_000/_???/' -e 's/_00/_??/'`
							n=`echo $files | wc -w`
							echo "<td><input type=radio class=formradio name=field value=cmip5_${var}_${type}_${modelp}_${exp}><small>${n}</small>"
						else
							echo "<td>&nbsp;<!-- cannot find $file -->"
						fi
					done
				fi
			done
		done
    done
done


