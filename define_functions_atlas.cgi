#!/bin/sh
function define_range {
	if [ $range = 80 ]; then
		lo=10
		hi=90
	elif [ $range = 50 ]; then
		lo=25
		hi=75
	else
		echo "$0: error: unknown range $range"
		exit -1
	fi
}

function define_exp {
	# define the different experiments
	exps="rcp85 rcp60 rcp45 rcp26" # to get the order right in gnuplot
	lw=5
	case $exp in
		rcp26) expname="RCP2.6";iexp=0;lt=1;;
		rcp45) expname="RCP4.5";iexp=1;lt=2;;
		rcp60) expname="RCP6.0";iexp=2;lt=3;;
		rcp85) expname="RCP8.5";iexp=3;lt=4;;
		piControl) expname="pre-industrial control";;
	esac
}

function define_var {
	# define the properties of the variables
	# defaults
	type=Amon
	normsd=""
	diffvar=diff
	cbar=0
	fac=1
	notimeseries=""
	case $var in
		tas) varname="temperature"
			Varname="Temperature"
			cbar=0 # for GrADS
			cmin=-2
			cmax=8.0
			cint=0.5
			rgbcbar=tas.txt # for NCL
			cnlevels="(/-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.,3.,4.,5.,7.,9.,11./)"
			units="[Celsius]"
			seasons="annual DJF MAM JJA SON"
			;;
		pr)
			varname="relative precipitation"
			Varname="Precipitation"
			cmin=-30
			cmax=30
			cint=5
			cbar=1
			rgbcbar=pr.txt
			cnlevels="(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
			units="[%]"
			fac=100
			normsd=normsd # relative differences
			diffvar=reldiff
			seasons="annual winter summer"
			;;
		prabs)
			varname="precipitation"
			Varname="Precipitation"
			cmin=-1
			cmax=1
			cint=0.1
			cbar=1
			rgbcbar=pr.txt
			cnlevels="(/-0.50,-0.40,-0.30,-0.20.,-0.10.,0.,0.10,0.20,0.30,0.40,0.50./)"
			units="[mm/dy]"
			fac=1
			normsd=standardunits # I prefer mm/day
			seasons="annual winter summer"
			notimeseries=true
			;;
		evspsbl)
			varname="evaporation"
			Varname="Evaporation"
			cmin=-30
			cmax=30
			cint=5
			cbar=1
			rgbcbar=precipg.rgb
			cnlevels="(/-80.,-40.,-20.,-10.,-5.,-2.5,0.,2.5,5.,10.,20.,40.,80./)"
			units="[%]"
			fac=100
			normsd=normsd # relative differences
			diffvar=reldiff
			seasons="annual winter summer"
			notimeseries=true
			;;
		pme)
			varname="precipitation minus evaporation"
			Varname="P-E"
			cmin=-10
			cmax=10
			cint=1
			cbar=1
			rgbcbar=pr.txt
			cnlevels="(/-50.,-40.,-30.,-20.,-10.,0.,10.,20.,30.,40.,50./)"
			units="[%]"
			fac=100
			seasons="annual winter summer"
			;;
		huss)
			varname="specific humidity"
			Varname="Specific humidity"
			cmin=-30
			cmax=30
			cint=5
			cbar=1
			rgbcbar=huss.rgb
			cnlevels="(/-2.5,-1.,1.,2.5,5.,10.,15.,20.,30.,40.,50.,75./)"
			normsd=normsd # relative differences
			diffvar=reldiff
			seasons="annual summer winter"
			units="[%]"
			fac=100
			notimeseries=true
			;;
		mrso)
			type=Lmon
			varname="soil moisture"
			Varname="Soil moisture"
			seasons="annual summer winter"
			units="[kg/m2]"
			cmin=-30
			cmax=30
			cint=5
			cbar=1
			rgbcbar=precipg.rgb
			cnlevels="(/-50.,-25.,-10.,-5,-2.5,-1.,0.,1.,2.5,5.,10.,25.,50./)"
			notimeseries=true
			;;
		mrro|mrros)
			type=Lmon
			if [ $var = mrro ]; then
				varname="runoff"
				Varname="Runoff"
			else
				varname="surface runoff"
				Varname="Surface runoff"
			fi
			seasons="annual summer winter"
			normsd=normsd # relative differences
			diffvar=reldiff
			units="[%]"
			fac=100
			cmin=-30
			cmax=30
			cint=5
			cbar=1
			rgbcbar=precipg.rgb
			cnlevels="(/-80.-40.,-20.,-10.,-5.,-2.5,0.,2.5,5.,10.,20.,40.,80./)"
			notimeseries=true
			;;
		*) echo "$0: error: unknown variable $var";exit -1;;
	esac
	if [ $units = '[%]' ]; then
		s2="(100*\$2)"
		s5="(100*\$5)"
		s8="(100*\$8)"
		s10="(100*\$10)"
		s12="(100*\$12)"
		s15="(100*\$15)"
	else
		s2=2
		s5=5
		s8=8
		s10=10
		s12=12
		s15=15
	fi
}

