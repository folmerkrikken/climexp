#!/bin/sh
. ./init.cgi

export DIR=`pwd`
. ./getargs.cgi

. ./queryfield.cgi

corrargs="" # correlate1 already filled out a bit - delete again
. $DIR/getopts.cgi
[ -n "$FORM_lon1" ] && corrargs="$corrargs lon1 $FORM_lon1"
[ -n "$FORM_lon2" ] && corrargs="$corrargs lon2 $FORM_lon2"
[ -n "$FORM_lat1" ] && corrargs="$corrargs lat1 $FORM_lat1"
[ -n "$FORM_lat2" ] && corrargs="$corrargs lat2 $FORM_lat2"

uniqname=${FORM_lon1}_${FORM_lon2}_${FORM_lat1}_${FORM_lat2}_${FORM_month}_${FORM_sum}_${FORM_anomal}_${FORM_begin}_${FORM_end}_${FORM_detrend}_${FORM_nens1}_${FORM_nens2}_${FORM_makeensfull}

# Writes to the log file what the user is doing
echo `date` "$FORM_EMAIL ($REMOTE_ADDR) getpotfield $file $corrargs" | sed -e  "s:$DIR/::g" >> log/log
obsfile="data/pot_` basename ${FORM_field} .$EMAIL.info`_$uniqname.nc"
corrargsfield="$file $corrargs plot $obsfile"
if [ ${FORM_var#pot} != $FORM_var ]; then
  . ./myvinkhead.cgi "Map of peak over threshold property" "$kindname $climfield" ""
elif  [ "${FORM_var#chi}" != $FORM_var ]; then
  . ./myvinkhead.cgi "Map of extreme dependence measure $FORM_var" "$station $NAME with $kindname $climfield" ""
else
  . ./myvinkhead.cgi "Error" "" ""
  echo "Can not handle $FORM_var (yet)"
  . ./myvinkfoot.cgi
  exit
fi

if [ 1 = 0 ]; then
  echo '<pre>'
  echo ./bin/getunits.sh $file
  ./bin/getunits.sh $file
  echo ./bin/month2string "$FORM_month" "$FORM_sum" ave
  ./bin/month2string "$FORM_month" "$FORM_sum" ave
  echo '</pre>'
fi
eval `./bin/getunits.sh $file`
if [ "$NEWUNITS" != "$UNITS" -a "$FORM_standardunits" = standardunits ];then
  echo "Converting $kindname $climfield from $UNITS to $NEWUNITS<br>"
fi

if [ -n "$FORM_lon1" ]; then
  if [ -n "$FORM_lon2" -a "$FORM_lon1" != "$FORM_lon2" ]; then
    cutting="cutting out ${FORM_lon1}:${FORM_lon2}&deg;E, "
  else
    cutting="cutting out ${FORM_lon1}&deg;E, "
  fi
fi
if [ -n "$FORM_lat1" ]; then
  if [ -n "$FORM_lat2" -a "$FORM_lat1" != "$FORM_lat2" ]; then
    cutting="$cutting ${FORM_lat1}:${FORM_lat2}&deg;N, "
  else
    cutting="$cutting ${FORM_lat1}&deg;N, "
  fi
fi
eval `./bin/month2string "$FORM_month" "$FORM_sum" ave`
cat <<EOF
Extreme property maps are under active development and may still contain bugs.  Please report problems back to <a href="http://www.knmi.nl/~oldenbor/">me</a>.<p>
EOF
if [ -s $obsfile ]; then
  echo "Using cached data<br>"
else
  cat <<EOF
Retrieving data, $cutting $seriesmonth, $anomalies ...
<br><small>If it takes too long you can abort the job <a href="killit.cgi?id=$FORM_EMAIL&pid=$$" target="_new">here</a> (using the [back] button of the browser does <it>not</it> kill the extraction program)</small><p>
EOF

  cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
extractfield $corrargsfield
$$
EOF
  export SCRIPTPID=$$
  export FORM_EMAIL
###  echo "DEBUG: extractfield $corrargsfield<p>"
# The FORTRAN program by GJ called extractfield is run here to produce a
# nice netcdf file
  ( (echo bin/extractfield $corrargsfield ; $DIR/bin/extractfield $corrargsfield) > /tmp/extractfield$$.log ) 2>&1
  rm pid/$$.$FORM_EMAIL
  if [ 1 = 0 ]; then
    cat /tmp/extractfield$$.log
  fi
  if [ ! -s $obsfile ]; then
    echo 'Something went wrong!' 
    echo '<pre>'
    cat /tmp/extractfield$$.log
    echo '</pre>'
  fi
  rm /tmp/extractfield$$.log
fi # file cached

if  [ "${FORM_var#chi}" != $FORM_var ]; then
# also convert time series
  series=data/${WMO}_$uniqname.txt
  if [ -s $series -a $series -nt $sfile ]; then
    echo "Using cached time series<p>"
  else
    years=`./bin/describefield $obsfile 2>&1 | fgrep "data available" | tr -d '[:alpha:]' | awk '{print "begin " $1 " end " $2}'`
    echo "Retrieving series...<p>"
###    echo "DEBUG: ./bin/extractseries $sfile $corrargs $years<p>"
    ./bin/extractseries $sfile $corrargs $years dump data/$$.txt > /tmp/extractseries$$.log
    if [ 0 = 1 ]; then
      echo 'DEBUG:<pre>'
      echo ./bin/extractseries $sfile $corrargs $years
      cat /tmp/extractseries$$.log
      echo '</pre>'      
    fi
    if [ -s data/$$.txt ]; then
      mv data/$$.txt $series
    else
      echo "Something went wrong"
      echo '<pre>'
      echo ./bin/extractseries $sfile $corrargs $years
      cat /tmp/extractseries$$.log
      echo '</pre>'
    fi
    rm /tmp/extractseries$$.log
  fi
fi

. ./month2string.cgi
. $DIR/setyaxis.cgi

if [ ! -s "$obsfile" ]; then
  echo 'No valid data were selected.  Please review the choices you made on the previous page.'
  . ./myvinkfoot.cgi
  exit
fi

if [ -z "$FORM_threshold" ]; then
  echo "</pre>This measure needs a threshold, please supply one on the previous page."
  . ./myvinkfoot.cgi
  exit
fi

threshold=`echo $FORM_threshold/100 | bc -l`
sign=`echo $threshold - 0.5 | bc -l | cut -b 1`
if [ " $sign" = " -" ]; then
  FORM_above=F
  threshold=`echo "1 - $threshold" | bc -l`
else
  FORM_above=T
fi

if [ -z $FORM_minfac ]; then
  FORM_minfac=60
fi
minfac=`echo $FORM_minfac/100 | bc -l`

if [ -n "$FORM_pot_tv" ]; then
  FORM_var=${FORM_var}_tv
fi

# include here all R functions that can be called
case $FORM_var in

pot_median) PROG="xexcessclimexp"
            args="fun='medianexcess',p=$threshold,threshold=FALSE"
            comp="\$out"
            lvar="median of excesses";;

pot_mean)   PROG="xexcessclimexp"
            args="fun='meanexcess',p=$threshold,threshold=FALSE"
            comp="\$out"
            lvar="mean of excesses";;

