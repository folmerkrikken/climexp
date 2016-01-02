#!/bin/sh
# is called from verification.cgi and regionverification.cgi
# or directly from this page
. ./init.cgi

if [ -z "$table" ]; then
  cat <<EOF
Content-Type: text/html


EOF
  export DIR=`pwd`
. ./getargs.cgi
  eval `bin/month2string "$FORM_month" "$FORM_sum" ave`
  NEWUNITS=$FORM_NEWUNITS
  table=$FORM_table
  verifxlabel=$FORM_verifxlabel
  verifylabel=$FORM_verifylabel
  ENSEMBLE=$FORM_ENSEMBLE
  if [ "${FORM_verif#map}" != "$FORM_verif" ]; then
    makemap=map
  fi
  sumstring=$FORM_sumstring
fi

if [ -z "$FORM_NPERYEAR" ]; then
  if [ -n "$NPERYEAR" ]; then
    FORM_NPERYEAR=$NPERYEAR
  else
    FORM_NPERYEAR=12 # I hope
  fi
fi
NPERYEAR=$FORM_NPERYEAR

if [ -n "$EMAIL" -a "$EMAIL" != "someone@somewhere" ]; then
  . ./save_commonoptions.cgi
  . ./save_plotoptions.cgi
  cat > ./prefs/$EMAIL.verifoptions.$FORM_NPERYEAR << EOF
FORM_verif=$FORM_verif;
FORM_month=$FORM_month;
FORM_sum=$FORM_sum;
FORM_begin=$FORM_begin;
FORM_end=$FORM_end;
FORM_detrend=$FORM_detrend;
FORM_debias=$FORM_debias;
FORM_nens1=$FORM_nens1;
FORM_nens2=$FORM_nens2;
FORM_makeensfull=$FORM_makeensfull;
FORM_fcstnameorg="$FORM_fcstnameorg";
FORM_fcstname="$FORM_fcstname";
EOF
fi

if [ ! -s "$table" ]; then
  . ./myvinkhead.cgi 'Error' '' ''
  echo 'No valid data were selected.  Please review the choices you made on the previous page.'
  . ./myvinkfoot.cgi
  exit
fi
if [ "$FORM_threshold_type" = "TRUE" ]; then
  threshold=$FORM_threshold
else
  threshold="${FORM_threshold}%"
fi
obsfile=`dirname $table`/`basename $table .nc`"_obs.nc"
if [ -z "$makemap" ]; then
  if [ -n "$startstop"  -a -s "$startstop" ]; then
    yrstart=`head -1 $startstop`
    yrstop=`tail -1 $startstop`
    verifxlabel="$verifxlabel ${yrstart}:${yrstop}"
  fi
fi
if [ "$FORM_threshold_type" = TRUE ]; then
    threshold_units=$NEWUNITS
else
    threshold_units="%"
fi
if [ -n "$FORM_lon1$FORM_lon12$FORM_lat1$FORM_lat2" ]; then
    area="\n${FORM_lat1:--90}-${FORM_lat2:-90}N, ${FORM_lon1:--0}-${FORM_lon2:-360}E"
fi

# include here all R functions that can be called

PROG=$FORM_verif
case $FORM_verif in

likelihood)
	args="data, xlab=\"$verifxlabel\", ylab=\"$verifylabel\"";
	lvar="likelihood";;

brierscore)
	args="data,u=$FORM_threshold,threshold=$FORM_threshold_type,nbins=$FORM_nbins,bsfile=\"$DIR/data/R$$.brierscore\"";
	noplot=T;
	needsthreshold="true";
	lvar="Brier Score";;

fairbrierscore)
	args="data,threshold=$FORM_threshold,is.value=$FORM_threshold_type,fbsfile=\"$DIR/data/R$$.brierscore\"";
	noplot=true;
	needsthreshold="true";
	lvar="Fair Brier Score";;

fairCRPSanalysis)
	args="data,fcafile=\"$DIR/data/R$$.brierscore\"";
	noplot=true;
	needsthreshold="false";
	lvar="Fair CRPS Analysis";;

