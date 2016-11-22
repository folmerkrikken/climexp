function plotbox(args)
*
*   read a file of the form
*
*   # lon1 lon2 lat1 lat2
*   code lon lat val sign name
*   code lon lat val sign name
*   ...
*
*   and plot the vals at the appropriate spots on the map
*
*   arguments
*   1 filename
*   2 scale
*   3 col: [flip]bw/[flip]colour | precipitation
*   4 greycut: value of sign in percent over which a grey mark is draw
*   5 '1'+val/code/name: plot the name or code near the spot
*   6 [empty=val] value (column 3) or sign (column 4)
*   7 [empty=0.6] last boundary on colourscale
*
file=subwrd(args,1)
scale=subwrd(args,2)
col=subwrd(args,3)
greycut=subwrd(args,4)
label=subwrd(args,5)
var=subwrd(args,6)
if ( var = '' )
  var = val
endif
maxcol=subwrd(args,7)
if ( maxcol = return )
  maxcol=0.6
  scaletype=return
endif
if ( maxcol = '' )
  maxcol=0.6
endif
say 'plotbox 'file' 'scale' 'col' 'greycut' 'label' 'var' 'maxcol
*
*  first the map
*
result=read(file)
if ( sublin(result,1) != 0 )
  say 'cannot open file 'file' 'sublin(result,1)
  exit
endif
line=sublin(result,2)
lon1=subwrd(line,2)
lon2=subwrd(line,3)
lat1=subwrd(line,4)
lat2=subwrd(line,5)
say lon1' 'lon2' 'lat1' 'lat2
'open null'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'set clevs 0'
# black map lines
'set map 1'
'set grads off'
'd null'
*
*  next the stations
*
while (1)
result=read(file)
if ( sublin(result,1) != 0 )
   break
endif
line=sublin(result,2)
cod=subwrd(line,1)
lon=subwrd(line,2)
lat=subwrd(line,3)
val=subwrd(line,4)
sig=subwrd(line,5)
nam=subwrd(line,6)
***say 'line ='line
***say 'parsed'cod' 'lon' 'lat' 'val' 'sig' 'nam
OK=1
if ( lon1 < lon2 )
  if ( lon < lon1 )
    lon=lon+360
  endif
  if ( lon > lon2 )
    lon = lon-360
  endif
  if ( lon < lon1 )
    OK=0
  endif
else
  if ( lon > lon1 )
    lon=lon-360
  endif
  if ( lon < lon2 )
    lon=lon+360
  endif
  if ( lon > lon1 )
    OK=0
  endif
endif
if ( lat < lat1 )
  OK=0
endif
if ( lat > lat2 )
  OK=0
endif
if ( OK = 1 )
***say cod' 'lon' 'lat' 'val' 'nam
'set rgb 50 230 230 230'
'query w2xy 'lon' 'lat
***say result
x=subwrd(result,3)
y=subwrd(result,6)
if ( var = sign )
  v=sig
else
  if ( col = flipcolor | col = flipcolour | col = br | col = newflipcolour )
    if ( scaletype = return )
      v=val
    else
      v=-val
    endif
  else
    v=val
  endif
  if ( col = precipitation )
*   only positive, map to -maxcol...maxcol
    v=2*v-maxcol
  endif
endif
if ( col = bw | col = rb | col = flipbw | col = br )
  if ( col = bw | col = flipbw )
    'set line 1'
    if ( sig > greycut/100 )
      'set line 15'
    endif
    size=val
  else
    if ( col = rb | col = br )
      if ( v > 0 )
        if ( sig < greycut/100 )
          'set line 2'
        else
          'set line 12'
        endif
      else
        if ( sig < greycut/100 )
          'set line 4'
        else
          'set rgb 51 0 200 255'
          'set line 51'
        endif
      endif
      size=val
      if ( size < 0 )
        size=-size
      endif
    else
      say 'unknown color scheme 'col
      exit
    endif
  endif
else
* colour scales
  c15 = 15
  c15a = 15
  if ( col = precipitation )
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
    c6 = 31
    c2 = 30
    c8 = 29
    c12 = 28
    c7 = 27
    c15a = 26
    c15 = 25
    c10 = 24
    c3 = 23
    c11 = 22
    c4 = 21
    c14 = 0
  else
    if ( col = newcolour | col = newflipcolour )
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
      c6 = 26
      c2 = 22
      c8 = 28
      c12 = 32
      c7 = 27
      c15 = 50
      c15a = 50
      c10 = 30
      c3 = 23
      c11 = 31
      c4 = 24
      c14 = 34
    else
      c6 = 6
      c2 = 2
      c8 = 8
      c12 = 12
      c7 = 7
      c10 = 10
      c3 = 3
      c11 = 11
      c4 = 4
      c14 = 14
    endif
  endif
