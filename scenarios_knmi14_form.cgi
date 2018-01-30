#!/bin/sh
. ./httpheaders_nocache.cgi
. ./init.cgi
. ./getargs.cgi

. ./myrijkshead_nl.cgi "Transformatie tijdreeksen KNMI&#8217;14" "<font color=#FF0000></font>" "index,follow"

cat <<EOF
<div class="datumtijd">19-sept-2014</div>
<div class="alineakop">Doel transformatie</div>
Het omzetten van een historische neerslag- of temperatuurreeks op dagbasis in een reeks die
 past bij het klimaat onder
&eacute;&eacute;n van de vier KNMI&#8217;14 klimaatscenario's voor een bepaalde tijdshorizon.

<p>Via het menu hieronder kan er gekozen worden uit verschillende klimaatscenario&#8217;s, stations
en tijdhorizonten. Het is ook mogelijk eigen historische tijdreeksen in te voeren.

<p>
<div class=formheader>Transformeer neerslagtijdreeks</div>
<div class=formbody>
<form method=post action="scenarios_knmi14.cgi">
<input type=hidden name=EMAIL value="$EMAIL">
<input type=hidden name=variable value="rr">
<table border=0 cellpadding=0 cellspacing=0 style="width:100%;">
<tr>
<td><span style="float:left">Station</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_stations.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=station>
<option selected>Kies een station</option>
<option value=999>eigen reeks uploaden
EOF
cat KNMI14/stationlist.html
cat <<EOF
</select></td>
</tr>
<tr>
<td><span style="float:left">Tijdshorizon</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=tijdshorizon>
<option selected>Kies een tijdshorizon</option>
<option value=1995>1995 (geen transformatie!)
<option>2000
<option>2005
<option>2010
<option>2015
<option>2020
<option>2025
<option>2030
<option>2035
<option>2040
<option>2045
<option>2050
<option>2055
<option>2060
<option>2065
<option>2070
<option>2075
<option>2080
<option>2085
</select></td>
</tr>
<tr>
<td><span style="float:left">Scenario</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_tijdshorizon.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scenario>
<option selected>Kies een scenario</option>
<option value="__">2030
<option>GL
<option>GH
<option>WL
<option>WH
</select></td>
</tr>
<tr>
<td><span style="float:left">Subscenario</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_neerslagrange.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scaling>
<option selected>Kies een subscenario</option>
<option value=lower>laag
<option value=centr>midden
<option value=upper>hoog
</select></td>
</tr>
<tr>
<td colspan=2 align=right><p><br><input type=submit value="transformeer" class="formbutton"></td>
</tr></table>
</form>
         </div>
<p>
<div class=formheader>Transformeer tijdreeks voor temperatuur</div>
<div class=formbody>
<form method=post action="scenarios_knmi14.cgi">
<input type=hidden name=EMAIL value="$EMAIL">
<table border=0 cellpadding=0 cellspacing=0 style="width:100%;">
<tr>
<td><span style="float:left">Variabele</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=variable>
<option selected>Kies een variabele</option>
<option value=tg>etmaalgemiddelde temperatuur
<option value=tn>minimumtemperatuur
<option value=tx>maximumtemperatuur
</select></td>
</tr>
<tr>
<td><span style="float:left">Station</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_stations.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=station>
<option selected>Kies een station</option>
<option value=999>eigen reeks uploaden
EOF
cat KNMI14/tstationlist.html
cat <<EOF
</select></td>
</tr>
<tr>
<td><span style="float:left">Tijdshorizon</span></td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=tijdshorizon>
<option selected>Kies een tijdshorizon</option>
<option value=1995>1995 (geen transformatie!)
<option>2000
<option>2005
<option>2010
<option>2015
<option>2020
<option>2025
<option>2030
<option>2035
<option>2040
<option>2045
<option>2050
<option>2055
<option>2060
<option>2065
<option>2070
<option>2075
<option>2080
<option>2085
</select></td>
</tr>
<tr>
<td><span style="float:left">Scenario</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_tijdshorizon.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=scenario>
<option selected>Kies een scenario</option>
<option value="__">2030
<option>GL
<option>GH
<option>WL
<option>WH
</select></td>
</tr>
<tr>
<td><span style="float:left">Regio</span> <a href="http://www.knmi.nl/klimaat/klimaatscenarios/KNMI'14/uitleg_regio.html" target="legenda">
                             <img style="vertical-align:top;margin-right:5px; margin-left:5px;" src="/images/info-i.gif" vspace=0 hspace=0 border=0 alt="Uitleg" title="Uitleg"></a>
 </td>
<td><p><br><span style="float:right;">
<select class="forminput" style="width:250px;" name=region>
<option selected value="">Op basis van stationslocatie</option>
<option value="NZK">Noordzeekust
<option value="NLD">Nederland
</select></td>
</tr>
<tr>
<td colspan=2 align=right><p><br><input type=submit value="transformeer" class="formbutton"></td>
</tr></table>
</form>
</div>
<p>De resultaten komen beschikbaar op de Engelstalige KNMI Climate Explorer web site, die de gelegenheid geeft de tijdreeks te downloaden, te analyseren of verder te bewerken.
<p><div class="bijschrift">Ligging van de neerslagstations (links; <a href="KNMI14/rr_map.kml">Google Earth</a>) en temperatuurstations (rechts; <a href="KNM14/t_map.kml">Google Earth</a>). Klik op de kaarten om een grotere en duidelijk leesbare versie te verkrijgen.</div>
<center>
<a href="javascript:pop_picture('http://www6.knmi.nl/klimatologie/images_algemeen/stations_neerslag.png', 'print')">
<img src="http://www6.knmi.nl/klimatologie/images_algemeen/stations_neerslag.png" alt="Neerslagstations" border=0 class="realimage" hspace=0 vspace=0 width="27.5"></a>
<a href="javascript:pop_picture('http://www.klimaatscenarios.nl/toekomstig_weer/transformatie/stations.jpg', 'print')">
<img src="http://www.klimaatscenarios.nl/toekomstig_weer/transformatie/stations.jpg" alt="Temperatuurstations" border=0 class="realimage" hspace=0 vspace=0 width="27.5%"></a>
</center><br clear=all>
EOF

./myvinkfoot_knmi14.cgi
