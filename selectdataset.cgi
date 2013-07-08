#!/bin/sh
# to be sourced from other scripts
NPERYEAR=12
timescale=monthly
case ${CLASS:-choose} in
Demeter) demeter_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC"
	 level=level;longitude=longitude;latitude=latitude
         file=demeter
         flatten=bin/flattennc;;
ENSEMBLES_stream_2) ensembles_2_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC/ensembles/stream2/seasonal/atmospheric/"
	 level=level;longitude=longitude;latitude=latitude
         file=monthly
         flatten=bin/flattennc;;
ENSEMBLES_stream_2_daily) ensembles_2_daily_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC/ensembles/stream2/seasonal/atmospheric/"
	 level=level;longitude=longitude;latitude=latitude
         file=daily
	 NPERYEAR=366
         timescale=daily
         flatten=bin/flattennc;;
ENSEMBLES_stream_1) ensembles_1_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC/ensembles/stream1/atmospheric/"
	 level=level;longitude=longitude;latitude=latitude
         file=monthly
         flatten=bin/flattennc;;
ENSEMBLES_stream_1_ocean) ensembles_1_ocean_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC/ensembles/stream1/"
	 level=level;longitude=longitude;latitude=latitude
         file=ocean
         flatten=bin/flattennc;;
ENSEMBLES_stream_1_daily) ensembles_1_daily_selected=selected
         path="http://ensembles.ecmwf.int/thredds/dodsC/ensembles/stream1/atmospheric/"
	 level=level;longitude=longitude;latitude=latitude
         file=daily
	 NPERYEAR=366
         timescale=daily
         flatten=bin/flattennc;;
ENSEMBLES_RT3) ensembles_rt3_selected=selected
         path="http://ensemblesrt3.dmi.dk/cgi-bin/nph-dods/data/"
	 level=lev;longitude=lon;latitude=lat
         file="ERA40"
	 levels=2;MM=MM
         flatten=bin/fix_undef.sh;;
ENSEMBLES_RT2b) ensembles_rt2b_selected=selected
         path="http://ensemblesrt3.dmi.dk/cgi-bin/nph-dods/data/"
	 level=lev;longitude=lon;latitude=lat
         file="A1B"
	 levels=1;MM=MM
         flatten=bin/fix_undef.sh;;
ENSEMBLES_AMMA) ensembles_amma_selected=selected
         path="http://ensemblesrt3.dmi.dk/cgi-bin/nph-dods/data/"
	 level=lev;longitude=lon;latitude=lat
         file="AMMA"
	 levels=2;MM=MM
         flatten=bin/fix_undef.sh;;
Prudence) prudence_selected=selected
         path="http://ensemblesrt3.dmi.dk/cgi-bin/nph-dods/data/"
	 level=lev;longitude=lon;latitude=lat
         file="prudence/monthly"
	 levels=2;MM=""
         flatten=mv;;
SODA)    soda_selected=selected
         path=SODAData
	 level=depth;longitude=lon;latitude=lat
         file=soda.nc
         flatten=mv;;
SODA_surface) soda_surface_selected=selected
         path=SODAData
	 level=depth1_1;longitude=lon;latitude=lat
         file=SODA_2.0.2_Surface.cdf
         flatten=mv;;
ENACT)   enact_selected=selected
         path=http://data.ecmwf.int/thredds/dodsC
	 level=depth;longitude=longitude;latitude=latitude
         file=""
	 [ -n "$FORM_var" ] && . ./enact2file.cgi
         flatten=mv;;
ECMWF_ORA-S3_ocean)  ecmwf_s3_selected=selected
         path=http://ensembles.ecmwf.int/thredds/dodsC/ocean/ecmwf/og
	 level=level;longitude=longitude;latitude=latitude
         file=$FORM_var
         flatten=bin/del_dimension;;
ECMWF_ORA-S3_ocean_scalar)  s3_scalar_selected=selected
         path=http://apdrc.soest.hawaii.edu:80/dods/public_data/ORA-S3/
	 level=lev;longitude=lon;latitude=lat
         file="hope_scalar"
         flatten=mv;;
ECMWF_ORA-S3_ocean_vector)  s3_vector_selected=selected
         path=http://apdrc.soest.hawaii.edu:80/dods/public_data/ORA-S3/
	 level=lev;longitude=lon;latitude=lat
         file="hope_vector"
         flatten=mv;;
Reanalysis-2_fluxes) r2_flx_selected=selected
         path=http://nomad3.ncep.noaa.gov:9090/dods/reanalyses/reanalysis-2/month/flx
	 level=lev;longitude=lon;latitude=lat
         file=flx
         flatten=mv;;
Reanalysis-2_pressure) r2_pgb_selected=selected
         path=http://nomad3.ncep.noaa.gov:9090/dods/reanalyses/reanalysis-2/month/pgb
	 level=lev;longitude=lon;latitude=lat
         file=pgb
         flatten=mv;;
NCEP_NCAR_reanalysis) r1_selected=selected
         path=http://nomad3.ncep.noaa.gov:9090/dods/reanalyses/reanalysis-1/month/prs
	 level=lev;longitude=lon;latitude=lat
         file=prs
         flatten=mv;;
20th_century_reanalysis) c20_selected=selected
         path=http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/20thC_ReanV2/
	 level=lev;longitude=lon;latitude=lat
         file=monolevel
         flatten=mv;;
*)       CLASS=choose
         choose_selected=selected;;
esac
