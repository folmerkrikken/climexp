#!/bin/sh
. ./init.cgi
if [ -z "$myvinkhead" ]; then
  echo 'Content-Type: text/html'
  . ./expires.cgi
  echo
  echo
fi

export DIR=`pwd`
# if called from upload.cgi or another routine dont bother
if [ -z "$FORM_field" ]; then
  . ./getargs.cgi
fi
# identify search engine robots
. ./searchengine.cgi
# check email address
. ./checkemail.cgi
if [ -z "$ROBOT" ]; then
  echo `date` "$EMAIL ($REMOTE_ADDR) $FORM_field" >> log/log
fi
if [ $EMAIL = oldenbor@knmi.nl ]; then
    lwrite=false
fi

# start real work
. ./queryfield.cgi
[ "$lwrite" = true ] && echo "FORM_field=$FORM_field<br>file=$file<br>"

if [ "$EMAIL" != someone@somewhere ]; then
    echo "FORM_field=$FORM_field;" > prefs/$EMAIL.field.$NPERYEAR
fi

. ./myvinkhead.cgi "Field" "$kindname $climfield" "nofollow,index"

if [ ${FORM_field#rt2b_} != $FORM_field -o ${FORM_field#rt3_} != $FORM_field ]; then
	if [ "$EMAIL" = someone@somewhere ]; then
		echo "Sorry, you need to be <a href=\"registerform.cgi\">logged in</a> to use ENSEMBLES data"
		FORM_field=""
		. ./myvinkfoot.cgi
		exit
	fi
	if [ ! -s prefs/${EMAIL}.ensemblesrt3 ]; then
		if [ "$FORM_iaccept" = on ]; then
		    echo "FORM_iaccept=on;" > prefs/${EMAIL}.ensemblesrt3
		else
			if [ -n "$FORM_iaccept" ]; then
				echo "<form color=#ff2222>You have to accept these conditions</font><br>"
			fi
			cat ensembles_rt_conditions.html
			cat <<EOF
<form action="select.cgi" method="POST">
<input type="hidden" name="email" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<br><input type="checkbox" name="iaccept">I accept these terms
<input type="submit" class="formbutton" value="Retrieve data">
</form>
EOF
			FORM_field=""
			. ./myvinkfoot.cgi
			exit
		fi
	fi
fi

if [ -n "$NPERYEAR" -a "$NPERYEAR" != 12 ]; then
cat <<EOF
<font color="#ff0000">Non-monthly fields are under development, some options do not work yet</font><br>
EOF
fi
case $file in
IPCCData*) url="wipefeet.cgi?http://www-pcmdi.llnl.gov/ipcc/about_ipcc.php";;
ESSENCE*)  url="http://www.knmi.nl/~sterl/Essence/";;
ERA*)      url="wipefeet.cgi?http://www.ecmwf.int/research/era/";;
Demeter*)  url="wipefeet.cgi?http://data.ecmwf.int/data";;
ECMWF*)    url="wipefeet.cgi?http://www.ecmwf.int";;
NCEPNCAR*) url="wipefeet.cgi?http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml";;
CMIP5_yr*) url="wipefeet.cgi?http://www.cccma.ec.gc.ca/data/climdex/climdex.shtml";;
CMIP5*)    url="showmetadata.cgi?EMAIL=$EMAIL&field=$FORM_field";;
data*)     url="";;
*)         url=`fgrep \"${FORM_field}\" selectfield_obs.html selectfield_rapid.html selectdailyfield*.html | sed -e 's/^.*href=\"//'  -e 's/\".*$//' -e "s/EMAIL/$EMAIL/"`;;
esac

if [ -n "$url" ]; then
  echo "<a href=\"$url\" target=\"_new\"><img src=\"images/info-i.gif\" alt=\"more information\" border=\"0\" align=\"right\"></a>"
fi
###echo $FORM_field,$file '<br>'
n=`echo $file | wc -w`
if [ $n != 1 ]; then
	echo "select: internal error: wrong value for file=$file<br>"
	. ./myvinkfoot.cgi
	exit
fi
./bin/describefield.sh $file
metadata=./metadata/`echo $file|tr '/' '.'`.txt
if [ -f $metadata.eval ]; then
  eval `cat $metadata.eval | egrep '(^NPERYEAR=|^VAR=|^UNITS=|^NEWUNITS=|^N.=)[-_" ^*/a-zA-Z0-9]*$'`
