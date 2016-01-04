<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- beheerder: Geert Jan van Oldenborgh -->
<head>
<link rel="stylesheet" href="/styles/rccstyle.css" type="text/css">
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<link rel="shortcut icon" href="/favicon.ico" /> 
<script language="javascript" src="/library/javascript/pop_picture.js"></script>
<META HTTP-EQUIV='imagetoolbar' CONTENT='no'>
<!-- Vul na de &lt;title&gt;-tag de titel van de pagina in -->
<title>
Maandverwachtingen
</title>
<!-- Insert the title of the page above the &lt;/title&gt;-tag -->
</head>
<body>
<?php
include $_SERVER["DOCUMENT_ROOT"].'/vinklude/rcc_pagehead.html';
?>
<table border="0" width="95.25%" cellspacing="0" cellpadding="0">
   <tr>
      <td width="10%">&nbsp;</td>
      <td width="56.375%" valign=top>
         <div id="printable" name="printable">
         <!-- div -->
<!-- Voeg hieronder de inhoud van de pagina in -->
         <div class="rubriekkop">Klimaat</div>
         <div class="hoofdkop">Maandverwachtingen</div>
         <div class="subkop">Experimenteel</div>
<!--         <div class="inhoudsopgave">
           <div class="inhoudlink"><a href="#inleiding">Inleiding</a></div>
         </div> -->
	 <p>
<a name="inleiding"></a>
<!--         <span class="inleiding">  -->
<!-- </span>  -->

<div class="alineakop"><a name="temperatuur"></a>Temperatuur in Nederland</div>

De temperatuur van de komende maand in Nederland wordt be&iuml;nvloed door de verwachte temperatuur van de komende week, en de temperatuur van de afgelopen maand (hoofdzakelijk via de Noordzee).

<div class="bijschrift">Verwachte maximumtemperatuur in De Bilt de komende vier weken.  De verticale lijnen van het weekgemiddelde geven het interval aan waarin de temperatuur zou moeten liggen met 50% (dik) resp 80% (dun) kans. De gestippelde lijn is normaal (het 10-daags gemiddelde over 1981-2010), de blauwe lijn zijn de dagelijkse waarnemingen en de rode lijn de weekgemiddelden.</div>
<center>
<img src="tx260.png" alt="Maximum temperatuur in De Bilt de komende vier weken" title="Maximum temperatuur in De Bilt de komende vier weken" border=0 class="realimage" hspace=0 vspace=0>
<?php
$filemtime = filemtime(dirname($_SERVER['SCRIPT_FILENAME'])."/tx260.png");
echo "<div class=datumtijd>Bijgewerkt: ".date ("d F Y H:i",$filemtime)." UTC</div>";
?>
<br>
</center>

<div class="bijschrift">Maximum, daggemiddelde en minimum temperatuur op de 6 hoofdstations de komende vier weken.</div>

<table class="onelinetable" width="100%" border=0 cellpadding=0 cellspacing=0>
<tr class="trcolor">
<th width="33%">Maximum temperatuur</th>
<th width="33%">Gemiddelde temperatuur</th>
<th width="33%">Minimum temperatuur</th>
</tr>
<?php
$stations = array('235' => 'Den Helder', '260' => 'De Bilt', '280' => 'Groningen', '290' => 'Twenthe', '310' => 'Vlissingen', '380' => 'Maastricht');
$elementen = array('tx' => 'Maximum Temperatuur', 'tg' => 'Gemiddelde Temperatuur', 'tn' => 'Minimum Temperatuur');
foreach ($stations as $stat_id => $stat_naam) { 
   echo '
<tr>
<td colspan="3"><a name="'.$stat_naam.'"></a>'.$stat_naam.'</td>
</tr>
<tr>';
   foreach ($elementen as $elem_id => $elem_naam) { 
      echo '
<td width="33%">
<script language="JavaScript">
<!--
document.write("<a href=\"javascript:pop_picture(\''.$elem_id.$stat_id.'.png\', \'copyright\')\">");
-->
</script>
<noscript>
<a href="'.$elem_id.$stat_id.'.png" target="picture">
</noscript>
<img src="'.$elem_id.$stat_id.'.png" width="100%" alt="'.$elem_naam.' '.$stat_naam.'" title="'.$elem_naam.' '.$stat_naam.'" border=0 class="realimage" hspace=0 vspace=0></a>
</td>
   ';
   }
   echo '</tr>';
}
?>
</table>

         <p><div class="noot">Dit is een experimentele pagina, de tijdige beschikbaarheid kan niet gegarandeerd worden.</div>
         </div>
<!-- Insert the body of the page above this line -->
      </td>
      <td width="1%">&nbsp;</td>
      <td width="27.5%" valign=top>
<!-- Voeg hieronder de lijst met links in -->
<?php
include dirname($_SERVER["SCRIPT_FILENAME"]).'/../menu_Verwachtingen.html';
?>
       <div class="menukopje">Verificatie experimentele maandverwachtingen</div>
       <div class="menulink"><a href="verificatie.html">Hoe zijn deze verwachtingen uitgekomen?</a></div>
<!-- Insert the link list above this line -->
      </td>
   </tr>
</table>

<?php
include $_SERVER["DOCUMENT_ROOT"].'/vinklude/bottom_en.html';
?>
</body>
</html>