rankhistogram)
	args="data,graphvaluefile=\"data/R$$.txt\",maintitle=\"$seriesmonth $verifylabel against\n$verifxlabel\"";
	needsthreshold="false";
	lvar="Fair CRPS Analysis";;

reliability) 
	args="data,u=$FORM_threshold,nbins=$FORM_nbins,threshold=$FORM_threshold_type,reliabfile=\"data/R$$.reliab\",graphvaluefile=\"data/R$$.txt\",maintitle=\"$seriesmonth $verifylabel against\n$verifxlabel, threshold=$FORM_threshold$threshold_units$area\"";
	needsthreshold="true";
	lvar="reliability";;

deterministic)
	args="data, detfile=\"$DIR/data/R$$.deterministic\"";
	noplot=T;
	lvar="ensemble mean scores";;

rps) args="data,\"$DIR/data/R$$.rps\""; lvar="tercile RPS";noplot=true;;

rocrclim) args="data,u=$FORM_threshold, threshold=$FORM_threshold_type, rocfile=\"$DIR/data/R$$.rocarea\",maintitle=\"$seriesmonth $verifylabel against\n$verifxlabel\""; needsthreshold="true"; lvar="ROC curve";;

rocdeb) myprog="./bin/rocdeb $threshold $table"; maintitle="$seriesmonth $verifylabel against $verifxlabel"; needsthreshold="true"; lvar="ROC curve";;

rocprob) myprog="./bin/roc prob $threshold same $table"; maintitle="$seriesmonth $verifylabel against $verifxlabel"; needsthreshold="true"; lvar="ROC curve";;

rocthreshold) myprog="./bin/roc threshold $threshold same $table"; maintitle="$seriesmonth $verifylabel against $verifxlabel"; needsthreshold="true"; lvar="ROC curve";;

mapcorr) PROG="cortwo3d";args="data1=fcst\$data,data2=obs\$data";comp="\$correlation";FORM_var="cor";lvar="correlation of ensemble mean";;

mapdiscmean) PROG="discrim";args="data1=fcst\$data,data2=obs\$data";comp="\$discrimination";FORM_var="disc";lvar="discrimination of ensemble mean";;

mapmae) PROG="maetwo3d";args="data1=fcst\$data,data2=obs\$data";comp="\$mae";FORM_var="mae";lvar="mean absolute error of ensemble mean";;

maprmse) PROG="rmsetwo3d";args="data1=fcst\$data,data2=obs\$data";comp="\$rmse";FORM_var="rmse";lvar="root mean square error of ensemble mean";;

mapbrier) PROG="bstwo3d";args="data1=fcst\$data,data2=obs\$data,nbins=$FORM_nbins,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$bs";FORM_var="bs";lvar="Brier Score";;

mapbriar) myprog="./bin/Briar $threshold $obsfile $table data/R$$.nc";FORM_var="bs";lvar="Brier Score";;

mapresolution) PROG="bstwo3d";args="data1=fcst\$data,data2=obs\$data,nbins=$FORM_nbins,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$res";FORM_var="resolution";lvar="Resolution component of the Brier Score";;

mapreliability) PROG="bstwo3d";args="data1=fcst\$data,data2=obs\$data,nbins=$FORM_nbins,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$rel";FORM_var="reliability";lvar="Reliability component of the Brier Score";;

mapuncertainty) PROG="bstwo3d";args="data1=fcst\$data,data2=obs\$data,nbins=$FORM_nbins,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$unc";FORM_var="uncertainty";lvar="Uncertainty component of the Brier Score";;

mapbss) PROG="bsstwo3d";args="data1=fcst\$data,data2=obs\$data,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$bss";FORM_var="bss";lvar="BSS wrt climatology";;

maprps) PROG="rpstwo3d";args="data1=fcst\$data,data2=obs\$data";comp="\$rps";FORM_var="rps3";lvar="tercile RPS";;

maprpss) PROG="rpsstwo3d";args="data1=fcst\$data,data2=obs\$data";comp="\$rpss";FORM_var="rpss3";lvar="tercile RPSS wrt climatology";;

