#!/bin/sh

cat << EOF
Content-Type: text/plain


EOF
if [ $REMOTE_ADDR != 127.0.0.1 -a $REMOTE_ADDR != 82.95.194.243 -a $REMOTE_ADDR != "::1" ]; then
echo "who are you, $REMOTE_ADDR ?"
exit
fi

type="$1"
if [ -z "$type" ]; then
     echo "usage: curl http://clocalhost/clean_atlas.cgi\\?plots|diff|regr|series|sd"
     exit -1
fi
[ $type = diff ] && rm -rf atlas/diff/*/rcp??/*
[ $type = diffext ] && rm -rf atlas/diff/CMIP5ext*/rcp??/*
[ $type = regr ] && rm -rf atlas/regr/*/rcp??/*
[ $type = mapsext ] && rm -rf atlas/maps/CMIP5ext*/* atlas/maps/CMIP5ext*/*
[ $type = mapsext ] && rm -f atlas/diff/CMIP5ext*/rcp??/quant/* atlas/diff/CMIP5ext/rcp??/*withsd.nc
[ $type = maps ] && rm -rf atlas/maps/*
[ $type = plots ] && rm -rf atlas/series/*/eps*/* atlas/series/*/quantiles/* atlas/series/*/plotfiles/*
[ $type = plotsext ] && rm -rf atlas/series/CMIP5ext*/eps*/* atlas/series/CMIP5ext*/quantiles/* atlas/series/CMIP5ext*/plotfiles/*
if [ $type = series ]; then
  rm -rf atlas/series/*/rcp??/monthly*/*
fi
if [ $type = anom ]; then
  rm -rf atlas/series/*/rcp??/monthly_anom*/*
fi
if [ $type = dump ]; then
  rm -rf atlas/series/*/rcp??/monthly_dump*/*
fi
# usage: eg vartas, varpr, ...
if [ ${type#var} != $type ]; then
	var=${type#var}
	find atlas/ -name "*_${var}_*" -exec rm {} \;
fi
