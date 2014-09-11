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
[ -z "$EMAIL" ] && EMAIL=someone@somewhere
###sed -e "s/EMAIL/$EMAIL/" ./menu_standard.html
sed -e "s/EMAIL/$EMAIL/" ./menu_choose.html
if [ -n "$listname" -o -n "$FORM_listname" ]; then
  . ./menu_investigateset.cgi
elif [ -n "$STATION" ]; then
  . ./menu_investigate.cgi
fi
###echo "FORM_field=$FORM_field"
if [ -n "$field2" ]; then
  FORM_field=$field1
  kindname=$kindname1
  climfield=$climfield1
  . ./menu_investigatefield.cgi | tr '_' ' '
  FORM_field=$field2
  kindname=$kindname2
  climfield=$climfield2
  . ./menu_investigatefield.cgi
elif [ -n "$FORM_field" ]; then
  . ./menu_investigatefield.cgi
fi
[ -x "./$1.cgi" ] && . "./$1.cgi"
###cat ./menu_contact.html
cat <<EOF
      </td>
   </tr>
</table>
EOF
cat ./vinklude/bottom_en.html
cat <<EOF
</body>
</html>
EOF
