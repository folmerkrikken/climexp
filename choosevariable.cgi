#!/bin/sh
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
  def=./prefs/$EMAIL.choosevariable
  if [ -s "$def" ]; then
    eval `egrep '^FORM_[a-z]*=[a-zA-Z0-9.]*;$' $def`
  fi
fi
case $FORM_var in
cov) cov_checked=checked;;
sign) sign_checked=checked;;
regr) regr_checked=checked;;
errorregr) errorregr_checked=checked;;
intercept) intercept_checked=checked;;
regr1) regr1_checked=checked;;
relregr) relregr_checked=checked;;
composite) composite_checked=checked;;
errorcomp) errorcomp_checked=checked;;
chi) chi_checked=checked;;
chibar) chibar_checked=checked;;
*) corr_checked=checked;;
esac

cat << EOF
<input type="radio" class="formradio" name="var" value="corr" $corr_checked>correlation
<input type="radio" class="formradio" name="var" value="cov" $cov_checked>covariance
<input type="radio" class="formradio" name="var" value="sign" $sign_checked>significance
<br>
<input type="radio" class="formradio" name="var" value="regr" $regr_checked>regression
(<input type="radio" class="formradio" name="var" value="errorregr" $errorregr_checked>error)
<input type="radio" class="formradio" name="var" value="regr1" $regr1_checked>reverse
<input type="radio" class="formradio" name="var" value="relregr" $relregr_checked>relative regression
<br>
<input type="radio" class="formradio" name="var" value="composite" $composite_checked>composite
(<input type="radio" class="formradio" name="var" value="errorcomp" $errorcomp_checked>error)
<!-- <input type="radio" class="formradio" name="var" value="abs(corr)">abs(corr)<br> -->
<br>
extreme dependence measures
<input type="radio" class="formradio" name="var" value="chi" $ch_checked>&chi;,
<input type="radio" class="formradio" name="var" value="chibar" $chibar_checked>&chi;bar,
threshold
<input type="$number" step=any class="forminput" name="threshold" $textsize2  style="width: 4em;" value="${FORM_threshold:-90}">%
<br>
EOF