function define_period {
# define properties of time slices
	yr1a=1986
	yr2a=2005
	case $period in
		beginning) yr1=1861;yr2=1880;;
		ref) yr1=1986;yr2=2005;;
		early) yr1=2016;yr2=2035;;
		mid) yr1=2046;yr2=2065;;
		late) yr1=2081;yr2=2100;;
		2030) yr1a=2001;yr2a=2010;yr1=2026;yr2=2035;;
		2065) yr1a=2001;yr2a=2010;yr1=2061;yr2=2070;;

		*) echo "$0: error: unknown period $period";exit -1;;
	esac
	yr1t=$yr1
	yr2t=$yr2
}

function define_season {
# define properties of the seasons
	case $season in
		winter) mon=10;ave=6;seasonname="October--March"
			varmin=$prmin_winter;varmax=$prmax_winter
			varmin2=$prmin_winter2;varmax2=$prmax_winter2;;
		summer) mon=4;ave=6;seasonname="April--September"
			varmin=$prmin_summer;varmax=$prmax_summer
			varmin2=$prmin_summer2;varmax2=$prmax_summer2;;
		DJF) mon=12;ave=3;seasonname="December--February"
			varmin=$tasmin_DJF;varmax=$tasmax_DJF;;
		MAM) mon=3;ave=3;seasonname="March--May";;
		JJA) mon=6;ave=3;seasonname="June--August"
			varmin=$tasmin_JJA;varmax=$tasmax_JJA;;
		SON) mon=9;ave=3;seasonname="September--November";;
		annual) mon=1;ave=12;seasonname="annual";;
		*) echo "$0: error: unknown season $season";exit -1;;
	esac
	sname=`echo $seasonname | sed -e 's/--/-/'`
}

function get_season_name {
	mon1="$FORM_mon"
	sum="$FORM_sum"
	mon2=$((mon1 + sum - 1))
	if [ $mon2 -gt 12 ]; then
		mon2=$((mon2-12))
	fi
	m=$mon1
	month2string
	cmon1=$cm
	if [ $sum = 1 ]; then
		sname=$cmon1
	else
		m=$mon2
		month2string
		cmon2=$cm
		sname="${cmon1}-${cmon2}"
	fi
}

function month2string {
	case $m in
		1) cm=Jan;;
		2) cm=Feb;;
		3) cm=Mar;;
		4) cm=Apr;;
		5) cm=May;;
		6) cm=Jun;;
		7) cm=Jul;;
		8) cm=Aug;;
		9) cm=Sep;;
		10) cm=Oct;;
		11) cm=Nov;;
		12) cm=Dec;;
		*) cm="unknown month number $m";;
	esac
}

function adjust_winter {
# for winter, start in the previous year
	if [ $((mon+ave)) -gt 13 ]; then
		[ -n "$yr1" ] && yr1=$((yr1-1))
		[ -n "$yr2" ] && yr2=$((yr2-1))
		[ -n "$yr1a" ] && yr1a=$((yr1a-1))
		[ -n "$yr2a" ] && yr2a=$((yr2a-1))
		s3="(\$3+1)"
	else
		s3=3
	fi
}

