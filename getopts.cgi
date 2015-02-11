#!/bin/sh
if [ "$FORM_month" = "-1" ]; then
  corrargs="$corrargs"
  FORM_month=0
  FORM_anomal="on"
fi
if [ "$FORM_var" = "composite" -o "$FORM_var" = "errorcomp" ]; then
  corrargs="$corrargs composite"
  if [ -z "$FORM_dgt" -a -z "$FORM_dlt" ]; then
    . ./myvinkhead.cgi "Compute composite" "Error"
    echo '<div class="alineakop">please specify the cut-off(s) for the composite</a>'
    . ./myvinkfoot.cgi
    exit
  fi
fi
[ -n "$FORM_masktype" ] && corrargs="$corrargs lsmask $LSMASK $FORM_masktype"
[ -n "$FORM_month" ]    && corrargs="$corrargs month $FORM_month"
[ -n "$FORM_day" ]      && corrargs="$corrargs day $FORM_day"
[ "$FORM_lag" = "0" ]   && FORM_lag=""
[ "$FORM_decor" = "0" ] && FORM_decor=""
[ "$FORM_sum" = "1" ]   && FORM_sum=""
[ "$FORM_sum2" = "$FORM_sum" ]  && FORM_sum2=""
if [ -n "$FORM_sum2" ]; then
  sumstring="${FORM_sum:-1},${FORM_sum2}"
else
  sumstring="${FORM_sum:-1}"
fi
if [ -n "$FORM_sel" ]; then
  corrargs="$corrargs select $FORM_sel"
  sumstring=$FORM_sel
fi
if [ "$FORM_operation" = "selecting" ]; then
  [ -n "$FORM_sum" ]  && corrargs="$corrargs select $FORM_sum"
elif [ "$FORM_operation" = "subtracting" ]; then
  [ -n "$FORM_sum" ]  && corrargs="$corrargs mdiff $FORM_sum"
  [ -n "$FORM_sum2" ] && corrargs="$corrargs mdiff2 $FORM_sum2"
elif [ "${FORM_operation#ave}" != "$FORM_operation" ]; then 
  if [ "$TYPE" = "p" -o "$TYPE" = "rh" -o "$TYPE" = "peca" -o "$TYPE" = "pa" -o "$FORM_field_type" = "Precipitation" ]; then
    FORM_operation="summing"
    [ -n "$FORM_sum" ]  && corrargs="$corrargs sum $FORM_sum"
    [ -n "$FORM_sum2" ] && corrargs="$corrargs sum2 $FORM_sum2"
  else
    [ -n "$FORM_sum" ]  && corrargs="$corrargs ave $FORM_sum"
    [ -n "$FORM_sum2" ] && corrargs="$corrargs ave2 $FORM_sum2"
  fi
else
  [ -n "$FORM_sum" ]  && corrargs="$corrargs ${FORM_operation:-ave} $FORM_sum"
  [ -n "$FORM_sum2" ] && corrargs="$corrargs ${FORM_operation:-ave} $FORM_sum2" 
fi
[ -n "$FORM_fix" ] && corrargs="$corrargs $FORM_fix"
[ -n "$FORM_lag" ] && corrargs="$corrargs lag $FORM_lag"
[ -n "$FORM_minnum" ] && corrargs="$corrargs minnum $FORM_minnum"
[ -n "$FORM_minfac" ] && corrargs="$corrargs minfac $FORM_minfac"
[ -n "$FORM_begin" ] && corrargs="$corrargs begin $FORM_begin"
[ -n "$FORM_end" ] && corrargs="$corrargs end $FORM_end"
[ -n "$FORM_begin2" ] && corrargs="$corrargs begin2 $FORM_begin2"
[ -n "$FORM_end2" ] && corrargs="$corrargs end2 $FORM_end2"
[ -n "$FORM_anomal" ] && corrargs="$corrargs anomal"
[ -n "$FORM_log" ] && corrargs="$corrargs log"
if [ "$FORM_changesign" != "both" ]; then
    [ -n "$FORM_changesign" ] && corrargs="$corrargs changesign"