else
  eval `./bin/getunits.sh $file`
fi
if [ "$lwrite" = true ]; then
    echo "./bin/getunits.sh $file"
    ./bin/getunits.sh $file
    echo "NY=$NY<br>"
fi

if [ -n "$LSMASK" ]; then
  if [ -f "$LSMASK" ]; then
    echo "The associated land/sea mask is available for some operations"
  else
    echo "<font color='#ff4444'>Cannot locate the land/sea mask file</font>"
  fi
fi
if [ ${NZ:-1} -le 1 ]; then
	cat <<EOF
<p><form action="get_index.cgi" method="POST">
<div class="formheader">Get grid points, average area or generate subset</div>
<div class="formbody">
<table width="452" border=0 cellspacing=0 cellpadding=0>
<input type="hidden" name="email" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
EOF
	SHOWMASK=true
	. ./choose_coordinates.cgi
	cat <<EOF 
</table>
</div>
</form>
EOF
fi # NZ <= 1

if [ $NPERYEAR -gt 1 ]; then
    case $NPERYEAR in
	4) monthly=seasonally;;
	12) monthly=monthly;;
	36) monthly=decadal;;
	360|365|366) monthly=daily;;
	*) monthly=period;;
    esac
    cat <<EOF
<div class="formheader"><a href="javascript:pop_page('help/daily2longer.shtml',568,450)"><img src="images/info-i.gif" align="right" alt="help" border="0"></a>Apply $monthly high/low-pass filter</div>
<div class="formbody">
EOF
    . ./filtermonthform.cgi
    echo '</div>'
fi
cat <<EOF
<div class="formheader"><a href="javascript:pop_page('help/daily2longer.shtml',568,450)"><img src="images/info-i.gif" align="right" alt="help" border="0"></a>Apply year-on-year high/low-pass filter</div>
<div class="formbody">
EOF
. ./filteryearform.cgi
echo '</div>'

cat <<EOF
<form action="fielddaily2longer.cgi" method="POST">
<div class="formheader"><a href="javascript:pop_page('help/lowerresolutionfield.shtml',568,450)"><img src="images/info-i.gif" align="right" alt="help" border="0"></a>Create a field with lower time resolution</div>
<div class="formbody">
<table border=0 cellspacing=0 cellpadding=0>
<tr><td>
EOF
. $DIR/daily2longerform.cgi
cat <<EOF
<input type="submit" class="formbutton" value="Make new field">
<input type="hidden" name="field" value="$FORM_field">
</td></tr>
</table>
</div>
</form>
EOF

. ./getfieldtype.cgi
if [ "$field_type" = Pressure ]; then
  echo "<p><a href=\"geowind.cgi?id=$EMAIL&field=$FORM_field\">Compute geostrophic wind components from this field</a>"
fi

if [ -z "$ENSEMBLE" ]; then
  echo "<p><a href=\"statmodelform.cgi?id=$EMAIL&field=$FORM_field\">Construct a statistical forecast model from this field</a>"
fi

if [ "$field_type" = SST ]; then
  echo "<p><a href=\"hurricane.cgi?email=$EMAIL&field=$FORM_field\">Compute expected number of Atlantic hurricanes</a>"
fi

if [ -n "$ENSEMBLE" ]; then
  cat <<EOF
<p><div class="formheader">Compute ensemble mean</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>
<form action="averagefield_ensemble.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<input type="submit" class="formbutton" value="Average">
</form>
</td></tr>
</table>
</div>
EOF
fi

if [ -n "$NY" -a "$NY" != 1 ]; then
  cat <<EOF
<p><div class="formheader">Compute zonal mean</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>
<form action="zonalmean.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<!--
Longitude: 
</td><td>
<input type="$number" step=any class="forminput" name="lon1" $textsize4 value="$FORM_lon1">&deg;E -
<input type="$number" step=any class="forminput" name="lon2" $textsize4 value="$FORM_lon2">&deg;E
</td></tr><tr><td colspan="2">
-->
<input type="submit" class="formbutton" value="Average">
</form>
</td></tr>
</table>
</div>
EOF
fi

