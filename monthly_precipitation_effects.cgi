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
weather in large parts of the world.  Thjese effects depend
strongy on the location and season.  We have correlated the
observations from 1185 precipitation statons in the GHCN v2
database with at least 40 years of data and 2&deg; apart with
the Ni&ntilde;o3.4 index, which is a measure of the strength
of El Ni&ntilde;o and La Ni&ntilde;a. Lighter colours denote 
correlations that are not significant at p&lt;0.05.


<div class="alineakop"><a name="precipitation"></a>Precipitation</div>

<p>Blue circles indicate that during El Ni&ntilde;o there was, on
average, more rain than normal, red circles indicate drought during El
Ni&ntilde;o.  La Ni&ntilde;a has the opposite effect in almost all
locations.  The size of the circles is a measure of the strength of
the relationship.

<center>
<div style="font-size:10px; width=451px;">
<a href="effects/nino34_logprcp_jan.pdf"><img src="effects/nino34_logprcp_jan.png" alt="Relationship between El Ni&ntilde;o and precipitation in January" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_feb.pdf"><img src="effects/nino34_logprcp_feb.png" alt="Relationship between El Ni&ntilde;o and precipitation in February" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_mar.pdf"><img src="effects/nino34_logprcp_mar.png" alt="Relationship between El Ni&ntilde;o and precipitation in March" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_apr.pdf"><img src="effects/nino34_logprcp_apr.png" alt="Relationship between El Ni&ntilde;o and precipitation in April" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_may.pdf"><img src="effects/nino34_logprcp_may.png" alt="Relationship between El Ni&ntilde;o and precipitation in May" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_jun.pdf"><img src="effects/nino34_logprcp_jun.png" alt="Relationship between El Ni&ntilde;o and precipitation in June" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_jul.pdf"><img src="effects/nino34_logprcp_jul.png" alt="Relationship between El Ni&ntilde;o and precipitation in July" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_aug.pdf"><img src="effects/nino34_logprcp_aug.png" alt="Relationship between El Ni&ntilde;o and precipitation in August" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_sep.pdf"><img src="effects/nino34_logprcp_sep.png" alt="Relationship between El Ni&ntilde;o and precipitation in September" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_oct.pdf"><img src="effects/nino34_logprcp_oct.png" alt="Relationship between El Ni&ntilde;o and precipitation in October" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_nov.pdf"><img src="effects/nino34_logprcp_nov.png" alt="Relationship between El Ni&ntilde;o and precipitation in November" border=0 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_logprcp_dec.pdf"><img src="effects/nino34_logprcp_dec.png" alt="Relationship between El Ni&ntilde;o and precipitation in December" border=0 class="realimage" hspace=0 vspace=0></a>
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
         <div class="menulink">Monthly precipitation</div>
         <div class="menulink"><a href="seasonal_precipitation_effects.cgi?id=FORM_EMAIL">Seasonal precipitation</a></div>
         <div class="menulink"><a href="monthly_temperature_effects.cgi?id=FORM_EMAIL">Monthly temperature</a></div>
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