#!/bin/sh
case "$FORM_verif" in
mapcorr)        checked_mapcorr="checked";;
mapdiscmean)    checked_mapdiscmean="checked";;
maprmse)        checked_maprmse="checked";;
mapmae)         checked_mapmae="checked";;
mapbrier)       checked_mapbrier="checked";;
mapbriar)       checked_mapbriar="checked";;
mapresolution)  ckecked_mapresolution="checked";;
mapreliability) checked_mapreliability="checked";;
mapuncertainty) checked_mapuncertainty="checked";;
mapbss)         checked_mapbss="checked";;
mapbsspersist)  checked_mapbsspersist="checked";;
mapbssnino34)   checked_mapbssnino34="checked";;
maprps)         checked_maprps="checked";;
maprpss)        checked_maprpss="checked";;
maprpss5)       checked_maprpss5="checked";;
maprps3)        checked_maprps3="checked";;
maprps5)        checked_maprps5="checked";;
maprocarea)     checked_maprocarea="checked";;
maproc)         checked_maproc="checked";;
maprocdeb)      checked_maprocdeb="checked";;
mapdebug)       checked_mapdebug="checked";;
esac

cat << EOF
<p><div class="formheader">Map verification measures</div>
<div class="formbody">
<input type="radio" name="verif" value="mapcorr" $checked_mapcorr>Correlation of the ensemble mean<br>
<input type="radio" name="verif" value="mapdiscmean" $checked_mapdiscmean>Discrimination score of the ensemble mean (1+&tau;)/2<br>
<input type="radio" name="verif" value="maprmse" $checked_maprmse>Root mean square error (RMSE) of the ensemble mean<br>
<input type="radio" name="verif" value="mapmae" $checked_mapmae>Mean absolute error (MAE) of the ensemble mean<br>
EOF
if [ "$ENSEMBLE" = true ]; then
cat <<EOF
<input type="radio" name="verif" value="mapbrier" $checked_mapbrier>Brier score<br>
<input type="radio" name="verif" value="mapresolution" $checked_mapresolution>&nbsp;Resolution<br>
<input type="radio" name="verif" value="mapreliability" $checked_mapreliability>&nbsp;Reliability<br>
<input type="radio" name="verif" value="mapuncertainty" $checked_mapuncertainty>&nbsp;Uncertainty<br>
<input type="radio" name="verif" value="mapbss" $checked_mapbss>BSS wrt climatology (including <a href="http://www.meteoschweiz.ch/nccr/weigel/weigel_brier_rpss_MWR2006.pdf">bias correction</a> for finite ensemble size)<br>
<!--
<input type="radio" name="verif" value="mapbsspersist" $checked_mapbsspersist>BSS wrt damped persistence<br>
-->
<input type="radio" name="verif" value="maprps" $checked_maprps>Tercile RPS<!--
<input type="radio" name="verif" value="maprps3" $checked_maprps3>alternative,
<input type="radio" name="verif" value="maprps5" $checked_maprps5>quintile RPS--><br>
<input type="radio" name="verif" value="maprpss" $checked_maprpss>Tercile RPSS wrt climatology, 
<input type="radio" name="verif" value="maprpss5" $checked_maprpss5>Quintile RPSS wrt climatology (including <a href="http://www.meteoschweiz.ch/nccr/weigel/weigel_brier_rpss_MWR2006.pdf">bias correction</a> for finite ensemble size)<br>
<input type="radio" name="verif" value="maproc" $checked_maproc>Area under the ROC curve<br>
<!--
<input type="radio" name="verif" value="maprocarea" $checked_maprocarea>R alternative, <input type="radio" name="verif" value="maprocdeb" $checked_maprocdeb>C alternative<br>
-->
<br>
EOF
fi
cat << EOF
<input type="radio" name="verif" value="mapdebug" $checked_mapdebug>Only compute the netcdf files with observations and forecasts
</div>
EOF
