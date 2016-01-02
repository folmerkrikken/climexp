#!/bin/sh

. ./getargs.cgi
. ./searchengine.cgi

cat <<EOF
Content-Type: text/html
Last-modified: 2003-01-01 00:00:00

EOF

. ./myvinkhead.cgi "Time series" "Demeter Ni&ntilde;o indices" "index,nofollow"

cat <<EOF
<table class="realtable" width="100%" border='0' cellpadding='0' cellspacing='0'>
<tr>
<th>&nbsp;</th>
<th>analysis</th>
<th colspan="7" align="left"><a href="wipefoot.cgi?http://www.ecmwf.int/research/demeter/" target="_new">DEMETER</a> 1958/1987- 2001</th>
</tr><tr>
<th>Ensemble means</th>
<th>ERA-40</th>
<th>M&eacute;t&eacute;o France</th>
<th>CERFACS</th>
<th>LODYC</th>
<th>INGV</th>
<th>ECMWF</th>
<th>MPI</th>
<th>UKMO</th>
</tr><tr>
<th>variable</th>
<th>1958- 2001</th>
<th>1958- 2001</th>
<th>1987- 2001</th>
<th>1974- 2001</th>
<th>1987- 2001</th>
<th>1958- 2001</th>
<th>1969- 2001</th>
<th>1959- 2001</th>
</tr><tr>
<td>NINO12</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_era40_nino12&STATION=ERA40_NINO12&TYPE=i&id=$EMAIL">all</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_feb&STATION=MeteoFrance_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_feb&STATION=CERFACS_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_feb&STATION=LODYC_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_feb&STATION=INGV_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_feb&STATION=ECMWF_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_feb&STATION=MPI_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_feb&STATION=UKMO_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_may&STATION=MeteoFrance_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_may&STATION=CERFACS_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_may&STATION=LODYC_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_may&STATION=INGV_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_may&STATION=ECMWF_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_may&STATION=MPI_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_may&STATION=UKMO_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_aug&STATION=MeteoFrance_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_aug&STATION=CERFACS_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_aug&STATION=LODYC_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_aug&STATION=INGV_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_aug&STATION=ECMWF_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_aug&STATION=MPI_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_aug&STATION=UKMO_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_nov&STATION=MeteoFrance_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_nov&STATION=CERFACS_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_nov&STATION=LODYC_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_nov&STATION=INGV_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_nov&STATION=ECMWF_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_nov&STATION=MPI_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_nov&STATION=UKMO_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO3</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_era40_nino3&STATION=ERA40_NINO3&TYPE=i&id=$EMAIL">all</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_feb&STATION=MeteoFrance_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_feb&STATION=CERFACS_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_feb&STATION=LODYC_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_feb&STATION=INGV_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_feb&STATION=ECMWF_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_feb&STATION=MPI_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_feb&STATION=UKMO_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_may&STATION=MeteoFrance_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_may&STATION=CERFACS_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_may&STATION=LODYC_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_may&STATION=INGV_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_may&STATION=ECMWF_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_may&STATION=MPI_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_may&STATION=UKMO_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_aug&STATION=MeteoFrance_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_aug&STATION=CERFACS_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_aug&STATION=LODYC_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_aug&STATION=INGV_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_aug&STATION=ECMWF_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_aug&STATION=MPI_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_aug&STATION=UKMO_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_nov&STATION=MeteoFrance_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_nov&STATION=CERFACS_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_nov&STATION=LODYC_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_nov&STATION=INGV_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_nov&STATION=ECMWF_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_nov&STATION=MPI_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_nov&STATION=UKMO_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO3.4</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_era40_nino3.4&STATION=ERA40_NINO3.4&TYPE=i&id=$EMAIL">all</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_feb&STATION=MeteoFrance_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_feb&STATION=CERFACS_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_feb&STATION=LODYC_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_feb&STATION=INGV_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_feb&STATION=ECMWF_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_feb&STATION=MPI_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_feb&STATION=UKMO_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_may&STATION=MeteoFrance_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_may&STATION=CERFACS_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_may&STATION=LODYC_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_may&STATION=INGV_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_may&STATION=ECMWF_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_may&STATION=MPI_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_may&STATION=UKMO_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_aug&STATION=MeteoFrance_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_aug&STATION=CERFACS_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_aug&STATION=LODYC_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_aug&STATION=INGV_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_aug&STATION=ECMWF_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_aug&STATION=MPI_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_aug&STATION=UKMO_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_nov&STATION=MeteoFrance_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_nov&STATION=CERFACS_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_nov&STATION=LODYC_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_nov&STATION=INGV_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_nov&STATION=ECMWF_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_nov&STATION=MPI_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_nov&STATION=UKMO_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO4</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_era40_nino4&STATION=ERA40_NINO4&TYPE=i&id=$EMAIL">all</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_feb&STATION=MeteoFrance_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_feb&STATION=CERFACS_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_feb&STATION=LODYC_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_feb&STATION=INGV_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_feb&STATION=ECMWF_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_feb&STATION=MPI_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_feb&STATION=UKMO_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_may&STATION=MeteoFrance_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_may&STATION=CERFACS_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_may&STATION=LODYC_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_may&STATION=INGV_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_may&STATION=ECMWF_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_may&STATION=MPI_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_may&STATION=UKMO_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_aug&STATION=MeteoFrance_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_aug&STATION=CERFACS_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_aug&STATION=LODYC_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_aug&STATION=INGV_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_aug&STATION=ECMWF_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_aug&STATION=MPI_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_aug&STATION=UKMO_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_nov&STATION=MeteoFrance_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_nov&STATION=CERFACS_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_nov&STATION=LODYC_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_nov&STATION=INGV_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_nov&STATION=ECMWF_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_nov&STATION=MPI_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_nov&STATION=UKMO_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<th>Full ensembles</th>
<th>&nbsp;</th>
<th>M&eacute;t&eacute;o France</th>
<th>CERFACS</th>
<th>LODYC</th>
<th>INGV</th>
<th>ECMWF</th>
<th>MPI</th>
<th>UKMO</th>
</tr><tr>
<th>variable</th>
<th>&nbsp;</th>
<th>1958- 2001</th>
<th>1987- 2001</th>
<th>1974- 2001</th>
<th>1987- 2001</th>
<th>1958- 2001</th>
<th>1969- 2001</th>
<th>1959- 2001</th>
</tr><tr>
<td>NINO12</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_feb_%%&STATION=MeteoFrance_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_feb_%%&STATION=CERFACS_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_feb_%%&STATION=LODYC_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_feb_%%&STATION=INGV_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_feb_%%&STATION=ECMWF_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_feb_%%&STATION=MPI_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_feb_%%&STATION=UKMO_NINO12_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_may_%%&STATION=MeteoFrance_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_may_%%&STATION=CERFACS_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_may_%%&STATION=LODYC_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_may_%%&STATION=INGV_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_may_%%&STATION=ECMWF_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_may_%%&STATION=MPI_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_may_%%&STATION=UKMO_NINO12_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_aug_%%&STATION=MeteoFrance_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_aug_%%&STATION=CERFACS_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_aug_%%&STATION=LODYC_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_aug_%%&STATION=INGV_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_aug_%%&STATION=ECMWF_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_aug_%%&STATION=MPI_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_aug_%%&STATION=UKMO_NINO12_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino12_nov_%%&STATION=MeteoFrance_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino12_nov_%%&STATION=CERFACS_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino12_nov_%%&STATION=LODYC_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino12_nov_%%&STATION=INGV_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino12_nov_%%&STATION=ECMWF_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino12_nov_%%&STATION=MPI_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino12_nov_%%&STATION=UKMO_NINO12_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO3</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_feb_%%&STATION=MeteoFrance_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_feb_%%&STATION=CERFACS_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_feb_%%&STATION=LODYC_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_feb_%%&STATION=INGV_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_feb_%%&STATION=ECMWF_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_feb_%%&STATION=MPI_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_feb_%%&STATION=UKMO_NINO3_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_may_%%&STATION=MeteoFrance_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_may_%%&STATION=CERFACS_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_may_%%&STATION=LODYC_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_may_%%&STATION=INGV_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_may_%%&STATION=ECMWF_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_may_%%&STATION=MPI_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_may_%%&STATION=UKMO_NINO3_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_aug_%%&STATION=MeteoFrance_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_aug_%%&STATION=CERFACS_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_aug_%%&STATION=LODYC_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_aug_%%&STATION=INGV_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_aug_%%&STATION=ECMWF_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_aug_%%&STATION=MPI_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_aug_%%&STATION=UKMO_NINO3_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3_nov_%%&STATION=MeteoFrance_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3_nov_%%&STATION=CERFACS_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3_nov_%%&STATION=LODYC_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3_nov_%%&STATION=INGV_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3_nov_%%&STATION=ECMWF_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3_nov_%%&STATION=MPI_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3_nov_%%&STATION=UKMO_NINO3_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO3.4</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_feb_%%&STATION=MeteoFrance_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_feb_%%&STATION=CERFACS_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_feb_%%&STATION=LODYC_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_feb_%%&STATION=INGV_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_feb_%%&STATION=ECMWF_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_feb_%%&STATION=MPI_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_feb_%%&STATION=UKMO_NINO3.4_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_may_%%&STATION=MeteoFrance_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_may_%%&STATION=CERFACS_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_may_%%&STATION=LODYC_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_may_%%&STATION=INGV_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_may_%%&STATION=ECMWF_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_may_%%&STATION=MPI_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_may_%%&STATION=UKMO_NINO3.4_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_aug_%%&STATION=MeteoFrance_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_aug_%%&STATION=CERFACS_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_aug_%%&STATION=LODYC_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_aug_%%&STATION=INGV_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_aug_%%&STATION=ECMWF_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_aug_%%&STATION=MPI_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_aug_%%&STATION=UKMO_NINO3.4_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino3.4_nov_%%&STATION=MeteoFrance_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino3.4_nov_%%&STATION=CERFACS_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino3.4_nov_%%&STATION=LODYC_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino3.4_nov_%%&STATION=INGV_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino3.4_nov_%%&STATION=ECMWF_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino3.4_nov_%%&STATION=MPI_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino3.4_nov_%%&STATION=UKMO_NINO3.4_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr><tr>
<td>NINO4</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_feb_%%&STATION=MeteoFrance_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_feb_%%&STATION=CERFACS_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_feb_%%&STATION=LODYC_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_feb_%%&STATION=INGV_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_feb_%%&STATION=ECMWF_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_feb_%%&STATION=MPI_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_feb_%%&STATION=UKMO_NINO4_feb&TYPE=i&id=$EMAIL">feb</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_may_%%&STATION=MeteoFrance_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_may_%%&STATION=CERFACS_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_may_%%&STATION=LODYC_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_may_%%&STATION=INGV_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_may_%%&STATION=ECMWF_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_may_%%&STATION=MPI_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_may_%%&STATION=UKMO_NINO4_may&TYPE=i&id=$EMAIL">may</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_aug_%%&STATION=MeteoFrance_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_aug_%%&STATION=CERFACS_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_aug_%%&STATION=LODYC_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_aug_%%&STATION=INGV_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_aug_%%&STATION=ECMWF_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_aug_%%&STATION=MPI_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_aug_%%&STATION=UKMO_NINO4_aug&TYPE=i&id=$EMAIL">aug</a></td>
</tr><tr>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_meteofrance_nino4_nov_%%&STATION=MeteoFrance_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_cerfacs_nino4_nov_%%&STATION=CERFACS_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_lodyc_nino4_nov_%%&STATION=LODYC_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ingv_nino4_nov_%%&STATION=INGV_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ecmwf_nino4_nov_%%&STATION=ECMWF_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_mpi_nino4_nov_%%&STATION=MPI_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
<td align="center"><a href="getindices.cgi?WMO=DemeterData/demeter_ukmo_nino4_nov_%%&STATION=UKMO_NINO4_nov&TYPE=i&id=$EMAIL">nov</a></td>
</tr>
</table>
EOF
. ./myvinkfoot.cgi
