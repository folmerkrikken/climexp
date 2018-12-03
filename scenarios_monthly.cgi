#!/bin/bash
. ./init.cgi
export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_station
DIR=`pwd`

if [ "$WMO" = 999 -a -z "$FORM_data" ]; then
  #
  # generate an input screen for the time series to be uploaded and quit
  #
  echo 'Content-Type: text/html'
  echo
  echo
  if [ "$FORM_var" = p ]; then
    variable=neerslag
  elif [ "$FORM_var" = t ]; then
    variable=temperatuur
  fi
  . ./myrijkshead_nl.cgi "Transformatie eigen tijdreeksen"
  cat << EOF
<div class="datumtijd">21-06-2007</div>
<div class="alineakop">Uploaden eigen ${variable}reeksen</div>
Kopieer uw eigen tijdreeks naar het onderstaande blok, geef de tijdreeks een naam en klik op "Upload en transformeer".
<p>
<b>Enkele aandachtspunten bij het gebruik:</b>
<ul>
<li><b>Tijdsperiode</b> en lengte van de tijdreeks: het programma gebruikt scenariogetallen ten opzichte van de periode 1976-2005;
<li><b>Kwaliteit</b> van de tijdreeks: als er fouten in de historische tijdreeks zitten, zullen er ook fouten in de getransformeerde 
tijdreeksen zitten. Controleer daarom uw tijdreeks op ontbrekende waarden, sterk afwijkende waarden, inhomogeniteiten, etc. Het KNMI is niet verantwoordelijk voor de kwaliteit van uw eigen tijdreeks.
</ul>
<p>
Kijk voor meer aanwijzingen bij het gebruik van eigen tijdreeksen onder "Toelichting" in het menu aan de rechterkant. 
<p>
<div class='formheader'>Upload ${variable}tijdreeks</div>
<div class='formbody'>
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<form action="scenarios_monthly.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$FORM_EMAIL">
<input type="hidden" name="station" value="$FORM_station">
<input type="hidden" name="var" value="$FORM_var">
<tr><td>
Name:
</td>
<td><p><br><span style="float:right"><input type="text" name="STATION" size=40></span>
</td></tr><tr><td colspan="2"><p><br><span style="float:right;">
<textarea class="forminput" name="data" class="forminput" rows="6" cols="40">
# Overschrijf deze tekst met uw data.
# Regels met een "#" zijn commentaar.
# Vorm:
#   yyyymmdd[00] val
#   yyyy mm dd val
#   dd mm yyyy val
# Geef ontbrekende data aan met -99.9
</textarea></span>
<tr>
<td><span style="float:left">Tijdshorizon</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=tijdshorizon>
EOF
if [ -z "$FORM_tijdshorizon" ]; then
  echo '<option selected>Kies een tijdshorizon'
fi
for tijdshorizon in 1990 2020 2030 2040 2050 2060 2070 2080 2090 2100
do
  if [ "$FORM_tijdshorizon" = $tijdshorizon ]
  then
    echo "<option selected>$tijdshorizon"
  else
    echo "<option>$tijdshorizon"
  fi
done
cat <<EOF
</select></span></td>
</tr>
<tr>
<td><span style="float:left">Scenario</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scenario>
EOF
if [ -z "$FORM_scenario" ]; then
  echo '<option selected>Kies een scenario</option>'
fi
if [ ${REMOTE_ADDR#145.23} != $REMOTE_ADDR \
  -o ${REMOTE_ADDR#134.146} != $REMOTE_ADDR ]; then
  scenarios="G G+ W W+ WX"
else
  scenarios="G G+ W W+"
fi  
for scenario in $scenarios
do
  if [ "$FORM_scenario" = $scenario ]
  then
    echo "<option selected>$scenario"
  else
    echo "<option>$scenario"
  fi
done
cat <<EOF
</select></span></td>
</tr>
</td></tr><tr><td colspan=2 align="right"><p><br><input type="submit" class="formbutton" value="upload en transformeer">
</td></tr>
</form>
</table>
</div>
De resultaten komen beschikbaar op de Engelstalige KNMI Climate Explorer web site, die de gelegenheid geeft de tijdreeks te downloaden, te analyseren of verder te bewerken.


EOF
  . ./myvinkfoot_scenarios.cgi
  exit
fi

if [ "$FORM_var" = "p" ]; then
  PROG="transform_monthly.sh $FORM_station"
  mytype=S
  file=${mytype}${WMO}_obs.txt
  case "$WMO" in
  496) STATION="West Terschelling";;
  497) STATION="De Kooy &amp; Den Helder";;
  499) STATION="Groningen";;
  500) STATION="Ter Apel";;
  501) STATION="Hoorn";;
  502) STATION="Heerde";;
  503) STATION="Hoofddorp";;
  504) STATION="De Bilt";;
  505) STATION="Winterswijk";;
  506) STATION="Kerwerve";;
  507) STATION="Westdorpe &amp; Axel";;
  509) STATION="Oudenbosch";;
  510) STATION="Roermond";;
  999) STATION="$FORM_STATION"
       i=0
       WMO=uploaded$i
       while [ -f $DIR/data/$TYPE$WMO.dat \
               -o -f $DIR/data/$TYPE${WMO}_00.dat ]
       do
         i=$(($i + 1))
         WMO=uploaded$i
       done
       echo "$FORM_data" | tr '\r' '\n' > $DIR/data/$TYPE$WMO.dat
       file=$DIR/data/$TYPE$WMO.dat
       ;;
  *)   echo 'Content-Type: text/html'
       echo
       echo
       . ./myrijkshead_nl.cgi "Fout" "Selecteer een station" ""
       echo "Selecteer een geldig station op de vorige pagina, niet \"$WMO\""
       . ./myvinkfoot_scenarios.cgi
       exit;;
  esac
