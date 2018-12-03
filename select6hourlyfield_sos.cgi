#!/bin/bash
echo '<tr>'
echo '<th colspan="11"><a href="http://www.knmi.nl/scatterometer/">ERS reprocessed scattermometer</a> 0.5&deg;&times;0.5&deg;</th>'

for var in header u v tx ty speed
do
  case $var in
  header) name="&nbsp;";;
  u) name=$var;;
  v) name=$var;;
  tx) name="&tau;<sub>x</sub>";;
  ty) name="&tau;<sub>y</sub>";;
  speed) name="|u|";;
  *) name="unknown";;
  esac
  echo "</tr><tr><td>$name</td>"
  yr=1992
  while [ $yr -lt 2002 ]
  do
    if [ $var = header ]; then
      echo "<td>$yr</td>"
    else
      echo "<td><input type=\"radio\" class=\"formradio\" name=\"field\" value=\"sos_${yr}_${var}\"></td>"
    fi
    yr=$(($yr + 1))
  done
done
echo '</tr>'
