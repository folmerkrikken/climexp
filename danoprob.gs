function dano(args)
*
*	GrADS script to display an anomaly field in a nice way
*	Version with hardcoded levels.
*
*		GJvO KNMI feb-1997 - now
*
say 'This is danoprob with args 'args
field=subwrd(args,1)
time=subwrd(args,2)
shadingtype=subwrd(args,3)
if ( substr(shadingtype,1,6) = geotif )
  file=substr(shadingtype,9,100)
  shadingtype=geotiff
  say 'exporting geotiff to file 'file
endif
flipcolor=subwrd(args,4)
say 'flipcolor = 'flipcolor
cbar=subwrd(args,5)
xylint=subwrd(args,6)
if ( xylint = '' )
  xylint = "0"
endif
if ( xylint = 'log' )
  ylogscale = "true"
  xylint = "0"
endif
if ( xylint = 'yflip' )
  yflip = "true"
  xylint = "0"
endif
if ( xylint = 'yfliplog' )
  yflip = "true"
  ylogscale = "true"
  xylint = "0"
endif
pmin=subwrd(args,7)
maskout=mask
colon=1
while ( colon < strlen(pmin) )
   colon=colon+1
   if ( substr(pmin,colon,1) = ':' )
       maskout=substr(pmin,colon+1,strlen(pmin)-colon)
       say 'maskout='maskout
       pmin=substr(pmin,1,colon-1)
       say 'pmin='pmin
   endif
endwhile
cmin=subwrd(args,8)
cmax=subwrd(args,9)
cint=subwrd(args,10)
scale = lin
if ( cmin = 'log' )
    scale = log
    cmin = ''
endif
if ( cmax = 'log' )
    scale = log
    cmax = ''
endif
if ( cint = 'log' )
    scale = log
    cint = ''
endif
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
   i=2
   isep=0
   while ( i < 10 )
      sep=substr(time,i,1)
      if ( sep = ':' )
         isep=i
      endif
      i=i+1
   endwhile
   if ( isep > 0 )
      time2=substr(time,isep+1,8)
      time=substr(time,1,isep-1)
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
'q dims'
say result
line=sublin(result,4)
varying=subwrd(line,3)
if ( varying = 'varying' )
  z1=subwrd(line,11)
  z2=subwrd(line,13)
  if ( z1 > z2 )
    say 'Z-axis decreases, flip'
    say 'set z 'z2' 'z1
    'set z 'z2' 'z1
  endif
endif

if ( cmin != '' & cmax != '' & cint = '' )
cint = (cmax-cmin)/10
endif
clevs = NULL
*
if ( flipcolor = '' )
flipped=0
else
flipped=flipcolor
endif
*
if ( ylogscale = 'true' )
  setylevs='set ylevs 0.001 0.002 0.005 0.01 0.02 0.05 0.1 0.2 0.5 1 2 5 10 20 50 100 200 500 1000 2000 5000'
else
  setylevs=''
endif

* no pattern matching in GrADS?
say 'determining scale...'
if ( field = mae | field = rmse | field = bs )
  if ( cmin = '' )
    cmin=0
  endif
endif
if ( field = roc )
  if ( cmin = '' )
    cmin = 0
  endif
  if ( cmax = '' )
    cmax = 1
  endif
endif
if ( field = cor )
  if ( cmin = '' )
    cmin = -1
  endif
  if ( cmax = '' )
    cmax = 1
  endif
endif
if ( field = corr )
  clevs='-0.6 -0.5 -0.4 -0.3 -0.2 0.2 0.3 0.4 0.5 0.6'
else
  if ( field = sign )
    clevs='0.9 0.95 0.99 0.995 0.999 0.9995 0.9999'
    flipped=13
  else
    if ( field = prob )
      clevs='0.0001 0.0005 0.001 0.005 0.01 0.05 0.1'
      flipped=7
    else
      if ( substr(field,1,9) = bo_pot_rt | substr(field,1,10) = bo_norm_rt | substr(field,1,9) = bo_gev_rt )
        clevs='-200 -100 -50 -20 -10 10 20 50 100 200'
    else
      if ( substr(field,1,2) = rt | substr(field,1,4) = lort | substr(field,1,4) = hirt | substr(field,1,6) = pot_rt | substr(field,4,9) = pot_rt | substr(field,1,7) = norm_rt | substr(field,4,10) = norm_rt | substr(field,1,6) = gev_rt | substr(field,4,10) = gev_rt )
        clevs='20 50 100 200 500 1000'
        flipped=13
      else
