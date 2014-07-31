[ "$EMAIL" = someone@somehere ] && EMAIL=someone@somewhere
c=`fgrep -c "^$EMAIL " log/list`
a=`echo "$EMAIL" | fgrep -c '@'`
if [ $c = 0 -o $a = 0 ];then
  . ./myvinkhead.cgi "Error" "Email addres \"$EMAIL\" unknown" "noindex,nofollow"
  echo "Please <a href=\"registerform.cgi\">register or log in</a>."
  EMAIL="someone@somewhere"
  . ./myvinkfoot.cgi
  exit
fi
