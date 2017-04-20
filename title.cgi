#!/bin/sh
# set the time-independent part of the title
case "${NPERYEAR:-12}" in
-1) timescale="year";timely="annual (Jul-Jun)";;
1) timescale="year";timely="annual";;
4) timescale="season";timely="seasonal";;
12) timescale="month";timely="monthly";;
36) timescale="decade";timely="decadal";;
73) timescale="pentad";timely="pentad";;
360) timescale="day";timely="daily";;
365) timescale="day";timely="daily";;
366) timescale="day";timely="daily";;
*) timescale="period";timely="period";;
esac

if [ "${FORM_month:-0}" = "0" ]; then
  if [ "${FORM_sum:-1}" -gt 1 ]; then
    seriesmonth="${FORM_sum}-"$timely
  else
    seriesmonth=$timely
  fi
  if [ -z "$FORM_lag" -o "$FORM_lag" = 0 ]; then
    indexmonth=""
  else
    indexmonth="${FORM_lag}$timescale-lag"
  fi
fi
if [ ${NPERYEAR:-12} != 12 ]; then
  if [ "${FORM_lag:-0}" != "0" ]; then
    indexmonth="${FORM_lag}$timescale-lag"
    if [ ${FORM_sum:-1} != 1 -a $NPERYEAR -gt 12 ]; then
      indexmonth="${FORM_sum}$timescale $indexmonth"
      if [ -n "$seriesmonth" ]; then
        seriesmonth="${FORM_sum}$timescale $seriesmonth"
      else
        seriesmonth="${FORM_sum}$timescale"
      fi
    fi
  elif [ $NPERYEAR -gt 12 ]; then
    if [ ${FORM_sum:-1} != 1 ]; then
      indexmonth="${FORM_sum}$timescale"
      if [ -n "$seriesmonth" ]; then
        seriesmonth="${FORM_sum}$timescale $seriesmonth"
      else
        seriesmonth="${FORM_sum}$timescale"
      fi
    elif [ ${FORM_sum:-1} != 1 ]; then
      indexmonth=$timely
      if [ -n "$seriesmonth" ]; then
        seriesmonth="${FORM_sum}$timescale $seriesmonth"
      else
        seriesmonth="${FORM_sum}$timescale"
      fi
    fi
  fi
fi
if [ "$FORM_plottype" = "time-lon" ]; then
  if [ -z "$FORM_lat2" -o "$FORM_lat1" = "$FORM_lat2" ]; then      
    indexmonth="$indexmonth ${FORM_lat1}N"
  else
    indexmonth=""
  fi
  if [ -n "$FORM_lag" ]; then
    if [ "$FORM_fix" = "fix1" ]; then
      indexmonth="${FORM_lag}$timescale-lag"
    else
      seriesmonth="${FORM_lag}$timescale-lag"
    fi
  fi
fi
if [ "$FORM_plottype" = "time-lat" ]; then
  if [ -z "$FORM_lon2" -o "$FORM_lon1" = "$FORM_lon2" ]; then
    indexmonth="${FORM_lon1}E"
  else
    indexmonth=""
  fi
  if [ -n "$FORM_lag" ]; then
    if [ "$FORM_fix" = "fix1" ]; then
      indexmonth="${FORM_lag}$timescale-lag"
    else
      seriesmonth="${FORM_lag}$timescale-lag"
    fi
  fi
fi

ylabel=" "
climfield1=$climfield
if [ -z "$FORM_field" ]; then
    [ -n "$FORM_log" ] && ylabel=" log$ylabel"
    [ -n "$FORM_sqrt" ] && ylabel=" sqrt$ylabel"
    [ -n "$FORM_square" ] && ylabel=" ${ylabel}^2"
else
    [ -n "$FORM_log" ] && climfield1="log $climfield"
    [ -n "$FORM_sqrt" ] && climfield1="sqrt $climfield"
    [ -n "$FORM_square" ] && climfield1="${climfield}^2"
fi
extra=""
if [ -n "$FORM_anomal" -o \( "FORM_operation" = "selecting" -a ${FORM_sum:-1} -gt 1 \) ]; then
  if [ `echo "$CLIM" | fgrep -c "anom"` = 0 ]; then
    anoclim="$CLIM anomalies"
  fi
  if [ `echo "$climfield" | fgrep -c "anom"` = 0 ]; then
    climfield1="$climfield1 anomalies"
  fi
else
  anoclim="$CLIM"
fi
if [ -n "$FORM_nens1" -o -n "$FORM_nens2" ]; then
  extra=" ${FORM_nens1}:${FORM_nens2}$extra"
fi

if [ -n "$FORM_ndiff" -o -n "$FORM_ndiff2" -o -n "$FORM_diff" -o -n "$FORM_detrend" -o "${FORM_debias:-none}" != "none" ]; then
  bracket=true
  extra="$extra ("
  started=""
fi
if [ -n "$FORM_nooverlap" ]; then
    nooverlap=", no overlap"
fi
if [ -n "$ndiff" ]; then
  if [ -n "$ndiff2" ]; then
    extra="$extra${ndiff2}, ${ndiff}-yr running means$nooverlap"
  else
    extra="$extra${ndiff}-yr running mean$nooverlap"
  fi
  started=true
else
  if [ -n "$ndiff2" ]; then
    extra="$extra$ndiff2 running mean$nooverlap"
    started=true
  fi
  if [ -n "$FORM_diff" ]; then
    extra="${extra}diff"
    started=true
  fi
