#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./myvinkhead.cgi "Questionnaire Climatic Events" "of interest for seasonal to decadal predictions" "noindex,nofollow"

c=`echo $0 | fgrep -c stakeholder`
if [ $c = 1 ]; then
	cat <<EOF
SPECS is a large project funded by the European Committee in which scientists all over Europe investigate climate predictions, months up to decades ahead. Predictions can be assessed on their value in hindsight. By studying actually occurred events, scientists increase understanding on the climate events and improve their predictions of similar events in the future. A well known example of such an event is the heatwave in the summer of 2003 in Europe. The recent snowy winters in western Europe are good examples as well.  We wish to investigate a limited number of these events. 

<p>In this questionnaire we ask you which climate events that occurred in the recent past are most interesting to you, as a stakeholder (from e.g. humanitarian, monetary, or ecological point of view). Your input will help us to improve predictions of events that are relevant for you as a stakeholder.

EOF
else
	cat <<EOF
Within the Cross Cutting Theme 3, Case Studies and Extremes, we will select a limited number of cases that will be addressed in all work packages. For instance, the evaluation of forecast quality, the process-based evaluation and the improvements of the prediction systems will be assessed. 

<p>In this questionnaire we ask you which events that occurred in the recent past are most interesting to you (from forecast failure point of view, or from physical mechanism point of view to test a specific hypothesis, or from downscaling and impact point of view etc.). 

<p>We will select a limited number of events based on your evaluation and a stakeholder questionnaire.  