function define_models {
# define list of models
	cmip3models="bccr_bcm2_0 cccma_cgcm3_1 cccma_cgcm3_1_t63 cnrm_cm3 csiro_mk3_0 csiro_mk3_5 gfdl_cm2_0 gfdl_cm2_1 giss_aom giss_model_e_h giss_model_e_r ingv_echam4 inmcm3_0 ipsl_cm4 miroc3_2_medres miroc3_2_hires miub_echo_g mpi_echam5 mri_cgcm2_3_2a ncar_ccsm3_0 ncar_pcm1 ukmo_hadgem1 ukmo_hadcm3"
	# these are the models with data in RCP4.5 on 07-jul-2012
	models="ACCESS1-0 ACCESS1-3 bcc-csm1-1 BNU-ESM CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CMCC-CM CMCC-CMS CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H-CC_p1 GISS-E2-R_p1 GISS-E2-R_p2 GISS-E2-R_p3 GISS-E2-R-CC_p1 HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-M NorESM1-ME"
	models_without_data_in_rcp45="CESM1-CAM5-1-FV2 CESM1-FASTCHEM CESM1-WACCM GISS-E2-H_p1 GISS-E2-H_p2 GISS-E2-H_p3 IPSL-CM5B-LR MPI-ESM-P "
	imax=1
	pmax=1
	rmax=17
	# add exceptions below. not crucial when running locally, important when running remote
	case $model in
	    "") ;;
		modmean)	     rmax=1;random=allmean;;
		onemean)	     rmax=1;random=mean;;
		ACCESS1-0)       rmax=1;random=23;;
		ACCESS1-3)       rmax=1;random=7;;
		bcc-csm1-1)	     rmax=1;random=3;;
		BNU-ESM)         rmax=1;random=17;;
		CanESM2)	     rmax=5;random=22;;
		CCSM4)		     rmax=6;random=37;;
		CESM1-CAM5)      rmax=3;random=4;;
		CESM1-BGC)       rmax=1;random=20;;
		CMCC-CM)         rmax=1;random=8;;
		CMCC-CMS)        rmax=1;random=38;;
		CNRM-CM5)	     rmax=10;random=33;;
		CSIRO-Mk3-6-0)   rmax=10;random=1;;
		EC-EARTH)	     rmax=17;random=11;;
		FGOALS-g2)       rmax=1;random=16;;
		FGOALS-s2)       rmax=1;random=0;;
		FIO-ESM)         rmax=3;random=2;;
		GFDL-CM3)	     rmax=1;random=19;;
		GFDL-ESM2G)      rmax=1;random=9;;
		GFDL-ESM2M)	     rmax=1;random=28;;
		GISS-E2-R)    	 rmax=5;random=-999;;
		GISS-E2-R_p1)    rmax=5;random=31;;
		GISS-E2-R_p2)    rmax=5;random=13;;
		GISS-E2-R_p3)    rmax=5;random=26;;
		GISS-E2-R-CC) 	 rmax=5;random=-999;;
		GISS-E2-R-CC_p1) rmax=5;random=30;;
		GISS-E2-H-CC)	 rmax=5;random=-999;;
		GISS-E2-H-CC_p1) rmax=5;random=36;;
		HadGEM2-AO)	     rmax=1;random=32;;
		HadGEM2-CC)	     rmax=1;random=21;;
		HadGEM2-ES)	     rmax=4;random=35;;
		inmcm4)		     rmax=1;random=12;;
		IPSL-CM5A-LR)    rmax=4;random=6;;
		IPSL-CM5A-MR)    rmax=1;random=24;;
		IPSL-CM5B-LR)    rmax=1;random=14;;
		MIROC5)		     rmax=3;random=34;;
		MIROC-ESM)	     rmax=1;random=5;;
		MIROC-ESM-CHEM)  rmax=1;random=29;;
		MPI-ESM-LR)	     rmax=3;random=25;;
		MPI-ESM-MR)	     rmax=3;random=10;;
		MRI-CGCM3)	     rmax=1;random=18;;
		NorESM1-M)	     rmax=1;random=27;;
		NorESM1-ME)	     rmax=1;random=15;;
		*) echo "$0: unknown model $model"; exit -1;;
	esac
}

function define_region {
	# define list of regions
	regions="world arctic highlatitudes westnorthamerica eastnorthamerica centralamerica northsouthamerica southsouthamerica northeurope mediterranean weafrica southafrica centralasia eastasia southasia southeastasia australia pacific antarctica"

	# define properties of the regions
	labelx=0.77
	labely=0.67
	abbr[1]="";npoly[1]=""
	abbr[2]="";npoly[2]=""
	abbr[3]="";npoly[3]=""
	shortname[1]=""
	shortname[2]=""
	shortname[3]=""
	lon1[1]=""
	lon2[1]=""
	lon1[2]=""
	lon2[2]=""
	lon1[3]=""
	lon2[3]=""
	lat1[1]=""
	lat2[1]=""
	lat1[2]=""
	lat2[2]=""
	lat1[3]=""
	lat2[3]=""
	firstpage=8
	subregions="1 2"
	prmin_winter2=""
	prmax_winter2=""
	prmin_summer2=""
	prmax_summer2=""
	case $region in
# home-defined
		world) name[0]="World"
			lon1[0]=-170;lon2[0]=190;lat1[0]=-90;lat2[0]=90;lsmask[0]=all
			name[1]="World (land)"
			shortname[1]="worldland"
			area[1]=""
			lon1[1]=-170;lon2[1]=190;lat1[1]=-90;lat2[1]=90;lsmask[1]=land
			name[2]="World (sea)"
			lon1[2]=-170;lon2[2]=190;lat1[2]=-90;lat2[2]=90;lsmask[2]=sea
			area[2]=""
			shortname[2]="worldsea"
			name[3]="World"
			shortname[3]=world
			lon1[3]=-170;lon2[3]=190;lat1[3]=-90;lat2[3]=90;lsmask[3]=all
			area[3]=""
			subregions="1 2 3"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			tascross="9.4.1, 9.4.2, 10.3, 11.3.2.2, 11.3.3.1, Box 11.2, 12.4.3 and 12.4.7"
			prcross="9.4.4, 11.3.2.3, Box 11.2, 12.4.5"
			;;
