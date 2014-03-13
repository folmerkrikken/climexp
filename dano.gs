function dano(args)
*
*	GrADS script to display an anomaly field in a nice way
*	Version with hardcoded levels.
*
*		GJvO KNMI feb-1997
*
field=subwrd(args,1)
time=subwrd(args,2)
shadingtype=subwrd(args,3)
flipcolor=subwrd(args,4)
cbar=subwrd(args,5)
ylint=subwrd(args,6)
if ( ylint = '' )
  ylint="0"
endif
cmin=subwrd(args,7)
cmax=subwrd(args,8)
cint=subwrd(args,9)
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
      say 'time in steps 'time
      'set t 'time' 'time2
   else
      say 'time in date 'time
      'set time 'time' 'time2
   endif
endif
'q time'
t1=subwrd(result,3)
dy=substr(t1,4,2)
mo=substr(t1,6,3)
yr=substr(t1,9,4)
say 'run danod 'field' 'shadingtype' 'flipcolor' 'ylint' 'cmin' 'cmax' 'cint
'run danod 'field' 'shadingtype' 'flipcolor' 'ylint' 'cmin' 'cmax' 'cint
***'draw title 'field' 'dy'-'mo'-'yr
say field' 'dy'-'mo'-'yr
***'draw title 'field' 'mo
say 'cbar = 'cbar
if ( cbar != '' & cbar != '-1' & cbar != 'off' )
  'run cbarn'
endif

return result