*
*	figure out maxval from the field
*
        if ( cmin = '' | cmax = '' )
          say 'figure out maxval from the field'
          'set gxout contour'
          say 'd 'field
          'd 'field
          say 'result = 'result
          i=1
          line=sublin(result,i)
          if ( subwrd(line,1) = 'Averaging.' )
            i=i+1
            line=sublin(result,i)
            say 'line = 'line
          endif
          while ( subwrd(line,1) = '***' )
            i=i+1
            line=sublin(result,i)
          endwhile
          if ( subwrd(line,i) = 'Constant' )
            cmax=subwrd(line,5)
            cmin=-cmax
            cint = (cmax-cmin)/10
          else
            if ( cmin = '' )
              cmin=subwrd(line,2)
            endif
            if ( cmax = '' )
              cmax=subwrd(line,4)
            endif
            if ( cint = '' )
              cint=subwrd(line,6)
            endif
          endif
* make sure we get 10 intervals
          if ( cint != '' )
            say 'cmin,cmax,cint = 'cmin', 'cmax', 'cint
            if ( cmax != cmin + 10*cint )
              n = 10 - (cmax - cmin)/cint
              if ( cmin != 0 )
                cmin = cmin - (n-n/2)*cint
                cmax = cmax + (n/2)*cint
              else
                cmax = cmin + 10*cint
              endif
            else
              cint = (cmax-cmin)/10
            endif
          endif
* make the range symmetric if close to it
          if ( flipped = 0 | flipped = 1 | flipped = 10 | flipped = 11 )
            say 'Symmetric colourbar 'flipped
            s = cmax+cmin
            if ( s < 0 )
              s = -s
            endif
            if ( s < 4*cint )
              say 'Adjusting cmin,cmax to symmetric, |cmin+cmax|='s' < 4*cint='4*cint
              cmax = 5*cint
              cmin = -5*cint
            endif
          endif
        endif
        if ( cint = '' )
          cint = (cmax-cmin)/10
        endif
        say 'taking cmin,cmax,cint = 'cmin' 'cmax' 'cint
        'clear'
      endif
    endif
    endif
  endif
endif
xlint=''
ylint=''
if ( substr(xylint,2,1) = ':' )
  xlint=substr(xylint,1,1)
  ylint=substr(xylint,3,3)
endif
if ( substr(xylint,3,1) = ':' )
  xlint=substr(xylint,1,2)
  ylint=substr(xylint,4,3)
endif
if ( substr(xylint,4,1) = ':' )
  xlint=substr(xylint,1,3)
  ylint=substr(xylint,5,3)
endif
say 'xylint,xlint,ylint = 'xylint' 'xlint' 'ylint
if ( xlint != 0 & xlint != '' )
'set xlint 'xlint
endif
if ( ylint != 0 & ylint != '' )
'set ylint 'ylint
endif
if ( shadingtype = shaded | shadingtype = shadedcontour )
  'set gxout shaded'
else
  'set gxout 'shadingtype
  if ( shadingtype = geotiff )
  'set geotiff 'file
  endif
endif
* "new" colours from http://www.colorbrewer2.org
if ( flipped = 10 | flipped = 11 )
'set rgb 50 248 248 248'
'set rgb 34  49  54 149'
'set rgb 24  69 117 180'
'set rgb 31 116 217 233'
'set rgb 23 171 217 233'
'set rgb 30 224 243 248'
'set rgb 27 254 224 144'
'set rgb 32 253 174  97'
'set rgb 28 244 109  67'
'set rgb 22 215  48  39'
'set rgb 26 165   0  38'
* no light colours for the new schemes...
else
if ( flipped = 13 | flipped = 18 )
'set rgb 50 248 248 248'
'set rgb 21 254 240 217'
'set rgb 22 253 212 158'
'set rgb 23 253 187 132'
'set rgb 24 252 141 89'
'set rgb 25 227 74 51'
'set rgb 26 179 0 0'
else
if ( flipped = 12 | flipped = 14 | flipped = 19 )
'set rgb 50 248 248 248'
'set rgb 21 241 238 246'
'set rgb 22 208 209 230'
'set rgb 23 166 189 219'
'set rgb 24 116 169 207'
'set rgb 25 43 140 190'
'set rgb 26 4 90 141'
'set rgb 27 253 187 132'
'set rgb 28 252 141 89'
'set rgb 29 227 74 51'
'set rgb 30 179 0 0'
'set rgb 31 0 0 0'
else
'set rgb 50 222 222 222'
* insert output from ligtcolour below
* factor 2
'set rgb 52 252 158 158'
'set rgb 53 128 237 128'
'set rgb 54 143 158 255'
'set rgb 55 128 227 227'
'set rgb 56 247 128 193'
'set rgb 57 242 237 152'
'set rgb 58 247 193 148'
'set rgb 59 208 128 227'
'set rgb 60 208 242 152'
'set rgb 61 128 208 255'
'set rgb 62 242 215 150'
'set rgb 63 128 232 198'
'set rgb 64 193 128 237'
'set rgb 65 213 213 213'
'set rgb 70 238 238 238'
* end of output of lightcolour
* factor 4 (shifted by 20)
'set rgb 72 254 207 207'
'set rgb 73 191 246 191'
'set rgb 74 199 207 255'
'set rgb 75 191 241 241'
'set rgb 76 251 191 224'
'set rgb 77 249 246 203'
'set rgb 78 251 224 201'
'set rgb 79 231 191 241'
'set rgb 80 231 249 203'
'set rgb 81 191 231 255'
'set rgb 82 249 235 203'
'set rgb 83 191 244 226'
'set rgb 84 224 191 246'
'set rgb 85 234 234 234'
'set rgb 90 247 247 247'
* end lightcolour defs
endif
endif
endif