maprpss5) PROG="rpssfive3d";args="data1=fcst\$data,data2=obs\$data";comp="\$rpss";FORM_var="rpss5";lvar="quintile RPSS wrt climatology";;

maprps3) myprog="./bin/RPS 3 33.33333 33.33333 $obsfile $table data/R$$.nc";FORM_var="rps3";lvar="tercile RPS";;

maprps5) myprog="./bin/RPS 5 20 20 20 20 $obsfile $table data/R$$.nc";FORM_var="rps5";lvar="tercile RPS";;

maprocarea) PROG="rocareatwo3d";args="data1=fcst\$data,data2=obs\$data,u=$FORM_threshold,threshold=$FORM_threshold_type";needsthreshold="true";comp="\$ra";FORM_var="roc";lvar="area under the ROC curve";;

maproc) myprog="./bin/rocmap $threshold same $obsfile $table data/R$$.nc";needsthreshold="true";FORM_var="roc";lvar="area under the ROC curve";;

maprocdeb) myprog="./bin/ROCscoremap $threshold $obsfile $table data/R$$.nc";needsthreshold="true";FORM_var="ROCarea";lvar="area under the ROC curve";;

debug) lvar="verification table";;

*) echo "</pre>Verification measure $FORM_verif not yet implemented, please choose another one"; PROG="";;

esac

if [ -z "$makemap" ]; then
  . ./myvinkhead.cgi "Time series $lvar" "$verifylabel against $verifxlabel" "noindex,nofollow"
else
  . ./myvinkhead.cgi "Field $lvar" "$verifylabel against $verifxlabel" "noindex,nofollow"
fi

if [ "$FORM_verif" = debug ]; then
  echo "<a href=\"$table\">table of observations and forecasts</a><p>"
  FORM_oper="corr"
  FORM_var="val"
  FORM_col="rb"
  FORM_title="grid points used"
  FORM_cmax="0.6"
  FORM_scale="1"
  FORM_greycut="5"
  . ./plotstations.cgi
  exit
fi
if [ "$FORM_verif" = mapdebug ]; then
  obsfile=`dirname $table`/`basename $table .nc`"_obs.nc"
  cat <<EOF
<a href="$table">forecasts</a>,<a href="$obsfile">observations</a> (netcdf)
</body></html>
EOF
  . ./myvinkfoot.cgi
  exit
fi
if [ "$FORM_verif" = maprocarea ]; then
  if [ $FORM_threshold_type = TRUE ]; then
    echo "Sorry, the ROC area routine does not support absolute thresholds yet, only quantiles"
    . ./myvinkfoot.cgi
    exit
  fi
fi

if [ -n "$needsthreshold" ]; then
  if [ -z "$FORM_threshold" ]; then
    echo "</pre>This measure needs a threshold, please supply one on the previous page."
  . ./myvinkfoot.cgi
  exit
  fi
fi

if [ -n "$myprog" ]; then
  echo "Computing $lvar<br>"
  if [ -z "$makemap" ]; then
    txtfile=data/roc$$.txt
    epsfile=data/roc$$.eps
    pngfile=data/roc$$.png
    if [ 0 = 1 ]; then
       echo $myprog '<br>'
    fi
    ($myprog > $txtfile) 2>&1
    area=`tail -1 $txtfile | cut -b 3-`
    ./bin/gnuplot <<EOF
$gnuplot_init
set size 0.6
set size square
set xrange [0:1]
set yrange [0:1]
set title "$maintitle"
set xlabel "FAR"
set ylabel "HR"
set key bottom
set term postscript epsf color solid
set output "$epsfile"
plot "$txtfile" u (1-\$2):(1-\$1) title "$area" with lines, x notitle with lines
set term png $gnuplot_png_font_hires
set output "$pngfile"
replot
EOF
    gzip $epsfile
	getpngwidth
    cat <<EOF
<div class="bijschrift">ROC curve (<a href="$epsfile.gz">postscript</a>, 
<a href="$txtfile">raw data</a>)</div>
<center>
<img src="$pngfile" alt="ROC curve" width="$halfwidth"><br clear=all>
</center>
EOF
  else # make map
    if [ 0 = 1 ]; then
      echo "$myprog <br>"
    fi
    $myprog 2>&1
  fi
