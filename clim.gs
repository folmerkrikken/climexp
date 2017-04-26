function clim(args)
*
*	construct a climatology from a field
*
say 'This is clim, args = 'args
field=subwrd(args,1)
nperyear=subwrd(args,2)
time=subwrd(args,3)
sum=subwrd(args,4)
yr1=subwrd(args,5)
yr2=subwrd(args,6)
*
if ( time = '1year' )
   'q file'
   line=sublin(result,5)   
   say line
   time2=subwrd(line,12)
   say 'set t 1 'time2
   'set t 1 'time2
* this is very dirty - I assume lag plots do not have 12 values
   if ( time2 = 12 )
      av = substr(field,1,4)
      if ( av = 'ave(' )
         komma=6
         while ( komma < 20 )
           if ( substr(field,komma,1) = ',' ); break; endif
           komma = komma + 1
         endwhile
         realfield = substr(field,5,komma-5)
         'define 'realfield' = 'realfield
         'modify 'realfield' seasonal'
      else
         'define 'field' = 'field
         'modify 'field' seasonal'
      endif
      'set t 0.5 12.5'
   endif
else
   sep=substr(time,9,1)
   if ( sep = ':' )
      time2=substr(time,10,8)
      time=substr(time,1,8)
   else
      time2=''
   endif
   if ( time > -10000 & time < 10000 )
      say 'time in steps 'time' 'time2
      'set t 'time' 'time2
   else
      say 'time in date 'time' 'time2
      'set time 'time' 'time2
   endif
endif
'q time'
t1=subwrd(result,3)
dy=substr(t1,4,2)
mo=substr(t1,6,3)
yr=substr(t1,9,4)

if ( yr1 > 1899 )
  yy1=substr(yr1,3,2)
else
  yy1=yr1
endif
if ( yr2 > 1899 )
  yy2=substr(yr2,3,2)
else
  yy2=yr2
endif

'set dfile 2'
'set t 1 'nperyear
'set z 1'
'q dims'
say result
line=sublin(result,4)
varying=subwrd(line,3)
if ( varying = 'varying' )
  z1=subwrd(line,11)
  z2=subwrd(line,13)
  if ( z1 > z2 )
    'set z 'z2' 'z1
  endif
endif
if ( yr1 > 0 | yr2 > 0 )
    say 'define clim'yy1 yy2' = 'field'.2'
    'define clim'yy1 yy2' = 'field'.2'
else
    say 'define clim = 'field'.2'
    'define clim = 'field'.2'
endif
if ( nperyear = 12 )
    'modify clim seasonal'
endif
'set dfile 1'
'set z 1'
