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
         HadCRUT2 analyses of sea surface temperature and 2-meter
         temperature over land with at least 35 years of data, and
         investigated how these observations correlate with the
         Ni&ntilde;o3.4 index that describes the strength of El
         Ni&ntilde;o and La Ni&ntilde;a.

<div class="alineakop"><a name="temperature"></a>Temperature</div>

<p>The colours encode the strength of the relationship with El
Ni&ntilde;o and La Ni&ntilde;a.  Red areas are almost always warmer
during El Ni&ntilde;a and colder during La Ni&ntilde;a.  In the dark
orange areas El Ni&ntilde;o determines about half the variability, in
the liht orange areas one quarter.  In the dark green areas it is
often colder during El Ni&ntilde;o or warmer during La Ni&ntilde;a.
In North America the effect is non-linear.

<center>
<div style="font-size:10px; width=451px;">
<a href="effects/nino34_hadcrut2_jan.pdf"><img src="effects/nino34_hadcrut2_jan.png" alt="relationship between El Ni&ntilde;o and temperature in January" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_feb.pdf"><img src="effects/nino34_hadcrut2_feb.png" alt="relationship between El Ni&ntilde;o and temperature in February" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_mar.pdf"><img src="effects/nino34_hadcrut2_mar.png" alt="relationship between El Ni&ntilde;o and temperature in March" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_apr.pdf"><img src="effects/nino34_hadcrut2_apr.png" alt="relationship between El Ni&ntilde;o and temperature in April" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_may.pdf"><img src="effects/nino34_hadcrut2_may.png" alt="relationship between El Ni&ntilde;o and temperature in May" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_jun.pdf"><img src="effects/nino34_hadcrut2_jun.png" alt="relationship between El Ni&ntilde;o and temperature in June" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_jul.pdf"><img src="effects/nino34_hadcrut2_jul.png" alt="relationship between El Ni&ntilde;o and temperature in July" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_aug.pdf"><img src="effects/nino34_hadcrut2_aug.png" alt="relationship between El Ni&ntilde;o and temperature in August" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_sep.pdf"><img src="effects/nino34_hadcrut2_sep.png" alt="relationship between El Ni&ntilde;o and temperature in September" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_oct.pdf"><img src="effects/nino34_hadcrut2_oct.png" alt="relationship between El Ni&ntilde;o and temperature in October" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_nov.pdf"><img src="effects/nino34_hadcrut2_nov.png" alt="relationship between El Ni&ntilde;o and temperature in November" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_hadcrut2_dec.pdf"><img src="effects/nino34_hadcrut2_dec.png" alt="relationship between El Ni&ntilde;o and temperature in December" border=0 class="realimage" hspace=0 vspace=0></a>
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