elif [ -n "$PROG" ]; then
  echo "Computing $lvar in <a href=\"http://cran.r-project.org/\">R</a>.  This will take (quite) a while..."
  echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$FORM_EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the R job)</small><p>"

# Make a temp file with R command (R does not accept input redirection)
  if [ -z "$makemap" ]; then
    cat > /tmp/R$$.r <<EOF
library("SpecsVerification")
dyn.load("./r/rkillfile.so")
.Fortran("rkillfile")
dyn.load("./r/rkeepalive.so")
.Fortran("rkeepalive",i=as.integer(0),n=as.integer(0))
# read the table produced by the FORTAN program verification
data<-read.table("$table",header=T);
pdf("data/R$$.pdf")
source("./r/$PROG.r")
$PROG($args)
###dev.off()
q("no")
EOF
  else
    # rpacks is a symlink to ~/Library/R/x.y/library on the Mac
    cat > /tmp/R$$.r  <<EOF
.libPaths("./rpacks")
.libPaths()
library("RNetCDF")
dyn.load("./r/rkillfile.so")
.Fortran("rkillfile")
dyn.load("./r/rkeepalive.so")
.Fortran("rkeepalive",i=as.integer(0),n=as.integer(4))
source("./r/maplibs.r")
library("SpecsVerification")
source("./r/applyfieldclimexp.r")
source("./r/$PROG.r")
infobs<-netcdfinfo("$obsfile")
.Fortran("rkeepalive",i=as.integer(1),n=as.integer(4))
obs<-netcdfread("$obsfile",infobs\$vars[2],infobs\$vars[3],infobs\$vars[4])
.Fortran("rkeepalive",i=as.integer(2),n=as.integer(4))
infofcst<-netcdfinfo("$table")
.Fortran("rkeepalive",i=as.integer(3),n=as.integer(4))
if ( length(infofcst\$vars) == 4 )
  fcst<-netcdfread("$table",infofcst\$vars[2],infofcst\$vars[3],infofcst\$vars[4])
if ( length(infofcst\$vars) == 5 )
  fcst<-netcdfreadclimexp("$table",infofcst\$vars[2],infofcst\$vars[3],infofcst\$vars[5])
.Fortran("rkeepalive",i=as.integer(4),n=as.integer(4))
###save(file="./data/data1.RData",fcst$data)
###save(file="./data/data2.RData",obs$data)
map<-$PROG($args)$comp
###pdf("data/R$$.pdf")
###plotmap(obs\$lonncfile,obs\$latncfile,map)
source("./r/netcdfwriteclimexp.r")
netcdfwriteclimexp(obs\$lonncfile,obs\$latncfile,map,filename="data/R$$.nc")
###dev.off()
q("no")
EOF
  fi # makemap

# Executes R in batch mode writing R prompt outputs to file  
# Note: file /tmp/R$$.r contains R commands to be executed
  cat | sed -e "s:$DIR::g" > pid/$$.$FORM_EMAIL <<EOF
$REMOTE_ADDR
R $FORM_field1 $FORM_field2 $CLIM $station $corrargs
$$
EOF
  export SCRIPTPID=$$
  export FORM_EMAIL
  export UDUNITS_PATH=$DIR/grads/udunits.dat
  cp /tmp/R$$.r data/
  echo "(<a href=data/R$$.r>R script being run</a>, <a href=r/$PROG.r>library routine</a>)<p>"
  (R --vanilla --ignore=$SCRIPTPID < /tmp/R$$.r > /tmp/R$$.log ) 2>&1 &
  status=running
  i=0
  while [ $status = running ]; do
    i=$((i+1))
    sleep 3
    if [ $((i%10)) = 0 ]; then
        echo "R still $status $((i/10)) `date`<p>"
    fi
    c=`ps axuw | fgrep -v grep | fgrep -c "ignore=$SCRIPTPID"`
    [ $c = 0 ] && status=ready
  done
  # pnmtopng chatters to stderr
  rm pid/$$.$FORM_EMAIL

  if [ -n "$makemap" ]; then
    if [ ! -s data/R$$.nc ]; then
      echo "<p>Something went wrong!"
        FORM_debug=true
        noplot=true
        nomap=true
    fi
  fi
  if [ -n "$FORM_debug" ]; then
    echo '<pre>'
