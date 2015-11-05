[ "$EMAIL" = someone@somehere ] && EMAIL=someone@somewhere
c=`fgrep -c "^$EMAIL " log/list`
a=`echo "$EMAIL" | fgrep -c '@'`
if [ $c = 0 -o $a = 0 ];then
  string=$EMAIL
  if [ ${string#p.della} != $string ]; then
    string=spam
  fi
  EMAIL="someone@somewhere"
  id=someone@somewhere
  FORM_id=someone@somewhere
  . ./myvinkhead.cgi "Error" "Email addres \"$EMAIL\" unknown" "noindex,nofollow"
  echo "Please <a href=\"registerform.cgi\">register or log in</a>."
  . ./myvinkfoot.cgi
  exit
fi
