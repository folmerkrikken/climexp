#!/bin/sh
sed -e 's@\([^,]*\),\([^,]*\),\([^,]*\).*@s/\2\\([0-9]*\\)<br>/\2\\1 (\1) [\3]<br>/@' -e 's/"//g' RCM_output_table_final.csv > RCM_output_table.sed