###   cat /tmp/R$$.r
      cat /tmp/R$$.log
    echo '</pre>'
  fi
  rm /tmp/R$$.r
  rm /tmp/R$$.log

  # Write on the screen the value of the Brier score achived in file data/R$$.brierscore
  if [ -f data/R$$.brierscore ]; then
    echo '<pre>'
    cat data/R$$.brierscore
    echo '</pre>'
    rm data/R$$.brierscore
    rm data/R$$.pdf
  fi

# Write on the screen the values of correlation, RMSE and MAE achived in file data/R$$.deterministic
  if [ -f data/R$$.deterministic ]; then
###  echo "$seriesmonth $verifylabel against $verifxlabel<br>"
    echo "Ensemble mean:<br>"
    echo "Correlation = "`head -2 data/R$$.deterministic | awk '{print substr($2,1,4)}' |tail -1`"<br>"
    echo "RMSE = "`head -3 data/R$$.deterministic | awk '{print substr($2,1,4)}' |tail -1`"$NEWUNITS<br>"
    echo "MAE = "`head -4 data/R$$.deterministic | awk '{print substr($2,1,4)}' |tail -1`"$NEWUNITS<br>"
    rm data/R$$.deterministic
    rm data/R$$.pdf
  fi

# Write to the screen the oputput of reliability
  if [ -f data/R$$.reliab ]; then
    if [ "$FORM_threshold_type" = TRUE ]; then
      echo "Threshold was "`tail -1 data/R$$.reliab | awk '{print substr($2,1,4)}'`"$NEWUNITS<br>"
    else
      echo "Threshold at ${FORM_threshold}% quantile corresponds to "`tail -1 data/R$$.reliab | awk '{print substr($2,1,4)}'`"$NEWUNITS<br>"
    fi
    rm data/R$$.reliab
  fi

# Write on the screen the value of the RPS achived in file data/R$$.rps
  if [ -f data/R$$.rps ]; then
    echo "RPS = "`head -2 data/R$$.rps | awk '{print substr($2,1,4)}' | tail -1`"<br>"
###    rm data/R$$.rps
  fi

# Write on the screen the value of the ROC area achived in file data/R$$.rocarea
  if [ -f data/R$$.rocarea ]; then
    echo "ROC area = "`head -2 data/R$$.rocarea | awk '{print substr($2,1,4)}' | tail -1`"<br>"
    if [ "$FORM_threshold_type" = TRUE ]; then
      echo "Threshold was "`tail -1 data/R$$.rocarea | awk '{print substr($2,1,4)}'`"$NEWUNITS<br>"
    else
      echo "Threshold at ${FORM_threshold}% quantile corresponds to "`tail -1 data/R$$.rocarea | awk '{print substr($2,1,4)}'`"$NEWUNITS<br>"
    fi
    rm data/R$$.rocarea
  fi

  if [ -z "$makemap" -a -z "$noplot" ]; then
###echo "<a name=\"plots\"><h3>Plots</h3></a>"
#. $DIR/showplots.cgi
    gs -q -r75 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -sDEVICE=pnmraw -sOutputFile=data/R$$.pnm data/R$$.pdf -c quit
    (pnmcrop data/R$$.pnm | pnmtopng > data/R$$.png) > /dev/null 2>&1 # 
    rm data/R$$.pnm
    #convert data/R$$.ps data/R$$.png
    echo "<div class=\"bijschrift\">$verifylabel verified against $verifxlabel"
    if [ -n "$FORM_lat1" ]; then
      echo "in ${FORM_lat1}:${FORM_lat2}N, ${FORM_lon1}:${FORM_lon2}E"
    fi
    echo -n "$debias ("
    if [ -s data/R$$.txt ]; then
      echo "<a href=\"data/R$$.txt\">raw data</a>,"
    fi
    if [ $FORM_verif = likelihood ]; then
      echo "<a href=\"$table\">raw data</a>,"
    fi
    echo "<a href=\"data/R$$.pdf\">PDF</a>)</div><center><img src=\"data/R$$.png\"  alt=\"$FORM_verif\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"
  fi
