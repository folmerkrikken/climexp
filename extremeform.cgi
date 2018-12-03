#!/bin/bash
# form with options for extremeseries.cgi

if [ "$EMAIL" != someone@somewhere ]; then
  if [ -n "$DIR" ]; then
    def=$DIR/prefs/$EMAIL.extremeoptions.$NPERYEAR
  else
    def=prefs/$EMAIL.extremeoptions.$NPERYEAR
  fi
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
  fi
fi

if [ -n "$FORM_nperyearnew" ]; then
  case $FORM_nperyearnew in
  -1) sel_annual_shifted="selected";;
  1) sel_annual="selected";;
  4) sel_seasonal="selected";;
  12) sel_monthly="selected";;
  36) sel_10daily="selected";;
  72) sel_5daily="selected";;
  360|365|366) sel_daily="selected";;
  esac
else
  sel_annual="selected"
fi

cat <<EOF
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<tr><td>Time scale:</td><td>
<select class="forminput" name="nperyearnew">
<!-- <option value="-1" $sel_annual_shifted>annual (Jul-Jun)</option> -->
<option value="1" $sel_annual>annual (Jan-Dec)</option>
<option value="4" $sel_seasonal>seasonal</option>
<option value="12" $sel_monthly>monthly</option>
</select>
</td></tr><tr><td>
Index:
</td><td>
EOF

###echo "VAR=$VAR<br>"
###echo "NAME=$NAME<br>"
###echo "NEWUNITS=$NEWUNITS<br>"
###echo "c1="`echo "$VAR" | fgrep -c max`"<br>"
###echo "c2="`echo "$NAME" | fgrep -c max`"<br>"
if [ "$NEWUNITS" = "Celsius" -a \( "$VAR" = tx -o `echo "$VAR" | fgrep -c max` != 0 -o `echo "$NAME" | fgrep -c max` != 0 \) ]; then
	climdex_type=tx
	case "${FORM_climdex_tx}" in
		SU)		climdex_tx_SU="selected";;
		CSU)	climdex_tx_CSU="selected";;
		ID)		climdex_tx_ID="selected";;
		TXx)	climdex_tx_TXx="selected";;
		TXn)	climdex_tx_TXn="selected";;
		TX10p)	climdex_tx_TX10p="selected";;
		TX90p)	climdex_tx_TX90p="selected";;
		WSDI)	climdex_tx_WSDI="selected";;
		*)      climdex_tx_none="selected";;
	esac

	cat <<EOF
<select class="forminput" name="climdex_tx">
<option value="none" $climdex_tx_none>select an extreme index
<option value="SU" $climdex_tx_SU>Summer days (TX > 25&deg;C)
<option value="CSU" $climdex_tx_CSU>Maximum number of consecutive summer days
<option value="ID" $climdex_tx_ID>Ice days (TX < 0&deg;C)
<option value="TXx" $climdex_tx_TXx>Maximum value of daily maximum temperature
<option value="TXn" $climdex_tx_TXn>Minimum value of daily maximum temperature
<option value="TX10p" $climdex_tx_TX10p>Days with TX < 10% of daily max temp (cold day-times)
<option value="TX90p" $climdex_tx_TX90p>Days with TX > 90% of daily max temp (warm day-times)
<option value="WSDI" $climdex_tx_WSDI>Warm-spell duration index
<option value="other" $climdex_tx_other>(other indices to be implemented soon)
EOF

elif [ "$NEWUNITS" = "Celsius" -a \( "$VAR" = tn -o `echo "$VAR" | fgrep -c min` != 0 -o `echo "$NAME" | fgrep -c min` != 0 \) ]; then
	climdex_type=tn
	case "${FORM_climdex_tn}" in
		FD)		climdex_tn_FD="selected";;
		CFD)	climdex_tn_CFD="selected";;
		TR)		climdex_tn_TR="selected";;
		TNx)	climdex_tn_TNx="selected";;
		TNn)	climdex_tn_TNn="selected";;
		TN10p)	climdex_tn_TN10p="selected";;
		TN90p)	climdex_tn_TN90p="selected";;
		CSDI)	climdex_tn_CSDI="selected";;
		*)      climdex_tn_none="selected";;
	esac

	cat <<EOF
<select class="forminput" name="climdex_tn">
<option value="none" $climdex_tn_none>select an extreme index
<option value="FD" $climdex_tn_FD>Frost days (TN < 0&deg;C)
<option value="CFD" $climdex_tn_CFD>Maximum number of consecutive frost days
<option value="TR" $climdex_tn_TR>Tropical nights (TN > 20&deg;C)
<option value="TNx" $climdex_tn_TNx>Maximum value of daily minimum temperature
<option value="TNn" $climdex_tn_TNn>Minimum value of daily minimum temperature
<option value="TN10p" $climdex_tn_TN10p>Days with TN < 10% of daily min temp (cold nights)
<option value="TN90p" $climdex_tn_TN90p>Days with TN > 90% of daily min temp (warm nights)
<option value="CSDI" $climdex_tn_CSDI>Cold-spell duration index
<option value="other" $climdex_tn_other>(other indices to be implemented soon)
EOF

