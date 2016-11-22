'query dims'
zline=sublin(result,4)
if ( subwrd(zline,3) = varying & subwrd(zline,6) < subwrd(zline,8) )
'set yflip on'
say 'set yflip on'
*else
*'set yflip off'
*say 'set yflip off'
endif
'set grads off'
***'set rgb 50 200 200 200'
