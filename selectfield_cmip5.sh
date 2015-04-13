#!/bin/sh
# constructs automatically but off-line the HTML file for the CMIP5 ensemble field selection.
timescale="$1"
if [ -z "$timescale" ]; then
    echo "usage: $0 monthly|annual"
    exit -1
fi
# get the list of vars and models from concatenate_years.sh
if [ $timescale = "monthly" ]; then
    vars1="tas tasmin tasmax pr evspsbl pme hurs taz psl" # prw clwvi # no space
    namevars1="<tr><th colspan=$((2+nvarmax))><a name=surface></a>Surface variables"
    vars2="rlds rlus rlut rsds rsus rsdt rsut hfss hfls"
    namevars2="<tr><th colspan=$((2+nvarmax))><a name=radiation></a>Radiation variables"
    vars3="mrso mrro mrros snc snd sic tos z200 z500"
    namevars3="<tr><th colspan=$((2+nvarmax))><a name=ocean></a>Land, Ocean, Sea Ice variables"
    models="modmean onemean mod one ens ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CESM1-CAM5-1-FV2 CESM1-FASTCHEM CESM1-WACCM CMCC-CM CMCC-CMS CMCC-CESM CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H GISS-E2-H-CC GISS-E2-R GISS-E2-R-CC HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MPI-ESM-P MRI-CGCM3 MRI-ESM1 NorESM1-M NorESM1-ME"
elif [ $timescale = 'annual' ]; then
    vars1="altcdd csdi altcwd dtr fd gsl id prcptot"
    namevars1="<tr><th colspan=$((2+nvarmax))><a name=mix></a>mixed variables"
    vars2="r1mm r10mm r20mm r95p r99p rx1day rx5day sdii su"
    namevars2="<tr><th colspan=$((2+nvarmax))><a name=prcp></a>precipitation extremes"
    vars3="tn10p tn90p tnn tnx tx10p tx90p txn txx wsdi"
    namevars3="<tr><th colspan=$((2+nvarmax))><a name=temp></a>temperature extremes"
models="modmean onemean mod one ens ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 CCSM4 CESM1-BGC CMCC-CM CMCC-CMS CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-R HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MPI-ESM-P MRI-CGCM3 MRI-ESM1 NorESM1-M"
else
    echo "$0: error: unknown timescale $timescale"
    exit -1
fi

nvarmax=10
exps="historical rcp26 rcp45 rcp60 rcp85 rcp45to85 piControl"

for table in 1 2 3
do
    case $table in
        1) vars=$vars1;echo $namevars1;;
        2) vars=$vars2;echo $namevars2;;
        3) vars=$vars3;echo $namevars3;;
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
						rx1day)  varname="rx1<br>day";;
						rx5day)  varname="rx5<br>day";;
						*)       varname=$var;;
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
						sn?) type=LImon;;
	                     cdd|altcdd|csdi|cwd|altcwd|dtr|fd|gsl|id|prcptot|r1mm|r10mm|r20mm|r95p|r99p|rx1day|rx5day|sdii|su|tn10p|tn90p|tnn|tnx|tx10p|tx90p|txn|txx|wsdi) type=yr;;
						*) type=Amon;;
					esac
					oldfile="CMIP5/$timescale/$var/${var}_${type}_${modelp}_${exp}_00.nc"
					file="CMIP5/$timescale/$var/${var}_${type}_${modelp}_${exp}_000.nc"
					if [ -e $file -o -L $file -o -s $oldfile -o -L $oldfile ]; then
						hasdata=true
					else
						if [ $p -gt 1 ]; then
							echo "<!-- cannot find CMIP5/$timescale/$var/${var}_${type}_${modelp}_${exp}_000.nc -->"
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
						        sn?) type=LImon;;
                        	cdd|altcdd|csdi|cwd|altcwd|dtr|fd|gsl|id|prcptot|r1mm|r10mm|r20mm|r95p|r99p|rx1day|rx5day|sdii|su|tn10p|tn90p|tnn|tnx|tx10p|tx90p|txn|txx|wsdi) type=yr;;
							*) type=Amon;;
						esac
						oldfile=CMIP5/$timescale/$var/${var}_${type}_${modelp}_${exp}_00.nc
						file=CMIP5/$timescale/$var/${var}_${type}_${modelp}_${exp}_000.nc
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