pot_sd)     PROG="xexcessclimexp"
            args="fun='stddevexcess',p=$threshold,threshold=FALSE"
            comp="\$out"
            lvar="s.d. of excesses";;

pot_scale)  PROG="xparetoclimexp"
            args="p=$threshold"
            comp="\$out[1,,]"
            lvar="scale of GPD";;

pot_shape)  PROG="xparetoclimexp"
            args="p=$threshold"
            comp="\$out[2,,]"
            lvar="shape of GPD";;

pot_return) PROG="paretoreturnlevels"
            args="p=$threshold,rt=$FORM_pot_return"
            comp="\$out"
            if [ $FORM_month != 0 -o $NPERYEAR = 1 ]; then
              lvar="${FORM_pot_return}-yr return level"
	    elif [ $NPERYEAR = 4 ]; then
              lvar="${FORM_pot_return}-season return level"
	    elif [ $NPERYEAR = 12 ]; then
              lvar="${FORM_pot_return}-month return level"
	    elif [ $NPERYEAR -ge 360 -a $NPERYEAR -le 366 ]; then
              lvar="${FORM_pot_return}-day return level"
	    else
              lvar="${FORM_pot_return}-period return level"
	    fi
	    ;;

pot_return_diff)   PROG="paretoreturnlevelsdiff"
            patfile=`egrep '^file=' $FORM_pot_pattern | tr '\`;<>&#' ' ' | sed -e 's/^file=//'`
            line="infpat<-netcdfinfo(\"$patfile\")