EOF
fi
cat <<EOF
<p>You can rate your interest on the scale of 1 (not interesting) to 5 (very important and interesting)
<p>
<form action="specs_questionnaire.cgi" method="POST">
<table class="realtable" border=0 cellpadding=0 cellspacing=0 width=692>
<tr>
<th colspan=2>User information</th>
</tr><tr>
<td><span style="float:left">Organisation</span></td>
<td><span style="float:right;"><input type="text" name="organisation" class="forminput" style="width:250px;" placeholder="organisation">&nbsp;&nbsp;</span></td>
</tr><tr>
<td><span style="float:left">Name</span></td>
<td><span style="float:right;"><input type="text" name="name" class="forminput" style="width:250px;" placeholder="name">&nbsp;&nbsp;</span></td>
</tr><tr>
<td><span style="float:left">E-mail address</span></td>
<td><span style="float:right;"><input type="email" name="email" class="forminput" style="width:250px;" placeholder="e-mail address">&nbsp;&nbsp;</span></td>
</tr><tr>
<td><span style="float:left">Main project involved with</span></td>
<td><span style="float:right;">
<input type="radio" name="project" class="formradio" value="SPECS">SPECS,
<input type="radio" name="project" class="formradio" value="EUPORIAS">EUPORIAS,
<input type="radio" name="project" class="formradio" value="ECLISE">ECLISE,
<input type="radio" name="project" class="formradio" value="CLIMRUN">CLIMRUN,
<input type="radio" name="project" class="formradio" value="EUCLEIA">EUCLEIA
&nbsp;&nbsp;
</tr><tr>
<td><span style="float:left">Main impact considered</span></td>
<td><span style="float:right;">
<input type="radio" name="type" class="formradio" value="humanitarian">humanitarian,
<input type="radio" name="type" class="formradio" value="economical">economical,
<input type="radio" name="type" class="formradio" value="ecological">ecological
<input type="radio" name="type" class="formradio" value="science">pure science&nbsp;&nbsp;
</span></td>
</tr></table>
</div class=formbody>
<p>
<table class="realtable" width=692 border=0 cellspacing=0 cellpadding=0>
<tr>
<th>Seasonal events</th><th><span style="float:right;">not interesting ... very important&nbsp;&nbsp;</span></th>
</tr><tr>
<td><span style="float:left">Sea ice minimum 2012 (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=icen_nsidc&mon1=sep&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="seaice2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="seaice2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="seaice2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="seaice2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="seaice2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought and heat wave summer 2012 in US (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaveus2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaveus2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaveus2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaveus2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaveus2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Hot summer 2012 around the Mediterranean (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="summermediterranean2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="summermediterranean2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="summermediterranean2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="summermediterranean2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="summermediterranean2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods summer 2012 in Britain (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodsbritainsummer2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Bad weather summer 2012 in Britain (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=slp_ncepncar&mon1=JJA&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="summerbritain2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="summerbritain2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="summerbritain2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="summerbritain2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="summerbritain2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Warm March 2012 in US (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=mar&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="hotmarchus2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="hotmarchus2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="hotmarchus2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="hotmarchus2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="hotmarchus2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold spell February 2012 in Europe (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=feb&year1=2012" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="coldspelleurope2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldspelleurope2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldspelleurope2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldspelleurope2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldspelleurope2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2012 <input type=text class=forminput name=other2012text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2012" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2012" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2012" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2012" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2012" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods Oct-Nov 2011 in East Africa (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=SON&year1=2011" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodseastafrica2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodseastafrica2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodseastafrica2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodseastafrica2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodseastafrica2011" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought 2010/2011 in East Africa (<a href="http://www.knmi.nl/klimatologie/annual_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=jun&year1=2011" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="droughteastafrica2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="droughteastafrica2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="droughteastafrica2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="droughteastafrica2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="droughteastafrica2011" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Monsoon floods 2011 in Thailand (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2011" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodsthailand2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodsthailand2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodsthailand2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodsthailand2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodsthailand2011" class="formradio" value="5">5&nbsp;&nbsp;
</tr><tr>
<td><span style="float:left">Drought and heat wave 2011 in southern US (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2011" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaveus2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaveus2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaveus2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaveus2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaveus2011" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods 2010/2011 in Australia (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=DJF&year1=2011" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodsaustralia2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodsaustralia2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodsaustralia2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodsaustralia2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodsaustralia2011" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2011 <input type=text class=forminput name=other2011text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2011" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2011" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2011" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2011" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2011" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold spell and snow December 2010 in Europe (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=dec&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="coldspelleuropedec2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldspelleuropedec2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldspelleuropedec2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldspelleuropedec2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldspelleuropedec2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought and heat wave 2010 in Russia (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaverussia2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaverussia2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaverussia2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaverussia2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaverussia2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods in Pakistan 2010 (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodspakistan2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodspakistan2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodspakistan2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodspakistan2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodspakistan2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought 2010 in Brazil (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="droughtamazon2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="droughtamazon2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="droughtamazon2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="droughtamazon2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="droughtamazon2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Heat wave 2010 in Japan (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwavejapan2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwavejapan2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwavejapan2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwavejapan2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwavejapan2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods in eastern Europe spring 2010 (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodseasteurope2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Severe winter storm Xynthia in Europe winter 2010</span></td>
<td><span style="float:right;">
<input type="radio" name="xynthia2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="xynthia2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="xynthia2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="xynthia2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="xynthia2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold and snowy winter 2010 in Europe (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=DJF&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="coldwintereurope2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldwintereurope2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldwintereurope2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldwintereurope2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldwintereurope2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold winter 2010 in the US (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=DJF&year1=2010" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="coldwinterus2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldwinterus2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldwinterus2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldwinterus2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldwinterus2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2010 <input type=text class=forminput name=other2010text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2010" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2010" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2010" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2010" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2010" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Snow in southern Norway winter 2009 (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=DJF&year1=2009" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="snownorway2009" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="snownorway2009" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="snownorway2009" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="snownorway2009" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="snownorway2009" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2009 <input type=text class=forminput name=other2009text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2009" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2009" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2009" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2009" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2009" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods in eastern Europe summer 2008 (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=jul&year1=2008" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodseasteurope2008" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2008" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2008" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2008" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodseasteurope2008" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods in central Europe spring 2008 (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=apr&year1=2008" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodscentraleurope2008" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodscentraleurope2008" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodscentraleurope2008" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodscentraleurope2008" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodscentraleurope2008" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2008 <input type=text class=forminput name=other2008text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2008" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2008" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2008" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2008" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2008" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Sea ice minimum 2007 (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=icen_nsidc&mon1=sep&year1=2007" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="seaice2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="seaice2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="seaice2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="seaice2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="seaice2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods summer 2007 in Britain (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2007" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodsbritainsummer2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodsbritainsummer2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Warm spring 2007 in Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=MAM&year1=2007" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="warmspringeurope2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="warmspringeurope2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="warmspringeurope2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="warmspringeurope2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="warmspringeurope2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Mild winter 2007 in Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=DJF&year1=2007" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="mildwintereurope2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="mildwintereurope2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="mildwintereurope2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="mildwintereurope2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="mildwintereurope2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Severe winter storm Kyrill in Europe winter 2007</span></td>
<td><span style="float:right;">
<input type="radio" name="kyrill2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="kyrill2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="kyrill2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="kyrill2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="kyrill2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2007 <input type=text class=forminput name=other2007text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2007" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2007" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2007" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2007" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2007" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Warm autumn 2006 in Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=SON&year1=2006" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="warmautmneurope2006" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="warmautmneurope2006" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="warmautmneurope2006" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="warmautmneurope2006" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="warmautmneurope2006" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Storm surges in the Baltic November 2006</span></td>
<td><span style="float:right;">
<input type="radio" name="stormsurgesbaltic2006" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="stormsurgesbaltic2006" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="stormsurgesbaltic2006" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="stormsurgesbaltic2006" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="stormsurgesbaltic2006" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold winter 2006 in Russia (<a href="http://www.knmi.nl/klimatologie/monthly_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=DJF&year1=2006" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="coldwinterrussia2006" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldwinterrussia2006" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldwinterrussia2006" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldwinterrussia2006" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldwinterrussia2006" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Heat wave July 2006 in NW Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=jul&year1=2006" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaveeurope2006" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2006" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2006" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2006" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2006" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2006 <input type=text class=forminput name=other2006text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2006" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2006" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2006" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2006" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2006" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought and heat wave summer 2005 in Spain and Portugal (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2005" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaveiberia2005" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaveiberia2005" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaveiberia2005" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaveiberia2005" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaveiberia2005" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods spring and summer 2007 in Romania (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2005" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodsromaniasummer2005" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodsromaniasummer2005" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodsromaniasummer2005" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodsromaniasummer2005" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodsromaniasummer2005" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2005 <input type=text class=forminput name=other2005text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2005" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2005" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2005" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2005" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2005" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2004 <input type=text class=forminput name=other2004text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2004" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2004" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2004" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2004" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2004" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Drought and heat wave summer 2003 in Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=t2m_ghcncams&mon1=JJA&year1=2003" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="heatwaveeurope2003" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2003" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2003" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2003" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="heatwaveeurope2003" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2003 <input type=text class=forminput name=other2003text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2003" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2003" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2003" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2003" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2003" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Floods summer 2002 in Central Europe (<a href="http://www.knmi.nl/klimatologie/seasonal_overview_world_weather/index.cgi?var=prcp_gpcc&mon1=JJA&year1=2002" target="_new">map</a>)</span></td>
<td><span style="float:right;">
<input type="radio" name="floodscentraleuropesummer2002" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="floodscentraleuropesummer2002" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="floodscentraleuropesummer2002" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="floodscentraleuropesummer2002" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="floodscentraleuropesummer2002" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event in 2002 <input type=text class=forminput name=other2002text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2002" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2002" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2002" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2002" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2002" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Severe winter storms in Europe winter 1999</span></td>
<td><span style="float:right;">
<input type="radio" name="stormseuropewinter1999" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="stormseuropewinter1999" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="stormseuropewinter1999" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="stormseuropewinter1999" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="stormseuropewinter1999" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Rhine floods winter 1995</span></td>
<td><span style="float:right;">
<input type="radio" name="rhinefloods1995" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="rhinefloods1995" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="rhinefloods1995" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="rhinefloods1995" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="rhinefloods1995" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event <input type=text class=forminput name=other1text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other1" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other1" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other1" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other1" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other1" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event <input type=text class=forminput name=other2text size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="other2" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="other2" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="other2" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="other2" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="other2" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<th>Multi-annual and decadal events</th><th><span style="float:right;">not interesting ... very important&nbsp;&nbsp;</span></th>
</tr><tr>
<td><span style="float:left">Less Arctic sea ice 2005-2012</span></td>
<td><span style="float:right;">
<input type="radio" name="lessseaicearctic" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="lessseaicearctic" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="lessseaicearctic" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="lessseaicearctic" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="lessseaicearctic" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Warm summers in Europe 2002-2012</span></td>
<td><span style="float:right;">
<input type="radio" name="warmsummerseurope2000s" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="warmsummerseurope2000s" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="warmsummerseurope2000s" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="warmsummerseurope2000s" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="warmsummerseurope2000s" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Dry winters in the eastern mediterranean 1990-2012</span></td>
<td><span style="float:right;">
<input type="radio" name="drywinterseastmediterranean" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="drywinterseastmediterranean" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="drywinterseastmediterranean" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="drywinterseastmediterranean" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="drywinterseastmediterranean" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Warmer North Atlantic Ocean since 1995</span></td>
<td><span style="float:right;">
<input type="radio" name="warmernorthatlantic" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="warmernorthatlantic" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="warmernorthatlantic" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="warmernorthatlantic" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="warmernorthatlantic" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">More Atlantic hurricanes since 1995</span></td>
<td><span style="float:right;">
<input type="radio" name="moreatlantichurricanes" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="moreatlantichurricanes" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="moreatlantichurricanes" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="moreatlantichurricanes" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="moreatlantichurricanes" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Pacific climate shift around 1976</span></td>
<td><span style="float:right;">
<input type="radio" name="1976pacificclimateshift" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="1976pacificclimateshift" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="1976pacificclimateshift" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="1976pacificclimateshift" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="1976pacificclimateshift" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Sahel drought starting around 1970</span></td>
<td><span style="float:right;">
<input type="radio" name="saheldrought" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="saheldrought" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="saheldrought" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="saheldrought" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="saheldrought" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Cold winters in Europe in the 1960s</span></td>
<td><span style="float:right;">
<input type="radio" name="coldwinterseurope1960s" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="coldwinterseurope1960s" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="coldwinterseurope1960s" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="coldwinterseurope1960s" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="coldwinterseurope1960s" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr><tr>
<td><span style="float:left">Other event <input type=text class=forminput name=otherdectext size=35></span></td>
<td><span style="float:right;">
<input type="radio" name="otherdec" class="formradio" value="1" checked>1&nbsp;&nbsp;
<input type="radio" name="otherdec" class="formradio" value="2">2&nbsp;&nbsp;
<input type="radio" name="otherdec" class="formradio" value="3">3&nbsp;&nbsp;
<input type="radio" name="otherdec" class="formradio" value="4">4&nbsp;&nbsp;
<input type="radio" name="otherdec" class="formradio" value="5">5&nbsp;&nbsp;
</span></td>
</tr>
</table>
<p>
<div class=formheader>
<input type="submit" value="submit form" class="formbutton">
</div>
<!-- footer starts here -->
         </div>
         </div>
<!-- Insert the body of the page above this line -->
      </td>
   </tr>
</table>
EOF
cat ./vinklude/bottom_en.html
cat <<EOF
</body>
</html>
EOF
