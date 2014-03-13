function sum(args)
*
*	construct a summed version of a field
*
field=subwrd(args,1)
sum=subwrd(args,2)
*
'q file'
nn=sublin(result,5)
nt=subwrd(nn,12)
nt=nt+1-sum
'set t 1 'nt
* one can define with the same name as the variable!
'define 'field' = ave('field',t+0,t+'sum-1')'