if ( flipped = 9 )
say 'blue - red - grey colourbar'
rbcols1='set rbcols 11  3 10  7 12  8  2  6  9 14  4 50'
else
if ( flipped = 19 )
say 'new blue - grey colourbar'
rbcols1='set rbcols  26 25 24 23 22 21 50'
else
if ( flipped = 8 )
say 'red - blue - grey colourbar'
rbcols1='set rbcols  9  6  2  8 12  7 10  3 11  4 14 50'
else
if ( flipped = 18 )
say 'new red - grey colourbar'
rbcols1='set rbcols 26 25 24 23 22 21 50'
else
if ( flipped = 7 )
rbcols1='set rbcols 6 2 8 12 7 10 3 50'
else
if ( flipped = 6 ) 
rbcols1='set rbcols 14 4 11 3 10 50  7 12 8 2 6'
else
if ( flipped = 5 ) 
rbcols1='set rbcols 11 3 10 50 7 12 8'
else
if ( flipped = 4 ) 
rbcols1='set rbcols 50 6 2 8 12 7 10 3 11 4 14'
else
if ( flipped = 3 ) 
say 'grey - blue - red colourbar'
rbcols1='set rbcols 50 11  3 10  7 12  8  2  6  9 14  4'
rbcols2='set rbcols 70 61 53 60 57 62 58 52 56 59 64 54'
rbcols3='set rbcols 90 81 73 80 77 82 78 72 76 79 84 74'
else
if ( flipped = 13 ) 
say 'new grey - red colourbar'
rbcols1='set rbcols 50 21 22 23 24 25 26'
else
if ( flipped = 2 ) 
say 'grey - red - blue colourbar'
rbcols1='set rbcols 50  9  6  2  8 12  7 10  3 11  4 14'
rbcols2='set rbcols 70 59 56 52 58 62 57 60 53 61 54 64'
rbcols3='set rbcols 90 79 76 72 78 82 77 80 73 81 74 84'
else
if ( flipped = 12 ) 
say 'new grey - blue colourbar'
rbcols1='set rbcols 50 21 22 23 24 25 26'
else
if ( flipped = 14 ) 
say 'new grey - blue - red colourbar'
rbcols1='set rbcols 50 21 22 23 24 25 26 27 28 29 30 31'
else
if ( flipped = 1 )
say 'red - grey - blue colourbar'
rbcols1='set rbcols  6  2  8 12  7 50 10  3 11  4 14'
rbcols2='set rbcols 56 52 58 62 57 70 60 53 61 54 64'
rbcols3='set rbcols 76 72 78 82 77 90 80 73 81 74 84'
else
if ( flipped = 11 )
say 'new red - grey - blue colourbar'
rbcols1='set rbcols 26 22 28 32 27 50 30 23 31 24 34'
else
if ( flipped = 0 )
say 'blue - grey - red colourbar'
rbcols1='set rbcols 14  4 11  3 10 50  7 12  8  2  6'
rbcols2='set rbcols 64 54 61 53 60 70 57 62 58 52 56'
rbcols3='set rbcols 84 74 81 73 80 90 77 82 78 72 76'
else
say 'new blue - grey - red colourbar'
rbcols1='set rbcols 34 24 31 23 30 50 27 32 28 22 26'
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
*
*	set clevs
*
if ( cint != '' & scale = lin )
***say 'set clevs 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax
if ( flipped > 11 & flipped != 14 )
setclevs='set clevs 'cmin' 'cmin+2*cint' 'cmin+4*cint' 'cmin+6*cint' 'cmin+8*cint' 'cmax
else
setclevs='set clevs 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax
endif
else
if ( clevs != NULL )
***say 'clevs were already set at 'clevs
setclevs='set clevs 'clevs
else
if ( scale = lin )
say 'linear colour scale'
if ( flipped = 0 | flipped = 1 | flipped = 6 | flipped = 8 | flipped = 9 | flipped = 10 | flipped = 11 )
***say 'set clevs -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' 0 '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval
setclevs='set clevs -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' 0 '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval
else
if ( flipped = 3 )
***say 'set clevs '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval
setclevs='set clevs '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval
else
if ( flipped = 4 )
if ( dval = 0 );say 'error: dval=0 but flipped=4';return;endif
***say 'set clevs 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
setclevs='set clevs 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
endif
endif
endif
else
if ( scale = log )
say 'logarithmic colour scale'
*	get first digit
maxval = cmax
d=substr(maxval,1,1)
i=1
while ( d = '0' | d = '.' )
    i=i+1
    d=substr(maxval,i,1)
