#!/bin/bash
# to be sourced from getdata.cgi, correlate.cgi
if [ "$TYPE" = "p" ]; then
  if [ $NPERYEAR = 12 ]; then
    if [ -z "$FORM_sum" -o "$FORM_sum" = "1" -o "$FORM_operation" = "selecting" ]; then
      ylabel="[mm/month]"
    elif [ "$FORM_sum" -eq "12" ]; then
      ylabel="[mm/year]"
    else
      ylabel="[mm/season]"
    fi
  else
    ylabel="[$UNITS]"
  fi
  setyrange="set yrange [0:]"
  setformaty="set format y \"%5.0f\""
elif [ "$TYPE" = "t" ]; then
  ylabel="[Celsius]"
  setformaty="set format y \"%5.1f\""
  setyrange=
else
  ylabel="[$UNITS]"
  setformaty="set format y \"%5.2f\""
  setyrange=
fi
### [ -n "$FORM_log" ] && ylabel="log $ylabel"
### [ -n "$FORM_sqrt" ] && ylabel="sqrt $ylabel"
[ -n "$FORM_detrend" ] && ylabel="$ylabel (detrended)"
if [ -n "$ndiff" ]; then
  ylabel="$ylabel ($ndiff-yr running mean)"
else
  if [ -n "$FORM_diff" ]; then
    ylabel="$ylabel (diff)"
  fi
fi
if [ -n "$FORM_hist" ]; then
  if [ -n "$FORM_anomal" ]; then
    ylabel="$ylabel (anomalies)"
  fi
else
  if [ -n "$FORM_anomal" ]; then
    ylabel="$ylabel (anomalies)"
  fi
fi
ylabel=`echo "$ylabel" | tr '_' ' '`