#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
if [ -z "$EMAIL" ]; then
  EMAIL=someone@somewhere
fi
if [ -z "$FORM_internal" ]; then
# only use saved preferences when the script is called without the hidden variable "internal"
  if [ "$EMAIL" != someone@somewhere ]; then
    def=./prefs/$EMAIL.forecastverification
    if [ -s $def ]; then
      eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9._]*;$' $def`
###      echo '<pre>'
###      egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9._]*;$' $def
###      echo '</pre>'
    fi
  fi
fi
# check email address
. ./checkemail.cgi

if [ "$EMAIL" != somene@somewhere ]; then
  pdef=./prefs/$EMAIL.plotoptions
  if [ -s $pdef ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $pdef`
    . ./getfieldopts.cgi
    map0=$map
  fi
fi
. ./myvinkhead.cgi "Seasonal forecast verification" "Monthly means" ""

if [ "$EMAIL" = someone@somewhere ]; then
  echo "If you <a href="registerform.cgi">register or log in</a> the form will remember its settings between sessions."
fi
cat << EOF
<form action="forecast_verification.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="internal" value="true">
<table class=realtable width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="2">Make you choices</th></tr>
EOF

###SYSTEM

case ${FORM_system:-choose} in
choose) choose_selected=selected;;
ecmwf2) ecmwf2_selected=selected;;
ecmwf3) ecmwf3_selected=selected;;
ecmwf4) ecmwf4_selected=selected;;
ukmo)   ukmo_selected=selected;;
cfs)    cfs_selected=selected;;
echam4.5) echam_selected=selected;;
demeter_meteofrance) demeter_meteofrance_selected=selected;;
demeter_cerfacs)     demeter_cerfacs_selected=selected;;
demeter_lodyc)       demeter_lodyc_selected=selected;;
demeter_ingv)        demeter_ingv_selected=selected;;
demeter_ecmwf)       demeter_ecmwf_selected=selected;;
demeter_mpi)         demeter_mpi_selected=selected;;
demeter_ukmo)        demeter_ukmo_selected=selected;;
demeter)             demeter_selected=selected;;
demeter3)            demeter3_selected=selected;;
*) echo "I know nothing about the seasonal forecast system $FORM_system, please choose another one"
   FORM_system=choose
   choose_selected=selected;;
esac
cat <<EOF
<tr><td width=100>Forecast system</td>
<td><select class="forminput" name="system" onchange="this.form.submit();">
<option value="choose" $choose_selected>choose a seasonal forecast system</option>
<option value="ecmwf4" $ecmwf4_selected>ECMWF S4</option>
<option value="ecmwf3" $ecmwf3_selected>ECMWF S3</option>
<option value="ecmwf2" $ecmwf2_selected>ECMWF S2</option>
<option value="ukmo" $ukmo_selected>UKMO GloSea</option>
<option value="cfs" $cfs_selected>NCEP CFS</option>
<option value="echam4.5" $echam_selected>IRI ECHAM4.5</option>
<option value="demeter_meteofrance" $demeter_meteofrance_selected>Demeter M&eacute;t&eacute;o France</option>
<option value="demeter_cerfacs" $demeter_cerfacs_selected>Demeter CERFACS</option>
<option value="demeter_lodyc" $demeter_lodyc_selected>Demeter LODYC</option>
<option value="demeter_ingv" $demeter_ingv_selected>Demeter INGV</option>
<option value="demeter_ecmwf" $demeter_ecmwf_selected>Demeter ECMWF</option>
<option value="demeter_mpi" $demeter_mpi_selected>Demeter MPI</option>
<option value="demeter_ukmo" $demeter_ukmo_selected>Demeter UKMO</option>
<option value="demeter" $demeter_selected>Demeter all</option>
<option value="demeter3" $demeter3_selected>Demeter MF+EC+UK</option>
</select>
EOF
if [ ${FORM_system:-choose} = choose ]; then
  echo "</td></tr><tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select system\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi
if [ $FORM_system = echam4.5 ]; then
  nmax=5
elif [ $FORM_system != cfs ]; then
  nmax=6
else
  nmax=9
fi

### NUMBER OF ENSEMBLE MEMBERS

FORM_field=ens_${FORM_system}_t2m_feb
. ./queryfield.cgi
###echo "file=$file<br>"
describefield=`./bin/describefield.sh $file`
###echo "describefield=$describefield<br>"
string=`echo $describefield | fgrep ensemble`
nens1=`echo $string | awk '{print $4}'`
nens2=`echo $string | awk '{print $6}'`
[ -z "$FORM_nens1" ] && FORM_nens1=$nens1
[ -z "$FORM_nens2" ] && FORM_nens2=$nens2
case ${FORM_ensemble:-all} in
custom) custom_checked=checked;;
*)      all_checked=checked;FORM_nens1=$nens1;FORM_nens2=$nens2;;
esac
echo "<br>Members <input type=radio class=formradio name=ensemble value=all $all_checked>all (${nens1}-${nens2})"
echo "<input type=radio class=formradio name=ensemble value=custom $custom_checked><select class=\"forminput\" name=\"nens1\">"
yrbeg=$nens1
yrend=$nens2
yr_selected[$FORM_nens1]="selected"
. ./make_year_list.cgi
echo "</select>"

echo " - <select class=\"forminput\" name=\"nens2\">"
yr_selected[$FORM_nens1]=""
yr_selected[$FORM_nens2]="selected"
. ./make_year_list.cgi
echo "</select></td></tr>"
yr_selected=""

###ANALYSIS DATE (Magdalena prefers "forecast initial conditions")
if [ "${FORM_system#demeter}" = $FORM_system ]; then
case ${FORM_analysis:-choose} in
choose) choose_selected=selected;;
jan) jan_selected=selected;;
feb) feb_selected=selected;;
mar) mar_selected=selected;;
apr) apr_selected=selected;;
may) may_selected=selected;;
jun) jun_selected=selected;;
jul) jul_selected=selected;;
aug) aug_selected=selected;;
sep) sep_selected=selected;;
oct) oct_selected=selected;;
nov) nov_selected=selected;;
dec) dec_selected=selected;;
*) echo "I know nothing about the analysis date $FORM_analysis, please choose another one"
   FORM_analysis=""
   choose_selected=selected;;
esac
else
case ${FORM_analysis:-choose} in
choose) choose_selected=selected;;
feb) feb_selected=selected;;
may) may_selected=selected;;
aug) aug_selected=selected;;
nov) nov_selected=selected;;
*) echo "Demeter does not contain forecasts started from $FORM_analysis, please choose another one"
   FORM_analysis=""
   choose_selected=selected;;
esac
fi

echo "<tr><td width=100>Forecast initial conditions</td>"
echo "<td><select class=\"forminput\" name=\"analysis\" onchange=\"this.form.submit();\">"
if [ "${FORM_system#demeter}" = $FORM_system ]; then
  cat <<EOF
<option value="choose" $choose_selected>choose the forecast starting date</option>
<option value="jan" $jan_selected>1 January</option>
<option value="feb" $feb_selected>1 February</option>
<option value="mar" $mar_selected>1 March</option>
<option value="apr" $apr_selected>1 April</option>
<option value="may" $may_selected>1 May</option>
<option value="jun" $jun_selected>1 June</option>
<option value="jul" $jul_selected>1 July</option>
<option value="aug" $aug_selected>1 August</option>
<option value="sep" $sep_selected>1 September</option>
<option value="oct" $oct_selected>1 October</option>
<option value="nov" $nov_selected>1 November</option>
<option value="dec" $dec_selected>1 December</option>
EOF
else
  cat <<EOF
<option value="choose" $choose_selected>choose the forecast starting date</option>
<option value="feb" $feb_selected>1 February</option>
<option value="may" $may_selected>1 May</option>
<option value="aug" $aug_selected>1 August</option>
<option value="nov" $nov_selected>1 November</option>
EOF
fi
echo "</select></td></tr>"
if [ ${FORM_analysis:-choose} = choose ]; then
  # save the rest
  echo "<input type=\"hidden\" name=\"var\" value=\"$FORM_var\">"
  echo "<input type=\"hidden\" name=\"field2\" value=\"$FORM_field2\">"
  echo "<input type=\"hidden\" name=\"debias\" value=\"$FORM_debias\">"
  echo "<input type=\"hidden\" name=\"detrend\" value=\"$FORM_detrend\">"
  echo "<input type=\"hidden\" name=\"sum\" value=\"$FORM_sum\">"
  echo "<input type=\"hidden\" name=\"month\" value=\"$FORM_month\">"
  echo "<input type=\"hidden\" name=\"period\" value=\"$FORM_period\">"
  echo "<input type=\"hidden\" name=\"begin\" value=\"$FORM_begin\">"
  echo "<input type=\"hidden\" name=\"end\" value=\"$FORM_end\">"
  echo "<input type=\"hidden\" name=\"region\" value=\"$FORM_region\">"
  echo "<input type=\"hidden\" name=\"lon1\" value=\"$FORM_lon1\">"
  echo "<input type=\"hidden\" name=\"lon2\" value=\"$FORM_lon2\">"
  echo "<input type=\"hidden\" name=\"lat1\" value=\"$FORM_lat1\">"
  echo "<input type=\"hidden\" name=\"masktype\" value=\"$FORM_masktype\">"
  echo "<input type=\"hidden\" name=\"verif\" value=\"$FORM_verif\">"
  echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
  echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
  echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select forecast initial conditions\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

###VARIABLE

case ${FORM_var:-choose} in
choose) choose_selected=selected;;
t2m)  t2m_selected=selected;;
t2n)  t2n_selected=selected;;
t2x)  t2x_selected=selected;;
tsfc) tsfc_selected=selected;;
prcp) prcp_selected=selected;;
msl)  msl_selected=selected;;
ssd)  ssd_selected=selected;;
snd)  snd_selected=selected;;
z500) z500_selected=selected;;
u10)  u10_selected=selected;;
v10)  v10_selected=selected;;
*) echo "I know nothing about the variable $FORM_var, please choose another one"
   FORM_var=""
   choose_selected=selected;;
esac
# does the combination system/variable exist?
if [ -n "$FORM_var" -a "$FORM_var" != "choose" ]; then
    if [ $FORM_system = ecmwf4 ]; then
        FORM_field=${FORM_system}_${FORM_var}_02
        . ./queryfield.cgi
        if [ -z "$file" ]; then
            echo "Sorry, variable $FORM_var is not available in the $FORM_system data.  Choose another one"
            FORM_var=""
        fi
        firstfile=`echo "$file" | tr '%' '0'`
        if [ ! -s "$firstfile" ]; then
            echo "Sorry, variable $FORM_var is not available in the $FORM_system data.  Choose another one"
            FORM_var=""
        fi
        firstfile=`echo "$file" | tr '%' '0'`
    else
        c=`fgrep -c ens_${FORM_system}_${FORM_var} queryfield.cgi`
        if [ $c = 0 ]; then
            echo "Sorry, variable $FORM_var is not available in the $FORM_system data.  Choose another one"
            FORM_var=""
        fi
    fi
fi
echo "<tr><td width=100>Variable</td>"
echo "<td><select class=\"forminput\" name=\"var\" onchange=\"this.form.submit();\">"
echo "<option value=\"choose\" $choose_selected>choose a variable</option>"
echo "<option value=\"t2m\" $t2m_selected>mean 2m temperature</option>"
if [ "${FORM_system#demeter}" = $FORM_system -a $FORM_system != echam4.5 ]; then
    echo "<option value=\"t2n\" $t2n_selected>minimum 2m temperature</option>"
    echo "<option value=\"t2x\" $t2x_selected>maximum 2m temperature</option>"
fi
echo "<option value=\"tsfc\" $tsfc_selected>SST/surface temperature</option>"
echo "<option value=\"prcp\" $prcp_selected>precipitation</option>"
if [ $FORM_system != echam4.5 ]; then
  echo "<option value=\"msl\" $msl_selected>sea-level pressure</option>"
fi
echo "<option value=\"z500\" $z500_selected>500hPa geopotential</option>"
if [ "${FORM_system#demeter}" = $FORM_system -a $FORM_system != echam4.5 ]; then
    echo "<option value=\"ssd\" $ssd_selected>downward solar radiation</option>"
    echo "<option value=\"snd\" $snd_selected>snow depth</option>"
fi
if [ $FORM_system = ecmwf2 -o $FORM_system = ecmwf3 -o "${FORM_system#demeter}" != $FORM_system ]; then
    echo "<option value=\"u10\" $u10_selected>zonal 10m wind</option>"
    echo "<option value=\"v10\" $v10_selected>meridional 10m wind</option>"
fi
echo "</select></td></tr>"
if [ ${FORM_var:-choose} = choose ]; then
  # save the rest
  echo "<input type=\"hidden\" name=\"field2\" value=\"$FORM_field2\">"
  echo "<input type=\"hidden\" name=\"debias\" value=\"$FORM_debias\">"
  echo "<input type=\"hidden\" name=\"detrend\" value=\"$FORM_detrend\">"
  echo "<input type=\"hidden\" name=\"sum\" value=\"$FORM_sum\">"
  echo "<input type=\"hidden\" name=\"month\" value=\"$FORM_month\">"
  echo "<input type=\"hidden\" name=\"period\" value=\"$FORM_period\">"
  echo "<input type=\"hidden\" name=\"begin\" value=\"$FORM_begin\">"
  echo "<input type=\"hidden\" name=\"end\" value=\"$FORM_end\">"
  echo "<input type=\"hidden\" name=\"region\" value=\"$FORM_region\">"
  echo "<input type=\"hidden\" name=\"lon1\" value=\"$FORM_lon1\">"
  echo "<input type=\"hidden\" name=\"lon2\" value=\"$FORM_lon2\">"
  echo "<input type=\"hidden\" name=\"lat1\" value=\"$FORM_lat1\">"
  echo "<input type=\"hidden\" name=\"masktype\" value=\"$FORM_masktype\">"
  echo "<input type=\"hidden\" name=\"verif\" value=\"$FORM_verif\">"
  echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
  echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
  echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select variable\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

###VERIFYING DATASET

VAR=$FORM_var
. ./getfieldtype.cgi
echo "<tr><td width=100>Observations</td>"
echo "<td><select class=\"forminput\" name=\"field2\" onchange=\"this.form.submit();\">"
tmpfile=/tmp/forecastverification$$
[ -f $tmpfile ] && rm $tmpfile
touch $tmpfile
for listfile in selectfield_obs.html selectfield_rea1.html
do
    if [ $listfile = selectfield_obs.html ]; then
	echo "<option> === Observations ===" >> $tmpfile
    else
	echo "<option> === Reanalyses ===" >> $tmpfile
    fi
# how about some horrible regexpes?
  fgrep "$field_type" $listfile \
  | sed -e "s/EMAIL/$EMAIL/" \
        -e '/>t.00</d' \
        -e '/>[uv]..0</d' \
        -e '/>z[^5].0</d' \
  | tr ',' '\n' \
  | sed -e 's/<!--[^-]*-->//g' \
        -e 's:</td><td><a.*$::' \
        -e 's:^<tr><td[^>]*>\(.*\)</td><td>\(.*\):\2 \1:' \
        -e 's/\([^<]*\)<input.*value=\([^>]*\)>\(.*\)/<option value=\2>\1\3/' \
        -e 's/> />\&nbsp;.../' \
        -e 's:$:</option>:' \
        -e "s/value=\"$FORM_field2\"/value=\"$FORM_field2\" selected/" \
  >> $tmpfile
done
c=`fgrep -c ${FORM_field2:-aapnootmies} $tmpfile`
if [ $c = 0 ]; then
  field2_choose_selected=selected
  FORM_field2=choose
fi
echo "<option value=\"choose\" $field2_choose_selected>Select a verifying field</option>"
cat $tmpfile
rm $tmpfile
echo "<option value=\"perfectmodel\">perfect model</option>"
echo "</select><br>"


### BIAS CORRECTION

if [ -n "$FORM_detrend" ]; then
  detrend_checked="checked"
fi

case ${FORM_debias:-mean} in
none) debias_none=selected;;
var)  debias_var=selected;;
all)  debias_all=selected;;
*)    debias_mean=selected;;
esac
echo "<select class=forminput name=debias>"
echo "<option value=none $debias_none>No bias correction</option>"
echo "<option value=mean $debias_mean>Correct for bias in mean</option>"
echo "<option value=var $debias_var>Correct for bias in mean and variance</option>"
echo "<option value=all $debias_all>Correct whole PDF</option>"
echo "</select>"
echo "<input type=checkbox class=formcheck name=detrend $detrend_checked>Detrend"
# always demand the same number of (repeated) observations fro each time step
echo "<input type=hidden name=makeensfull value=on>"
echo "</td></tr>"

if [ ${FORM_field2:-choose} = choose ]; then
  # save the rest
  echo "<input type=\"hidden\" name=\"sum\" value=\"$FORM_sum\">"
  echo "<input type=\"hidden\" name=\"month\" value=\"$FORM_month\">"
  echo "<input type=\"hidden\" name=\"period\" value=\"$FORM_period\">"
  echo "<input type=\"hidden\" name=\"begin\" value=\"$FORM_begin\">"
  echo "<input type=\"hidden\" name=\"end\" value=\"$FORM_end\">"
  echo "<input type=\"hidden\" name=\"region\" value=\"$FORM_region\">"
  echo "<input type=\"hidden\" name=\"lon1\" value=\"$FORM_lon1\">"
  echo "<input type=\"hidden\" name=\"lon2\" value=\"$FORM_lon2\">"
  echo "<input type=\"hidden\" name=\"lat1\" value=\"$FORM_lat1\">"
  echo "<input type=\"hidden\" name=\"masktype\" value=\"$FORM_masktype\">"
  echo "<input type=\"hidden\" name=\"verif\" value=\"$FORM_verif\">"
  echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
  echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
  echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select verifying $field_type field\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi
# does the combination system/variable/analysis exist?
if [ -n "$analysis" -a "$analysis" != "choose" ]; then
  c=`fgrep -c ens_${FORM_system}_${var}_${FORM_analysis} queryfield.cgi`
  if [ $c = 0 ]; then
    echo "Sorry, the combination of variable $FORM_var with starting date $FORM_analysis is not available in the $FORM_system data.  Choose another one"
    FORM_analysis=""
    analysis=""
  fi
fi

###SEASON

case ${FORM_sum:-choose} in
choose) sum_choose_selected="selected";;
1) sum_1_selected="selected";;
2) sum_2_selected="selected";;
3) sum_3_selected="selected";;
4) sum_4_selected="selected";;
5) sum_5_selected="selected";;
6) sum_6_selected="selected";;
7) sum_7_selected="selected";;
8) sum_8_selected="selected";;
9) sum_9_selected="selected";;
*) echo "The length of the season should be less than 10 months, not $FORM_sum, please choose another one"
   FORM_sum=""
   sum_choose_selected="selected";;
esac
if [ "${FORM_sum:-0}" -gt $nmax ]; then
  echo "$FORM_system forecasts only go out to $nmax months"
  FORM_sum=choose
  sum_choose_selected="selected"
fi
case ${FORM_month:-choose} in
choose) month_choose_selected="selected";;
1) month_1_selected="selected";;
2) month_2_selected="selected";;
3) month_3_selected="selected";;
4) month_4_selected="selected";;
5) month_5_selected="selected";;
6) month_6_selected="selected";;
7) month_7_selected="selected";;
8) month_8_selected="selected";;
9) month_9_selected="selected";;
10) month_10_selected="selected";;
11) month_11_selected="selected";;
12) month_12_selected="selected";;
*) echo "The starting month should be in the range 1-12, not $FORM_month, please choose another one"
   FORM_month=""
   month_choose_selected=selected;;
esac

case "$FORM_analysis" in
jan) analysis=1;;
feb) analysis=2;;
mar) analysis=3;;
apr) analysis=4;;
may) analysis=5;;
jun) analysis=6;;
jul) analysis=7;;
aug) analysis=8;;
sep) analysis=9;;
oct) analysis=10;;
nov) analysis=11;;
dec) analysis=12;;
*) echo "Internal error: FORM_analysis = $FORM_analysis"
   exit
esac
if [ ${FORM_sum:-choose} != choose -a ${FORM_month:-choose} != choose ]; then
  n1=$(($FORM_month - $FORM_analysis))
  if [ $n1 -lt 1 ]; then
    n1=$(($n1 + 12))
  fi
  n1=$(($n2 + $FORM_sum))
  if [ $n1 -gt $nmax ]; then
    echo "The verification season of $FORM_sum months from month $FORM_month is not contained in the ${nmax}-month forecasts from $FORM_analysis of system $FORM_system."
    FORM_month=choose
  fi
fi

echo "<tr><td width=100>Verification season</td>"
echo "<td><select class=\"forminput\" name=\"sum\" onchange=\"this.form.submit();\">"
echo "<option $sum_choose_selected>choose</option>"
echo "<option $sum_1_selected>1</option>"
echo "<option $sum_2_selected>2</option>"
echo "<option $sum_3_selected>3</option>"
echo "<option $sum_4_selected>4</option>"
echo "<option $sum_5_selected>5</option>"
if [ $FORM_system != echam4.5 ]; then
  echo "<option $sum_6_selected>6</option>"
  if [ $FORM_system = cfs ]; then
    echo "<option $sum_7_selected>7</option>"
    echo "<option $sum_8_selected>8</option>"
    echo "<option $sum_9_selected>9</option>"
  fi
fi
echo "</select>-month season starting in"

if [ ${FORM_sum:-choose} != choose ]; then
  length=$(($nmax - $FORM_sum + 1))
else
  length=$nmax
fi
month=$analysis
while [ $month -lt $(($analysis + $length)) ]; do
  m=$month
  if [ $m -gt 12 ]; then
    m=$(($m - 12))
  fi
  month_possible[$m]="possible"
  month=$(($month + 1))
done
if [ "${month_possible[$FORM_month]}" != possible ]; then
  FORM_month=choose
  month_choose_selected=selected
fi

echo "<select class=\"forminput\" name=\"month\" onchange=\"this.form.submit();\">"
echo "<option value=\"choose\" $month_choose_selected>choose month</option>"
[ -n "${month_possible[1]}" ] && echo "<option value=\"1\" $month_1_selected>January</option>"
[ -n "${month_possible[2]}" ] && echo "<option value=\"2\" $month_2_selected>February</option>"
[ -n "${month_possible[3]}" ] && echo "<option value=\"3\" $month_3_selected>March</option>"
[ -n "${month_possible[4]}" ] && echo "<option value=\"4\" $month_4_selected>April</option>"
[ -n "${month_possible[5]}" ] && echo "<option value=\"5\" $month_5_selected>May</option>"
[ -n "${month_possible[6]}" ] && echo "<option value=\"6\" $month_6_selected>June</option>"
[ -n "${month_possible[7]}" ] && echo "<option value=\"7\" $month_7_selected>July</option>"
[ -n "${month_possible[8]}" ] && echo "<option value=\"8\" $month_8_selected>August</option>"
[ -n "${month_possible[9]}" ] && echo "<option value=\"9\" $month_9_selected>September</option>"
[ -n "${month_possible[10]}" ] && echo "<option value=\"10\" $month_10_selected>October</option>"
[ -n "${month_possible[11]}" ] && echo "<option value=\"11\" $month_11_selected>November</option>"
[ -n "${month_possible[12]}" ] && echo "<option value=\"12\" $month_12_selected>December</option>"
echo "</select></td></tr>"
if [ ${FORM_sum:-choose} = choose -o ${FORM_month:-choose} = choose ]; then
  # save the rest
  echo "<input type=\"hidden\" name=\"period\" value=\"$FORM_period\">"
  echo "<input type=\"hidden\" name=\"begin\" value=\"$FORM_begin\">"
  echo "<input type=\"hidden\" name=\"end\" value=\"$FORM_end\">"
  echo "<input type=\"hidden\" name=\"region\" value=\"$FORM_region\">"
  echo "<input type=\"hidden\" name=\"lon1\" value=\"$FORM_lon1\">"
  echo "<input type=\"hidden\" name=\"lon2\" value=\"$FORM_lon2\">"
  echo "<input type=\"hidden\" name=\"lat1\" value=\"$FORM_lat1\">"
  echo "<input type=\"hidden\" name=\"masktype\" value=\"$FORM_masktype\">"
  echo "<input type=\"hidden\" name=\"verif\" value=\"$FORM_verif\">"
  echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
  echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
  echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select verification season\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

###PERIOD

FORM_field=$FORM_field2
###echo "DEBUG: calling queryfield with $FORM_field"
. ./queryfield.cgi
. ./get_begin_end_field.cgi
field2=$FORM_field2
file2=$file
kindname2=$kindname
climfield2=$climfield
map2=$map
flipcolor2=$flipcolor
yrbeg2=$yrbeg
mobeg2=$mobeg
yrend2=$yrend
moend2=$moend

FORM_field=ens_${FORM_system}_${FORM_var}_${FORM_analysis}
###echo "DEBUG: calling queryfield with $FORM_field"
. ./queryfield.cgi
eval `bin/getunits.sh $file`
. ./get_begin_end_field.cgi
field1=$FORM_field
file1=$file
kindname1=$kindname
climfield1=$climfield
map1=$map
flipcolor1=$flipcolor
yrbeg1=$yrbeg
mobeg1=$mobeg
yrend1=$yrend
moend1=$moend

# horrible computations, I hope they are correct

yr1=$yrbeg1
if [ $yr1 = $yrbeg1 -a $FORM_month -lt $mobeg1 ]; then
  yr1=$(($yr1 + 1))
fi
if [ $yr1 -lt $yrbeg2 ]; then
  yr1=$yrbeg2
fi
if [ $yr1 = $yrbeg2 -a $FORM_month -lt $mobeg2 ]; then
  yr1=$(($yr1 + 1))
fi
if [ ${FORM_begin:-1} -lt $yr1 ]; then
  FORM_begin=$yr1
fi

end=$(($FORM_month + $FORM_sum - 1))
yr2=$yrend1
if [ $yr2 = $yrend1 -a $end -gt $moend1 ]; then
  yr2=$(($yr2 - 1))
fi
if [ $yr2 -gt $yrend2 ]; then
  yr2=$yrend2
fi
if [ $yr2 = $yrend2 -a $end -gt $moend2 ]; then
  yr2=$(($yr2 - 1))
fi
if [ ${FORM_end:-999999} -gt $yr2 -o ${FORM_end:-1} -lt $yr1 ]; then
  FORM_end=$yr2
fi

# make sure the default is to change the period with the dataset

case ${FORM_period:-all} in
custom) custom_checked=checked;;
*)      all_checked=checked;;
esac

##echo "DEBUG: mobeg1,yrbeg1,moend1,yrend1=$mobeg1,$yrbeg1,$moend1,$yrend1"
##echo "DEBUG: mobeg2,yrbeg2,moend2,yrend2=$mobeg2,$yrbeg2,$moend2,$yrend2"
##echo "DEBUG: FORM_begin,FORM_end=$FORM_begin,$FORM_end."
echo "<tr><td width=100>Verification period</td>"
echo "<td><input type=radio class=formradio name=period value=all $all_checked>all (${yr1}-${yr2})"
echo "<input type=radio class=formradio name=period value=custom $custom_checked><select class=\"forminput\" name=\"begin\">"
# the user can select years for there are observations but no forecasts
yrbeg=$yrbeg2
yrend=$yrend2
yr_selected[$FORM_begin]="selected"
. ./make_year_list.cgi
echo "</select>"

echo " - <select class=\"forminput\" name=\"end\" onchange=\"this.form.submit();\">"
yr_selected[$FORM_begin]=""
yr_selected[$FORM_end]="selected"
. ./make_year_list.cgi
echo "</select></td></tr>"

###AREA

case ${FORM_region:-World} in
World)      world_selected=selected
	    FORM_lon1=-180;FORM_lon2=180;FORM_lat1=-90;FORM_lat2=90;;
World1)     world1_selected=selected
	    FORM_lon1=-300;FORM_lon2=60;FORM_lat1=-90;FORM_lat2=90;;
World2)     world2_selected=selected
	    FORM_lon1=-30;FORM_lon2=330;FORM_lat1=-90;FORM_lat2=90;;
World3)     world3_selected=selected
	    FORM_lat1=30;FORM_lat2=390;FORM_lat1=-90;FORM_lat2=90;;
Europe)     europe_selected=selected
            FORM_lon1=-30;FORM_lon2=50;FORM_lat1=30;FORM_lat2=75;;
N.America)  namerica_selected=selected
            FORM_lon1=-170;FORM_lon2=-30;FORM_lat1=0;FORM_lat2=80;;
S.America)  samerica_selected=selected
            FORM_lon1=-90;FORM_lon2=-30;FORM_lat1=-60;FORM_lat2=20;;
Africa)     africa_selected=selected
            FORM_lon1=-20;FORM_lon2=60;FORM_lat1=-40;FORM_lat2=40;;
Asia)       asia_selected=selected
            FORM_lon1=20;FORM_lon2=190;FORM_lat1=-10;FORM_lat2=80;;
S.Asia)     sasia_selected=selected
            FORM_lon1=60;FORM_lon2=100;FORM_lat1=5;FORM_lat2=40;;
E.Asia)     easia_selected=selected
            FORM_lon1=90;FORM_lon2=150;FORM_lat1=15;FORM_lat2=55;;
SE.Asia)    seasia_selected=selected
            FORM_lon1=90;FORM_lon2=150;FORM_lat1=-20;FORM_lat2=20;;
Australia)  australia_selected=selected
            FORM_lon1=110;FORM_lon2=160;FORM_lat1=-45;FORM_lat2=-10;;
Antarctica) antarctica_selected=selected
            FORM_lon1=-180;FORM_lon2=180;FORM_lat1=-90;FORM_lat2=-60;;
Atlantic)   atlantic_selected=selected
            FORM_lon1=-100;FORM_lon2=30;FORM_lat1=-80;FORM_lat2=80;;
Pacific)    pacific_selected=selected
            FORM_lon1=90;FORM_lon2=300;FORM_lat1=-80;FORM_lat2=80;;
Indian)     indian_selected=selected
            FORM_lon1=20;FORM_lon2=140;FORM_lat1=-70;FORM_lat2=30;;
Arctic)     arctic_selected=selected
            FORM_lon1=-180;FORM_lon2=180;FORM_lat1=65;FORM_lat2=90;;

Custom)     custom_selected=selected;;
*)          world_selected=selected
            FORM_region=World
            FORM_lon1=-180;FORM_lon2=180;FORM_lat1=-90;FORM_lat2=90;;
esac

case ${masktype:-all} in
land) land_selected="selected";;
5sea) sea5_selected="selected";;
5lan) lan5_selected="selected";;
sea)  sea_selected="selected";;
notl) notl_selected="selected";;
nots) nots_selected="selected";;
*)    all_selected="selected";;
esac

cat <<EOF
<tr><td width=100>Area</td>
<td><select class="forminput" name="region" onchange="this.form.submit();">
<option $custom_selected>Custom</option>
<option value="World" $world_selected>World (Europe-Africa centered)</option>
<option value="World1" $world1_selected>World (America centered)</option>
<option value="World2" $world2_selected>World (Asia centered)</option>
<option value="World3" $world3_selected>World (Oceans)</option>
<option $europe_selected>Europe</option>
<option $namerica_selected>N.America</option>
<option $samerica_selected>S.America</option>
<option $africa_selected>Africa</option>
<option $asia_selected>Asia</option>
<option $sasia_selected>S.Asia</option>
<option $easia_selected>E.Asia</option>
<option $seasia_selected>SE.Asia</option>
<option $australia_selected>Australia</option>
<option $antarctica_selected>Antarctica</option>
<option $atlantic_selected>Atlantic</option>
<option $pacific_selected>Pacific</option>
<option $indian_selected>Indian</option>
<option $arctic_selected>Arctic</option>
</select>
EOF
if [ "${FORM_region}" = Custom ]; then
  cat <<EOF
<br><input type="$number" step=any class="forminput" name="lat1" value="${FORM_lat1:--90}" $textsize4>&deg;N
 - <input type="$number" step=any class="forminput" name="lat2" value="${FORM_lat2:-90}" $textsize4>&deg;N, 
<input type="$number" step=any class="forminput" name="lon1" value="${FORM_lon1:--180}" $textsize4>&deg;E
 - <input type="$number" step=any class="forminput" name="lon2" value="${FORM_lon2:-180}" $textsize4>&deg;E
EOF
fi
# not yet ready
#cat <<EOF
#<br><select class="forminput" name="masktype">
#<option "all"  "$all_selected">all points</option>
#<option "land" "$land_selected">land points only</option>
#<option "sea"  "$sea_selected">sea points only</option>
#</select></td></tr>
#EOF

###MEASURE

case "$FORM_verif" in
mapcorr)        selected_mapcorr="selected";;
mapdiscmean)    selected_mapdiscmean="selected";;
maprmse)        selected_maprmse="selected";;
mapmae)         selected_mapmae="selected";;
mapbrier)       selected_mapbrier="selected";;
mapbriar)       selected_mapbriar="selected";;
mapresolution)    selected_mapresolution="selected";;
mapreliability) selected_mapreliability="selected";;
mapuncertainty) selected_mapuncertainty="selected";;
mapbss)         selected_mapbss="selected";;
maprps)         selected_maprps="selected";;
maprpss)        selected_maprpss="selected";;
maprpss5)       selected_maprpss5="selected";;
maprps3)        selected_maprps3="selected";;
maprps5)        selected_maprps5="selected";;
maprocarea)     selected_maprocarea="selected";;
maproc)         selected_maproc="selected";;
maprocdeb)      selected_maprocdeb="selected";;
mapdebug)       selected_mapdebug="selected";;
likelihood)    selected_likelihood="selected";;
deterministic) selected_deterministic="selected";;
brierscore)    selected_brierscore="selected";;
fairbrierscore)   selected_fairbrierscore="selected";;
fairCRPSanalysis) selected_fairCRPSanalysis="selected";;
rankhistogram)    selected_rankhistogram="selected";;
reliability)   selected_reliability="selected";;
rps)           selected_rps="selected";;
rocrclim)      selected_rocrclim="selected";;
rocprob)       selected_rocprob="selected";;
rocdeb)        selected_rocdeb="selected";;
rocthreshold)  selected_rocthreshold="selected";;
debug)         selected_debug="selected";;
*)             selected_choose="selected";FORM_verif=choose;;
esac

cat <<EOF
<tr><td width=100>Measure</td>
<td><select class="forminput" name="verif" onchange="this.form.submit();">
<option value="choose" $selected_choose>== Select a measure to get a map</option>
<option value="mapcorr" $selected_mapcorr>Correlation of the ensemble mean</option>
<option value="mapdiscmean" $selected_mapdiscmean>Discrimination of the ensemble mean</option>
<option value="maprmse" $selected_maprmse>RMSE of the ensemble mean</option>
<option value="mapmae" $selected_mapmae>MAE of the ensemble mean</option>

<option value="mapbrier" $selected_mapbrier>Brier score</option>
<option value="mapresolution" $selected_mapresolution>&nbsp;Resolution</option>
<option value="mapreliability" $selected_mapreliability>&nbsp;Reliability</option>
<option value="mapuncertainty" $selected_mapuncertainty>&nbsp;Uncertainty</option>
<option value="mapbss" $selected_mapbss>BSS wrt climatology</option>
<option value="maprps" $selected_maprps>Tercile RPS</option>
<option value="maprpss" $selected_maprpss>Tercile RPSS wrt climatology, 
<option value="maprpss5" $selected_maprpss5>Quintile RPSS wrt climatology</option>
<option value="maproc" $selected_maproc>Area under the ROC curve</option>

<option value="mapdebug" $selected_mapdebug>Compute the observations/forecasts netcdf</option>
<option value="choose">== Select a measure for grid points</option>
<option value="likelihood" $selected_likelihood>Plot likelihood </option>
<option value="deterministic" $selected_deterministic>Deterministic scores
 for the ensemble mean</option>
<option value="brierscore" $selected_brierscore>Brier score</option>
<option value="fairbrierscore" $selected_fairbrierscore>Fair Brier score</option>
<option value="fairCRPSanalysis" $selected_fairCRPSanalysis>Fair CRPS analysis</option>
<option value="rankhistogram" $selected_rankhistogram>Rank histogram analysis</option>
<option value="reliability" $selected_reliability>Reliability diagram</option>
<option value="rps" $selected_rps>Ranked Probability Score for terciles</option>
<option value="rocprob" $selected_rocprob>ROC curve for members below threshold
<option value="rocthreshold" $selected_rocthreshold>ROC curve varying the model threshold</option>
<option value="debug" $selected_debug>Compute the observations/forecasts table</option>
</select>
EOF
if [ "${FORM_verif#mapbss}" != $FORM_verif -o "${FORM_verif#maprpss}" != $FORM_verif ]; then
echo '<br>The BSS and RPSS include a <a href="http://www.meteoschweiz.ch/nccr/weigel/weigel_brier_rpss_MWR2006.pdf">bias correction</a> for finite ensemble size'
fi
if [ ${FORM_verif:-choose} = choose ]; then
  # save the rest
  echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
  echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
  echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  echo "<tr><td colspan="2"><input type=\"submit\" class=\"formbutton\" value=\"Select verification measure\"></td></tr>"
  echo "</table></form>"
  . ./myvinkfoot.cgi
  exit
fi

### Threshold

###echo "DEBUG: FORM_verif=$FORM_verif."
case $FORM_verif in
mapbrier|mapresolution|mapreliability|mapuncertainty|mapbss|maproc) needs_threshold=true;;
brierscore|fairbrierscore|fairCRPSanalysis|reliability|rocprob|rocthreshold) needs_threshold=true;;
*) needs_threshold="";;
esac
if [ "$needs_threshold" = true ]; then
  case $FORM_threshold_type in
  TRUE) checked_threshold_type_true="selected";;
  *) checked_threshold_type_false="selected";;
  esac

  cat <<EOF
<br>Threshold
<input type="$number" step=any $textsize4 name="threshold" value="${FORM_threshold:-50}">
<select name="threshold_type">
<option value="FALSE" $checked_threshold_type_false>%</option>
<option value="TRUE" $checked_threshold_type_true>${NEWUNITS:-absolute}</option></select>
EOF
if [ "$FORM_verif" = reliability ]; then
  echo " with  <input type=\"$number\" $textsize4 name=\"nbins\" value=\"${FORM_nbins:-10}\"> bins"
fi
echo '</td></tr>'
else
  if [ -n "$FORM_threshold" ]; then
    echo "<input type=\"hidden\" name=\"threshold\" value=\"$FORM_threshold\">"
    echo "<input type=\"hidden\" name=\"threshold_type\" value=\"$FORM_threshold_type\">"
    echo "<input type=\"hidden\" name=\"nbins\" value=\"$FORM_nbins\">"
  fi
fi
echo "</td></tr>"
if [ "$FORM_verif#map" != "$FORM_verif" ]; then
  tocompute=map
elif [ "$FORM_verif#roc" != "$FORM_verif" ]; then
  tocompute="ROC curve"
elif [ "$FORM_verif" = reliability ]; then
  tocompute=diagram
elif [ "$FORM_verif#map" = likelihood ]; then
  tocompute="scatterplot"
fi
echo "<tr><td colspan=\"2\"><input type=\"submit\" class=\"formbutton\" value=\"Compute map\"></td></tr>"
if [ -z "$FORM_doit" -o \( -n "$needs_threshold" -a -z "$FORM_threshold" \) ]; then
  # do not autmatically recompute when the user changes one value,
  # but only compute things when the form ends here.
  # this leaves the problem when two things are changed with onchange-submit...
  echo "<input type=\"hidden\" name=\"doit\" value=\"true\">"
  echo '</table></form>'
  . ./myvinkfoot.cgi
  exit
fi
echo '</table></form>'

# save choices on disk
if [ $EMAIL != someone@somewhere ]; then
    . ./save_commonoptions.cgi
    def=./prefs/$EMAIL.forecastverification
    cat > $def << EOF
FORM_system=$FORM_system;
FORM_ensemble=$FORM_ensemble;
FORM_nens1=$FORM_nens1;
FORM_analysis=$FORM_analysis;
FORM_var=$FORM_var;
FORM_field2=$FORM_field2;
FORM_debias=$FORM_debias;
FORM_detrend=$FORM_detrend;
FORM_sum=$FORM_sum;
FORM_month=$FORM_month;
FORM_period=$FORM_period;
FORM_begin=$FORM_begin;
FORM_end=$FORM_end;
FORM_region=$FORM_region;
FORM_lon1=$FORM_lon1;
FORM_lon2=$FORM_lon2;
FORM_lat1=$FORM_lat1;
FORM_lat2=$FORM_lat2;
FORM_masktype=$FORM_masktype;
FORM_verif=$FORM_verif;
FORM_threshold_type=$FORM_threshold_type;
FORM_threshold=$FORM_threshold;
FORM_nbins=$FORM_nbins
EOF
fi

###CONTOURS, LABELS

FORM_fcstname="${kindname1#ens } $climfield1"
if [ ${FORM_verif#map} != $FORM_verif ]; then
  # prescibe contour levels in case of bounded variables
  # these can be overruled on the next page
  case "$FORM_verif" in
  mapcorr)        FORM_cmin=-1;FORM_cmax=1;FORM_colourscale=0;;
  mapdiscmean)    FORM_cmin=0;FORM_cmax=1;FORM_colourscale=0;;
  maprmse)        FORM_colourscale=3;;
  mapmae)         FORM_colourscale=3;;
  mapbrier)       FORM_colourscale=3;;
  mapbriar)       FORM_colourscale=3;;
  mapresolution)  FORM_colourscale=3;;
  mapreliability) FORM_colourscale=3;;
  mapuncertainty) FORM_colourscale=3;;
  mapbss)         FORM_cmin=-0.5;FORM_cmax=0.5;FORM_colourscale=0;;
  maprps)         FORM_colourscale=3;;
  maprps3)        FORM_colourscale=3;;
  maprps5)        FORM_colourscale=3;;
  maprpss)        FORM_cmin=-1;FORM_cmax=1;FORM_colourscale=0;;
  maprpss5)       FORM_cmin=-1;FORM_cmax=1;FORM_colourscale=0;;
  maprocarea)     FORM_cmin=0;FORM_cmax=1;FORM_colourscale=0;;
  maproc)         FORM_cmin=0;FORM_cmax=1;FORM_colourscale=0;;
  maprocdeb)      FORM_cmin=0;FORM_cmax=1;FORM_colourscale=0;;
  esac
  if [ -z "$FORM_shadingtype" ]; then
    FORM_shadingtype="shaded"
  fi
fi

###THE REST IS THE SAME AS THE OLD ROUTE

. ./regionverification.cgi
