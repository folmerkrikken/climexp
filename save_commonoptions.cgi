#!/bin/bash
# save all the commonn options in a preferences file

if [ -n "$EMAIL" -a "$EMAIL" != "someone@somewhere" ]; then
  if [ -n "$FORM_timeseries" ]; then
    echo $FORM_timeseries > ./prefs/$EMAIL.series.$FORM_NPERYEAR
  fi
  if [ -z "$FORM_NPERYEAR" ]; then
    FORM_NPERYEAR=$NPERYEAR
  fi
  cat > ./prefs/$EMAIL.commonoptions.$FORM_NPERYEAR << EOF
FORM_whichvar=$FORM_whichvar;
FORM_var=$FORM_var;
FORM_fix=$FORM_fix;
FORM_month=$FORM_month;
FORM_year=$FORM_year;
FORM_operation=$FORM_operation;
FORM_sel=$FORM_sel;
FORM_sum=$FORM_sum;
FORM_sum2=$FORM_sum2;
FORM_subsum=$FORM_subsum;
FORM_subsum2=$FORM_subsum2;
FORM_lag=$FORM_lag;
FORM_anomal=$FORM_anomal;
FORM_begin=$FORM_begin;
FORM_end=$FORM_end;
FORM_gt=$FORM_gt;
FORM_lt=$FORM_lt;
FORM_dgt=$FORM_dgt;
FORM_dlt=$FORM_dlt;
FORM_log=$FORM_log;
FORM_sqrt=$FORM_sqrt;
FORM_square=$FORM_square;
FORM_cube=$FORM_cube;
FORM_twothird=$FORM_twothird;
FORM_rank=$FORM_rank;
FORM_conting=$FORM_conting;
FORM_decor=$FORM_decor;
FORM_detrend=$FORM_detrend;
FORM_diff=$FORM_diff;
FORM_ndiff=$FORM_ndiff;
FORM_ndiff2=$FORM_ndiff2;
FORM_nooverlap=$FORM_nooverlap;
FORM_runcorr=$FORM_runcorr;
FORM_runvar=$FORM_runvar;
FORM_runwindow=$FORM_runwindow;
FORM_minnum=$FORM_minnum;
FORM_random=$FORM_random;
FORM_noisetype=$FORM_noisetype;
FORM_fitfunc=$FORM_fitfunc;
FORM_nfittime=$FORM_nfittime;
FORM_xlo=$FORM_xlo;
FORM_xhi=$FORM_xhi;
FORM_ylo=$FORM_ylo;
FORM_yhi=$FORM_yhi;
FORM_nens1=$FORM_nens1;
FORM_nens2=$FORM_nens2;
FORM_ensanom=$FORM_ensanom;
EOF
fi