# continents (KNMI Atlas only)
		NAmerica) name[0]="North America"
			lon1[0]=-170;lon2[0]=-15;lat1[0]=5;lat2[0]=85;lsmask[0]=land
			name[1]="North America"
			shortname[1]="NAmerica"
			area[1]=""
			lon1[1]=-170;lon2[1]=-15;lat1[1]=5;lat2[1]=85;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
		SAmerica) name[0]="South America"
			lon1[0]=-90;lon2[0]=-30;lat1[0]=-60;lat2[0]=15;lsmask[0]=land
			name[1]="Southth America"
			shortname[1]="SAmerica"
			area[1]=""
			lon1[1]=-90;lon2[1]=-30;lat1[1]=-60;lat2[1]=15;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
		Europe) name[0]="Europe"
			lon1[0]=-25;lon2[0]=45;lat1[0]=35;lat2[0]=72.5;lsmask[0]=land
			name[1]="Europa"
			shortname[1]="Europe"
			area[1]=""
			lon1[1]=-25;lon2[1]=45;lat1[1]=35;lat2[1]=72.5;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
		Africa) name[0]="Africa"
			lon1[0]=-20;lon2[0]=52.5;lat1[0]=-37.5;lat2[0]=37.5;lsmask[0]=land
			name[1]="Africa"
			shortname[1]="Africa"
			area[1]=""
			lon1[1]=-20;lon2[1]=52.5;lat1[1]=-37.5;lat2[1]=37.5;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
		Asia) name[0]="Aisa"
			lon1[0]=40;lon2[0]=190;lat1[0]=-10;lat2[0]=80;lsmask[0]=land
			name[1]="Asia"
			shortname[1]="Asia"
			area[1]=""
			lon1[1]=40;lon2[1]=190;lat1[1]=-10;lat2[1]=80;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
		Australia) name[0]="Australia"
			lon1[0]=110;lon2[0]=180;lat1[0]=-47.5;lat2[0]=-10;lsmask[0]=land
			name[1]="Australia"
			shortname[1]="Australia"
			area[1]=""
			lon1[1]=110;lon2[1]=180;lat1[1]=-47.5;lat2[1]=-10;lsmask[1]=land
			subregions="1"
			labely=0.63
			xwidth=0.33
			page=$((firstpage+0))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-15"
			prmax_winter="25"
			prmin_summer="-15"
			prmax_summer="25"
			;;
# home-defined
		arctic) name[0]="Arctic"
			lon1[0]=-180;lon2[0]=180;lat1[0]=67.5;lat2[0]=90;lsmask[0]=all
			name[1]="Arctic (land)"
			shortname[1]="Arcticland"
			area[1]="67.5\dg--90\dg N"
			lon1[1]=-180;lon2[1]=180;lat1[1]=67.5;lat2[1]=90;lsmask[1]=land
			name[2]="Arctic (sea)"
			shortname[2]="Arcticsea"
			lon1[2]=-180;lon2[2]=180;lat1[2]=67.5;lat2[2]=90;lsmask[2]=sea
			area[2]=""
			labelx=0.79
			labely=0.79
			xwidth=0.213
			page=$((firstpage+4))
			tasmin_DJF="-12.5"
			tasmax_DJF="27.5"
			tasmin_JJA="-4"
			tasmax_JJA="12"
			prmin_winter="-40"
			prmax_winter="140"
			prmin_summer="-30"
			prmax_summer="100"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.2"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.2"
			;;
# CGI + NAS
		highlatitudes) name[0]="High latitudes"
			lon1[0]=-180;lon2[0]=180;lat1[0]=50;lat2[0]=90;lsmask[0]=land
			name[1]="Canada/\\discretionary{}{}{}Greenland/\\discretionary{}{}{}Iceland"
			area[1]="50\dg--85\dg N, 105\dg--10\dg W"
			lon1[1]=-105;lon2[1]=-10;lat1[1]=50;lat2[1]=85;lsmask[1]=land
			abbr[1]="CGI";npoly[1]=4
			name[2]="North Asia"
			area[2]="50\dg--70\dg N, 40\dg--180\dg E"
			lon1[2]=40;lon2[2]=180;lat1[2]=50;lat2[2]=70;lsmask[2]=land
			abbr[2]="NAS";npoly[2]=4
			labelx=0.79
			labely=0.79
			xwidth=0.213
			page=$((firstpage+8))
			tasmin_DJF="-10"
			tasmax_DJF="17.5"
			tasmin_JJA="-5"
			tasmax_JJA="11"
			prmin_winter="-30"
			prmax_winter="100"
			prmin_summer="-25"
			prmax_summer="50"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.8"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.8"
			;;
