#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
. ./init.cgi
. ./searchengine.cgi
. ./myvinkhead.cgi "Climate Explorer results" "Effects of El Ni&ntilde;o on world weather" "index,follow"

cat | sed -e "s/FORM_EMAIL/$EMAIL/" <<EOF
         <div class="subkop"></div>
         <div class="inhoudsopgave">
           <div class="inhoudlink"><a href="#precipitation">Precipitation</a></div>
           <div class="inhoudlink"><a href="#temperature">Temperature</a></div>
           <div class="inhoudlink"><a href="#cyclones">Tropical Cyclones</a></div>
         </div>
	 <p>
         <span class="inleiding">El Ni&ntilde;o</a> affects the
         weather in large parts of the world.  The effects depend
         strongly on the location and the season.  The strongest
         effects on precipitation are in South-East Asia and the
         western Pacifc Ocean, especially in the dry season
         (August-November).  There are temperature effects throughout
         most of the tropics.  The number of tropical cyclones also
         depends on El Ni&ntilde;o in most basins.  In boreal winter
         the effects are most wide-spread: from southern Africa to
         eastern Russia and most of the Americas.</span>

<p>For the four meteorological seasons we computed how El Ni&ntilde;o
and La Ni&ntilde;a perturbed the average weather of the last century.
We used the GPCC V7 analysis of monthly mean precipitation and the 
CRU TS 3.22 analysis of temperature.</span>

<div class="alineakop"><a name="precipitation"></a>Precipitation</div>

Blue colours indicate that during El Ni&ntilde;o there was, on
average, more rain than normal, red colours indicate drought during El
Ni&ntilde;o.  La Ni&ntilde;a has the opposite effect in almost all
locations. As a measure of the strength of the relationship we used the 
correlation coefficient with the Ni&ntilde;o3.4 index. The square of this 
number gives the fraction of the variance that is explained by this aspect
of El Ni&ntilde;o.

<div class="bijschrift"><b>March-May</b> In boreal spring the
strongest effects are in the western Pacific Ocean: along the equator
rainfall increases during El Ni&ntilde; and at 10&deg;-15&deg; North
and South rainfall decreases.  The north of Mexico and the desert
states of the U.S. usually get more rain.  The North-East of Brasil
often stays drier than usual during El Ni&ntilde;o.  Even in our part
of Europe it rains more on average during El Ni&ntilde;o.</div>

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_gpcc_25_n1_MAM.png" alt="Relationship between El Ni&ntilde;o and rainfall in March-May" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>June-August</b> In these months eastern
Indonesia often suffers droughts during El Ni&ntilde;o.  The rain zone
has moved east to the islands along the equator in the Pacific Ocean.
The Indian Monsoon is often weaker during El Ni&ntilde;o, although by
no means always.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_gpcc_25_n1_JJA.png" 
alt="Relationship between El Ni&ntilde;o and rainfall in June-August" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>September-November</b> This season the
effects of El Ni&ntilde;o are strongest.  Almost all of Indonesia, the
Philippines and eastern Australia are drier than usual during most El
Ni&ntilde;o events.  Large parts of India are often drier than usual,
but the Sri Lanka and some southern states get more rain.  East
Africa, parts of Central Asia and Spain are also on average wetter
than normal during El Ni&ntilde;o in this season, as are Chili and
Uruguay.</div>

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_gpcc_25_n1_SON.png" alt="Relationship between El Ni&ntilde;o and rainfall in September-November" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>December-February</b> In boreal winter the
Philippines and East Indonesia stay drier, whereas the Pacific islands
along the equator remain wetter.  Florida also gets more rain than
normal during El Ni&ntilde;o, this effect extends to other southern
states of the U.S. and into Mexico.  South Africa is more frequently
dry, as is the northern coast of South America and some of the leeward
Antilles.  In Uruguay en South Brasil rainfall increases on average.
Along the coasts of Ecuador and Peru rainfall increases when the
coastal waters heat up, an effect also named El Ni&ntilde;o but not
always coincident with the warming along the equator that affects the
rest of the world.

<Center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_gpcc_25_n1_DJF.png" 
alt="Relationship between El Ni&ntilde;o and rainfall in December-February" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="alineakop"><a name="temperature"></a>Temperature</div>

In the temperature maps, red colours denote locations that on
average are warmer during El Ni&ntilde;o and cooler during La
Ni&ntilde;a.  Blue colours are colder during El Ni&ntilde;o and/or
warmer during La Ni&ntilde;a.  Some North America effects are
non-linear: the effect of La Ni&ntilde;a is not the opposite of the
effect of El Ni&ntilde;o.

<div class="bijschrift"><b>March-May</b> In this season El Ni&ntilde;o
causes warmer weather in most of the tropics.  The north-western coast
of North America is also warmer than usual.  In constrast, the
south-east of the U.S. and north-eastern Mexico are often warmer
during La Ni&ntilde;a.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_cru_tmp_25_MAM.png" 
alt="Relationship between El Ni&ntilde;o and temperature in March-May" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>June-August</b> The heat signal is very
clear in India, West Africa and eastern South America.  Summer in 
East-Asia and eastern Canada is often somewhat cooler than normal.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_cru_tmp_25_JJA.png" 
alt="Relationship between El Ni&ntilde;o and temperature in Jun-August" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>September-November</b> The east coast of
Central and South America, India and southern Australia are often
warmer during El Ni&ntilde;o.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_cru_tmp_25_SON.png" 
alt="Relationship between El Ni&ntilde;o and temperature in September-November" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="bijschrift"><b>December-February</b> The effects of El
Ni&ntilde;o on temperature are clearest in boreal winter, when El
Ni&ntilde;o normally is strongest.  Northern North and South 
America, Australia and also southern Africa usually have warmer
weather than normal during El Ni&ntilde;o.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_cru_tmp_25_DJF.png" 
alt="Relationship between El Ni&ntilde;o and temperature in December-February" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<div class="alineakop"><a name="cyclones"></a>Tropical Cyclones</div>

During El Ni&ntilde;o there are on average fewer hurricanes over
the Atlantic Ocean, the Caribian Sea and the Gulf of Mexico.  La
Ni&ntilde;a often brings more.  The west coast of Mexico and the
United States see more landfalling hurricanes during El Ni&ntilde;o.
In the central Pacific Ocean El Ni&ntilde;o brings more typhoons,
both north and south of the equator.  Their more easterly genesis
makes that fewer of these tropical cyclones reach Australia.  In the
northern Pacific Ocean the area with typhoons also shifts east.  Ther
are no effects on the number of cyclones over the Indian Ocean.

<center>
<div style="font-size:10px; width=451px;">
<img src="effects/nino34_nstracks.png" 
alt="Relationship between El Ni&ntilde;o and the number of tropical stroms" border=0 width=430 class="realimage" hspace=0 vspace=0>
<br clear=all>
</div>
</center>

<!-- Insert the body of the page above this line -->
      </td>
      <td width="11">&nbsp;</td>
      <td width=220 valign=top>
<!-- Voeg hieronder de lijst met links in -->
         <div class="menukopje">Standard seasons</div>
         <div class="menulink">Precipitation, temperature and tropical storms</div>

         <div class="menukopje">Other seasons</div>
         <div class="menulink"><a href="monthly_precipitation_effects.cgi?id=FORM_EMAIL">Monthly precipitation</a></div>
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