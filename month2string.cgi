#!/bin/sh
if [ "$NPERYEAR" = 366 -o "$NPERYEAR" = 365 -o "$NPERYEAR" = 360 ]; then
  eval `$DIR/bin/month2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix | sed -e 's/monthly/daily/g'`
elif [ "$NPERYEAR" = 12 ]; then
  eval `$DIR/bin/month2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix`
elif [ "$NPERYEAR" = 73 ]; then
  eval `$DIR/bin/month2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix | sed -e 's/monthly/5-daily/g'`
elif [ "$NPERYEAR" = 1 ]; then
  eval `$DIR/bin/annual2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix | sed -e 's/monthly/yearly/g'`
elif [ "$NPERYEAR" = 4 ]; then
  eval `$DIR/bin/season2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix`
elif [ "$NPERYEAR" = 2 ]; then
  eval `$DIR/bin/halfyear2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix`
else
  echo "warning: could not determine value of NPERYEAR = $NPERYEAR<br>"
  eval `$DIR/bin/month2string "$FORM_month" "${sumstring}" "$FORM_lag" "$FORM_operation" $FORM_fix | sed -e 's/monthly/separately/g'`
fi
if [ $NPERYEAR = 1 ]; then
  period=year
elif [ $NPERYEAR = 4 ]; then
  period="season"
elif [ $NPERYEAR = 12 ]; then
  period="month"
elif [ $NPERYEAR = 360 -o $NPERYEAR -eq 365 -o $NPERYEAR -eq 366 ]; then
  period="day"
else
  period="period"
fi
if [ -n "$FORM_sel" ]; then
    if [ -n "$FORM_sum" ]; then
	    seriesmonth="$seriesmonth ${FORM_sum}-${period} ave"
    fi
fi
