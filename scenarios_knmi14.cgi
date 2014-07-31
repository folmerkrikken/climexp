#!/bin/sh
. ./init.cgi
export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_station
EMAIL=someone@somewhere

if [ "$FORM_variable" = rr ]; then  
    NAME=neerslag
elif [ "$FORM_variable" = tg ]; then
    NAME="daggemiddelde temperatuur"
elif [ "$FORM_variable" = tx ]; then
    NAME="maximum temperatuur"
elif [ "$FORM_variable" = tn ]; then
    NAME="minimmum temperatuur"
fi
if [ "$WMO" = 999 -a -z "$FORM_data" ]; then
  #
  # generate an input screen for the time series to be uploaded and quit
  #
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myrijkshead_nl.cgi "Transformatie eigen tijdreeksen"
  cat << EOF
<div class="datumtijd">21-06-2007</div>
<div class="alineakop">Uploaden eigen ${NAME} reeksen</div>
Kopieer uw eigen tijdreeks naar het onderstaande blok, geef de tijdreeks een naam en klik op "Upload en transformeer".
<p>
<b>Enkele aandachtspunten bij het gebruik:</b>
<ul>
<li><b>Tijdsperiode</b> en lengte van de tijdreeks: het programma gebruikt scenariogetallen ten opzichte van de periode 1981-2010;
<li><b>Kwaliteit</b> van de tijdreeks: als er fouten in de historische tijdreeks zitten, zullen er ook fouten in de getransformeerde 
tijdreeksen zitten. Controleer daarom uw tijdreeks op ontbrekende waarden, sterk afwijkende waarden, inhomogeniteiten, etc. Het KNMI is niet verantwoordelijk voor de kwaliteit van uw eigen tijdreeks.
</ul>
<p>
Kijk voor meer aanwijzingen bij het gebruik van eigen tijdreeksen onder "Toelichting" in het menu aan de rechterkant. 
<p>
<div class='formheader'>Upload ${variable}tijdreeks</div>
<div class='formbody'>
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<form action="scenarios_knmi14.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$FORM_EMAIL">
<input type="hidden" name="station" value="$FORM_station">
<input type="hidden" name="variable" value="$FORM_variable">
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
    tijdshorizon=1990
    while [ $tijdshorizon -lt 2085 ]
    do
      tijdshorizon=$((tijdshorizon+5))
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
    scenarios="__ GL GH WL WH"
    for scenario in $scenarios
    do
      if [ "$FORM_scenario" = $scenario ]
      then
        echo "<option selected>$scenario"
      else
        echo "<option>$scenario"
      fi
    done
    if [ $FORM_variable != 'rr' ]; then
        cat <<EOF
</select></span></td>
</tr>
<tr>
<td><span style="float:left">Regio</span>&nbsp;<a href="javascript:pop_picture('KNMI14/KNMI14_regios.jpg', 'print')" target="_new"><img src="images/info-i.gif" alt="more information" border="0"></a></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=region>
<option value="ongeldig">Selecteer een regio
<option value=NZK>Noordzeekust
<option value=NWN>Noord-West Nederland
<option value=ZWN>Zuid-West Nederland
<option value=ZON>Zuid-Oost Nederland
<option value=MON>Midden-Oost Nederland
<option value=NON>Noord-Oost Nederland
<option value=NLD>Nederland (gemiddeld)
EOF
    else
        cat << EOF
</select></span></td>
</tr>
<tr>
<td><span style="float:left">Subscenario</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scaling>
EOF
        if [ -z "$FORM_scaling" ]; then
            echo '<option selected>Kies een subscenario</option>'
        fi
        case "$FORM_scaling" in
            upper) upperselected=selected;;
            centr) centrselected=selected;;
            lower) lowerselected=selected;;
        esac
        echo "<option value=upper $upperselected>hoog"
        echo "<option value=centr $centrselected>midden"
        echo "<option value=lower $lowerselected>laag"
    fi
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
  . ./myvinkfoot_knmi14.cgi
  exit
fi

