#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
. ./init.cgi
. ./searchengine.cgi
. ./myvinkhead.cgi "Climate Explorer results" "Effects of El Ni&ntilde;o on world weather: all seasons" "index,follow"

cat | sed -e "s/FORM_EMAIL/$EMAIL/" <<EOF
         El Ni&ntilde;o</a> affects the
         weather in large parts of the world.  The effects depend
         strongly on the location and the season.  We have studied the
         HadCRUT4 analyses of sea surface temperature and 2-meter
         temperature over land. As a measure of the strength of the 
         relationship we used the correlation coefficient with the 
         Ni&ntilde;o3.4 index. The square of this number gives the 
         fraction of the variance that is explained by this aspect
         of El Ni&ntilde;o.

<div class="alineakop"><a name="temperature"></a>Temperature</div>

In the temperature maps, red colours denote locations that on
average are warmer during El Ni&ntilde;o and cooler during La
Ni&ntilde;a.  Blue colours are colder during El Ni&ntilde;o and/or
warmer during La Ni&ntilde;a.  Some North America effects are
non-linear: the effect of La Ni&ntilde;a is not the opposite of the
effect of El Ni&ntilde;o.

<center>
<div style="font-size:10px; width=451px;">
<a href="effects/nino34_had4_krig_v2_JFM.pdf"><img src="effects/nino34_had4_krig_v2_JFM.png" alt="Relationship between El Ni&ntilde;o and temperature in January-March" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_FMA.pdf"><img src="effects/nino34_had4_krig_v2_FMA.png" alt="Relationship between El Ni&ntilde;o and temperature in February-April" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_MAM.pdf"><img src="effects/nino34_had4_krig_v2_MAM.png" alt="Relationship between El Ni&ntilde;o and temperature in March-May" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_AMJ.pdf"><img src="effects/nino34_had4_krig_v2_AMJ.png" alt="Relationship between El Ni&ntilde;o and temperature in April-June" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_MJJ.pdf"><img src="effects/nino34_had4_krig_v2_MJJ.png" alt="Relationship between El Ni&ntilde;o and temperature in May-July" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_JJA.pdf"><img src="effects/nino34_had4_krig_v2_JJA.png" alt="Relationship between El Ni&ntilde;o and temperature in June-August" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_JAS.pdf"><img src="effects/nino34_had4_krig_v2_JAS.png" alt="Relationship between El Ni&ntilde;o and temperature in July-September" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_ASO.pdf"><img src="effects/nino34_had4_krig_v2_ASO.png" alt="Relationship between El Ni&ntilde;o and temperature in August-October" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_SON.pdf"><img src="effects/nino34_had4_krig_v2_SON.png" alt="Relationship between El Ni&ntilde;o and temperature in September-November" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_OND.pdf"><img src="effects/nino34_had4_krig_v2_OND.png" alt="Relationship between El Ni&ntilde;o and temperature in October-December" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_NDJ.pdf"><img src="effects/nino34_had4_krig_v2_NDJ.png" alt="Relationship between El Ni&ntilde;o and temperature in November-January" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_DJF.pdf"><img src="effects/nino34_had4_krig_v2_DJF.png" alt="Relationship between El Ni&ntilde;o and temperature in December-February" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
</div>
</center>


<!-- Insert the body of the page above this line -->
      </td>
      <td width="11">&nbsp;</td>
      <td width=220 valign=top>
<!-- Voeg hieronder de lijst met links in -->
         <div class="menukopje">Standard seasons</div>
         <div class="menulink"><a href="effects.cgi?id=FORM_EMAIL">Precipitation, temperature and tropical storms</a></div>

         <div class="menukopje">Other seasons</div>
         <div class="menulink"><a href="monthly_precipitation_effects.cgi?id=FORM_EMAIL">Monthly precipitation</a></div>
         <div class="menulink"><a href="seasonal_precipitation_effects.cgi?id=FORM_EMAIL">Seasonal precipitation</a></div>
         <div class="menulink"><a href="monthly_temperature_effects.cgi?id=FORM_EMAIL">Monthly temperature</a></div>
         <div class="menulink">Seasonal temperature</div>
<!-- Insert the link list above this line -->
      </td>
   </tr>
</table>
EOF

cat ./vinklude/bottom_en.html
 cat <<EOF
</body>
</html>
EOF