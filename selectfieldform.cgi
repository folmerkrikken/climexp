#!/bin/sh

if [ $NPERYEAR = 12 ]; then
  if [ -z "$NO_OBS" ]; then
    echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
    echo '<tr><th colspan="4">Observations</th></tr>'
    sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
    echo '</table>'
  fi
  if [ -z "$NO_REA" ]; then
    echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
    echo '<tr><th colspan="8">Reanalyses</th></tr>'
    cat $DIR/selectfield_rea.html
    echo '</table>'
  fi
  if [ -z "$NO_SEA" ]; then
    echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
    echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
    cat $DIR/selectfield_sea.html
    echo '</table>'
  fi
  if [ -z "$NO_SEA" ]; then
    echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
    echo '<tr><th colspan="13">Seasonal forecasts full ensembles</th></tr>'
    cat $DIR/selectfield_seaens.html
    ENSEMBLE=true
    echo '</table>'
  fi
  if [ -z "$NO_CSM" ]; then
    echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
    echo '<tr><th colspan="15">Scenario runs</th></tr>'
    fgrep -v getindices $DIR/selectfield_ipcc.html
    echo '</table>'
    ENSEMBLE=true
  fi
elif [ $NPERYEAR = 360 -o $NPERYEAR = 366 -o $NPERYEAR = 366 ]; then
  if [ -z "$NO_OBS" ]; then
    echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
    cat selectdailyfield_obs.html
    echo '</table>'
  fi
  if [ -z "$NO_REA" ]; then
    echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
    cat selectdailyfield_rea.html
    echo '</table>'
  fi
  if [ -z "$NO_CSM" ]; then
    echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
    cat selectdailyfield_ipcc.html
    echo '</table>'
  fi
else
  echo "No system-defined $NPERYEAR fields available yet"
fi # NPERYEAR
if [ -z "$NO_USE" ]; then
  . $DIR/selectuserfield.cgi
fi