echo "<div class=\"alineakop\"><a name=\"download\">Download $kindname $climfield</a></div>"

###echo "FORM_field=$FORM_field<br>"
if [ ${FORM_field#had} != $FORM_field -o ${FORM_field#mohmat} != $FORM_field ]; then
  echo "(c) Crown copyright 2006, data supplied by the Met Office."
  echo "The UKMO license does not allow us to redistribute this file. "
  echo "Please consult their <a href="wipefeet.cgi?http://www.hadobs.org" target=\"_new\">website</a> for further information."
elif [ ${FORM_field#ukmo} != $FORM_field -o ${FORM_field#ens_ukmo} != $FORM_field ]; then
  echo "(c) Crown copyright 2006, data supplied by the Met Office."
  echo "The UKMO does not allow us to redistribute this file. "
  echo "Please consult their <a href="wipefeet.cgi?http://www.metoffice.gov.uk" target=\"_new\">website</a> for further information."
elif [ "${FORM_field#era}" != "${FORM_field}" -o "${FORM_field#ecmwf}" != "${FORM_field}" -o "${FORM_field#ens_ecmwf}" != "${FORM_field}" ]; then
  echo "The ECMWF member states do not permit us to give you access to the raw data."
  echo "Please consult the ECMWF <a href=\"http://www.ecmwf.int/research/era/\" target="_new">ERA</a> or <a href=\"http://www.ecmwf.int/services/seasonal/\" target="_new">seasonal forecasting</a> website for further information."
elif [ "${FORM_field#demeter}" != "${FORM_field}" -o "${FORM_field#ens_demeter}" != "${FORM_field}" ]; then
  echo "Please download the data from the ECMWF <a href=\"http://www.ecmwf.int/research/demeter/\" target="_new">DEMETER</a> website."
elif [ "${FORM_field#ensembles}" != "${FORM_field}" -o "${FORM_field#ens_demeter}" != "${FORM_field}" ]; then
  echo "Please download the data from the <a href=\"http://www.ecad.eu/download/ensembles/ensembles.php/\" target="_new">ENSEMBLES</a> website."
elif [ ${file#IPCCData} != $file -o ${file#ESSENCE} != $file ]; then
  model=`echo $FORM_field | sed -e 's/^[^_]*_//' -e 's/_[^_]*$//'`
  ###echo "model=$model<br>"
  case $model in
  bccr*) download=OK;;
  gfdl*) download=OK;;
  giss*) download=OK;;
  mpi*)  download=OK;;
  ncar*) download=OK;;
  ukmo*) download=OK;;
  essence*) download=OK;;
  *) download=OK
  echo "Downloading is only allowed for non-commercial use. "
  echo "Please consult the <a href=\"wipefeet.cgi?http://www-pcmdi.llnl.gov/ipcc/about_ipcc.php\" target=\"_new\">PCMDI website</a> for further information.<p>"
  ;;
  esac
elif [ "${FORM_field#rutgers}" != "${FORM_field}" ]; then
  echo "Rutgers University does not allow us to redistribute this file. "
  echo "Please contact <a href=\"wipefeet.cgi?http://climate.rutgers.edu/snowcover/docs.php?target=datareq\" target=\"_new\">Thomas Estilow</a> for access to these data."
elif [  "${FORM_field#cmip5_yr}" != "${FORM_field}" ]; then
    echo "Please download the CMIP5 fields from the <a href=\"http://www.cccma.ec.gc.ca/data/climdex/climdex.shtml\">CCCMA ETCCDI site</a>."
elif [  "${FORM_field#cmip5}" != "${FORM_field}" ]; then
    echo "Please download the CMIP5 fields from the Earth System Grid servers, eg at <a href=\"http://cmip-pcmdi.llnl.gov/cmip5/data_getting_started.html\">PCMDI</a>. Contact <a href="http://www.knmi.nl/~oldenbor/">me</a> if you need access via this site."
else
  download=OK
fi
###echo "download=$download<br>"
###echo "ENSEMBLE=$ENSEMBLE<br>"