# ALA + WNA
		westnorthamerica) name[0]="North America (West)"
			lon1[0]=-170;lon2[0]=-105;lat1[0]=30;lat2[0]=70;lsmask[0]=land
			name[1]="Alaska/NW Canada"
			lon1[1]=-168.0220;lon2[1]=-105;lat1[1]=60;lat2[1]=72.5540;lsmask[1]=land
			area[1]="60\dg--72.6\dg N, 168\dg--105\dg W"
			abbr[1]="ALA";npoly[1]=4
			name[2]="West North America"
			lon1[2]=-130;lon2[2]=-105;lat1[2]=28.5660;lat2[2]=60;lsmask[2]=land
			area[2]="28.6\dg--60\dg N, 130\dg--105\dg W"
			abbr[2]="WNA";npoly[2]=4
			page=$((firstpage+12))
			labely=0.678
			xwidth=0.33
			tasmin_DJF="-12.5"
			tasmax_DJF="22.5"
			tasmin_JJA="-5"
			tasmax_JJA="12"
			prmin_winter="-50"
			prmax_winter="125"
			prmin_summer="-30"
			prmax_summer="70"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.3"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.3"
			;;
# CNA + ENA
		eastnorthamerica) name[0]="North America (East)"
			lon1[0]=-105;lon2[0]=-60;lat1[0]=25;lat2[0]=50;lsmask[0]=land
			name[1]="Central North America"
			lon1[1]=-105;lon2[1]=-85;lat1[1]=28.5660;lat2[1]=50;lsmask[1]=land
			area[1]="28.6\dg--50\dg N, 105\dg--85\dg W"
			abbr[1]="CNA";npoly[1]=4
			name[2]="Eastern North America"
			lon1[2]=-85;lon2[2]=-60;lat1[2]=25;lat2[2]=50;lsmask[2]=land
			area[2]="25\dg--50\dg N, 85\dg--60\dg W"
			abbr[2]="ENA";npoly[2]=4
			page=$((firstpage+16))
			labely=0.716
			xwidth=0.27
			tasmin_DJF="-7.5"
			tasmax_DJF="12.5"
			tasmin_JJA="-4"
			tasmax_JJA="12"
			prmin_winter="-60"
			prmax_winter="90"
			prmin_summer="-60"
			prmax_summer="60"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.3"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.3"
			;;
# CAM + home-defined
		centralamerica) name[0]="Central America and Caribbean"
			lon1[0]=-115;lon2[0]=-60;lat1[0]=0;lat2[0]=30;lsmask[0]=land
			name[1]="Central America"
			lsmask[1]=land
			area[1]="68.8\dg W,\discretionary{}{}{}11.4\dg N; 79.7\dg W, 1.2\dg S; 116.3\dg W,28.6\dg N; 90.3\dg W,28.6\dg N"
			abbr[1]="CAM";npoly[1]=4
			shortname[2]="Caribbean"
			name[2]="Caribbean (land and sea)"
			lon1[2]=-85;lon2[2]=-60;lat1[2]=10;lat2[2]=25;lsmask[2]=all
			area[2]="10\dg--25\dg N, 85\dg--60\dg W"
			labely=0.665
			xwidth=0.33
			page=$((firstpage+20))
			tasmin_DJF="-2.5"
			tasmax_DJF="7.5"
			tasmin_JJA="-2.5"
			tasmax_JJA="7.5"
			prmin_winter="-100"
			prmax_winter="100"
			prmin_summer="-100"
			prmax_summer="150"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.4"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.4"
			;;
# AMZ + NEB
		northsouthamerica) name[0]="Northern South America"
			lon1[0]=-80;lon2[0]=-35;lat1[0]=-20;lat2[0]=10;lsmask[0]=land
			name[1]="Amazon"
			lsmask[1]=land
			area[1]="20\dg S--10\dg N, 82.5\dg--60\dg W"
			abbr[1]="AMZ";npoly[1]=5
			name[2]="North-East Brazil"
			lon1[2]=-50;lon2[2]=-34;lat1[2]=-20;lat2[2]=0;lsmask[2]=land
			area[2]="20\dg S--EQ, 50\dg--34\dg W"
			abbr[2]="NEB";npoly[2]=4
			labely=0.693
			xwidth=0.315
			page=$((firstpage+24))
			tasmin_DJF="-4"
			tasmax_DJF="12"
			tasmin_JJA="-4"
			tasmax_JJA="10"
			prmin_winter="-80"
			prmax_winter="120"
			prmin_summer="-100"
			prmax_summer="150"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.5"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.5"
			;;
