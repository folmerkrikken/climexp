function danoloop(args)
*
*	GrADS script to loop over an anomaly field
*	run danoloop field date1 date2 args ...
*
*		GJvO KNMI feb-1997
*
field=subwrd(args,1)
t1=subwrd(args,2)
t2=subwrd(args,3)
i=3
arg=''
while ( a != '' )
  i=i+1
  a=subwrd(args,i)
  arg=arg' 'a
endwhile
if ( t1 > -10000 & t1 < 10000 )
'set t 't1
else
'set time 't1
'q dims'
lin=sublin(result,5)
t1=subwrd(lin,9)
say 't1 = 't1
endif
if ( t2 > -10000 & t2 < 10000 )
'set t 't2
else
'set time 't2
'q dims'
lin=sublin(result,5)
t2=subwrd(lin,9)
say 't2 = 't2
endif
t=t1
if ( t1 <= t2 )
while ( t <= t2 )
say 'run dano 'field' 't' 'arg
'run dano 'field' 't' 'arg
if ( result = '' )
'q dims'
lin=sublin(result,5)
time=subwrd(lin,6)
date=substr(time,6,7)
'draw title 'field' 'date
'print'
endif
t = t+1
endwhile
else
while ( t >= t2 )
say 'run dano 'field' 't' 'arg
'run dano 'field' 't' 'arg
'q dims'
lin=sublin(result,5)
time=subwrd(lin,6)
date=substr(time,6,7)
'draw title 'field' 'date
'print'
t = t-1
endwhile
endif
return