fi
if [ -n "$FORM_detrend" ]; then
  [ -n "$started" ] && extra="${extra}, "
  extra="${extra}detrend"
  started=true
fi
if [ ${FORM_debias:-none} != none ]; then
  [ -n "$started" ] && extra="${extra}, "
  extra="${extra}debias $FORM_debias"
  started=true
fi
if [ -n "$bracket" ]; then
  extra="${extra})"
fi
if [ -n "$ENSEMBLE" -a -n "$FORM_ensanom" ]; then
  extra="$extra\\ anomalies wrt ensemble mean"
fi
###echo "startstop=$startstop, "`cat $startstop`
if [ -n "$startstop" -a -s ${startstop:-aap} ]; then
  yrstart=`head -1 $startstop`
  yrstop=`tail -1 $startstop`
  if [ ${startstop#/tmp} != $startstop ]; then
    rm $startstop
  fi
fi
if [ -n "$yrstart" ]; then
  extra="$extra $yrstart:$yrstop"
elif [ -n "$FORM_begin2" ]; then
  extra="$extra ${FORM_begin2}-$FORM_end2"
  if [ -n "$FORM_begin" ]; then
    extrap=" ${FORM_begin}-$FORM_end"
  fi
elif [ -n "$FORM_end" ]; then
  if [ -n "$FORM_begin" ]; then
    extra="$extra ${FORM_begin}-$FORM_end"
  else
    extra="$extra ending $FORM_end"
  fi
elif [ -n "$FORM_begin" ]; then
  extra="$extra beginning $FORM_begin"
fi

if [ -n "$FORM_dgt" ]; then
  if [ -n "$FORM_dlt" ]; then
    titleclim="$anoclim, $FORM_dgt < $anoclim < $FORM_dlt"
  else
    titleclim="$anoclim > $FORM_dgt"
  fi
elif [ -n "$FORM_dlt" ]; then
  titleclim="$anoclim < $FORM_dlt"
else
  titleclim="$anoclim"
fi

if [ -n "$FORM_gt" ]; then
  if [ -n "$FORM_lt" ]; then
    extra="$extra, $FORM_gt < $climfield < $FORM_lt"
  else
    extra="$extra, $climfield > $FORM_gt"
  fi
elif [ -n "$FORM_lt" ]; then
  extra="$extra, $climfield < $FORM_lt"
fi

if [ "$FORM_type" = histogram ]; then
  with=""
elif [ -n "$FORM_STATION" ]; then
  if [ "$FORM_var" = "composite" ]; then
    with="of"
  else
    with="with"
  fi
  if [ -n "$kindname" ]; then
    with="\\$with $indexmonth $kindname $climfield1$extra"
  else
    with="\\$with $indexmonth $climfield1$extra"
  fi
elif [ -n "$extra" ]; then
  with="\ $extra"
fi
if [ -n "$FORM_year2" ]; then
  seriesmonth=""
fi
case "$FORM_var" in
higa) var="fit of Gaussian to";;
hime) var="mean";;
hisd) var="s.d.";;
hisk) var="skew";;
higr) var="return time of $FORM_year in normal fit\\";;
higR) var="2.5% lower bound on return time of $FORM_year in normal fit\\";;
hipr) var="return time of $FORM_year in GPD fit, threshold ${FORM_threshold}%\\";;
hipR) var="2.5% lower bound on return time of $FORM_year in GPD fit, threshold ${FORM_threshold}%\\";;
hivr) var="return time of $FORM_year in GEV fit\\";;
hivR) var="2.5% lower bound on return time of $FORM_year in GEV fit\\";;
atr1) var="return time of $FORM_year";;
atr2) var="return time in climate of $FORM_begin2";;
atra) var="log10(ratio) of return times";; 
"") var="corr";;
ave*) var=`echo $FORM_var | sed -e 's/ave[(]\([a-z0-9]*\),t[^)]*[)]/\1/' -e 's/[(]time=[^)]*[)]//'`;;
*) var="${FORM_var%(*}";;
esac

if [ -n "$FORM_day" ]; then
    if [ -z "$FORM_hour" ]; then
        day="$FORM_day"
        if [ -n "$FORM_plotsum" ]; then
            day=${day}-$((day+FORM_plotsum-1))
        fi
    else
        day="${FORM_hour}Z$FORM_day"
        if [ -n "$FORM_plotsum" ]; then
            day=${day}-$((FORM_hour+FORM_plotsum-1))"Z$FORM_day"
        fi
    fi
fi
if [ "$lwrite" = true ]; then
  echo '<pre>'
  echo title.cgi
  echo RANK=$RANK
  echo var=$var
  echo day=$day
  echo seriesmonth=$seriesmonth
  echo climfield1=$climfield1
  echo kindname=$kindname
  echo plotyear=$plotyear
  echo ylabel=$ylabel
  echo station=$station
  echo titleclim=$titleclim
  echo extrap=$extrap
  echo with=$with
  echo '</pre>'
fi
title="$RANK$var $day$seriesmonth$plotyear$ylabel$station $titleclim$extrap$with"
if [ -n "$FORM_pmin" ]; then
  if [ ${FORM_pmin#-} = ${FORM_pmin} -a $FORM_pmin != 100 -a $FORM_pmin != 0 ]; then
    title="$title p<${FORM_pmin}%"
  fi
fi
