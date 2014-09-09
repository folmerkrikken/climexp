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
*   3 col: [flip]bw/[flip]colour
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
if ( lat2-lat1 < 41 )
  'set mpdset hires'
endif
'set clevs 0'
# black map lines
'set map 1'
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
  if ( col = flipcolor | col = flipcolour | col = br )
    if ( scaletype = return )
      v=val
    else
      v=-val
    endif
  else
    v=val
  endif
endif
if ( col = color | col = colour | col = flipcolor | col = flipcolour )
***  say 'var = 'var
  if ( scaletype = return )
    say 'return times, v = 'v
    if ( v > 10000 )
      linecol = 14
    else
      if ( v > 5000 )
        linecol = 6
      else
        if ( v > 2000 )
          linecol = 2
        else
          if ( v > 1000 )
            linecol = 8
          else
            if ( v > 500 )
              linecol = 12
            else
              if ( v > 200 )
                  linecol = 7
              else
                if ( v > 100 )
                    linecol = 10
                else
                  if ( v > 50 )
                      linecol = 3
                  else
                    if ( v > 20 )
                        linecol = 11
                    else
                      if ( v > 10 )
                          linecol = 15
                      else
                          linecol = 50
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
        linecol = 6
      else
        if ( v < 0.005 )
          linecol = 2
        else
          if ( v < 0.01 )
            linecol = 12
          else
            if ( v < 0.05 )
              linecol = 7
            else
              if ( v < 0.1 )
                  linecol = 15
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
      if ( maxcol = 0.6 )
        offset = 0.1
        maxcol = 0.5
      else
        offset = 0
    endif
    if ( v > maxcol+offset )
      linecol = 6
      else
        if ( v > 0.8*maxcol+offset )
          linecol = 2
        else
          if ( v > 0.6*maxcol+offset )
            linecol = 8
          else
            if ( v > 0.4*maxcol+offset )
              linecol = 12
            else
              if ( v > 0.2*maxcol+offset )
                linecol = 7
              else
                if ( v > -0.2*maxcol-offset )
                  linecol = 15
                else
                  if ( v > -0.4*maxcol-offset )
                    linecol = 10
                  else
                    if ( v > -0.6*maxcol-offset )
                      linecol = 3
                    else
                      if ( v > -0.8*maxcol-offset )
                        linecol = 11
                      else
                        if ( v > -0.8*maxcol-offset )
                          linecol = 4
                        else
                          linecol = 14
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
***  say 'v,maxcol,linecol = 'v' 'maxcol' 'linecol
else
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
