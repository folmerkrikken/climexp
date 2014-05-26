#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

eval `bin/proccgi $*`
EMAIL=$FORM_id
# in order not to break bookmarks to this entry point allow QUERY_STRING (with some checking)
[ -z "$FORM_id" ] && FORM_id=`echo "$QUERY_STRING" | tr -cd '[:alnum:]@.-_'`
# do not allow / in email address
EMAIL="${FORM_id#*/}"
[ "$EMAIL" != "$QUERY_STRING" ] && EMAIL=""
[ -z "$EMAIL" ] && EMAIL=someone@somewhere

(cd ..; . ./myrijkshead_nl.cgi "Transformatie tijdreeksen" "" "index,follow")

cat <<EOF
<div class="datumtijd">28-nov-2008</div>
<div class="alineakop">Doel transformatie</div>
Het omzetten van een historische neerslag- of temperatuurreeks op dagbasis in een reeks die
 past bij het klimaat onder
&eacute;&eacute;n van de vier KNMI'06 klimaatscenario's voor een bepaalde tijdshorizon.
<p>
Via het menu hieronder kan er gekozen worden uit verschillende klimaatscenario's, stations
en tijdhorizonten. Het is ook
mogelijk eigen historische tijdreeksen in te voeren.
<p>
<div class="alineakop">Enkele aandachtspunten bij het gebruik:</div>
<ul>
<li>Het transformeren van historische tijdreeksen is slechts &eacute;&eacute;n manier om tijdreeksen voor de toekomst te verkrijgen. De volgorde van tempera- tuurwisselingen, jaar-op-jaar variaties, etc. in de getransformeerde tijdreeksen wordt sterk bepaald door wat er in het verleden is gebeurd;
</li>
<li>De getransformeerde tijdreeksen passen bij het <b>klimaat</b> in de toekomst volgens de KNMI'06 klimaatscenario's. Dit betekent dat ze informatie geven over de gemiddelden, variatie tussen dagen, kans op extremen, etc. Ze leveren echter <b>g&eacute;&eacute;n voorspelling van het weer</b> in de toekomst op een bepaalde dag of in een bepaald jaar!
</li>
</ul>
<p>
Meer informatie over hoe het programma werkt, het gebruik van eigen tijdreeksen en de voordelen en beperkingen van getransformeerde tijdreeksen is te vinden via het menu hiernaast onder "Toelichting".
<p>
<div class=formheader>Transformeer neerslagtijdreeks (wijziging per 10-4-2008)</div>
<div class=formbody>
<form method=post action="http://climexp.knmi.nl/scenarios_monthly.cgi">
<!--<form method=post action="http://zuidzee.knmi.nl/~oldenbor/climexp/scenarios_monthly.cgi">-->
<input type=hidden name=EMAIL value="$EMAIL">
<input type=hidden name=var value="p">
<table border=0 cellpadding=0 cellspacing=0 style="width:445px;">
<tr>
<td><span style="float:left">Station</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=station>
<option selected>Kies een station</option>
<option value=496>496 West Terschelling
<option value=497>497/498 De Kooy &amp; Den Helder
<option value=499>499 Groningen
<option value=500>500 Ter Apel
<option value=501>501 Hoorn
<option value=502>502 Heerde
<option value=503>503 Hoofddorp
<option value=504>504 De Bilt
<option value=505>505 Winterswijk
<option value=506>506 Kerkwerve
<option value=507>507/508 Westdorpe &amp; Axel
<option value=509>509 Oudenbosch
<option value=510>510 Roermond
<option value=999>eigen reeks uploaden
</select></td>
</tr>
<tr>
<td><span style="float:left">Tijdshorizon</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=tijdshorizon>
<option selected>Kies een tijdshorizon</option>
<option value=1990>1990 (geen transformatie!)
<option>2020
<option>2030
<option>2040
<option>2050
<option>2060
<option>2070
<option>2080
<option>2090
<option>2100
</select></td>
</tr>
<tr>
<td><span style="float:left">Scenario</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scenario>
<option selected>Kies een scenario</option>
<option>G
<option>G+
<option>W
<option>W+
</select></td>
</tr>
<tr>
<td colspan=2 align=right><p><br><input type=submit value="transformeer" class="formbutton"></td>
</tr></table>
</form>
         </div>
<p>
<div class=formheader>Transformeer tijdreeks voor gemiddelde etmaaltemperatuur</div>
<div class=formbody>
<form method=post action="../scenarios_monthly.cgi">
<input type=hidden name=EMAIL value="$EMAIL">
<input type=hidden name=var value="t">
<table border=0 cellpadding=0 cellspacing=0 style="width:445px;">
<tr>
<td><span style="float:left">Station</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=station>
<option selected>Kies een station</option>
<option value=235>235 De Kooy &amp; Den Helder
<option value=260>260 De Bilt
<option value=280>280 Groningen &amp; Eelde
<option value=310>310 Vlissingen
<option value=380>380 Maastricht
<option value=999>eigen reeks uploaden
</select></td>
</tr>
<tr>
<td><span style="float:left">Tijdshorizon</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=tijdshorizon>
<option selected>Kies een tijdshorizon</option>
<option value=1990>1990 (geen transformatie!)
<option>2020
<option>2030
<option>2040
<option>2050
<option>2060
<option>2070
<option>2080
<option>2090
<option>2100
</select></td>
</tr>
<tr>
<td><span style="float:left">Scenario</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scenario>
<option selected>Kies een scenario</option>
<option>G
<option>G+
<option>W
<option>W+
EOF
if [ ${REMOTE_ADDR#145.23} != $REMOTE_ADDR \
  -o ${REMOTE_ADDR#134.146} != $REMOTE_ADDR \
  -o ${REMOTE_ADDR#82.95.194.243} != $REMOTE_ADDR ]; then
echo '<option>WX'
fi
cat <<EOF
</select></td>
</tr>
<tr>
<td colspan=2 align=right><p><br><input type=submit value="transformeer" class="formbutton"></td>
</tr></table>
</form>
</div>
<p>De resultaten komen beschikbaar op de Engelstalige KNMI Climate Explorer web site, die de gelegenheid geeft de tijdreeks te downloaden, te analyseren of verder te bewerken.
<p><div class="bijschrift">Ligging van de neerslagstations (<a href="placemarks.kml">Google Earth</a>) en temperatuurstations (<a href="tplacemarks.kml">Google Earth</a>)</div>
<center>
<img src="stations.png" alt="Neerslagstations" border=0 class="realimage" hspace=0 vspace=0>
<img src="tstations.png" alt="Temperatuurstations" border=0 class="realimage" hspace=0 vspace=0>
</center><br clear=all>
EOF

(cd ..;. ./myvinkfoot_scenarios.cgi)
