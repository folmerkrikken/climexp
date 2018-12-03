#!/bin/bash
# show the plots produced by scripts above.

for ext in "$stack" ".trc"
do
  if [ -f $corrroot$ext.eps ]
  then
    gzip -f $corrroot$ext.eps
###( $DIR/bin/ppmtogif $corrroot$ext.ppm > $corrroot$ext.gif )2> /dev/null
###rm $corrroot$ext.ppm
        echo "<div class=\"bijschrift\">$title (<a href=\"data/$TYPE${WMO}corr$FORM_num$ext.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=data/$TYPE${WMO}corr$FORM_num$ext.eps.gz\">pdf</a>,"
    if [ -f ${corrroot}_yr.eps ]; then
       epstopdf ${corrroot}_yr.eps
       gzip -f ${corrroot}_yr.eps
       echo "<a href=\"data/$TYPE${WMO}corr$FORM_num${ext}_yr.eps.gz\">month.year format</a>,"
       echo "<a href=\"data/$TYPE${WMO}corr$FORM_num${ext}_yr.pdf\">pdf</a>,"
    fi
    if [ -f data/$TYPE$WMO${FORM_num}.cor ]; then
      echo "<a href=\"data/$TYPE$WMO${FORM_num}.cor\">plot data</a>, "
    fi
    if [ -f data/$TYPE$WMO$FORM_num.dump$ext1$ext ]; then
      echo "<a href=\"data/$TYPE$WMO$FORM_num.dump$ext1$ext\">raw data</a>"
    fi
    pngfile=data/$TYPE${WMO}corr$FORM_num$ext.png
    getpngwidth
    echo ")</div><center><img src=\"data/$TYPE${WMO}corr$FORM_num$ext.png\" alt=\"correlation and $CLIM\" width=\"$halfwidth\" hspace=0 vspace=0>"
  fi
done
