#!/bin/bash
case "$FORM_verif" in
likelihood)       checked_likelihood="checked";;
deterministic)    checked_deterministic="checked";;
brierscore)       checked_brierscore="checked";;
fairbrierscore)   checked_fairbrierscore="checked";;
fairCRPSanalysis) checked_fairCRPSanalysis="checked";;
rankhistogram)    checked_rankhistogram="checked";;
reliability)      checked_reliability="checked";;
rps)              checked_rps="checked";;
rocrclim)         checked_rocrclim="checked";;
rocprob)          checked_rocprob="checked";;
rocdeb)           checked_rocdeb="checked";;
rocthreshold)     checked_rocthreshold="checked";;
debug)            checked_debug="checked";;
esac

cat << EOF
<p><div class="formheader">Timeseries verification measures</div>
<div class="formbody">
<input type="radio" name="verif" value="likelihood" $checked_likelihood>Plot likelihood <br>
<input type="radio" name="verif" value="deterministic" $checked_deterministic>Deterministic scores
 for the ensemble mean (correlation, root mean squared error, and mean absolute error) <br>
EOF
if [ "$ENSEMBLE" = true ]; then
cat <<EOF
<input type="radio" name="verif" value="brierscore" $checked_brierscore>Brier score<br>
<input type="radio" name="verif" value="fairbrierscore" $checked_fairbrierscore>Fair Brier score<br>
<input type="radio" name="verif" value="fairCRPSanalysis" $checked_fairCRPSanalysise>Fair CRPS analysis<br>
<input type="radio" name="verif" value="rankhistogram" $checked_rankhistogram>Rank histogram analysis<br>
<input type="radio" name="verif" value="reliability" $checked_reliability>Plot reliability diagram<br>
<input type="radio" name="verif" value="rps" $checked_rps>Compute Ranked Probability Score for terciles<br>
EOF
fi
cat << EOF
<input type="radio" name="verif" value="rocrclim" $checked_rocrclim>Plot ROC curve for number of ensemble members below threshold,
<input type="radio" name="verif" value="rocprob" $checked_rocprob>alternative<br>
<!--<input type="radio" name="verif" value="rocdeb" $checked_rocdeb>alternative2-->
<!--<input type="radio" name="verif" value="rocthreshold" $checked_rocthreshold>Plot ROC curve varying the model threshold<br>-->
<input type="radio" name="verif" value="debug" $checked_debug>Only compute the observations/forecasts table
</div>
EOF