TYPE=$FORM_variable
WMO=$FORM_station
if [ $WMO = 999 ]; then ! uploaded file
    STATION="$FORM_STATION"
    i=0
    WMO=uploaded$i
    while [ -f ./data/$TYPE$WMO.dat \
           -o -f ./data/$TYPE${WMO}_00.dat -o -f ./data/$TYPE${WMO}_01.dat ]
    do
        i=$((i + 1))
        WMO=uploaded$i
    done
    echo "$FORM_data" | tr '\r' '\n' | tr -d -C '[\n\t^#A-Za-z().,0-9:/-?= ]' > ./data/$TYPE$WMO.dat
    file=./data/$TYPE$WMO.dat
else
    file=./KNMI14/${FORM_variable}${FORM_station}.dat
fi
if [ ! -s $file ]; then
    echo 'Content-Type: text/html'
    echo
    echo
    . ./myrijkshead_nl.cgi "Fout" "Selecteer een station" ""
    echo "Selecteer een geldig station op de vorige pagina, niet \"$WMO\""
    . ./myvinkfoot_scenarios.cgi
    exit
fi
if [ "$FORM_variable" = "rr" ]; then
    NPERYEAR=366
    scenario=${FORM_scenario}.$FORM_scaling
    region=NLD
    if [ -z "$STATION" ]; then
        STATION=`head -3 $file | tail -1 | sed -e 's/^# //' -e 's/[(] .*//'`
    fi
elif [ "$FORM_variable" = "tg" -o "$FORM_variable" = "tx" -o "$FORM_variable" = "tn" ]; then
    NPERYEAR=366
    scenario=$FORM_scenario
    if [ -n "$FORM_region" ]; then
        region=$FORM_region
    else
        # from stationscoordinaten.txt
        case "$FORM_station" in
            210|235|240|249) region=NWN;;
            251|267|270|273|279|280|286|290) region=NON;;
            260|269|275|283) region=MON;;
            310|319|323|344|350) region=ZWN;;
            370|375|380|391) region=ZON;;
            *)  echo 'Content-Type: text/html'
                echo
                echo
                . ./myrijkshead_nl.cgi "Fout" "Ken station niet" ""
                echo "$0: error: do not know region of station $FORM_station"
                . ./myvinkfoot_scenarios.cgi
                exit;;
        esac
    fi
else
    echo 'Content-Type: text/html'
    echo
    echo
    . ./myrijkshead_nl.cgi "Fout" "Selecteer een variabele" ""
    echo "Selecteer een geldige variabele op de vorige pagina, niet \"$FORM_variable\""
    . ./myvinkfoot_scenarios.cgi
    exit
fi

if [ 1 = 0 ]; then
    echo 'Content-Type: text/html'
    echo
    echo
    echo "file=$file<br>"
    echo "FORM_variable=$FORM_variable<br>"
    echo "FORM_tijdshorizon=$FORM_tijdshorizon<br>"
    echo "scenario=$scenario<br>"
    echo "region=$region<br>"
fi
PROG="transform $file $FORM_variable $FORM_tijdshorizon $scenario $region"

if [ $FORM_scenario = __ -a $FORM_tijdshorizon -gt 2030 ]; then
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myrijkshead_nl.cgi "Fout" "Tijdshorizon te ver" ""
  echo "Het 2030 scenario is alleen geldig voor tijdshorizonten tot 2030, niet  \"$FORM_tijdshorizon\""
  . ./myvinkfoot_scenarios.cgi
  exit
fi
if [ $FORM_tijdshorizon -lt 1995 -o $FORM_tijdshorizon -gt 2085 ]; then
  echo 'Content-Type: text/html'
  echo
  echo
  . ./myrijkshead_nl.cgi "Fout" "Tijdshorizon ongeldig" ""
  echo "De KNMI'14 scenario's zijn alleen geldig voor tijdshorizonten vanaf 1995 tot en met 2085, niet  \"$FORM_tijdshorizon\""
  . ./myvinkfoot_scenarios.cgi
  exit
fi

export file
export STATION
export TYPE
WMO=${WMO}_${scenario}_${FORM_tijdshorizon}
FROM='of the <a href="http://www.climatescenarios.nl/">KNMI 2014 scenarios</a>'
LASTMODIFIED=""

. ./getdata.cgi
