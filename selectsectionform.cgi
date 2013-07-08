#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
CLASS="$FORM_CLASS"

lwrite=false
if [ "$EMAIL" = oldenbor@knmi.nl ]; then
    lwrite=true # false # true
fi

if [ "${CLASS#ENSEMBLES_RT}" != "$CLASS" -o "$CLASS" = ENSEMBLES_AMMA -o "$CLASS" = Prudence ]; then
  if [ "$FORM_iaccept" = on ]; then
    echo "FORM_iaccept=on;" > prefs/${EMAIL}.ensemblesrt3
  fi
fi

###[ -n "$lwrite" ] && echo "FORM_complete = $FORM_complete<br>"
if [ "$FORM_complete" = "OK" \
   -a "$FORM_iaccept" = on \
   -a "$CLASS" = "$FORM_oldclass" \
   -a "$FORM_expid" = "$FORM_oldexpid" \
   -a "$FORM_var" = "$FORM_oldvar" \
   -a "$FORM_level" = "$FORM_oldlevel" \
   -a "$FORM_lat" = "$FORM_oldlat" \
   -a "$FORM_lon" = "$FORM_oldlon" ]; then

  . ./selectsection.cgi
  exit
fi

subtitle=`echo $CLASS | tr '_' ' '`
. ./myvinkhead.cgi "Select a monthly field or time series" "$subtitle" "index,nofollow"

###echo '<pre>'
###set | fgrep FORM_
###echo '</pre>'

. ./nosearchengine.cgi
. ./checkemail.cgi

cat <<EOF
<font color="#FF2222">Due to a bug in the netcdf4 library this functionality does not currently work for all datasets</font>
This page allows access to remotely stored datasets.  Please select a 2D field from one of these datasets.  This will be transferred to the Climate Explorer for further analysis.  The field will be available under <span class=kalelink><a href="selectfield_use.cgi?id=$EMAIL">user-defined fields</a></span> for the next 3 days.
EOF

if [ "$EMAIL" = "someone@somewhere" ]; then
  echo "<li>Anonymous users cannot retrieve non-local data</ul>"
  . ./myvinkfoot.cgi
  exit
fi

cat <<EOF
<form action="selectsectionform.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="oldclass" value="$CLASS">
<table class=realtable width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="2">Select a 2D field
<tr><th colspan="2"><small>the metadata is fetched from the server, so the form may be slow at times
EOF

### Dataset

. ./selectdataset.cgi

cat <<EOF
<tr>
<td width=100>Dataset:
<td><select class="forminput" name="CLASS" onchange="this.form.submit();">
<option value="choose" $choose_selected>choose a dataset
<option $demeter_selected>Demeter
<option $ensembles_2_selected>ENSEMBLES_stream_2
<option $ensembles_2_daily_selected>ENSEMBLES_stream_2_daily
<option $ensembles_1_selected>ENSEMBLES_stream_1
<option $ensembles_1_ocean_selected>ENSEMBLES_stream_1_ocean
<option $ensembles_1_daily_selected>ENSEMBLES_stream_1_daily
<option $ensembles_rt3_selected>ENSEMBLES_RT3
<option $ensembles_rt2b_selected>ENSEMBLES_RT2b
<option $ensembles_amma_selected>ENSEMBLES_AMMA
<option $prudence_selected>Prudence
<option $r2_pgb_selected>Reanalysis-2_pressure
<option $r2_flx_selected>Reanalysis-2_fluxes
<option $r1_selected>NCEP_NCAR_reanalysis
<option $c20_selected>20th_century_reanalysis
<option $soda_selected>SODA
<option $soda_surface_selected>SODA_surface
<option $enact_selected>ENACT
<option $ecmwf_s3_selected>ECMWF_ORA-S3_ocean
</select>
EOF

if [ ${CLASS:-choose} = 20th_century_reanalysis ]; then
    echo "<br><font color="#ff0000">Sorry, this dataset does not yet work</font>"
    CLASS=choose
fi
if [ ${CLASS:-choose} = choose ]; then
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select dataset\">"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

