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
         GPCC V7 analyses of precipitation over land. White areas did 
         not have enough data. As a measure of the strength of the 
         relationship we used the correlation coefficient with the 
         Ni&ntilde;o3.4 index. The square of this number gives the 
         fraction of the variance that is explained by this aspect
         of El Ni&ntilde;o.

<div class="alineakop"><a name="precipitation"></a>Precipitation</div>

Blue colours indicate that during El Ni&ntilde;o there was, on
average, more rain than normal, red colours indicate drought during El
Ni&ntilde;o.  La Ni&ntilde;a has the opposite effect in almost all
locations. 

<center>
<a href="effects/nino34_gpcc_25_n1_jan.pdf"><img src="effects/nino34_gpcc_25_n1_jan.png" alt="Relationship between El Ni&ntilde;o and precipitation in January" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_feb.pdf"><img src="effects/nino34_gpcc_25_n1_feb.png" alt="Relationship between El Ni&ntilde;o and precipitation in February" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_mar.pdf"><img src="effects/nino34_gpcc_25_n1_mar.png" alt="Relationship between El Ni&ntilde;o and precipitation in March" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_apr.pdf"><img src="effects/nino34_gpcc_25_n1_apr.png" alt="Relationship between El Ni&ntilde;o and precipitation in April" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_may.pdf"><img src="effects/nino34_gpcc_25_n1_may.png" alt="Relationship between El Ni&ntilde;o and precipitation in May" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_jun.pdf"><img src="effects/nino34_gpcc_25_n1_jun.png" alt="Relationship between El Ni&ntilde;o and precipitation in June" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_jul.pdf"><img src="effects/nino34_gpcc_25_n1_jul.png" alt="Relationship between El Ni&ntilde;o and precipitation in July" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_aug.pdf"><img src="effects/nino34_gpcc_25_n1_aug.png" alt="Relationship between El Ni&ntilde;o and precipitation in August" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_sep.pdf"><img src="effects/nino34_gpcc_25_n1_sep.png" alt="Relationship between El Ni&ntilde;o and precipitation in September" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_oct.pdf"><img src="effects/nino34_gpcc_25_n1_oct.png" alt="Relationship between El Ni&ntilde;o and precipitation in October" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_nov.pdf"><img src="effects/nino34_gpcc_25_n1_nov.png" alt="Relationship between El Ni&ntilde;o and precipitation in November" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
<a href="effects/nino34_gpcc_25_n1_dec.pdf"><img src="effects/nino34_gpcc_25_n1_dec.png" alt="Relationship between El Ni&ntilde;o and precipitation in December" border=0 width="100%" class="realimage" hspace=0 vspace=0></a>
<br>
</center>


<!-- Insert the body of the page above this line -->
      </td>
      <td width="1%">&nbsp;</td>
      <td width="27.5%" valign=top>
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