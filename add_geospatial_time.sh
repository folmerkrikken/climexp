#!/bin/bash
###et -x
# add geospatial* metadata variables to netcdf metadata
[ -z "$file" ] && echo "$0: error: set variable file" && exit -1
[ ! -s "$file" ] && echo "$0: error: cannot find file $file" && exit -1
c=`ncdump -h $file | fgrep -v _resolution | fgrep -c ":geospatial_"`
if [ $c != 0 ]; then
    echo "$0: geospatial information already in $file, do nothing"
else
    tmpfile=/tmp/add_geospatial_$$.txt
    describefield $file > $tmpfile 2>&1
    latline=`cat $tmpfile | fgrep "Y axis"`
    gridtype=`echo $latline | awk '{print $3}'`
    if [ $gridtype = regular ]; then
        latstep=`echo $latline | awk '{print $7}' | sed -e 's/&deg;//'`
        latstep=${latstep#-} # no negative steps
    fi
    if [ $gridtype = irregular ]; then
        latline=`cat $tmpfile | fgrep 'Y axis'`
        lat1=`echo $latline | awk '{print $9}'`
        n=8
        l=start
        while [ -n "$l" -a $n -lt 100 ]; do
            ((n++))
            lat2=$l
            l=`echo $latline | awk "{print \$"$n"}"`
            ###echo "l=$l"
        done
    else
        latline=`cat $tmpfile | fgrep 'first point' | tail -n 1`
        lat1=`echo $latline | awk '{print $4}' | sed -e 's/&deg;//'`
        ns1=`echo $latline | awk '{print $5}' | tr -d ','`
        [ $ns1 = 'S' ] && lat1="-$lat1"
        lat2=`echo $latline | awk '{print $9}' | sed -e 's/&deg;//'`
        ns2=`echo $latline | awk '{print $10}'`
        [ $ns2 = 'S' ] && lat2="-$lat2"
    fi
    ilat1=${lat1%\.*}
    ilat2=${lat2%\.*}
    if [ $ilat1 -gt $ilat2 ]; then
        aap=$lat1
        lat1=$lat2
        lat2=$aap
    fi
    if [ $gridtype = regular ]; then
        [ $ilat1 -gt -90 ] && lat1=`echo "$lat1-$latstep/2" | bc -l | sed -e 's/0*$//'`
        [ $ilat2 -lt  90 ] && lat2=`echo "$lat2+$latstep/2" | bc -l | sed -e 's/0*$//'`
    elif [ $gridtype = Gaussian ]; then
        [ $ilat1 -le -87 ] && lat1=90
        [ $ilat2 -ge  87 ] && lat2=90
    fi
    lonline=`cat $tmpfile | fgrep "X axis"`
    gridtype=`echo $lonline | awk '{print $3}'`
    if [ "$gridtype" = irregular ]; then
        lon1=`echo $lonline | awk '{print $9}'`
        n=8
        l=start
        while [ -n "$l" -a $n -lt 100 ]; do
            ((n++))
            lon2=$l
            l=`echo $lonline | awk "{print \$"$n"}"`
            ###echo "l=$l"
        done
    elif [ -n "$gridtype" ]; then
        lonstep=`echo $lonline | awk '{print $7}' | sed -e 's/&deg;//' | tr -d ' -'`
        lonline=`cat $tmpfile | fgrep 'first point' | head -n 1`
        lon1=`echo $lonline | awk '{print $4}' | sed -e 's/&deg;//'`
        ew1=`echo $lonline | awk '{print $5}' | tr -d ','`
        [ $ew1 = 'W' ] && lon1="-$lon1"
        lon2=`echo $lonline | awk '{print $9}' | sed -e 's/&deg;//'`
        ew2=`echo $lonline | awk '{print $10}'`
        [ $ew2 = 'W' ] && lon2="-$lon2"
    fi
    if [ -n "$lonstep" ]; then
        lon1=`echo "$lon1-$lonstep/2" | bc -l | sed -e 's/0*$//'`
        [ -z "$lon1" ] && lon1=0 # gets deleted completely :-(
        lon2=`echo "$lon2+$lonstep/2" | bc -l | sed -e 's/0*$//'`
        [ -z "$lon2" ] && lon2=0 # gets deleted completely :-(
    fi

    ncatted -h -a "geospatial_lat_min",global,c,f,$lat1 \
            -a "geospatial_lat_max",global,c,f,$lat2 \
            -a "geospatial_lat_units",global,c,c,"degrees_north" \
            -a "geospatial_lon_min",global,c,f,$lon1 \
            -a "geospatial_lon_max",global,c,f,$lon2 \
            -a "geospatial_lon_units",global,c,c,"degrees_east" \
                $file
    if [ -n "$latstep" ]; then
        ncatted -h -a "geospatial_lat_resolution",global,c,f,"$latstep" $file
    fi
    if [ -n "$lonstep" ]; then
        ncatted -h -a "geospatial_lon_resolution",global,c,f,"$lonstep" $file
    fi
fi
c=`ncdump -h $file | fgrep -c ':time_coverage_end'`
if [ $c != 0 ]; then
    echo "$0: time_coverage information already in $file, do nothing"
else
    if [ -z "$tmpfile" ]; then
        tmpfile=/tmp/add_geospatial_$$.txt
        describefield $file > $tmpfile 2>&1
    fi
    startdate=`cat $tmpfile | fgrep 'available from' | awk '{print $5}'`
    stopdate=`cat $tmpfile | fgrep 'available from' | awk '{print $7}'`
    c=`cat $tmpfile | fgrep available | fgrep -c Monthly`
    d=`cat $tmpfile | fgrep available | fgrep -c daily`
    if [ $c = 1 ]; then
        startyr=${startdate#???}
        startmon=${startdate%????}
        stopyr=${stopdate#???}
        stopmon=${stopdate%????}
        startday=15
        stopday=15
    elif [ $d = 1 ]; then
        startyr=${startdate#?????}
        startmon=${startdate%????}
        startmon=${startmon#??}
        startday=${startdate%???????}
        stopyr=${stopdate#?????}
        stopmon=${stopdate%????}
        stopmon=${stopmon#??}
        startday=${stopdate%???????}    
    else
        echo "$0: cannot handle this time scale yet"
        exit
    fi
    i=0
    for mon in $startmon $stopmon; do
        ((i++))
        case $mon in
            Jan) mo=01;;
            Feb) mo=02;;
            Mar) mo=03;;
            Apr) mo=04;;
            May) mo=05;;
            Jun) mo=06;;
            Jul) mo=07;;
            Aug) mo=08;;
            Sep) mo=09;;
            Oct) mo=10;;
            Nov) mo=11;;
            Dec) mo=12;;
            *) echo "$0: error: unknown month $mon" in $file; cat $tmpfile; exit -1
        esac
        [ $i = 1 ] && startmo=$mo
        [ $i = 2 ] && stopmo=$mo
    done
    ncatted -h -a time_coverage_start,global,c,c,"${startyr}-${startmo}-${startday}" \
           -a time_coverage_end,global,c,c,"${stopyr}-${stopmo}-${startday}" \
                $file
fi
