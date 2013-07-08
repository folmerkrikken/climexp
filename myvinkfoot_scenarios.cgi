#!/bin/sh
cat <<EOF
         </div>
         </div>
<!-- Insert the body of the page above this line -->
      </td>
      <td width="11">&nbsp;</td>
      <td width=220 valign=top>
<!-- Voeg hieronder de lijst met links in -->
EOF
cat Scenarios_monthly/menu.html
cat <<EOF
      </td>
   </tr>
</table>
EOF
sed -e 's@href="/@href="http://www.knmi.nl/@g' ./vinklude/rijksbottomfloat.html
cat <<EOF
</body>
</html>
EOF