elif [ "$FORM_var" = "t" ]; then
  PROG="transform_monthly.sh $FORM_station"
  mytype=T
  file=${mytype}${WMO}_obs.txt
  case "$WMO" in
  235) STATION="De Kooy &amp; Den Helder";;
  260) STATION="De Bilt";;
  280) STATION="Eelde";;
  310) STATION="Vlissingen";;
  380) STATION="Maastricht";;
  999) STATION="$FORM_STATION"
       i=0
       WMO=uploaded$i
       while [ -f $DIR/data/$TYPE$WMO.dat \
               -o -f $DIR/data/$TYPE${WMO}_00.dat ]
       do
         i=$(($i + 1))
         WMO=uploaded$i
       done
       echo "$FORM_data" | tr '\r' '\n' > $DIR/data/$TYPE$WMO.dat
       file=$DIR/data/$TYPE$WMO.dat
       ;;
  *)   echo 'Content-Type: text/html'
       echo
       echo
       . ./myrijkshead_nl.cgi "Fout" "Selecteer een station" ""
       echo "Selecteer een geldig station op de vorige pagina, niet \"$WMO\""
       . ./myvinkfoot_scenarios.cgi
       exit;;
  esac
else
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myrijkshead_nl.cgi "Fout" "Selecteer een variabele" ""
       echo "Selecteer een geldige variabele op de vorige pagina, niet \"$FORM_var\""
  . ./myvinkfoot_scenarios.cgi
  exit
fi

TYPE=$FORM_var
NPERYEAR=366

  
case "$FORM_scenario" in
G|G+|W|W+|WX)  
     PROG="$PROG $FORM_scenario"
     ;;
*)   if [ $FORM_tijdshorizon = 1990 ]
     then
       PROG="$PROG G"
       FORM_scenario=G
     else
       echo 'Content-Type: text/html'
       echo
       echo
       . ./myrijkshead_nl.cgi "Fout" "Selecteer een scenario" ""
       echo "Selecteer een geldig scenario op de vorige pagina, niet \"$FORM_scenario\""
       . ./myvinkfoot_scenarios.cgi
       exit
     fi
     ;;
esac

case "$FORM_tijdshorizon" in
1990|2020|2030|2040|2050|2060|2070|2080|2090|2100) PROG="$PROG $FORM_tijdshorizon";;
*)   echo 'Content-Type: text/html'
     echo
     echo
     . ./myrijkshead_nl.cgi "Fout" "Selecteer een tijdshorizon" ""
     echo "Selecteer een geldige tijdshorizon op de vorige pagina, niet \"$FORM_tijdshorizon\""
     . ./myvinkfoot_scenarios.cgi
     exit;;
esac

if [ $FORM_scenario = WX -a $FORM_tijdshorizon -gt 2050 ]; then
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myrijkshead_nl.cgi "Fout" "Tijdshorizon te ver" ""
  echo "De WX extrapolatie is alleen geldig voor tijdshorizonten tot 2050, niet  \"$FORM_tijdshorizon\""
  . ./myvinkfoot_scenarios.cgi
  exit
fi

export file
export mytype
export STATION
WMO=${mytype}${WMO}_${FORM_scenario}_${FORM_tijdshorizon}
FROM='of the <a href="http://www.knmi.nl/climatescenarios/">KNMI 2006 scenarios</a>'
LASTMODIFIED=""

. $DIR/getdata.cgi