pat<-netcdfreadpat(\"$patfile\",infpat\$vars[1],infpat\$vars[2],infpat\$vars[3])"
            args="pat\$data,p=$threshold"
            comp="\$out"
            name=`egrep '^name=' $FORM_pot_pattern | tr '\`;<>&#' ' ' | sed -e 's/^name=//'`
            shortname=${name%aap}
            if [ $FORM_month != 0 -o $NPERYEAR = 1 ]; then
              lvar="${FORM_pot_return}-yr return level"
	      NEWUNITS="yr"
            elif [ $NPERYEAR = 4 ]; then
              lvar="${FORM_pot_return}-season return level"
	      NEWUNITS="season"
            elif [ $NPERYEAR = 12 ]; then
              lvar="${FORM_pot_return}-month return level"
	      NEWUNITS="mo"
            elif [ $NPERYEAR -ge 360 -a $NPERYEAR -le 366 ]; then
              lvar="${FORM_pot_return}-day return level"
	      NEWUNITS="dy"
            else
              lvar="${FORM_pot_return}-period return level"
	      NEWUNITS="periods"
            fi
            ;;

pot_median_tv) PROG="xparetotvtclimexp"
               args="p=$threshold"
               comp="\$medianexcesses"
               lvar="median of excesses wrt a time-varying threshold";;

pot_mean_tv)   PROG="xparetotvtclimexp"
               args="p=$threshold"
               comp="\$meanexcesses"
               lvar="mean of excesses wrt a time-varying threshold";;

pot_sd_tv)     PROG="xparetotvtclimexp"
               args="p=$threshold"
               comp="\$stdevexcesses"
               lvar="s.d. of excesses wrt a time-varying threshold";;

pot_scale_tv)  PROG="xparetotvtclimexp"
               args="p=$threshold"
               comp="\$out[1,,]"
               lvar="scale of GPD wrt a time-varying threshold";;

pot_shape_tv)  PROG="xparetotvtclimexp"
               args="p=$threshold"
               comp="\$out[2,,]"
               lvar="shape of GPD wrt a time-varying threshold";;

chi)           PROG="xdependenceclimexp"
               line="timeseries<-as.matrix(read.table(\"$series\",header=T))
timeseries[timeseries==-999.9]<-NA"
               args="ts=timeseries,u=$threshold,fun='chi'"
               comp="\$out"
	       lvar="extreme dependence measure chibar";;

chibar)        PROG="xdependenceclimexp"
               line="timeseries<-as.matrix(read.table(\"$series\",header=T))
timeseries[timeseries==-999.9]<-NA"
               args="ts=timeseries,u=$threshold,fun='chibar'"
               comp="\$out"
	       lvar="extreme dependence measure chi";;

*) echo "I cannot handle $FORM_var yet"
   . ./myvinkfoot.cgi
   exit;;

esac

if [ -z "$ENSEMBLE" ]; then
  readnetcdf="obs<-netcdfread(\"$obsfile\",infobs\$vars[2],infobs\$vars[3],infobs\$vars[4])"
  new=obs
else
  readnetcdf="obs<-netcdfreadclimexp(\"$obsfile\",infobs\$vars[2],infobs\$vars[3],infobs\$vars[5])
obsflat<-manipensemble(obs\$data)"
  new=obsflat
fi

echo "Computing $lvar at threshold ${FORM_threshold}% at points with at least ${FORM_minfac}% valid data in <a href=\"http://cran.r-project.org/\">R</a>.  This will take (quite) a while...<br>"
  echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$FORM_EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the R job)</small><p>"
echo "<small>Keepalive messages have not yet been implemented fully, so if R takes more than 5 minutes the connection may be lost.  Eventually the results will appear as <a href="data/g$$_1.png">plot</a>, <a href="data/g$$_1.eps.gz">eps</a> and <a href="data/R$$.nc">netcdf</a>.</small><p>"

# Make a temp file with R command (R does not accept input redirection)
cat > /tmp/R$$.r  <<EOF
dyn.load("./r/rkillfile.so")
.Fortran("rkillfile")
dyn.load("./r/rkeepalive.so")
.Fortran("rkeepalive",i=as.integer(0),n=as.integer(0))
source("./r/maplibs.r")
source("./r/$PROG.r")
infobs<-netcdfinfo("$obsfile")
$readnetcdf
$line
map<-$PROG(obs\$lonncfile,obs\$latncfile,${new}\$data,$args,upper=$FORM_above,nonmissing=$minfac)
source("./r/netcdfwriteclimexp.r")
netcdfwriteclimexp(obs\$lonncfile,obs\$latncfile,map$comp,filename="data/R$$.nc")
q("no")
EOF

