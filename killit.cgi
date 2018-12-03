#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

cat <<EOF
<html>
<head>
<title>Killing a Climate Explorer job</title>
</head>
<body bgcolor="ff0000">

<h2>Killing a Climate Explorer job</h2>

<p>
EOF
. ./getargs.cgi
pid="$FORM_pid"
if [ ! -f pid/$pid.$EMAIL ]; then
  echo "Cannot locate the job $pid.$EMAIL.  Has it finished already?"
else
  ip=`head -1 pid/$pid.$EMAIL`
  if [ $ip != $REMOTE_ADDR ]; then
    echo "Please kill the job from the same computer from which it was launched."
    echo "You are now at $REMOTE_ADDR"
  else
    desc=`head -2 pid/$pid.$EMAIL | tail -1 | sed -e "s:$DIR/::g"`
    child=`tail -1 pid/$pid.$EMAIL`
    if [ "$child" = "@" ]; then
      echo "killit: cannot find the job $desc<br>"
      echo "killit: cannot find the job $desc" 1>&2
      exit -1
    fi
    echo "Killing job $child of user $EMAIL:<br>$desc<br><pre>"
    ps p $child
    # this kills the child, i.e., the long-running Fortran job
    kill $child
    rm pid/$pid.$EMAIL
    echo `date` "$EMAIL ($REMOTE_ADDR) killed $desc" >> log/log
    sleep 1
    ps p $child
    echo "</pre><br><br>Dead."
  fi
fi

cat <<EOF
<p><address><a href="mailto:oldenborgh@knmi.nl">G. J. van Oldenborgh</a>, KNMI, 14-jan-2005</address>
</body>
</html>
EOF
