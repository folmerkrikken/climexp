function danod(args)
*
*	set the contour levels of various types of fields and display
*
say 'this is danod with args 'args
field=subwrd(args,1)
shadingtype=subwrd(args,2)
flipcolor=subwrd(args,3)
xylint=subwrd(args,4)
cmin=subwrd(args,5)
cmax=subwrd(args,6)
cint=subwrd(args,7)
if ( cmin != '' & cmax != '' & cint = '' )
cint = (cmax-cmin)/10
endif
clevs = NULL
scale = lin
*
if ( flipcolor = '' )
flipped=0
else
flipped=flipcolor
endif
*
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
  if ( field = prob | field = prob.1 | field = prob.2 | field = prob.3 )
***    clevs='0.9 0.95 0.99 0.995 0.999 0.9995 0.9999'
***    flipped=3
    clevs='0.0001 0.0002 0.0005 0.001 0.002 0.005 0.01 0.02 0.05 0.1'
    flipped=7
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
      if ( subwrd(result,1) = 'Averaging.' )
        result=sublin(result,2)
        say 'result = 'result
      endif
      if ( cmin = '' )
        cmin=subwrd(result,2)
      endif
      if ( cmax = '' )
        cmax=subwrd(result,4)
      endif
      if ( cint = '' )
        cint=subwrd(result,6)
      endif
