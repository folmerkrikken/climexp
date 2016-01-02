#!/bin/sh
. ./init.cgi
# plot a 3D view of a correlation coefficient with both month and lag varying

# only numbers in viewing angles
FORM_hor=`echo $FORM_hor | tr -c '0-9.-' ' '`
FORM_ver=`echo $FORM_ver | tr -c '0-9.-' ' '`

if [ "$FORM_whichvar" = regr ]; then
   col=15
else
   col=3
fi

if [ "$FORM_fix" = fix2 ]; then
  var=$index
else
  var=$CLIM
fi
if [ -n "$FORM_sum" ];then
  if [ "$FORM_operation" = "selecting" ]; then
    tmp="${FORM_sum}-month monthly "
  else
    tmp="${FORM_sum}-month averaged "
  fi
  xlabel="Starting month of $var"
else
  tmp=""
  xlabel="Month of $var"
fi
echo "<div class=\"alineakop\">${tmp}lag correlations</div>"
echo "<div class=\"formbody\">"
echo "<form action=\"plot3dnew.cgi\" method=\"POST\"><p>New viewing angles: "
echo "<input type=\"hidden\" name=\"CLIM\" value=\"$CLIM\">"
echo "<input type=\"hidden\" name=\"WMO\" value=\"$WMO\">"
echo "<input type=\"hidden\" name=\"TYPE\" value=\"$TYPE\">"
echo "<input type=\"hidden\" name=\"index\" value=\"$index\">"
echo "<input type=\"hidden\" name=\"title\" value=\"$title\">"
echo "<input type=\"hidden\" name=\"corrroot\" value=\"$corrroot\">"
echo "<input type=\"hidden\" name=\"sum\" value=\"$FORM_sum\">"
echo "<input type=\"hidden\" name=\"num\" value=\"$FORM_num\">"
echo "<input type=\"$number\" name=\"ver\" $textsize3 value=\"${FORM_ver}\">"
echo "<input type=\"$number\" name=\"hor\" $textsize3 value=\"${FORM_hor}\">"
echo "<input type=\"submit\" value=\"replot\">"
echo "</form>"
echo "</div>"

./bin/gnuplot << EOF
$gnuplot_init
set size 0.7,0.7
set title "$tmp$title"
set xrange [1:12]
set xtics ("J" 1, "F" 2, "M" 3, "A" 4, "M" 5, "J" 6, "J" 7, "A" 8, "S" 9, "O" 10, "N" 11, "D" 12)
set ylabel "lag [months]" #(lag positive: $index leading $CLIM)
set xlabel "$xlabel"
set zlabel "$correlation"
set term postscript epsf color solid
set output "$corrroot$stack.eps"
#set view 0,0
set contour
#set nosurface
#set ticslevel 0
set view ${FORM_ver},${FORM_hor}
set hidden3d
splot "data/$TYPE$WMO$FORM_num.cor" using 1:2:$col notitle w l
set term png $gnuplot_png_font_hires
set output "$corrroot$stack.png"
replot
EOF