# WSA + SSA
		southsouthamerica) name[0]="Southern South America"
			lon1[0]=-82.5;lon2[0]=-35;lat1[0]=-55;lat2[0]=-4;lsmask[0]=land
			name[1]="West Coast South America"
			lsmask[1]=land
			area[1]="79.7\dg W,1.2\dg S; 66.4\dg W,20\dg S; 72.1\dg W,50\dg S; 67.3\dg W56.7\dg S; 82.0\dg W 56.7\dg S; 82.2\dg W,0.5\dg N"
			abbr[1]="WSA";npoly[1]=6
			name[2]="Southeastern South America"
			lsmask[2]=land
			area[2]="39.4\dg W,20\dg S; 39.4\dg W,\discretionary{}{}{}56.6\dg S; 67.3\dg W,56.7\dg S; 72.1\dg W,50\dg S; 66\dg W,20\dg S"
			abbr[2]="SSA";npoly[2]=5
			labelx=0.77
			labely=0.785
			xwidth=0.2025
			page=$((firstpage+28))
			tasmin_DJF="-3"
			tasmax_DJF="8"
			tasmin_JJA="-4"
			tasmax_JJA="7"
			prmin_winter="-50"
			prmax_winter="70"
			prmin_summer="-60"
			prmax_summer="100"
			tascross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.5"
			prcross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.5"
			;;
# NEU + CEU
		northeurope) name[0]="North and Central Europe"
			lon1[0]=-10;lon2[0]=40;lat1[0]=45;lat2[0]=75;lsmask[0]=land
			name[1]="North Europe"
			lsmask[1]=land
			area[1]="10\dg W,48\dg N; 10\dg W,75\dg N; 40\dg E,75\dg N; 40\dg E,61.3\dg N"
			abbr[1]="NEU";npoly[1]=4
			name[2]="Central Europe"
			lsmask[2]=land
			area[2]="10\dg W, 45\dg N; 10\dg W,48\dg N; 40\dg E, 61.3\dg N; 40\dg E,45\dg N"
			abbr[2]="CEU";npoly[2]=4
			labely=0.67
			xwidth=0.33
			page=$((firstpage+32))
			tasmin_DJF="-12.5"
			tasmax_DJF="15"
			tasmin_JJA="-5"
			tasmax_JJA="12.5"
			prmin_winter="-50"
			prmax_winter="75"
			prmin_summer="-60"
			prmax_summer="80"
			tascross="9.6.1, 10.3, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.6"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.6"
			;;
# MED + SAH
		mediterranean) name[0]="Mediterranean and Sahara"
			lon1[0]=-20;lon2[0]=40;lat1[0]=15;lat2[0]=45;lsmask[0]=land
			name[1]="South Europe/\discretionary{}{}{}Mediterranean"
			lon1[1]=-10;lon2[1]=40;lat1[1]=30;lat2[1]=45;lsmask[1]=land
			area[1]="30\dg--45\dg N, 10\dg W--40\dg E"
			abbr[1]="MED";npoly[1]=4
			name[2]="Sahara"
			lon1[2]=-20;lon2[2]=40;lat1[2]=15;lat2[2]=30;lsmask[2]=land
			area[2]="15\dg--30\dg N, 20\dg W--40\dg E"
			abbr[2]="SAH";npoly[2]=4
			labely=0.655
			xwidth=0.33
			page=$((firstpage+36))
			tasmin_DJF="-4"
			tasmax_DJF="10"
			tasmin_JJA="-4"
			tasmax_JJA="12"
			prmin_winter="-60"
			prmax_winter="60"
			prmin_winter2="-100"
			prmax_winter2="1000"
			prmin_summer="-100"
			prmax_summer="100"
			prmin_summer2="-100"
			prmax_summer2="350"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.6"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.6"
			;;
# WAF + EAF
		weafrica) name[0]="West and East Africa"
			lon1[0]=-20;lon2[0]=55;lat1[0]=-10;lat2[0]=15
			name[1]="west Africa"
			lon1[1]=-20;lon2[1]=25;lat1[1]=-11.3650;lat2[1]=15;lsmask[1]=land
			area[1]="11.4\dg S--15\dg N, 20\dg W--25\dg E"
			abbr[1]="WAF";npoly[1]=4
			name[2]="East Africa"
			lon1[2]=25;lon2[2]=52;lat1[2]=-11.3650;lat2[2]=15;lsmask[2]=land
			area[2]="11.3\dg S--15\dg N, 25\dg--52\dg E"
			abbr[2]="EAF";npoly[2]=4
			labely=0.608
			xwidth=0.33
			page=$((firstpage+40))
			tasmin_DJF="-4"
			tasmax_DJF="8"
			tasmin_JJA="-4"
			tasmax_JJA="8"
			prmin_winter="-60"
			prmax_winter="80"
			prmin_summer="-40"
			prmax_summer="80"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.7"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.7"
			;;
