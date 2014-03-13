
def define_season(var, season):
    """define properties of the seasons"""

    if var in ['pr', 'prabs', 'pme']:
        if season == 'winter':
            mon, ave, sname = 10, 6, "October-March"
        elif season == 'summer':
            mon, ave, sname = 4, 6, "April-September"
        elif season == 'annual':
            mon, ave, sname = 1, 12, "annual"
        else:
            raise ValueError('Unknown season {season} for var {var}'.format(season=season, var=var))

    elif var == 'tas':
        if season == 'DJF':
            mon, ave, sname = 12, 3, "December-February"
        elif season == 'MAM':
            mon, ave, sname = 3, 3, "March-May"
        elif season == 'JJA':
            mon, ave, sname = 6, 3, "June-August"
        elif season == 'SON':
            mon, ave, sname = 9, 3, "September-November"
        elif season == 'annual':
            mon, ave, sname = 1, 12, "annual"
        else:
            raise ValueError('Unknown season {season}'.format(season=season))

    else:
        raise ValueError('Unknow var {var}'.format(var=var))

    return mon, ave, sname

def define_exp(exp):
    """define the different experiments."""

    lw = 5
    expname, iexp, lt = None, None, None

    if exp == 'rcp26':
        expname, iexp, lt = "RCP2.6", 0, 1
    elif exp == 'rcp45':
        expname, iexp, lt = "RCP4.5", 1, 2
    elif exp == 'rcp60':
        expname, iexp, lt = "RCP6.0", 2, 3
    elif exp == 'rcp85':
        expname, iexp, lt = "RCP8.5", 3, 4
    elif exp == 'piControl':
        expname = "pre-industrial control"
    elif exp == 'sresa1b':
        expname, iexp, lt = "SRES A1b", 4, 9
    else:
        expname, iexp, lt = exp, -1, 9

    return expname, iexp, lt, lw

#def define_season(var, season):
#    """define properties of the seasons"""

#    # TODO: replace if-then-else by a dict

#    if var in ['pr', 'prabs', 'pme']:
#        if season == 'winter':
#            sname =  "October-March"
#        elif season == 'summer':
#            sname =  "April-September"
#        elif season == 'annual':
#            sname =  "annual"
#        else:
#            raise ValueError('Unknown season {season} for var {var}'.format(season=season, var=var))

#    elif var == 'tas':
#        if season == 'DJF':
#            sname =  "December-February"
#        elif season == 'MAM':
#            sname =  "March-May"
#        elif season == 'JJA':
#            sname =  "June-August"
#        elif season == 'SON':
#            sname =  "September-November"
#        elif season == 'annual':
#            sname =  "annual"
#        else:
#            raise ValueError('Unknown season {season}'.format(season=season))

#    else:
#        raise ValueError('Unknown variable {var}'.format(var=var))

#    return sname

def adjust_winter(mon, ave):
    """for winter, start in the previous year"""

    if (mon+ave) > 13:
        s3 = '($3+1)'
    else:
        s3 = '3'

    return s3        