fi # -n $PROG

if [ -s data/R$$.nc ]; then
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
      ncrename -v data,$FORM_var data/R$$.nc > /dev/null 2>&1
    fi
    file="data/R$$.nc"
  fi
  map="$map
set lon $FORM_lon1 $FORM_lon2
set lat $FORM_lat1 $FORM_lat2"
  station=$verifylabel
  os=`uname`
  if [ $os = Darwin ]; then #!%$@
      CLIM="\\\\against $verifxlabel"
  else
      CLIM="\\against $verifxlabel"
  fi
  if [ -n "$needsthreshold" ]; then
    CLIM="$CLIM, threshold $FORM_threshold"
    if [ "$FORM_threshold_type" = FALSE ]; then
      CLIM="${CLIM}%"
    else
      CLIM="$CLIM$NEWUNITS"
    fi
  fi
  . ./grads.cgi
  echo "Download <a href=\"data/R$$.nc\">netcdf file of plot</a>"
  if [ -f data/R$$.ctl ]; then
    echo "(and <a href=\"data/R$$.ctl\">ctl</a> file for GrADS)"
  fi
fi # makemap

if [ -z "$FORM_period" ]; then
#
# choose another operation on the same table,
# but not when called from forecast_verification.cgi
#
cat <<EOF
<form action="verification1.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$FORM_EMAIL">
<input type="hidden" name="NEWUNITS" value="$NEWUNITS">
<input type="hidden" name="ENSEMBLE" value="$ENSEMBLE">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="table" value="$table">
<input type="hidden" name="verifxlabel" value="$verifxlabel">
<input type="hidden" name="verifylabel" value="$verifylabel">
<input type="hidden" name="month" value="$FORM_month">
<input type="hidden" name="sum" value="$FORM_sum">
<input type="hidden" name="sumstring" value="$sumstring">
<input type="hidden" name="detrend" value="$FORM_detrend">
<input type="hidden" name="debias" value="$FORM_debias">
EOF
if [ -z "$makemap" ]; then
. ./choose_verification.cgi
else
. ./choose_mapverification.cgi
fi
. ./choose_threshold.cgi

if [ -n "$makemap" ]; then
  cat <<EOF
<p><div class="formheader">Area</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
EOF
  intable=true
  . ./plotoptions.cgi
###  if [ -z "$replot" ]; then
###    if [ -n "$LSMASK" ]; then
###      echo "<br>One day I\'ll implement a land-sea mask"
###    else
###      echo "<br>Land/sea mask not yet available"
###    fi
###  fi
  echo '</table></div>'
fi
echo "<div class=\"formbody\"><input type=\"submit\" class=\"formbutton\" value=\"Verify again\"></div>"

fi

echo '<div class="note">Verification measures in R have been kindly provided by the
<A HREF="http://www1.secam.ex.ac.uk/?nav=695" target=_new>RCLIM initiative</A> and ongoing research on verification by the <a href="http://www.specs-fp7.eu/SPECS/Home.html" target=_new>EU project SPECS</a></div>'

if [ -n "$FORM_field" ]; then
  if [ ${FORM_field#ukmo} != $FORM_field -o ${FORM_field#ens_ukmo} != $FORM_field ]; then
    echo "Underlying data (c) Crown copyright 2006, supplied by the Met Office."
  fi
  if [ -n "$makemap" ]; then
    . ./myvinkfoot.cgi
  else
    echo "<p>"
    FORM_oper="grid"
    FORM_var="val"
    FORM_col="rb"
    FORM_title="grid points of $verifylabel"
    FORM_cmax="1"
    FORM_scale="1"
    FORM_greycut="5"
    . ./plotstations.cgi
  fi
else
  . ./myvinkfoot.cgi
fi
