#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
. ./init.cgi
. ./searchengine.cgi
. ./myvinkhead.cgi "Climate Explorer results" "Effects of El Ni&ntilde;o on world weather: all months" "index,follow"

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
<a href="effects/nino34_had4_krig_v2_jan.pdf"><img src="effects/nino34_had4_krig_v2_jan.png" alt="relationship between El Ni&ntilde;o and temperature in January" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_feb.pdf"><img src="effects/nino34_had4_krig_v2_feb.png" alt="relationship between El Ni&ntilde;o and temperature in February" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_mar.pdf"><img src="effects/nino34_had4_krig_v2_mar.png" alt="relationship between El Ni&ntilde;o and temperature in March" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_apr.pdf"><img src="effects/nino34_had4_krig_v2_apr.png" alt="relationship between El Ni&ntilde;o and temperature in April" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_may.pdf"><img src="effects/nino34_had4_krig_v2_may.png" alt="relationship between El Ni&ntilde;o and temperature in May" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_jun.pdf"><img src="effects/nino34_had4_krig_v2_jun.png" alt="relationship between El Ni&ntilde;o and temperature in June" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_jul.pdf"><img src="effects/nino34_had4_krig_v2_jul.png" alt="relationship between El Ni&ntilde;o and temperature in July" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_aug.pdf"><img src="effects/nino34_had4_krig_v2_aug.png" alt="relationship between El Ni&ntilde;o and temperature in August" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_sep.pdf"><img src="effects/nino34_had4_krig_v2_sep.png" alt="relationship between El Ni&ntilde;o and temperature in September" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_oct.pdf"><img src="effects/nino34_had4_krig_v2_oct.png" alt="relationship between El Ni&ntilde;o and temperature in October" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_nov.pdf"><img src="effects/nino34_had4_krig_v2_nov.png" alt="relationship between El Ni&ntilde;o and temperature in November" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_had4_krig_v2_dec.pdf"><img src="effects/nino34_had4_krig_v2_dec.png" alt="relationship between El Ni&ntilde;o and temperature in December" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
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
         <div class="menulink">Monthly temperature</div>
         <div class="menulink"><a href="seasonal_temperature_effects.cgi?id=FORM_EMAIL">Seasonal temperature</a></div>
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