* make sure we get 10 intervals
      if ( cint != '' )
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
      if ( flipped < 2 )
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
endif
'set rgb 50 222 222 222'
if ( flipped = 7 ) 
'set rbcols 6 2 8 12 7 10 3 11 4 14 50'
else
if ( flipped = 6 ) 
'set rbcols 14 4 11 3 10 50  7 12 8 2 6'
else
if ( flipped = 5 ) 
'set rbcols 11 3 10 50 7 12 8'
else
if ( flipped = 4 ) 
'set rbcols 50 6 2 8 12 7 10 3 11 4 14'
else
if ( flipped = 3 ) 
'set rbcols 50 4 11 3 10 7 12 8 2 6 9 14'
else
if ( flipped = 2 ) 
'set rbcols 50 9 6 2 8 12 7 10 3 11 4 14'
else
if ( flipped = 1 )
'set rbcols 6 2 8 12 7 50 10 3 11 4 14'
else
'set rbcols 14 4 11 3 10 50 7 12 8 2 6'
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
if ( cint != '' )
***say 'set clevs 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax
'set clevs 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax
else
if ( clevs != NULL )
***say 'clevs were already set at 'clevs
'set clevs 'clevs
else
if ( scale = lin )
if ( flipped = 0 | flipped = 1 | flipped = 6 )
***say 'set clevs -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' 0 '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval
'set clevs -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' 0 '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval
else
if ( flipped = 3 )
***say 'set clevs '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval
'set clevs '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval
else
if ( flipped = 4 )
if ( dval = 0 );say 'error: dval=0 but flipped=4';return;endif
'set clevs 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
***say 'set clevs 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
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
***say 'set clevs -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval
'set clevs -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval
else
if ( d = 2 )
***say 'set clevs -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval
'set clevs -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 0 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval
else
if ( d = 5 )
***say 'set clevs -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 0 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval
'set clevs -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 0 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval
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
'd 'field
***'draw string 0.35 0.35 KNMI'
* also contours?
if ( shadingtype != shadedcontour )
return
endif
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
if ( flipped = 0 | flipped = 1 | flipped = 6 )
'set clevs 'cmin-5*cint' 'cmin-4*cint' 'cmin-3*cint' 'cmin-3*cint' 'cmin-2*cint' 'cmin-cint' 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax' 'cmax+cint' 'cmax+2*cint' 'cmax+3*cint' 'cmax+4*cint' 'cmax+5*cint
else
'set clevs 'cmin-5*cint' 'cmin-4*cint' 'cmin-3*cint' 'cmin-3*cint' 'cmin-2*cint' 'cmin-cint' 'cmin' 'cmin+cint' 'cmin+2*cint' 'cmin+3*cint' 'cmin+4*cint' 'cmin+5*cint' 'cmin+6*cint' 'cmin+7*cint' 'cmin+8*cint' 'cmin+9*cint' 'cmax' 'cmax+cint' 'cmax+2*cint' 'cmax+3*cint' 'cmax+4*cint' 'cmax+5*cint
endif
else
if ( clevs != NULL )
***say 'clevs were already set at 'clevs
if ( field = corr )
clevs='-0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
endif
'set clevs 'clevs
else
if ( scale = lin )
if ( flipped = 0 | flipped = 1 | flipped = 6 )
***say 'set clevs -'2*maxval' -'1.8*maxval' -'1.6*maxval' -'1.4*maxval' -'1.2*maxval' -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval' '1.2*maxval' '1.4*maxval' '1.6*maxval' '1.8*maxval' '2*maxval
'set clevs -'3*maxval' -'2.8*maxval' -'2.6*maxval' -'2.4*maxval' -'2.2*maxval' -'2*maxval' -'1.8*maxval' -'1.6*maxval' -'1.4*maxval' -'1.2*maxval' -'maxval' -'0.8*maxval' -'0.6*maxval' -'0.4*maxval' -'0.2*maxval' '0.2*maxval' '0.4*maxval' '0.6*maxval' '0.8*maxval' 'maxval' '1.2*maxval' '1.4*maxval' '1.6*maxval' '1.8*maxval' '2*maxval' '2.2*maxval' '2.4*maxval' '2.6*maxval' '2.8*maxval' '3*maxval
else
if ( flipped = 3 )
***say 'set clevs 0 '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval' '1.1*maxval' '1.2*maxval' '1.3*maxval' '1.4*maxval' '1.5*maxval' '1.6*maxval' '1.7*maxval' '1.8*maxval' '1.9*maxval' '2*maxval
'set clevs 0 '0.1*maxval' '0.2*maxval' '0.3*maxval' '0.4*maxval' '0.5*maxval' '0.6*maxval' '0.7*maxval' '0.8*maxval' '0.9*maxval' 'maxval' '1.1*maxval' '1.2*maxval' '1.3*maxval' '1.4*maxval' '1.5*maxval' '1.6*maxval' '1.7*maxval' '1.8*maxval' '1.9*maxval' '2*maxval
else
if ( flipped = 4 )
if ( dval = 0 );say 'error: dval=0 but flipped=4';return;endif
'set clevs 'maxval-15*dval' 'maxval-14*dval' 'maxval-13*dval' 'maxval-12*dval' 'maxval-11*dval' 'maxval-10*dval' 'maxval-9*dval' 'maxval-8*dval' 'maxval-7*dval' 'maxval-6*dval' 'maxval-5*dval' 'maxval-4*dval' 'maxval-3*dval' 'maxval-2*dval' 'maxval-dval' 'maxval
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
'set clevs -'20*maxval' -'10*maxval' -'5*maxval' -'2*maxval' -'maxval' -'maxval/2' -'maxval/5' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/5' 'maxval/2' 'maxval' '2*maxval' '5*maxval' '10*maxval' '20*maxval
else
if ( d = 2 )
***say 'set clevs -'25*maxval' -'10*maxval' -'5*maxval' -'2.5*maxval' -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval' '2.5*maxval' '5*maxval' '10*maxval' '25*maxval
'set clevs -'25*maxval' -'10*maxval' -'5*maxval' -'2.5*maxval' -'maxval' -'maxval/2' -'maxval/4' -'maxval/10' -'maxval/20' 'maxval/20' 'maxval/10' 'maxval/4' 'maxval/2' 'maxval' '2.5*maxval' '5*maxval' '10*maxval' '25*maxval
else
if ( d = 5 )
***say 'set clevs -'20*maxval' -'10*maxval' -'4*maxval' -'2*maxval' -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval' '2*maxval' '4*maxval' '10*maxval' '20*maxval
'set clevs -'20*maxval' -'10*maxval' -'4*maxval' -'2*maxval' -'maxval' -'maxval/2.5' -'maxval/5' -'maxval/10' -'maxval/25' 'maxval/25' 'maxval/10' 'maxval/5' 'maxval/2.5' 'maxval' '2*maxval' '4*maxval' '10*maxval' '20*maxval
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
'd 'field
'set clab on'
'set grid on'
'set xlab on'
'set ylab on'
return