fi
[ -n "$FORM_normsd" ] && corrargs="$corrargs normsd"
[ -n "$FORM_sqrt" ] && corrargs="$corrargs sqrt"
[ -n "$FORM_square" ] && corrargs="$corrargs square"
[ -n "$FORM_twothird" ] && corrargs="$corrargs twothird"
[ -n "$FORM_rank" ] && corrargs="$corrargs rank" && RANK="rank "
[ -n "$FORM_conting" ] && corrargs="$corrargs conting"
[ -n "$FORM_decor" ] && corrargs="$corrargs decor $FORM_decor"
[ -n "$FORM_detrend" ] && corrargs="$corrargs detrend"
[ -n "$FORM_diff" ] && corrargs="$corrargs diff"
if [ -n "$FORM_ndiff" ]; then
  corrargs="$corrargs diff $(($FORM_subsum * $FORM_ndiff))"
  if [ "$FORM_subsum" = 1 ]; then
    ndiff="minus $FORM_ndiff"
    FORM_nooverlap=""
  else
    ndiff=$((1+$FORM_ndiff))
  fi
fi
if [ -n "$FORM_ndiff2" ]; then
  corrargs="$corrargs diff $(($FORM_subsum2 * $FORM_ndiff2))"
  if [ "$FORM_subsum2" = 1 ]; then
    ndiff2="minus $FORM_ndiff2"
    FORM_nooverlap=""
  elif [ -n "$FORM_ndiff" ]; then
    ndiff2="plus $((1+$FORM_ndiff2))"
  else
    ndiff2="$((1+$FORM_ndiff2))"
  fi
fi
[ -n "$FORM_nooverlap" ] && corrargs="$corrargs nooverlap"
###echo "<br>FORM_ndiff2 = $FORM_ndiff2<br>"
[ -n "$FORM_gt" ] && corrargs="$corrargs gt $FORM_gt"
[ -n "$FORM_lt" ] && corrargs="$corrargs lt $FORM_lt"
[ -n "$FORM_dgt" ] && corrargs="$corrargs dgt $FORM_dgt"
[ -n "$FORM_dlt" ] && corrargs="$corrargs dlt $FORM_dlt"
if [ -n "$FORM_runcorr$FORM_moment" -a -n "$FORM_runwindow" ]; then
  corrargs="$corrargs run$FORM_runvar $FORM_runwindow $DIR/data/$TYPE$WMO${FORM_num}.runcor"
  [ -n "$FORM_random" ] && corrargs="$corrargs random $FORM_random"
  [ -n "$FORM_noisetype" ] && corrargs="$corrargs noise $FORM_noisetype"
fi
if [ "$FORM_fitfunc" = "fittime" ]; then
  corrargs="$corrargs fittime"
  [ -n "$FORM_nfittime" ] && corrargs="$corrargs $FORM_nfittime"
elif [ -n "$FORM_fitfunc" -a "$FORM_fitfunc" != phase ]; then
  corrargs="$corrargs fitfunc $FORM_fitfunc"
fi
if [ -n "$ENSEMBLE" ]; then
  if [ -n "$FORM_nens1" ]; then
    if [ -n "$FORM_nens2" ]; then
      corrargs="$corrargs ensemble $FORM_nens1 $FORM_nens2"
    else
      echo '<html><head><title>error</title></head><body bgcolor="#ffffff">'
      echo 'Error: please specify the final ensemble member</body></html>'
      exit
    fi
  else
    if [ -n "$FORM_nens2" ]; then
      corrargs="$corrargs ensemble 0 $FORM_nens2"
    fi
  fi
fi
[ -n "$FORM_makeensfull" ] && corrargs="$corrargs makeensfull"
[ -n "$FORM_ensanom" ] && corrargs="$corrargs ensanom"
[ -n "$FORM_debias" ] && corrargs="$corrargs debias $FORM_debias"
[ -n "$FORM_standardunits" ] && corrargs="$corrargs $FORM_standardunits"
[ -n "$startstop" ] && corrargs="$corrargs startstop $startstop"
[ -n "$FORM_restrain" ] && corrargs="$corrargs restrain $FORM_restrain"
[ -n "$FORM_normalization" ] && corrargs="$corrargs normalization $FORM_normalization"
[ -n "$FORM_xyear" ] && corrargs="$corrargs xyear $FORM_xyear"
[ -n "$FORM_ci" ] && corrargs="$corrargs confidenceinterval $FORM_ci"