endwhile
* temp solution to get a plot, will round up to 1 2 5 later
if ( d = '3' | d = '4' | d = '6' | d = '7' | d = '8' | d = '9' )
    d = 1
endif
if ( d = 1 )
***say 'set clevs -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval
setclevs='set clevs -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval
else
if ( d = 2 )
***say 'set clevs -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval
setclevs='set clevs -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval
else
if ( d = 5 )
***say 'set clevs -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 0 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval
setclevs='set clevs -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 0 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval
else
say 'cannot handle logscale based on 'maxval
say 'use 1 2 5 as first digit'
return
endif
endif
endif
else
say 'unknown scale 'scale
return
endif
endif
endif
endif
*
*	display
*
'set grads off'
'query dims'
say result
zline=sublin(result,4)
say zline
if ( yflip= "true" | subwrd(zline,3) = varying & subwrd(zline,6) > subwrd(zline,8) )
  say 'hence setting yflip on'
  'set yflip on'
else
* special case for MOC-like figures
  if ( subwrd(zline,3) = varying & subwrd(zline,6) > -1 & subwrd(zline,6) < 20 & subwrd(zline,8) > 4000 & subwrd(zline,8) < 9000 )
    say 'looks like an ocean, setting yflip on'
    'set yflip on'
  else
    say 'hence not setting yflip on'
  endif
endif
say 'pmin input = 'pmin
if ( pmin < 100 )
* check whether prob is a variable
haveprob=0
havecoi=0
'q file'
say result
var=unknown
i=7
while ( var != '' )
  line=sublin(result,i)
  say 'line = 'line
  var=subwrd(line,1)
  say 'found var = 'var
  if ( var = prob )
    haveprob=1
  endif
  if ( var = coi )
    havecoi=1
  endif
  i=i+1
endwhile
'q define'
say result
var=unknown
i=1
while ( var != '' )
  line=sublin(result,i)
  say 'line = 'line
  var=subwrd(line,1)
  say 'found var = 'var
  if ( var = prob )
    haveprob=1
  endif
  i=i+1
endwhile
if ( havecoi = 1 )
  say 'setting yflip off'
  'set yflip off'
endif
if ( haveprob = 0 )
  say 'could not find variable prob'
  pmin = 0
endif
endif
if ( pmin < 100 & pmin > 0 )
   say 'pmin = 'pmin
   if ( maskout = light )
      say 'plotting light colours'
      rbcols2
      setclevs
      setylevs
      'd 'field
   endif
   if ( maskout = lighter )
      say 'plotting lighter colours'
      rbcols3
      setclevs
      setylevs
      'd 'field
   endif
   rbcols1
   setclevs
   setylevs
   say 'plotting masked field'
   'd maskout('field','pmin/100'-prob)'
else
   say rbcols1
   rbcols1
   say setclevs
   setclevs
   say setylevs
   setylevs
   say 'd 'field
   'd 'field