# SAF + home-grown
		southafrica) name[0]="Southern Africa and West Indian Ocean"
			lon1[0]=-10;lon2[0]=75;lat1[0]=-35;lat2[0]=10
			name[1]="Southern Africa"
			lon1[1]=-10;lon2[1]=52;lat1[1]=-35;lat2[1]=-11.3650;lsmask[1]=land
			area[1]="35\dg--11.4\dg S, 10\dg W--52\dg E"
			abbr[1]="SAF";npoly[1]=4
			shortname[2]='WIndian'
			name[2]='West Indian Ocean'
			lon1[2]=52;lon2[2]=75;lat1[2]=-25;lat2[2]=5;lsmask[2]=sea
			area[2]="25\dg S--5\dg N, 52\dg--75\dg E"
			labely=0.663
			xwidth=0.33
			page=$((firstpage+44))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-3"
			tasmax_JJA="9"
			prmin_winter="-40"
			prmax_winter="60"
			prmin_summer="-100"
			prmax_summer="100"
			tascross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.7"
			prcross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.7"
			;;
# WAS + CAS
		centralasia) name[0]="West and Central Asia"
			lon1[0]=40;lon2[0]=75;lat1[0]=15;lat2[0]=50;lsmask[0]=land
			name[1]="West Asia"
			lon1[1]=40;lon2[1]=60;lat1[1]=15;lat2[1]=50;lsmask[1]=land
			area[1]="15\dg--50\dg N, 40\dg--60\dg E"
			abbr[1]="WAS";npoly[1]=4
			name[2]="Central Asia"
			lon1[2]=60;lon2[2]=75;lat1[2]=30;lat2[2]=50;lsmask[2]=land
			area[2]="30\dg--50\dg N, 60\dg--75\dg E"
			abbr[2]="CAS";npoly[2]=4
			labely=0.76
			xwidth=0.24
			page=$((firstpage+48))
			tasmin_DJF="-7.5"
			tasmax_DJF="12.5"
			tasmin_JJA="-4"
			tasmax_JJA="12"
			prmin_winter="-100"
			prmax_winter="250"
			prmin_summer="-100"
			prmax_summer="250"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.8"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.8"
			;;
# TIB + EAS
		eastasia) name[0]="Eastern Asia and Tibetan Plateau"
			lon1[0]=75;lon2[0]=145;lat1[0]=20;lat2[0]=50
			name[1]="Eastern Asia"
			lon1[1]=100;lon2[1]=145;lat1[1]=20;lat2[1]=50;lsmask[1]=land
			area[1]="20\dg--50\dg N, 100\dg--145\dg E"
			abbr[1]="EAS";npoly[1]=4
			name[2]="Tibetan Plateau"
			lon1[2]=75;lon2[2]=100;lat1[2]=30;lat2[2]=50;lsmask[2]=land
			area[2]="30\dg--50\dg N, 75\dg--100\dg E"
			abbr[2]="TIB";npoly[2]=4
			labely=0.635
			xwidth=0.33
			page=$((firstpage+52))
			tasmin_DJF="-8"
			tasmax_DJF="12"
			tasmin_JJA="-4"
			tasmax_JJA="12"
			prmin_winter="-50"
			prmax_winter="100"
			prmin_summer="-50"
			prmax_summer="100"
			tascross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.3, 14.9.9"
			prcross="9.6.1, 11.3.2.4.1, Box 11.2, 12.4.5, 14.9.9"
			;;
# SAS + homegrown sea area
		southasia) name[0]="South Asia"
			lon1[0]=60;lon2[0]=100;lat1[0]=5;lat2[0]=30
			name[1]="South Asia"
			lsmask[1]=land
			area[1]="60\dg E,5\dg N; 60\dg E,30\dg N; 100\dg E,30\dg N; 100\dg E,20\dg E; 95\dg E,20\dg N; 95\dg E,5\dg N"
			abbr[1]="SAS";npoly[1]=6
			shortname[2]='NIndian'
			name[2]='North Indian Ocean'
			lon1[2]=60;lon2[2]=95;lat1[2]=5;lat2[2]=30;lsmask[2]=sea
			area[2]="5\dg--30\dg N, 60\dg--95\dg E"
			labely=0.683
			xwidth=0.3175
			page=$((firstpage+56))
			tasmin_DJF="-3"
			tasmax_DJF="9"
			tasmin_JJA="-4"
			tasmax_JJA="8"
			prmin_winter="-100"
			prmax_winter="200"
			prmin_summer="-60"
			prmax_summer="100"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.10"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.10"
			;;
# SEA
		southeastasia) name[0]="Southeast Asia"
			lon1[0]=95;lon2[0]=155;lat1[0]=-10;lat2[0]=20;lsmask[0]=land
			name[1]='Southeast Asia (land)'
			lon1[1]=95;lon2[1]=155;lat1[1]=-10;lat2[1]=20;lsmask[1]=land
			area[1]="10\dg S--20\dg N, 95\dg--155\dg E"
			abbr[1]="SEA";npoly[1]=4
			shortname[2]='SEAsia_sea'
			name[2]='Southeast Asia (sea)'
			lon1[2]=95;lon2[2]=155;lat1[2]=-10;lat2[2]=20;lsmask[2]=sea
			area[2]=""
			labely=0.653
			xwidth=0.33
			page=$((firstpage+60))
			tasmin_DJF="-2"
			tasmax_DJF="7"
			tasmin_JJA="-2"
			tasmax_JJA="7"
			prmin_winter="-60"
			prmax_winter="60"
			prmin_summer="-40"
			prmax_summer="80"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.11"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.11"
			;;