if [ "$download" = OK ]; then
if [ -n "$ENSEMBLE" ]; then
  i=0
  c2=`echo $file | fgrep -c '%%'`
  if [ $c2 = 0 ]; then
    imax=1
  else
    c3=`echo $file | fgrep -c '%%%'`
    if [ $c3 = 0 ]; then
      imax=100
    else
      imax=1000
    fi
  fi
  while [ $i -lt $imax ]
  do
    if [ $i -lt 10 ]; then
      member=`echo $file | sed -e "s/%%%/00$i/" -e "s/%%/0$i/"`
    elif [ $i -lt 100 ]; then
      member=`echo $file | sed -e "s/%%%/0$i/" -e "s/%%/$i/"`
    else
      member=`echo $file | sed -e "s/%%%/$i/"`
    fi
    ###echo "member=$member<br>"
    if [ -f $member ]; then
      if [ ${member%nc} = $member ]; then
        datfile=`dirname $member`/`head -1 $member \
	    | sed -e 's/DSET *//' -e 's/dset *//' -e 's/\^//'`
	if [ ! -f $datfile ]; then
	  datfile=$datfile.gz
        fi
        echo "ensemble member $i: download <a href=\"$member\">ctl</a> and <a href=\"$datfile\">dat</a> files or <a href=\"grads2nc.cgi?file=$member&id=$EMAIL\">netcdf</a>,"
      else
        echo "ensemble member $i: download <a href=\"$member\">netcdf</a>,"
      fi
      echo "analyse <a href=\"selectmember.cgi?id=$EMAIL&i=$i&field=$FORM_field\">separately</a><br>"
    fi
    i=$(($i + 1))
  done
  ensemble_done=true
else
  if [ ${FORM_field#sos} = "$FORM_field" ]; then
    if [ -n "$url" ]; then
      echo "Please consider downloading this field from the <a href=\"$url\">authoritative site</a>."
      echo "<p>If you <i>really</i> want to get it here,"
    fi
  fi
  echo "$kindname $climfield is available as"
  ctlfile=`echo $file | sed -e s:$DIR/::`
  title=`echo "$kindname $climfield" | tr ' ' '_'`
  args="file=$file&id=$EMAIL&title=$title"
  if [ `echo $ctlfile | fgrep -c '.ctl'` = 1 ]; then
    ctldir=`dirname $file`
    datfile=`head -1 $file | sed -e 's/DSET //' -e 's/dset //' -e "s:\^:$ctldir/:" -e 's/ *$//'`
    echo "GrADS <a href=\"$ctlfile\">.ctl</a> and gzipped"
    if [ -f $datfile.gz ]; then
      echo "<a href=\"$datfile.gz\">.dat</a>"
      size=`ls -l $datfile.gz | awk '{print $5/1048576}'`
    else
      echo "<a href=\"getdat.cgi?file=$file\">.dat</a>"
      size=`ls -l $datfile | awk '{print $5/1048576}'`
    fi
    echo "files (size $size MB)<br>Alternatively, you can generate a gzipped <a href=\"grads2nc.cgi?$args\">netCDF</a> file of the same size."
  else
    size=`ls -l $file | awk '{print $5/1048576}'`
    echo "a <a href=\"$file\">netcdf file</a> (size $size MB)."
  fi
fi
fi
if [ -z "$ensemble_done" -a -n "$ENSEMBLE" ]; then
echo "<div class=\"alineakop\"><a name=\"members\"></a>Ensemble members</div>"
  i=0
  c2=`echo $file | fgrep -c '%%'`
  if [ $c2 = 0 ]; then
    nmax=1
  else
    c3=`echo $file | fgrep -c '%%%'`
    if [ $c3 = 0 ]; then
  	  nmax=100
    else
      nmax=1000
    fi
  fi
  while [ $i -lt $nmax ]
  do
    if [ $i -lt 10 ]; then
      member=`echo $file | sed -e "s/%%%/00$i/" -e "s/%%/0$i/"`
    elif [ $i -lt 100 ]; then
      member=`echo $file | sed -e "s/%%%/0$i/" -e "s/%%/$i/"`
    else
      member=`echo $file | sed -e "s/%%%/$i/"`
    fi
    if [ -f $member ]; then
      echo "analyse ensemble member $i <a href=\"selectmember.cgi?id=$EMAIL&i=$i&field=$FORM_field\">separately</a><br>"
    fi
    i=$((i + 1))
  done
fi

. ./myvinkfoot.cgi
