#!/bin/bash
function getfile {
    if [ $gcm = ave ]; then
        file=CORDEX/$domain/$timescale/$var/${var}_${domain}_cordex_${exp}_${timescale}_ave.nc
    elif [ $gcm = ens ]; then
        file=CORDEX/$domain/$timescale/$var/${var}_${domain}_cordex_${exp}_${timescale}_000.nc
    else
        file=`ls CORDEX/$domain/$timescale/$var/${var}_${domain}_${gcm}_${exp}_${rip}_${rcm}_${version}_${timescale}_*_latlon.nc 2> /dev/null | head -1 `
    fi
}
# constructs automatically but off-line the HTML file for the CORDEX ensemble field selection.
timescale="$1"
if [ -z "$timescale" ]; then
    echo "usage: $0 mon|annual"
    exit -1
fi
# get the list of vars and models from concatenate_years.sh
for domain in EUR-44
do
    version=v1
    echo "<th colspan=13>$domain</th>"

    exps="historical rcp26 rcp45 rcp85"
    if [ $timescale = "mon" ]; then
        vars="tas tasmin tasmax pr" # prw clwvi # no space
        gcms="CCCma-CanESM2 CNRM-CERFACS-CNRM-CM5 CSIRO-QCCCE-CSIRO-Mk3-6-0 ICHEC-EC-EARTH IPSL-IPSL-CM5A-MR MIROC-MIROC5 MOHC-HadGEM2-ES MPI-M-MPI-ESM-LR NCC-NorESM1-M NOAA-GFDL-GFDL-ESM2M"
        rcms="SMHI-RCA4 CNRM-ALADIN53 KNMI-RACMO22E DMI-HIRHAM5 MPI-CSC-REMO2009"
    elif [ $timescale = 'annual' ]; then
        echo "not yet ready"
        exit -1
    else
        echo "$0: error: unknown timescale $timescale"
        exit -1
    fi

    nmodel=-2
    for gcm in ave ens $gcms
    do
        if [ $nmodel -ge 10 ]; then
            nmodel=0
        fi
        if [ $nmodel -le 0 ]; then
            if [ $nmodel -lt 0 ]; then
                echo "<tr><th>GCM/RCM<th>&nbsp;<th>exp"
            else
                echo "<tr><th>GCM<th>RCM<th>exp"
            fi
            for var in $vars; do
                echo "<th>$var"
            done
        fi
        if [ $gcm = ave -o $gcm = ens ]; then
            rcmlist="all"
            riplist="all"
        else
            rcmlist="$rcms"
            riplist="r1i1p1 r2i1p1 r3i1p1 r12i1p1"
        fi
        for rcm in $rcmlist
        do
            for rip in $riplist
            do
                nexp=0
                anydata=false
                for exp in $exps
                do
                    hasdata=false
                    for var in $vars; do
                        getfile
                        if [ -n "$file" -a \( -e "$file" -o -L "$file" \) ]; then
                            hasdata=true
                        fi
                    done
                    if [ $hasdata = true ]; then
                        anydata=true
                        nexp=$((nexp+1))
                        if [ $nexp = 1 ]; then
                            if [ $rcm = all ]; then
                                echo "<tr><td>$gcm<td>all 1951-2099"
                            else
                                echo "<tr><td>$gcm $rip<td>$rcm"
                            fi
                        else
                            echo "<tr><td>&nbsp;<td>&nbsp;"
                        fi
                        echo "<td>$exp"
                        for var in $vars
                        do
                            getfile
                            if [ -n "$file" -a \( -e "$file" -o -L "$file" \) ]; then
                                echo "<td><input type=radio class=formradio name=field value=cordex_${domain}_${var}_${gcm}_${exp}_${rip}_${rcm}_${timescale}>"
                            else
                                echo "<td>&nbsp;<!-- cannot find $file -->"
                            fi
                        done
                    fi
                done # exp
                if [ $anydata = true ]; then
                    nmodel=$((nmodel+1))
                fi
            done # rip
        done # rcm
    done # gcm
done # domain