#function define_models {
## define list of models
##	cmip3models="bccr_bcm2_0 cccma_cgcm3_1 cccma_cgcm3_1_t63 cnrm_cm3 csiro_mk3_0 csiro_mk3_5 gfdl_cm2_0 gfdl_cm2_1 giss_aom giss_model_e_h giss_model_e_r ingv_echam4 inmcm3_0 ipsl_cm4 miroc3_2_medres miroc3_2_hires miub_echo_g mpi_echam5 mri_cgcm2_3_2a ncar_ccsm3_0 ncar_pcm1 ukmo_hadgem1 ukmo_hadcm3"
#	# these are the models with data in RCP4.5 on 07-jul-2012
#	models="ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CMCC-CM CMCC-CMS CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H_p1 GISS-E2-H_p2 GISS-E2-H_p3 GISS-E2-H-CC_p1 GISS-E2-R_p1 GISS-E2-R_p2 GISS-E2-R_p3 GISS-E2-R-CC_p1 HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC5 MIROC-ESM MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-M NorESM1-ME"
##	models_without_data_in_rcp45="CESM1-CAM5-1-FV2 CESM1-FASTCHEM CESM1-WACCM GISS-E2-H_p1 GISS-E2-H_p2 GISS-E2-H_p3 IPSL-CM5B-LR MPI-ESM-P "
#	piControl_models="ACCESS1-0 ACCESS1-3 bcc-csm1-1 BNU-ESM CanESM2 CCSM4 CESM1-BGC CMCC-CMS CNRM-CM5 CSIRO-Mk3-6-0 FGOALS-g2 FIO-ESM GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H_p2 GISS-E2-H_p3 GISS-E2-R_p2 GISS-E2-R_p3 inmcm4 IPSL-CM5A-LR MIROC5 MIROC-ESM MPI-ESM-LR MPI-ESM-MR MPI-ESM-P MRI-CGCM3 NorESM1-M" # list from Jan
#	imax=1
#	pmax=1
#	rmax=17
#	# add exceptions below. not crucial when running locally, important when running remote
#	case $model in
#	    "") ;;
#		modmean)	     rmax=1;random=allmean;;
#		onemean)	     rmax=1;random=mean;;
#		ACCESS1-0)       rmax=1;random=23;;
#		ACCESS1-3)       rmax=1;random=7;;
#		bcc-csm1-1)	     rmax=1;random=3;;
#		bcc-csm1-1-m)	 rmax=1;random=39;;
#		BNU-ESM)         rmax=1;random=17;;
#		CanESM2)	     rmax=5;random=22;;
#		CCSM4)		     rmax=6;random=37;;
#		CESM1-CAM5)      rmax=3;random=4;;
#		CESM1-BGC)       rmax=1;random=20;;
#		CMCC-CM)         rmax=1;random=8;;
#		CMCC-CMS)        rmax=1;random=38;;
#		CNRM-CM5)	     rmax=10;random=33;;
#		CSIRO-Mk3-6-0)   rmax=10;random=1;;
#		EC-EARTH)	     rmax=17;random=11;;
#		FGOALS-g2)       rmax=1;random=16;;
#		FGOALS-s2)       rmax=1;random=0;;
#		FIO-ESM)         rmax=3;random=2;;
#		GFDL-CM3)	     rmax=1;random=19;;
#		GFDL-ESM2G)      rmax=1;random=9;;
#		GFDL-ESM2M)	     rmax=1;random=28;;
#		GISS-E2-H)    	 rmax=6;random=-999;;
#		GISS-E2-H_p1)    rmax=6;random=41;;
#		GISS-E2-H_p2)    rmax=6;random=42;;
#		GISS-E2-H_p3)    rmax=6;random=40;;
#		GISS-E2-H-CC)	 rmax=6;random=-999;;
#		GISS-E2-H-CC_p1) rmax=1;random=36;;
#		GISS-E2-R)    	 rmax=6;random=-999;;
#		GISS-E2-R_p1)    rmax=6;random=31;;
#		GISS-E2-R_p2)    rmax=6;random=13;;
#		GISS-E2-R_p3)    rmax=6;random=26;;
#		GISS-E2-R-CC) 	 rmax=6;random=-999;;
#		GISS-E2-R-CC_p1) rmax=1;random=30;;
#		HadGEM2-AO)	     rmax=1;random=32;;
#		HadGEM2-CC)	     rmax=1;random=21;;
#		HadGEM2-ES)	     rmax=4;random=35;;
#		inmcm4)		     rmax=1;random=12;;
#		IPSL-CM5A-LR)    rmax=4;random=6;;
#		IPSL-CM5A-MR)    rmax=1;random=24;;
#		IPSL-CM5B-LR)    rmax=1;random=14;;
#		MIROC5)		     rmax=3;random=34;;
#		MIROC-ESM)	     rmax=1;random=5;;
#		MIROC-ESM-CHEM)  rmax=1;random=29;;
#		MPI-ESM-LR)	     rmax=3;random=25;;
#		MPI-ESM-MR)	     rmax=3;random=10;;
#		MPI-ESM-P)       rmax=0;random=-999;;
#		MRI-CGCM3)	     rmax=1;random=18;;
#		NorESM1-M)	     rmax=1;random=27;;
#		NorESM1-ME)	     rmax=1;random=15;;
#		*) echo "$0: unknown model $model"; exit -1;;
#	esac
#}

def define_range(rangeVal):

    lo, hi = None, None
    
    if rangeVal == 80:
        lo, hi = 10, 90
    elif rangeVal == 50:
        lo, hi = 25, 75
    return lo, hi