elif [ "$NEWUNITS" = "Celsius" ]; then
	climdex_type=tg
	case "${FORM_climdex_tg}" in
		GSL)	climdex_tg_GSL="selected";;
		GD4)	climdex_tg_GD4="selected";;
		HD17)	climdex_tg_HD17="selected";;
		*)      climdex_tg_none="selected";;
	esac

	cat <<EOF
<select class="forminput" name="climdex_tg">
<option value="none" $climdex_tg_none>select an extreme index
<option value="GSL" $climdex_tg_GSL>Growing season length
<option value="GD4" $climdex_tg_GD4>Growing degree days (sum of TG > 4&deg;C)
<option value="HD17" $climdex_tg_HD17>Heating degree days (sum of 17&deg;C - TG)
EOF

elif [ "$NEWUNITS" = "mm/day" ]; then
	climdex_type=rr
	case "${FORM_climdex_rr}" in
		RX1day)	climdex_rr_RX1day="selected";;
		RX5day)	climdex_rr_RX5day="selected";;
		SDII)	climdex_rr_SDII="selected";;
		SDIInn)	climdex_rr_SDIInn="selected";;
		RR1)	climdex_rr_RR1="selected";;
		R10mm)	climdex_rr_R10mm="selected";;
		R20mm)	climdex_rr_R20mm="selected";;
		Rnnmm)	climdex_rr_Rnnmm="selected";;
		CDD)	climdex_rr_CDD="selected";;
		CWD)	climdex_rr_CWD="selected";;
		R95pTOT) climdex_rr_R95pTOT="selected";;
		R99pTOT) climdex_rr_R99pTOT="selected";;
		SPI3)	climdex_rr_SPI3="selected";;
		SPI6)	climdex_rr_SPI6="selected";;
		PRCPTOT) climdex_rr_PRCPTOT="selected";;
		*)      climdex_rr_none="selected";;
	esac

	cat <<EOF
<select class="forminput" name="climdex_rr">
<option value="none" $climdex_rr_none>select an extreme index
<option value="RX1day" $climdex_rr_RX1day>Highest 1-day precipitation amount
<option value="RX5day" $climdex_rr_RX5day>Highest 5-day precipitation amount
<option value="SDII" $climdex_rr_SDII>Simple daily intensity index
<option value="SDIInn" $climdex_rr_SDIInn>SDII with other threshold
<option value="RR1" $climdex_rr_RR1>Wet days (RR >= 1mm)
<option value="R10mm" $climdex_rr_R10mm>Heavy precipitation days (RR>=10mm)
<option value="R20mm" $climdex_rr_R20mm>Very heavy precipitation days (RR>=20mm)
<option value="Rnnmm" $climdex_rr_Rnnmm>Heavy precipitation days (RR>=threshold)
<option value="CDD" $climdex_rr_CDD>Maximum # of consecutive dry days (RR<1mm)
<option value="CWD" $climdex_rr_CWD>Maximum # of consecutive wet days (RR>=1mm)
<option value="R95pTOT" $climdex_rr_R95pTOT>Precip. fraction on very wet days (>95%)
<option value="R99pTOT" $climdex_rr_R99pTOT>Precip. fraction on extremely wet days (>99%)
<option value="RnnTOT" $climdex_rr_RnnTOT>Precip. fraction above threshold
<option value="SPI3" $climdex_rr_SPI3>3-Month Standardized Precipitation Index
<option value="SPI6" $climdex_rr_SPI6>6-Month Standardized Precipitation Index
<option value="PRCPTOT" $climdex_rr_PRCPTOT>Total precipitation on wet days
<option value="other" $climdex_rr_other>(other indices to be implemented soon)
EOF

fi # $FORM_var
echo '</select>'

# error message if I was mistaken in the if-statement in getdata.cgi, otherwise propagate $climexp_type
if [ -z "$climdex_type" ]; then
	echo "I think this is not precipitation or minimum, maximum or mean temperature"
else
	echo "<input type=\"hidden\" name=\"climdex_type\" value=\"$climdex_type\">"
fi
# propagate the choices for the other variables to keep them in the defaults file
[ "$climdex_type" != tx -a -n "$FORM_climdex_tx" ] && echo "<input type=\"hidden\" name=\"climdex_tx\" value=\"$FORM_climdex_tx\">"
[ "$climdex_type" != tn -a -n "$FORM_climdex_tn" ] && echo "<input type=\"hidden\" name=\"climdex_tn\" value=\"$FORM_climdex_tn\">"
[ "$climdex_type" != tg -a -n "$FORM_climdex_tg" ] && echo "<input type=\"hidden\" name=\"climdex_tg\" value=\"$FORM_climdex_tg\">"
[ "$climdex_type" != rr -a -n "$FORM_climdex_rr" ] && echo "<input type=\"hidden\" name=\"climdex_rr\" value=\"$FORM_climdex_rr\">"

cat <<EOF
</td></tr><tr><td>
Threshold:
</td><td>
<input type="$number" step=any class="forminput" name="gt" size="4" style="width: 5em;" value="$FORM_cut"> (for SDIInn, Rnnmm, RnnTOT)
</td></tr><tr><td colspan="2">
EOF