# Executes R in batch mode writing R prompt outputs to file  
# Note: file /tmp/R$$.r contains R commands to be executed
cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
R $FORM_field $sfile $corrargs
$$
EOF
export SCRIPTPID=$$
export FORM_EMAIL
export UDUNITS_PATH=$DIR/grads/udunits.dat
(./bin/R --vanilla < /tmp/R$$.r > /tmp/R$$.log ) 2>&1
# pnmtopng chatters to stderr
rm pid/$$.$FORM_EMAIL

if [ ! -s data/R$$.nc ]; then
  echo "<p>Something went wrong!"
    FORM_debug=true
    noplot=true
    nomap=true
fi

if [ 1 = 0 -o -n "$FORM_debug" ]; then
  echo '<pre>'
    cat /tmp/R$$.r
    cat /tmp/R$$.log
  echo '</pre>'
fi
rm /tmp/R$$.r
rm /tmp/R$$.log

# two ways to fix the netcdf file: choose one
if [ 0 = 1 ]; then
# either use GrADS xdfopen
  cat > data/R$$.ctl <<EOF
dset ^R$$.nc
XDEF lon
YDEF lat
VARS 1
data=>$FORM_var 0 99 $lvar
ENDVARS
EOF
  file="data/R$$.ctl"
else
  # or add the required attributes by hand
  # this requires nco to be in the path
  #ncatted -O \
  #  -a long_name,lon,a,c,"Longitude" \
  #  -a units,lon,a,c,"degrees_east" \
  #  -a axis,lon,a,c,"X" \
  #  -a long_name,lat,a,c,"Latitude" \
  #  -a units,lat,a,c,"degrees_north" \
  #  -a axis,lat,a,c,"Y" \
  #  data/R$$.nc
  # and rename the variable
  if [ -z "$myprog" ] ; then
    ncrename -v data,$FORM_var data/R$$.nc
    ncatted -O -a long_name,$FORM_var,a,c,"$lvar" data/R$$.nc
    case $FORM_var in
    pot_shape|pot_shape_tv|chi|chibar) units=1;;
    *) units=$NEWUNITS;;
    esac
    ncatted -O -a units,$FORM_var,a,c,"$units" data/R$$.nc
  fi
  file="data/R$$.nc"
fi
map="set lon $FORM_lon1 $FORM_lon2
set lat $FORM_lat1 $FORM_lat2"
if [ -n "$FORM_anom" ]; then
  climfield="$climfield anomalies"
fi
if [ "$FORM_standardunits" = standardunits ]; then
  units=$NEWUNITS
else
  units=$UNITS
fi
climfield="$climfield [${units}]"

if [ "${FORM_var#chi}" = $FORM_var ]; then
  station=$kindname
  CLIM="$climfield\\$lvar, threshold ${FORM_threshold}%"
else
  climfield="$climfield\\threshold ${FORM_threshold}%"
fi
if [ -n "$FORM_detrend" ]; then
  climfield="$climfield (detrended)"
fi
. ./grads.cgi
echo "<br><a href=\"data/R$$.nc\">netcdf file of plot</a>"
if [ -f data/R$$.ctl ]; then
  echo "(and <a href=\"data/R$$.ctl\">ctl</a> file for GrADS)"
fi

if [ $FORM_var = pot_return -a $EMAIL != someone@somewhere ]; then
  name="$kindname $climfield ${lvar%return level}${FORM_threshold}% ${seriesmonth%averaged} ${FORM_lon1}:${FORM_lon2}E ${FORM_lat1}:${FORM_lat2}N"
  [ -n "$FORM_begin" -o -n "$FORM_end" ] && name="$name ${FORM_begin}:${FORM_end}"
  [ -n "$FORM_anom" ] && name="$name anom"
  [ -n "$FORM_detrend" ] && name="$name detrend"
  [ -n "$FORM_nens1" -o -n "$FORM_nens2" ] && name="$name ${FORM_nens1}:${FORM_nens2}"
    cat > ./data/R$$.$EMAIL.pat << EOF
file=data/R$$.nc
name=$name
units=$units
rt=$FORM_pot_return
EOF
fi

if [ ${FORM_var#pot} != $FORM_var ]; then
  echo '<div class="note">R peak-over-threshold routines are kindly provided by the <a href="http://www.met.rdg.ac.uk/cag/rclim/rclim.html" target="_new">RCLIM</a> initiative</div>'
elif  [ "${FORM_var#chi}" != $FORM_var ]; then
  echo '<div class="note">R extreme dependence routines are kindly provided by the <a href="http://www.met.rdg.ac.uk/cag/rclim/rclim.html" target="_new">RCLIM</a> initiative</div>'
fi
. ./myvinkfoot.cgi
