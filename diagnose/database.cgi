#!/bin/sh

interval="1981-2010"
climexpfield=""
climexpseries=""
verderlezen=""
prefix=""
postfix=""
case "$var" in
	slp_ncepncar) 
		if [ "$FORM_lang" = nl ]; then
			naam="luchtdruk (noordelijk halfrond)"
			bron="NCEP/NCAR heranalyse"
		else
			naam="sea-level pressure (northern hemisphere)"
			bron="NCEP/NCAR reanalysis"
		fi
		url=http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml
		climexpfield=nslp
		units=[mb]
		anomalie=ja;;
	z500_ncepncar)
		if [ "$FORM_lang" = nl ]; then
			naam="500mb hoogte (noordelijk halfrond)"
			bron="NCEP/NCAR heranalyse"
		else
			naam="500mb height (northern hemisphere)"
			bron="NCEP/NCAR reanalysis"
		fi
		url=http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml
		climexpfield=nz500
		units=[m]
		anomalie=ja;;
	z500_ncepncar_sh)
		if [ "$FORM_lang" = nl ]; then
			naam="500mb hoogte (zuidelijk halfrond)"
			bron="NCEP/NCAR heranalyse"
		else
			naam="500mb height (southern hemisphere)"
			bron="NCEP/NCAR reanalysis"
		fi
		url=http://www.cdc.noaa.gov/cdc/reanalysis/reanalysis.shtml
		climexpfield=nz500
		units=[m]
		anomalie=ja;;
	t2m_ghcncams)
		if [ "$FORM_lang" = nl ]; then
			naam="temperatuur (2m hoogte, noordelijk halfrond)"
		else
			naam="temperature (2m height, northern hemisphere)"
		fi
		bron="NCEP/CPC"
		url=ftp://ftp.cpc.ncep.noaa.gov/wd51yf/GHCN_CAMS/
		climexpfield=ghcn_cams_05
		units=[K]
		anomalie=ja;;
	t2m_ghcncams_w) 
		if [ "$FORM_lang" = nl ]; then
			naam="temperatuur (2m hoogte, wereld)"
		else
			naam="temperature (2m height, world)"
		fi
		bron="NCEP/CPC"
		url=ftp://ftp.cpc.ncep.noaa.gov/wd51yf/GHCN_CAMS/
		climexpfield=ghcn_cams_05
		units=[K]
		anomalie=ja;;
	tlt_uah)
		if [ "$FORM_lang" = nl ]; then
			naam="temperatuur van de lagere troposfeer"
			bron="Universiteit van Alabama, Huntsville"
		else
			naam="temperature of the lower troposphere"
			bron="University of Alabama, Huntsville"
		fi
		url=http://www.atmos.uah.edu/data/msu/
		climexpfield=tlt
		units=[K]
		anomalie=ja;;
	ssta|sst_ncep|sst_ncep_w)
		if [ "$FORM_lang" = nl ]; then	
			naam="zeewatertemperatuur"
		else
			naam="sea surface temperature"
		fi
		bron="NCEP"
		url=http://www.emc.ncep.noaa.gov/research/cmb/sst_analysis//
		climexpfield=sstoi_v2
		units=[Celsius]
		anomalie=ja;interval=1982-2010;;
	snow_noaa)
		if [ "$FORM_lang" = nl ]; then	
			naam="sneeuwbedekking (noordelijk halfrond)"
		else
			naam="snow cover (northern hemisphere)"
		fi
		bron="NOAA"
		url=http://www.cpc.noaa.gov/data/snow
		climexpfield=nhsnow
		units=[1]
		anomalie=ja;;
	snow_rucl)
		if [ "$FORM_lang" = nl ]; then	
			naam="sneeuwbedekking (noordelijk halfrond)"
		else
			naam="snow cover (northern hemisphere)"
		fi
		bron="Rutgers University"
		url=http://climate.rutgers.edu/snowcover/index.php
		climexpfield=rutgers_nhsnow
		units=[1]
		anomalie=ja;;
	ice_ncep)
		if [ "$FORM_lang" = nl ]; then	
			naam="zeeijsbedekking (noordelijk halfrond)"
		else
			naam="sea ice extent (northern hemisphere)"
		fi
		bron="NCEP"
		url=http://www.emc.ncep.noaa.gov/research/cmb/sst_analysis//
		climexpfield=ice_ncep
		units=[1]
		anomalie=ja;interval=1982-2000;;
	icen_nsidc)
		if [ "$FORM_lang" = nl ]; then	
			naam="zeeijsconcentratie (noordpoolgebied)"
			verderlezen="Zeeijs in het noordpoolgebied"
		verderlezenurl=http://www.knmi.nl/cms/content/66255/zeeijs_in_het_noordpoolgebied
		else
			naam="sea ice concentration (Arctic)"
		fi
		bron="NSIDC"
		url=http://nsidc.org/data/docs/daac/nsidc0051_gsfc_seaice.gd.html
		climexpfield=ice_index_n
		units=[1]
		anomalie=ja;;
	ices_nsidc)
		if [ "$FORM_lang" = nl ]; then	
			naam="zeeijsconcentratie (zuidpoolgebied)"
		else
			naam="sea ice concentration (Antarctic)"
		fi
		bron="NSIDC"
		url=http://nsidc.org/data/docs/daac/nsidc0051_gsfc_seaice.gd.html
		climexpfield=ice_index_s
		units=[1]
		anomalie=ja;;
	prcp_cmorph)
		if [ "$FORM_lang" = nl ]; then			
			naam="neerslag (satelliet)"
			units=[mm/dag]
			interval="1998-nu"
		else
			naam="precipitation (satellite)"
			units=[mm/day]
			interval="1998-now"
		fi
		bron="CMORPH"
		url=http://www.cpc.ncep.noaa.gov/products/janowiak/cmorph_description.html
		climexpfield=cmorph_monthly
		anomalie=nee;;
	prcp_gpcc)
		if [ "$FORM_lang" = nl ]; then			
			naam="neerslag (regenmeters)"
			units=[mm/maand]
			interval="1986-nu"
		else
			naam="precipitation (rain gauges)"
			units=[mm/month]
			interval="1986-now"
		fi
		bron="GPCC"
		url=ftp://ftp-anon.dwd.de/pub/data/gpcc/html/monitoring_download.html
		climexpfield=gpcc
		anomalie=nee;;
	o3nh_knmi)
		if [ "$FORM_lang" = nl ]; then			
			naam="ozon (noordelijk halfrond)"
		else
			naam="ozone (northern hemisphere)"
		fi
		bron="KNMI"
		url=http://temis.knmi.nl
		climexpfield=o3col
		units="[Dobson Units]"
		anomalie=ja;;
	o3sh_knmi)
		if [ "$FORM_lang" = nl ]; then			
			naam="ozon (zuidelijk halfrond)"
		else
			naam="ozone (southern hemisphere)"
		fi
		bron="KNMI"
		url=http://temis.knmi.nl
		climexpfield=o3col
		units="[Dobson Units]"
		anomalie=ja;;
	giss_al_gl_m)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde temperatuur"
		else
			naam="global mean temperature"
		fi
		bron=NASA/GISS
		url=http://data.giss.nasa.gov/gistemp/
		name=GISS_global_temperature
		climexpseries=NASAData/$var
		units=[Celsius];;
	giss_land)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde landtemperatuur"
		else
			naam="global mean land temperature"
		fi			
		bron=NASA/GISS
		url=http://data.giss.nasa.gov/gistemp/
		name=GISS_land_temperature
		climexpseries=NASAData/$var
		units=[Celsius];;
	hadcrut3_gl)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde temperatuur"
		else
			naam="global mean temperature"
		fi
		bron="CRU/UKMO"
		url=http://hadobs.metoffice.com/hadcrut3/diagnostics
		name=HadCRUT3_global_temperature
		climexpseries=UKMOData/$var
		units=[Celsius];;
	hadcrut4110_ns_avg)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde temperatuur"
		else
			naam="global mean temperature"
		fi
		bron="CRU/UKMO"
		url=http://www.metoffice.gov.uk/hadobs/hadcrut4/
		name=HadCRUT4_global_temperature
		climexpseries=UKMOData/$var
		units=[Celsius];;
	crutem3gl|crutem4gl)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde landtemperatuur"
		else
			naam="global mean land temperature"
		fi			
		bron="CRU"
		url=http://www.cru.uea.ac.uk/cru/data/temperature/
		name=CRUTEM4_land_temperature
		climexpseries=CRUData/$var;;
	ncdc_gl)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde temperatuur"
		else
			naam="global mean temperature"
		fi
		bron=NCDC
		url=http://www.ncdc.noaa.gov/cmb-faq/anomalies.html
		name=NCDC_global_temperature
		climexpseries=NCDCData/$var
		units=[Celsius];;
	ncdc_gl_land)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde landtemperatuur"
		else
			naam="global mean land temperature"
		fi			
		bron=NCDC
		url=http://www.ncdc.noaa.gov/cmb-faq/anomalies.html
		name=NCDC_global_land_temperature
		climexpseries=NCDCData/$var
		units=[Celsius];;
	erai_t2msst_gl)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde temperatuur"
		else
			naam="global mean temperature"
		fi
		bron=ECMWF
		url=http://www.ecmwf.int/research/era/
		name=ERAi_global_temperature
		climexpseries=ERA-interim/$var
		units=[Celsius];;
	erai_t2m_landnoice)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde landtemperatuur"
		else
			naam="global mean land temperature"
		fi
		bron=ECMWF
		url=http://www.ecmwf.int/research/era/
		name=ERAi_global_land_temperature
		climexpseries=ERA-interim/$var
		units=[Celsius];;
	tlt_gl) naam="wereldgemiddelde	temperatuur"
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddelde troposfeer temperatuur"
			bron="Universiteit van Alabama, Huntsville"
		else
			naam="global mean troposphere temperature"
			bron="University of Alabama, Huntsville"
		fi			
		url=http://climexp.knmi.nl/wipefeet.cgi?http://www.atmos.uah.edu/data/msu/
		name=TLT
		climexpseries=UAHData/$var
		units=[Celsius];;
	sl_ib_global|sl_global)
		if [ "$FORM_lang" = nl ]; then			
			naam="wereldgemiddeld zeeniveau"
		else
			naam="global mean sea level"
		fi
		bron="University of Colorado at Boulder"
		url=http://sealevel.colorado.edu/results.php
		name="global_sealevel"
		verderlezen="Gemeten zeespiegelveranderingen"
		verderlezenurl=http://www.knmi.nl/cms/content/73921/gemeten_zeespiegelveranderingen
		climexpseries=CUData/$var
		units=[mm];;
	N_ice_area)
		if [ "$FORM_lang" = nl ]; then			
			naam="zeeijsoppervlakte (noordpool)"
			units="[miljoen km<sup>2</sup>]"
			verderlezen="Zeeijs in het noordpoolgebied"
			verderlezenurl=http://www.knmi.nl/cms/content/66255/zeeijs_in_het_noordpoolgebied
		else
			naam="sea ice area (Arctic)"
			units="[million km<sup>2</sup>]"
		fi
		bron="NSIDC"
		url=http://nsidc.org/data/g02135.html
		prefix=tsi;postfix=season
		name="NH_seaice_area"
		climexpseries=NSIDCData/$var;;
	S_ice_area)
		if [ "$FORM_lang" = nl ]; then			
			naam="zeeijsoppervlakte (zuidpool)"
			units="[miljoen km<sup>2</sup>]"
		else
			naam="sea ice area (Antarctic)"
			units="[million km<sup>2</sup>]"
		fi
		bron="NSIDC"
		url=http://nsidc.org/data/g02135.html
		prefix=tsi;postfix=season
		name="SH_seaice_area"
		climexpseries=NSIDCData/$var;;
	cnt)
		if [ "$FORM_lang" = nl ]; then			
			naam="Centraal Nederland Temperatuur"
			verderlezen="Temperatuur reeksen"
			verderlezenurl=http://www.knmi.nl/cms/content/71466/temperatuur_reeksen
		else
			naam="Central Netherlands Temperature"
		fi
		bron=KNMI
		url=http://www.knmi.nl/publications/fulltexts/CNT.pdf
		prefix=tsi;postfix=season
		name=CNT
		climexpseries=KNMIData/$var
		units=[Celsius];;
	nino5)
		if [ "$FORM_lang" = nl ]; then			
			verderlezen="El Ni&ntilde;o en La Ni&ntilde;a"
		verderlezenurl=http://www.knmi.nl/cms/content/72473/el_nino_en_la_nina
		fi
		naam="Ni&ntilde;o 3.4 index"
		bron="NCEP"
		url=http://www.cpc.noaa.gov/data/indices/
		name=NINO3.4
		climexpseries=NCEPData/$var
		units=[Celsius];;
	nino2)
		naam="Ni&ntilde;o 12 index"
		bron="NCEP"
		url=http://www.cpc.noaa.gov/data/indices/
		name=NINO12
		climexpseries=NCEPData/nino2
		units=[Celsius];;
	cpc_nao)
		if [ "$FORM_lang" = nl ]; then			
			naam="Noord-Atlantische Oscillatie"
			verderlezen="De Noord-Atlantische Oscillatie"
		verderlezenurl=http://www.knmi.nl/cms/content/72634/de_noord-atlantische_oscillatie
		else
			naam="North Atlantic Oscillation"
		fi
		bron=NCEP
		url=http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/nao.shtml
		name=CPC_NAO
		prefix=tsi;postfix=season
		climexpseries=NCEPData/$var
		units=[1];;
	snao_ncepncar)
		if [ "$FORM_lang" = nl ]; then			
			naam="Zomer Noord-Atlantische Oscillatie"
		else
			naam="Summer North Atlantic Oscillation"
		fi
		bron="KNMI/NCEPNCAR"
		url=http://www.knmi.nl/publications/fulltexts/clidyd11001301.pdf
		name=SNAO
		prefix=tsi;postfix=season
		climexpseries=NCEPNCAR40/$var
		units=[1];;
	nh_snow)
		if [ "$FORM_lang" = nl ]; then			
			naam="sneeuwbedekking (noordelijk halfrond)"
			units="[miljoen km<sup>2</sup>]"
		else
			naam="snow cover (northern hemisphere)"
			units="[million km<sup>2</sup>]"
		fi
		bron="Rutgers University"
		url=http://climate.rutgers.edu/snowcover/table_area.php?ui_set=2
		prefix=tsi;postfix=season
		name=NH_snow_cover
		climexpseries=RutgersData/$var;;
	maunaloa_f)
		if [ "$FORM_lang" = nl ]; then			
			naam="CO2 concentratie"
			verderlezen="Stijging broeikasgas concentraties"
		verderlezenurl=http://www.knmi.nl/cms/content/66958/4._stijging_broeikasgas_concentraties
		else
			naam="CO2 concentration"
		fi
		bron=CDIAC
		url=http://www.esrl.noaa.gov/gmd/ccgg/trends/
		name=Mauna_Loa_CO2
		climexpseries=CDIACData/$var
		units=[ppm];;
	maunaloa_ch4)
		if [ "$FORM_lang" = nl ]; then			
			naam="CH4 concentratie"
			verderlezen="Stijging broeikasgas concentraties"
		verderlezenurl=http://www.knmi.nl/cms/content/66958/4._stijging_broeikasgas_concentraties
		else
			naam="CH4 concentration"
		fi
		bron=ESRL
		url=http://www.esrl.noaa.gov/gmd/
		name=
		climexpseries=CDIACData/$var
		units=[ppb];;
	tsi)
		if [ "$FORM_lang" = nl ]; then	
			naam="zonneconstante"
		else
			naam="solar constant"
		fi
		bron=PMOD
		url=http://www.pmodwrc.ch/pmod.php?topic=tsi/composite/SolarConstant
		name=measured_total_solar_irradiance
		climexpseries=PMODData/$var
		units="[W/m<sup>2</sup>]";;
	sunspots)
		if [ "$FORM_lang" = nl ]; then	
			naam="zonnevlekkengetal"
		else
			naam="sunspot number"
		fi
		bron=SIDC
		name=sunspots
		url=http://sidc.oma.be
		climexpseries=SIDCData/$var
		units=[1];;
	tg_eobs)
		if [ "$FORM_lang" = nl ]; then	
			naam="daggemiddelde temperatuur"
		else
			naam="daily mean temperature"
		fi
		bron="ECA&amp;D E-OBS"
		url="http://eca.knmi.nl/download/ensembles/ensembles.php"
		climexpfield="ensembles_05_tg_mo"
		units="[Celsius]"
		anomalie=ja;;
	tx_eobs)
		if [ "$FORM_lang" = nl ]; then	
			naam="maximum temperatuur"
		else
			naam="maximum temperature"
		fi
		bron="ECA&amp;D E-OBS"
		url="http://eca.knmi.nl/download/ensembles/ensembles.php"
		climexpfield="ensembles_05_tx_mo"
		units="[Celsius]"
		anomalie=ja;;
	tn_eobs)
		if [ "$FORM_lang" = nl ]; then	
			naam="minimum temperatuur"
		else
			naam="minimum temperature"
		fi
		bron="ECA&amp;D E-OBS"
		url="http://eca.knmi.nl/download/ensembles/ensembles.php"
		climexpfield="ensembles_05_tn_mo"
		units="[Celsius]"
		anomalie=ja;;
	rr_eobs)
		if [ "$FORM_lang" = nl ]; then	
			naam="neerslag"
			units="[mm/maand]"
		else
			naam="precipitation"
			units="[mm/month]"
		fi
		bron="ECA&amp;D E-OBS"
		url="http://eca.knmi.nl/download/ensembles/ensembles.php"
		climexpfield="ensembles_05_rr_mo"
		anomalie=ja;;
	pp_eobs)
		if [ "$FORM_lang" = nl ]; then	
			naam="luchtdruk op zeeniveau"
		else
			naam="sea level pressure"
		fi
		units="[hPa]"
		bron="ECA&amp;D E-OBS"
		url="http://eca.knmi.nl/download/ensembles/ensembles.php"
		climexpfield="ensembles_05_pp_mo"
		anomalie=ja;;
	*) . ./myvinkheader.cgi "Maandoverzicht wereld" "fout"
		echo "variabele $FORM_var is onbekend"
		. ./myvinkfooter.cgi
		exit;;
esac
if [ "$naam" = "wereldgemiddelde temperatuur" ]; then
	verderlezen="Een winter vol extremen"
	verderlezenurl="http://www.knmi.nl/cms/content/77820/een__winter_vol_extremen"
fi