endif
***'draw string 0.35 0.35 KNMI'
* also contours?
if ( shadingtype = shadedcontour )
'set gxout contour'
'set clab off'
'set grid off'
'set xlab off'
'set ylab off'
'set cterp off'
*
*	set clevs again
*
if ( cint != '' )
***say 'set clevs 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax
if ( flipped = 0 | flipped = 1 | flipped = 6 | flipped = 8 | flipped = 9 )
setclevs='set clevs 'cmin-5*cint' 'cmin-4*cint' 'cmin-3*cint' 'cmin-3*cint' 'cmin-2*cint' 'cmin-cint' 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax' 'cmax+cint' 'cmax+2*cint' 'cmax+3*cint' 'cmax+4*cint' 'cmax+5*cint
else
setclevs='set clevs 'cmin-5*cint' 'cmin-4*cint' 'cmin-3*cint' 'cmin-3*cint' 'cmin-2*cint' 'cmin-cint' 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax' 'cmax+cint' 'cmax+2*cint' 'cmax+3*cint' 'cmax+4*cint' 'cmax+5*cint
endif
else
if ( clevs != NULL )
***say 'clevs were already set at 'clevs
if ( field = corr )
clevs='-0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
endif
setclevs='set clevs 'clevs
else
if ( scale = lin )
if ( flipped = 0 | flipped = 1 | flipped = 6 | flipped = 8 | flipped = 9 )
***say 'set clevs -'2*maxval' -'1.8*maxval' -'1.6*maxval' -'1.4*maxval' -'1.2*maxval' -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval' '1.2*maxval' '1.4*maxval' '1.6*maxval' '1.8*maxval' '2*maxval
setclevs='set clevs -'3*maxval' -'2.8*maxval' -'2.6*maxval' -'2.4*maxval' -'2.2*maxval' -'2*maxval' -'1.8*maxval' -'1.6*maxval' -'1.4*maxval' -'1.2*maxval' -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval' '1.2*maxval' '1.4*maxval' '1.6*maxval' '1.8*maxval' '2*maxval' '2.2*maxval' '2.4*maxval' '2.6*maxval' '2.8*maxval' '3*maxval
else
if ( flipped = 3 )
***say 'set clevs 0 '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval' '1.1*maxval' '1.2*maxval' '1.3*maxval' '1.4*maxval' '1.5*maxval' '1.6*maxval' '1.7*maxval' '1.8*maxval' '1.9*maxval' '2*maxval
setclevs='set clevs 0 '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval' '1.1*maxval' '1.2*maxval' '1.3*maxval' '1.4*maxval' '1.5*maxval' '1.6*maxval' '1.7*maxval' '1.8*maxval' '1.9*maxval' '2*maxval
else
if ( flipped = 4 )
if ( dval = 0 );say 'error: dval=0 but flipped=4';return;endif
setclevs='set clevs 'maxval-15*dval' 'maxval-14*dval' 'maxval-13*dval' 'maxval-12*dval' 'maxval-11*dval' 'maxval-10*dval' 'maxval-9*dval' 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
***say 'set clevs 'maxval-15*dval' 'maxval-14*dval' 'maxval-13*dval' 'maxval-12*dval' 'maxval-11*dval' 'maxval-10*dval' 'maxval-9*dval' 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
endif
endif
endif
else
if ( scale = log )
*	get first digit
d=substr(maxval,1,1)
i=1
while ( d = '0' | d = '.' )
i=i+1
d=substr(maxval,i,1)
endwhile
if ( d = 1 )
***say 'set clevs -'20*maxval' -'10*maxval' -'5*maxval' -'2*maxval' -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval' '2*maxval' '5*maxval' '10*maxval' '20*maxval
setclevs='set clevs -'20*maxval' -'10*maxval' -'5*maxval' -'2*maxval' -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval' '2*maxval' '5*maxval' '10*maxval' '20*maxval
else
if ( d = 2 )
***say 'set clevs -'25*maxval' -'10*maxval' -'5*maxval' -'2.5*maxval' -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval' '2.5*maxval' '5*maxval' '10*maxval' '25*maxval
setclevs='set clevs -'25*maxval' -'10*maxval' -'5*maxval' -'2.5*maxval' -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval' '2.5*maxval' '5*maxval' '10*maxval' '25*maxval
else
if ( d = 5 )
***say 'set clevs -'20*maxval' -'10*maxval' -'4*maxval' -'2*maxval' -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval' '2*maxval' '4*maxval' '10*maxval' '20*maxval
setclevs='set clevs -'20*maxval' -'10*maxval' -'4*maxval' -'2*maxval' -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval' '2*maxval' '4*maxval' '10*maxval' '20*maxval
else
say 'cannot handle logscale based on 'maxval
say 'use 1 2 5 as first digit'
return
endif
endif
endif
else
say 'unknown scale 'scale
return
endif
endif
endif
endif
*
*	display
*
'set grads off'
setclevs
setylevs
'd 'field
'set clab on'
'set grid on'
'set xlab on'
'set ylab on'
endif

say field' 'dy'-'mo'-'yr
say 'cbar = 'cbar
if ( cbar != '' & cbar != '-1' & cbar != 'off' )
  'run cbarn'
endif

return result