# NAU + SAU
		australia) name[0]="Australia and New Zealand"
			lon1[0]=110;lon2[0]=180;lat1[0]=-47.5;lat2[0]=-10;lsmask[0]=land
			name[1]="North Australia"
			lon1[1]=110;lon2[1]=155;lat1[1]=-30;lat2[1]=-10;lsmask[1]=land
			area[1]="30\dg--10\dg S, 110\dg--155\dg E"
			abbr[1]="NAU";npoly[1]=4
			name[2]="South Australia/New Zealand"
			lon1[2]=110;lon2[2]=180;lat1[2]=-50;lat2[2]=-30;lsmask[2]=land
			area[2]="50\dg--30\dg S, 110\dg--180\dg E"
			abbr[2]="SAU";npoly[2]=4
			labely=0.665
			xwidth=0.33
			page=$((firstpage+64))
			tasmin_DJF="-4"
			tasmax_DJF="8"
			tasmin_JJA="-4"
			tasmax_JJA="8"
			prmin_winter="-100"
			prmax_winter="200"
			prmin_summer="-100"
			prmax_summer="350"
			tascross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.12"
			prcross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.12"
			;;
# Pacific Island (home-grown)
		pacific) name[0]="Pacific Islands region"
			lon1[0]=155;lon2[0]=230;lat1[0]=-25;lat2[0]=25;lsmask[0]=all
			shortname[1]="NTPacific"
			name[1]="Northern Tropical Pacific"
			lon1[1]=155;lon2[1]=210;lat1[1]=5;lat2[1]=25;lsmask[1]=all
			area[1]="5\dg--25\dg N, 155\dg E--150\dg W"
			shortname[2]="EQPacific"
			name[2]="Equatorial Pacific"
			lon1[2]=155;lon2[2]=210;lat1[2]=-5;lat2[2]=5;lsmask[2]=all
			area[2]="5\dg S--5\dg N, 155\dg E--150\dg W"
			shortname[3]="STPacific"
			name[3]="Southern Tropical Pacific"
			lon1[3]=155;lon2[3]=230;lat1[3]=-25;lat2[3]=-5;lsmask[3]=all
			area[3]="25\dg--5\dg S, 155\dg E--130\dg W"
			labely=0.698
			xwidth=0.325
			page=$((firstpage+68))
			subregions="1 2 3"
			tasmin_DJF="-3"
			tasmax_DJF="5"
			tasmin_JJA="-3"
			tasmax_JJA="5"
			prmin_winter="-100"
			prmax_winter="300"
			prmin_summer="-100"
			prmax_summer="150"
			tascross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.3, 14.9.13"
			prcross="9.6.1, 11.3.2.4.3, Box 11.2, 12.4.5, 14.9.13"
			;;
# home-grown
		antarctica) name[0]="Antarctica"
			lon1[0]=-180;lon2[0]=180;lat1[0]=-90;lat2[0]=-50;lsmask[0]=all
			name[1]='Antarctica (land)'
			shortname[1]="Antarcticland"
			area[1]="90\dg--50\dg S"
			lon1[1]=-180;lon2[1]=180;lat1[1]=-90;lat2[1]=-50;lsmask[1]=land
			name[2]='Antarctica (sea)'
			shortname[2]="Antarcticsea"
			lon1[2]=-180;lon2[2]=180;lat1[2]=-90;lat2[2]=-50;lsmask[2]=sea
			area[2]=""
			labelx=0.79
			labely=0.79
			xwidth=0.213
			page=$((firstpage+72))
			tasmin_DJF="-3"
			tasmax_DJF="7"
			tasmin_JJA="-5"
			tasmax_JJA="10"
			prmin_winter="-30"
			prmax_winter="70"
			prmin_summer="-30"
			prmax_summer="70"
			tascross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.3, 14.9.14"
			prcross="9.6.1, 11.3.2.4.2, Box 11.2, 12.4.5, 14.9.14"
			;;
		"") echo "defined list of regions, $regions";;
		*) echo "$0: error: unknown region $region"; exit -1;;
	esac
	[ -z "$prmin_winter2" ] && prmin_winter2=$prmin_winter
	[ -z "$prmax_winter2" ] && prmax_winter2=$prmax_winter
	[ -z "$prmin_summer2" ] && prmin_summer2=$prmin_summer
	[ -z "$prmax_summer2" ] && prmax_summer2=$prmax_summer
}