***say 'var = 'var', c6 = 'c6
  if ( scaletype = return )
    say 'return times, v = 'v
    if ( v > 10000 )
      linecol = c14
    else
      if ( v > 5000 )
        linecol = c6
      else
        if ( v > 2000 )
          linecol = c2
        else
          if ( v > 1000 )
            linecol = c8
          else
            if ( v > 500 )
              linecol = c12
            else
              if ( v > 200 )
                  linecol = c7
              else
                if ( v > 100 )
                    linecol = c10
                else
                  if ( v > 50 )
                      linecol = c3
                  else
                    if ( v > 20 )
                        linecol = c11
                    else
                      if ( v > 10 )
                          linecol = c15
                      else
                          linecol = c50
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
    say 'linecol = 'linecol
    'set line 'linecol
  else
    if ( var = sign )
      if ( v < 0.001 )
        linecol = c6
      else
        if ( v < 0.005 )
          linecol = c2
        else
          if ( v < 0.01 )
            linecol = c12
          else
            if ( v < 0.05 )
              linecol = c7
            else
              if ( v < 0.1 )
                  linecol = c15
              else
                  'set rgb 50 230 230 230'
                  linecol = 50
              endif
            endif
          endif
        endif
      endif
      'set line 'linecol
    else
*     not return value or significance
      if ( maxcol = 0.6 )
        offset = 0.1
        maxcol = 0.5
      else
        offset = 0
      endif
*indentation error
    if ( v > maxcol+offset )
      linecol = c6
      else
        if ( v > 0.8*maxcol+offset )
          linecol = c2
        else
          if ( v > 0.6*maxcol+offset )
            linecol = c8
          else
            if ( v > 0.4*maxcol+offset )
              linecol = c12
            else
              if ( v > 0.2*maxcol+offset )
                linecol = c7
              else
                if ( v > 0 )
                  linecol = c15a
                else
                  if ( v > -0.2*maxcol-offset )
                    linecol = c15
                  else
                    if ( v > -0.4*maxcol-offset )
                      linecol = c10
                    else
                      if ( v > -0.6*maxcol-offset )
                        linecol = c3
                      else
                        if ( v > -0.8*maxcol-offset )
                          linecol = c11
                        else
                          if ( v > -1*maxcol-offset )
                            linecol = c4
                          else
                            linecol = c14
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
      'set line 'linecol
      if ( sig > greycut/100 )
***         say 'sig,cut = 'sig' 'greycut/100
        'set rgb 50 230 230 230'
        'set line 50'
      endif
    endif
  endif
  size=0.5
***  say 'v,maxcol,offset,linecol = 'v' 'maxcol' 'offset' 'linecol
endif


if ( size > 0 )
  if ( col = flipbw )
    'draw mark 2 'x' 'y' 'scale*size/2
  else
    'draw mark 3 'x' 'y' 'scale*size/2
    if ( col != color & col != flipcolor )
      if ( col = bw )
        'set line 0 1 1'
      else
        if ( sig > greycut/100 )
          'set line 15 1 1'
        else
          'set line 1 1 1'
        endif
      endif
      'draw mark 2 'x' 'y' 'scale*size/2
*     set linewidth back to default=3
      'set line 1 1 3'
    endif
  endif
else
  if ( col != bw )
    'draw mark 3 'x' 'y' 'scale*size/2
    if ( col != color & col != flipcolor )
      if ( col = flipbw )
        'set line 0 1 1'
      else
        if ( sig > greycut/100 )
          'set line 15 1 1'
        else
          'set line 1 1 1'
        endif
      endif
      'draw mark 2 'x' 'y' 'scale*size/2
*     set linewidth back to default=3
      'set line 1 1 3'
    endif
  else
    'draw mark 2 'x' 'y' 'scale*size/2
  endif
endif
***say 'scale = 'scale', val = 'val', size = 'size', x = 'x
if ( scale*size > 0 )
  x=x+scale*size/4
else
  x=x-scale*size/4
endif
'set line 1'
if ( label = 1value )
  'draw string 'x' 'y' 'val
endif
if ( label = 1code )
  'draw string 'x' 'y' 'cod
endif
if ( label = 1name )
  'draw string 'x' 'y' 'nam
endif
if ( label = 1valuecode )
  'draw string 'x' 'y' 'val' 'cod
endif
if ( label = 1valuename )
  'draw string 'x' 'y' 'val' 'nam
endif
if ( label = 1codename )
  'draw string 'x' 'y' 'cod' 'nam
endif
if ( label = 1valuecodename )
  'draw string 'x' 'y' 'val' 'cod' 'nam
endif
endif
endwhile
'set line 1'
'close 1'