### ID, institute, model

if [ ${CLASS#ENSEMBLES_RT} != $CLASS -o $CLASS = ENSEMBLES_AMMA -o $CLASS = Prudence ]; then
  # DMI archive, HTML listings
  if [ -z "$FORM_expidlist" -o "$CLASS" != "$FORM_oldclass" ]
  then
    cachefile=metadata/cache_${CLASS}_expids.txt
    if [ -s $cachefile ]; then
      FORM_expidlist=`cat $cachefile`
    else
      if [ "$lwrite" = true ]; then
        echo '<pre>'
        echo DEBUG
        echo "./htmlmetadata.cgi $path$file $levels $MM | fgrep -v HC/MM"
        ./htmlmetadata.cgi $path$file $levels $MM | fgrep -v "HC/MM" 2>&1 
        echo '</pre>'
      fi
      FORM_expidlist=`./htmlmetadata.cgi $path$file $levels $MM | fgrep -v "HC/MM"`
      echo "$FORM_expidlist" > $cachefile
    fi
    FORM_expid=choose
  fi
  echo '<tr><td>Experiment:<td>'
  echo "<input type=hidden name=expidlist value=\"$FORM_expidlist\">"
  echo "<input type=hidden name=oldexpid value=\"$FORM_expid\">"
  echo '<select class=forminput name=expid onchange=this.form.submit();>'
  echo '<option value=choose>Choose an experiment'
  if [ $levels = 2 ]; then
    echo "$FORM_expidlist" | tr ' '  '\n' \
      | sed -e 's@^ *\([^/]*\)/\([^/]*\)/\([A-Za-z0-9-]*\)/*@<option value="\1/\2/\3/" onchange=this.form.submit();>\1 \2@g' \
      | sed -e 's@value="'$FORM_expid'"@value="'$FORM_expid'" selected@'
  else
    echo "$FORM_expidlist" | tr ' '  '\n' \
      | sed -e 's@^ *\([^/]*\)/\([^/]*\)/\([A-Za-z0-9-]*\)/*@<option value="\1/\2/\3/" onchange=this.form.submit();>\1@g' \
      | sed -e 's@value="'$FORM_expid'"@value="'$FORM_expid'" selected@'
  fi
  echo '</select>'
  if [ ${FORM_expid:-choose} = choose ]; then
    echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select model\">"
    echo "</table></form>"
    . ./myvinkfoot.cgi
    exit
  fi
elif [ $CLASS = Demeter -o ${CLASS#ENSEMBLES} != $CLASS ]
then
  # ECMWF ENSEMBLES archive, opendap aggregated
  if [ -z "$FORM_expidlist" -o "$CLASS" != "$FORM_oldclass" ]
  then
    cachefile=metadata/cache_${CLASS}_expids.txt
    if [ -s $cachefile ]; then
      FORM_expidlist=`cat $cachefile`
    else
      if [ "$lwrite" = true ]; then
        echo '<pre>'
        echo DEBUG
        echo "bin/convertmetadata $path/$file list ids"
        bin/convertmetadata $path/$file list ids 2>&1 
        echo '</pre>'
      fi
      FORM_expidlist=`bin/convertmetadata $path/$file list ids`
      echo "$FORM_expidlist" > $cachefile
    fi
    FORM_expid=choose
  fi
  echo '<tr><td>Model:<td>'
  echo "<input type=hidden name=expidlist value=\"$FORM_expidlist\">"
  echo "<input type=hidden name=oldexpid value=\"$FORM_expid\">"
  echo '<select class=forminput name=expid onchange=this.form.submit();>'
  echo '<option value=choose>Choose an experiment'
  if [ "$FORM_expid" = all ]; then
    echo "<option value=all selected>multimodel $CLASS"
  else
    echo "<option value=all>multimodel $CLASS"
  fi
  if [ $CLASS = Demeter -o $CLASS = ENSEMBLES_stream_1_ocean ]; then
    expid=experiment_id
    echo "$FORM_expidlist" \
    | sed -e 's@[^0-9A-Za-z]*\([^ ]*\) \([^ ]*\) \([^ ]*\)@<option value="\1" onchange=this.form.submit();>\1 \2@g' \
    | sed -e 's@value="'$FORM_expid'"@value="'$FORM_expid'" selected@'
  else
    expid=source
    echo "$FORM_expidlist" \
    | sed -e 's@[^0-9A-Za-z]*\([^ ]*\) \([^ ]*\) \([^ ]*\)@<option value="\2" onchange=this.form.submit();>\3 \2@g' \
    | sed -e 's@value="'$FORM_expid'"@value="'$FORM_expid'" selected@'
  fi
  echo '</select>'
  if [ ${FORM_expid:-choose} = choose ]; then
    echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select model\">"
    echo "</table></form>"
    . ./myvinkfoot.cgi
    exit
  fi
fi

form_expid=`echo $FORM_expid | tr '/' '_'`

if [ $CLASS = Demeter -o ${CLASS#ENSEMBLES_s} != $CLASS -o $CLASS = ECMWF_ORA-S3_ocean ]
then

  # ensemble members

  if [ $CLASS = ECMWF_ORA-S3_ocean ]; then
    FORM_enslist="0 1 2 3 4"
  else
    if [ -z "$FORM_enslist" -o "$FORM_expid" != "$FORM_oldexpid" ]
    then
      cachefile=metadata/cache_${CLASS}_${form_expid}_ens.txt
      if [ -s $cachefile ]; then
        FORM_enslist=`cat $cachefile`
      else
        if [ "$lwrite" = true ]; then
          echo '<pre>'
          echo DEBUG
          echo "bin/convertmetadata $path/$file convert $expid $FORM_expid"
          bin/convertmetadata $path/$file convert $expid $FORM_expid 2>&1 
          echo '</pre>'
        fi
        FORM_enslist=`bin/convertmetadata $path/$file convert $expid $FORM_expid | tr '\n' ' '`
        echo "$FORM_enslist" > $cachefile
      fi
    fi
  fi
  ensarray=($FORM_enslist)
  offset=${ensarray[0]}
  n=${#ensarray[*]}
  n=$(($n - 1))
  last=${ensarray[$n]}
  [ -z "$FORM_nens1" ] && FORM_nens1=$offset
  [ "${FORM_nens2:-9999}" -gt "$last" -o "$FORM_nens2" = "$FORM_last" ] && FORM_nens2=$last
  echo '<tr><td>Ensemble members<td>'
  echo "<input type=hidden name=enslist value=\"$FORM_enslist\">"
  echo "<input type=hidden name=offset value=\"$offset\">"
  echo "<input type=hidden name=last value=\"$last\">"
  echo '<select class=forminput name=nens1>'
  for ens in $FORM_enslist
  do
    if [ $ens = "$FORM_nens1" ]
    then
      echo "<option selected value="$ens">$(($ens - $offset))"
    else
      echo "<option value="$ens">$(($ens - $offset))"
    fi
  done
  echo '</select> to <select class=forminput name=nens2>'
  for ens in $FORM_enslist
  do
    if [ $ens = "$FORM_nens2" ]
    then
      echo "<option selected value="$ens">$(($ens - $offset))"
    else
      echo "<option value="$ens">$(($ens - $offset))"
    fi
  done
  echo '</select>'
fi

if [ $CLASS = Demeter -o ${CLASS#ENSEMBLES_s} != $CLASS ]
then

  # start date

  if [ -z "$FORM_reflist" -o "$FORM_expid" != "$FORM_oldexpid" ]
  then
    cachefile=metadata/cache_${CLASS}_${form_expid}_analysis.txt
    if [ -s $cachefile ]; then
      FORM_reflist=`cat $cachefile`
    else
      if [ "$lwrite" = true ]; then
        echo '<pre>'
        echo DEBUG
        echo "bin/convertmetadata $path/$file list reftime"
        bin/convertmetadata $path/$file list reftime 2>&1 
        echo '</pre>'
      fi
      FORM_reflist=`bin/convertmetadata $path/$file list reftime | tr '\n' ' '`
      echo "$FORM_reflist" > $cachefile
    fi
    FORM_analysis=choose
  fi
  echo '<tr><td>Forecast reference date:<td>'
  echo "<input type=hidden name=reflist value=\"$FORM_reflist\">"
  echo '<select class=forminput name=analysis onchange=this.form.submit();>'
  echo '<option value=choose>Choose a reference date'
  for analysis in $FORM_reflist
  do
    if [ $analysis = "$FORM_analysis" ]
    then
      echo "<option selected>$analysis"
    else
      echo "<option>$analysis"
    fi
  done
  echo '</select>'
  if [ ${FORM_analysis:-choose} = choose ]; then
    echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select reference date\">"
    echo "</table></form>"
    . ./myvinkfoot.cgi
    exit
  fi

elif [ $CLASS = ENACT ]; then

  echo '<tr><td>Model:<td>'
  echo "<input type=hidden name=expidlist value=\"$FORM_expidlist\">"
  echo "<input type=hidden name=oldexpid value=\"$FORM_expid\">"
  echo '<select class=forminput name=expid onchange=this.form.submit();>'
  cat <<EOF | sed -e "s/${FORM_expid:-choose}/$FORM_expid selected/g"
<option value=choose>Choose an ocean reanalysis
<option value=cerfacs-fd1>CERFACS (OPA 3D-VAR T-S 1962-2001)
<option value=ecmwf-ekw1>ECMWF (HOPE OI T-S 1962-2003)
<option value=ingv-0001>INGV (OPA OI T-S 1962-2001)
<option value=metuk-EEXM>METUK ASSIM RUN (GloSea OI T-S 1962-1998)
<option value=metuk_EMAB>METUK OBJECTIVE ANALYSIS (1960-2004)
</select>
EOF
  if [ ${FORM_expid:-choose} = choose ]; then
    echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select analysis\">"
    echo "</table></form>"
    . ./myvinkfoot.cgi
    exit
  fi
fi

# variables


if [ $CLASS = ENACT ]; then

  echo '<tr valign="baseline"><td>Variable:<td>'
  echo "<input type=hidden name=varlist value=\"$FORM_varlist\">"
  echo "<input type=hidden name=oldvar value=\"$FORM_var\">"
  tmpfile=/tmp/selectsectionform$$.txt
  echo '<input type=radio class=formradio name=var value=sea_water_potential_temperature onchange=this.form.submit();>Potential temperature ref to surface [K]<br>'  > $tmpfile
  echo '<input type=radio class=formradio name=var value=sea_water_salinity onchange=this.form.submit();>Sea Water salinity [PSU]<br>' >> $tmpfile
  if [ $FORM_expid != ukmo-EMAB ]; then
    echo '<input type=radio class=formradio name=var value=sea_water_x_velocity onchange=this.form.submit();>Zonal Current [m.s-1]<br>' >> $tmpfile
    echo '<input type=radio class=formradio name=var value=sea_water_y_velocity onchange=this.form.submit();>Meridional Current [m.s-1]<br>' >> $tmpfile
    if [ $FORM_expid != ecmwf-ekw1 -a $FORM_expid != ingv-0001 ]; then
      echo '<input type=radio class=formradio name=var value=upward_sea_water_velocity onchange=this.form.submit();>Vertical current [m/day]<br>' >> $tmpfile
    fi
    if [ $FORM_expid != metuk-EEXM ]; then
      echo '<input type=radio class=formradio name=var value=sea_surface_height onchange=this.form.submit();>Sea Surface Height above Sea Level [m]<br>' >> $tmpfile
    fi
  fi
  sed -e "s/${FORM_var:-choose}/$FORM_var checked/g" $tmpfile
  rm $tmpfile

elif [ $CLASS = ECMWF_ORA-S3_ocean ]; then

  echo '<tr><td>Variable:<td>'
  echo "<input type=hidden name=varlist value=\"$FORM_varlist\">"
  echo "<input type=hidden name=oldvar value=\"$FORM_var\">"
  tmpfile=/tmp/selectsectionform$$.txt
  echo '<input type=radio class=formradio name=var value=thetao onchange=this.form.submit();>Temp (sea water potential temperature) [K]<br>'  > $tmpfile
  echo '<input type=radio class=formradio name=var value=so onchange=this.form.submit();>Salt (salinity) [PSU]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=uo onchange=this.form.submit();>Zonal Current [m.s-1]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=vo onchange=this.form.submit();>Meridional Current [m.s-1]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=wo onchange=this.form.submit();>Vertical current [m/day]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=zoh onchange=this.form.submit();>Sea Surface Height [m]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=zmlo onchange=this.form.submit();>Mixed-layer Depth [m]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=t20d onchange=this.form.submit();>Depth of 20C isotherm [m]<br>' >> $tmpfile
  echo '<input type=radio class=formradio name=var value=thetaot onchange=this.form.submit();>300m averaged temperature [K]<br>' >> $tmpfile

  sed -e "s/=${FORM_var:-choose}/=$FORM_var checked/g" $tmpfile
  rm $tmpfile

elif [ ${CLASS#ENSEMBLES_RT} != $CLASS -o $CLASS = ENSEMBLES_AMMA -o $CLASS = Prudence ]; then
  # variables are in the HTML listings

  if [ -z "$FORM_varlist" -o "$FORM_expid" != "$FORM_oldexpid" -o "$CLASS" != "$FORM_oldclass" ]; then
    cachefile=metadata/cache_${CLASS}_${form_expid}_vars.txt
    if [ -s $cachefile ]; then
      FORM_varlist=`cat $cachefile`
    fi
    if [ -z "$FORM_varlist" ]; then
      if [ "$lwrite" = true ]; then
        echo '<pre>'
        echo DEBUG
        echo "./htmlmetadata.cgi $path/$file/$FORM_expid 1 | fgrep 'CRU|METO-HadCM|METO-HC_HadCM|MRI_JMA'"
        (./htmlmetadata.cgi $path/$file/$FORM_expid 1 | fgrep 'CRU|METO-HadCM|METO-HC_HadCM|MRI_JMA') 2>&1
        echo '</pre>'
      fi
      FORM_varlist=`./htmlmetadata.cgi $path/$file/$FORM_expid 1 | egrep 'CRU|METO-HadCM|METO-HC_HadCM|MRI_JMA'`
      [ -n "$FORM_varlist" ] && echo "$FORM_varlist" > $cachefile
    fi
    FORM_var=choose
  fi
  echo '<tr><td>Variable:<td>'
  echo "<input type=hidden name=varlist value=\"$FORM_varlist\">"
  echo "<input type=hidden name=oldvar value=\"$FORM_var\">"
  # again, do not try this at home!  (see grads.cgi)
  if [ $CLASS = Prudence ]; then
    regexp='s/\(.*\)\.[^.]*\.\([.a-zA-Z0-9_-]*\)\.nc\.gz/<input type="radio" class="formradio" name="var" value="\1" onchange=this.form.submit();>\1<br>/g'
  else
    regexp='s/\(.*\)_\([a-zA-Z0-9-]*\)\.nc\.gz/<input type="radio" class="formradio" name="var" value="\2" onchange=this.form.submit();>\2<br>/g'
  fi
  echo "$FORM_varlist" | tr ' ' '\n' \
    | sed -e "$regexp" | sort | uniq\
    | sed -e 's/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\([^>]*\)>\(.*\)$/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\1 checked>\2/' \
    | sed -f RCM_output_table.sed

else # variables are in the netcdf metadata

  if [ -z "$FORM_varlist" -o "$FORM_expid" != "$FORM_oldexpid" -o "$CLASS" != "$FORM_oldclass" ]; then
    cachefile=metadata/cache_${CLASS}_${form_expid}_vars.txt
    if [ -s $cachefile ]; then
      FORM_varlist=`cat $cachefile`
    else
      if [ "$lwrite" = true ]; then
        echo '<pre>'
        echo DEBUG
        echo "bin/convertmetadata $path/$file list variables"
        bin/convertmetadata $path/$file list variables 2>&1 
        echo '</pre>'
      fi
      FORM_varlist=`bin/convertmetadata $path/$file list variables`
      [ -n "$FORM_varlist" ] && echo "$FORM_varlist" > $cachefile
    fi
    FORM_var=choose
  fi
  echo '<tr><td>Variable:<td>'
  echo "<input type=hidden name=varlist value=\"$FORM_varlist\">"
  echo "<input type=hidden name=oldvar value=\"$FORM_var\">"
  # again, do not try this at home!  (see grads.cgi)
  echo "$FORM_varlist" \
    | sed -e 's/[^A-Za-z]*\([^ ]*\) \([^]]*]\)/<input type="radio" class="formradio" name="var" value="\1" onchange=this.form.submit();>\1\2<br>/g' \
          -e 's/<br>n/<br>/g' \
    |  sed -e 's/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\([^>]*\)>\(.*\)$/<input type="radio" class="formradio" name="var" value="'$FORM_var'"\1 checked>\2/'
fi

if [ ${FORM_var:-choose} = choose ]; then
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select variable\">"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

if [ $CLASS = ENACT ]; then
  . ./enact2file.cgi
fi
if [ $CLASS = ECMWF_ORA-S3_ocean ]; then
  file=$FORM_var
fi
if [ ${CLASS#ENSEMBLES_RT} != $CLASS -o $CLASS = ENSEMBLES_AMMA -o $CLASS = Prudence ]; then
  path=$path$file/$FORM_expid
  file=`echo "$FORM_varlist" | tr ' \r' '\n ' | egrep "_$FORM_var\.nc\.gz|^$FORM_var\." | head -1`
  if [ $CLASS != Prudence ]; then
    FORM_var=`echo $FORM_var | sed -e 's/[-A-Z].*//'`
  fi
fi

# latitude, longitude

if [ -z "$FORM_lonlist" -o "$FORM_expid" != "$FORM_oldexpid" -o "$FORM_var" != "$FORM_oldvar" -o "$CLASS" != "$FORM_oldclass" ]
then
  cachefile=metadata/cache_${CLASS}_${form_expid}_${FORM_var}_lons.txt
  if [ -s $cachefile ]; then
    [ $lwrite = true ] && echo "using cachefile $cachefile<br>"
    FORM_lonlist=`cat $cachefile`
  else
    if [ "$lwrite" = true ]; then
      echo '<pre>'
      echo BEGIN DEBUG
      echo "bin/convertmetadata $path/$file list $longitude $FORM_var"
      bin/convertmetadata $path/$file list $longitude $FORM_var 2>&1 
      echo END DEBUG
      echo '</pre>'
    fi
    FORM_lonlist=`bin/convertmetadata $path/$file list $longitude $FORM_var | sort -g | tr '\n' ' '`
    c=`echo $FORM_lonlist | wc -c`
    if [ $c -lt 5 ]; then
        FORM_lonlist=`bin/convertmetadata $path/$file list longitude $FORM_var | sort -g | tr '\n' ' '`
    fi
    [ -n "$FORM_lonlist" ] && echo "$FORM_lonlist" > $cachefile
  fi
  FORM_lon=range
else
  [ $lwrite = true ] && echo "using variable FORM_lonlist=$FORM_lonlist<br>"
fi
nlon=`echo "$FORM_lonlist" | wc -w`
echo "<input type=hidden name=lonlist value=\"$FORM_lonlist\">"

if [ -z "$FORM_latlist" -o "$FORM_expid" != "$FORM_oldexpid" -o "$FORM_var" != "$FORM_oldvar" -o "$CLASS" != "$FORM_oldclass" ]
then
  cachefile=metadata/cache_${CLASS}_${form_expid}_${FORM_var}_lats.txt
  if [ -s $cachefile ]; then
    [ $lwrite = true ] && echo "using cachefile $cachefile<br>"
    FORM_latlist=`cat $cachefile`
  else
    if [ "$lwrite" = true ]; then
      echo '<pre>'
      echo BEGIN DEBUG
      echo "bin/convertmetadata $path/$file list $latitude $FORM_var"
      bin/convertmetadata $path/$file list $latitude $FORM_var 2>&1 
      echo END DEBUG
      echo '</pre>'
    fi
    FORM_latlist=`bin/convertmetadata $path/$file list $latitude $FORM_var | sort -g | tr '\n' ' '`
    if [ $c -lt 5 ]; then
        FORM_latlist=`bin/convertmetadata $path/$file list latitude $FORM_var | sort -g | tr '\n' ' '`
    fi
    [ -n "$FORM_latlist" ] && echo "$FORM_latlist" > $cachefile
  fi
  FORM_lat=range
else
  [ $lwrite = true ] && echo "using variable FORM_latlist=$FORM_latlist<br>"
fi
nlat=`echo "$FORM_latlist" | wc -w`
echo "<input type=hidden name=latlist value=\"$FORM_latlist\">"

# level

if [ -z "$FORM_levellist" -o "$FORM_expid" != "$FORM_oldexpid" -o "$FORM_var" != "$FORM_oldvar" -o "$CLASS" != "$FORM_oldclass" ]
then
  cachefile=metadata/cache_${CLASS}_${form_expid}_${FORM_var}_levels.txt
  if [ -s $cachefile ]; then
    FORM_levellist=`cat "$cachefile"`
  else
    if [ "$lwrite" = true ]; then
      echo '<pre>'
      echo BEGIN DEBUG
      echo "bin/convertmetadata $path/$file list $level $FORM_var"
      bin/convertmetadata $path/$file list $level $FORM_var 2>&1 
      echo END DEBUG
      echo '</pre>'
    fi
    FORM_levellist=`bin/convertmetadata $path/$file list $level $FORM_var | tr '\n' ' '`
    [ -n "$FORM_levellist" ] && echo "$FORM_levellist" > $cachefile
  fi
  FORM_level=range
fi
nlevel=`echo "$FORM_levellist" | wc -w`
echo "<input type=hidden name=levellist value=\"$FORM_levellist\">"

# 2D section

if [ $nlevel -gt 1 -a $nlon -gt 1 -a $nlat -gt 1 ]; then
  echo '<tr><td>2D section at:'
  echo "<td><table border=0 cellpadding=0 cellspacing=0><tr><td>$level<td>"
  echo "<input type=hidden name=oldlevel value=\"$FORM_level\">"
  echo '<select class=forminput name=level onchange=this.form.submit();>'
  echo "<option value=range>All ${level}s"
  for level in $FORM_levellist
  do
    if [ $level = "$FORM_level" ]
    then
      echo "<option selected>$level"
    else
      echo "<option>$level"
    fi
  done
  echo '</select> or'
  echo "<tr><td>$latitude<td><input type=hidden name=oldlat value=\"$FORM_lat\">"
  echo '<select class=forminput name=lat onchange=this.form.submit();>'
  echo "<option value=range>Range of ${latitude}s"
  for lat in $FORM_latlist
  do
    if [ $lat = "$FORM_lat" ]
    then
      echo "<option selected>$lat"
    else
      echo "<option>$lat"
    fi
  done
  echo '</select> or'
  echo "<tr><td>$longitude<td><input type=hidden name=oldlon value=\"$FORM_lon\">"
  echo '<select class=forminput name=lon onchange=this.form.submit();>'
  echo "<option value=range>Range of ${longitude}s"
  for lon in $FORM_lonlist
  do
    if [ $lon = "$FORM_lon" ]
    then
      echo "<option selected>$lon"
    else
      echo "<option>$lon"
    fi
  done
  echo '</select></table>'
###  echo "FORM_level=$FORM_level,FORM_lat=$FORM_lat,FORM_lon=$FORM_lon"
  if [ ${FORM_level:-range} = range -a ${FORM_lat:-range} = range -a ${FORM_lon:-range} = range ]; then
    echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select 2D section\">"
    echo "</table></form>"
    . ./myvinkfoot.cgi
    exit
  fi
else
  echo "<!-- found 2D data, nlevel=$nlevel, nlon=$nlon, nlat=$nlat -->"
fi 

# longitude, latitude

if [ $nlat -gt 0 -a ${FORM_lat:-range} = range ]; then
  echo '<tr><td>Latitude:<td>'
  echo '<select class=forminput name=lat1>'
  latarray=($FORM_latlist)
  firstlat=${latarray[0]}
  [ -z "$FORM_lat1" ] && FORM_lat1=$firstlat
  for lat in $FORM_latlist
  do
    if [ $lat = "$FORM_lat1" -o $nlat = 1 ]
    then
      echo "<option selected>$lat"
    else
      echo "<option>$lat"
    fi
  done
  echo '</select>'
  echo ' to <select class=forminput name=lat2>'
  n=${#latarray[*]}
  n=$(($n - 1))
  lastlat=${latarray[$n]}
  [ -z "$FORM_lat2" ] && FORM_lat2=$lastlat
  for lat in $FORM_latlist
  do
    if [ $lat = "$FORM_lat2" -o $nlat = 1 ]
    then
      echo "<option selected>$lat"
    else
      echo "<option>$lat"
    fi
  done
  echo '</select>'
  echo "<input type=hidden name=firstlat value=\"$firstlat\">"
  echo "<input type=hidden name=lastlat value=\"$lastlat\">"
fi

if [ $nlon -gt 0 -a ${FORM_lon:-range} = range ]; then
  echo '<tr><td>Longitude:<td>'
  echo '<select class=forminput name=lon1>'
  lonarray=($FORM_lonlist)
  firstlon=${lonarray[0]}
  [ -z "$FORM_lon1" ] && FORM_lon1=$firstlon
  for lon in $FORM_lonlist
  do
    if [ $lon = "$FORM_lon1" -o $nlon = 1 ]
    then
      echo "<option selected>$lon"
    else
      echo "<option>$lon"
    fi
  done
  echo '</select>'
  echo ' to <select class=forminput name=lon2>'
  n=${#lonarray[*]}
  n=$(($n - 1))
  lastlon=${lonarray[$n]}
  [ -z "$FORM_lon2" ] && FORM_lon2=$lastlon
  for lon in $FORM_lonlist
  do
    if [ $lon = "$FORM_lon2" -o $nlon = 1 ]
    then
      echo "<option selected>$lon"
    else
      echo "<option>$lon"
    fi
  done
  echo '</select>'
  echo "<input type=hidden name=firstlon value=\"$firstlon\">"
  echo "<input type=hidden name=lastlon value=\"$lastlon\">"
fi

if [ $CLASS = ENSEMBLES_stream_1_daily ]; then
# filter daily data
  VAR=$FORM_var
  . ./daily2longerform.cgi
fi

if [ -s prefs/$EMAIL.ensemblesrt3 ]; then
  FORM_iaccept=1
fi
if [ \( ${CLASS#ENSEMBLES_RT} != $CLASS -o $CLASS = ENSEMBLES_AMMA -o $CLASS = Prudence \) -a -z "$FORM_iaccept" ]; then
  echo "<tr><td>Conditions:<td>"
  cat ensembles_rt_conditions.html
  echo '<br><input type="checkbox" name="iaccept">I accept these terms'
  if [ "$FORM_complete" = OK ]; then
    echo "<br><font color="#ff2222">You have to agree to these terms before downloading data</font>"
  fi
else
  echo "<input type=\"hidden\" name=\"iaccept\" value=\"on\">"
fi

echo "<tr><td colspan=\"2\"><input type=\"hidden\" name=\"complete\" value=\"OK\"><input type=\"submit\" class=\"formbutton\" value=\"Retrieve data\">"

echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi


echo '</table>'

. ./myvinkfoot.cgi
