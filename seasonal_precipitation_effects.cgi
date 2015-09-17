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
<div style="font-size:10px; width=451px;">
<a href="effects/nino34_gpcc_25_n1_JFM.pdf"><img src="effects/nino34_gpcc_25_n1_JFM.png" alt="Relationship between El Ni&ntilde;o and precipitation in January-March" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_FMA.pdf"><img src="effects/nino34_gpcc_25_n1_FMA.png" alt="Relationship between El Ni&ntilde;o and precipitation in February-April" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_MAM.pdf"><img src="effects/nino34_gpcc_25_n1_MAM.png" alt="Relationship between El Ni&ntilde;o and precipitation in March-May" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_AMJ.pdf"><img src="effects/nino34_gpcc_25_n1_AMJ.png" alt="Relationship between El Ni&ntilde;o and precipitation in April-June" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_MJJ.pdf"><img src="effects/nino34_gpcc_25_n1_MJJ.png" alt="Relationship between El Ni&ntilde;o and precipitation in May-July" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_JJA.pdf"><img src="effects/nino34_gpcc_25_n1_JJA.png" alt="Relationship between El Ni&ntilde;o and precipitation in June-August" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_JAS.pdf"><img src="effects/nino34_gpcc_25_n1_JAS.png" alt="Relationship between El Ni&ntilde;o and precipitation in July-September" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_ASO.pdf"><img src="effects/nino34_gpcc_25_n1_ASO.png" alt="Relationship between El Ni&ntilde;o and precipitation in August-October" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_SON.pdf"><img src="effects/nino34_gpcc_25_n1_SON.png" alt="Relationship between El Ni&ntilde;o and precipitation in September-November" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_OND.pdf"><img src="effects/nino34_gpcc_25_n1_OND.png" alt="Relationship between El Ni&ntilde;o and precipitation in October-December" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_NDJ.pdf"><img src="effects/nino34_gpcc_25_n1_NDJ.png" alt="Relationship between El Ni&ntilde;o and precipitation in November-January" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
<br clear=all>
<a href="effects/nino34_gpcc_25_n1_DJF.pdf"><img src="effects/nino34_gpcc_25_n1_DJF.png" alt="Relationship between El Ni&ntilde;o and precipitation in December-February" border=0 width=430 class="realimage" hspace=0 vspace=0></a>
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
         <div class="menulink">Seasonal precipitation</div>
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