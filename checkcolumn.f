        program checkcolumn
!
!       check whether the number of columns is consistent
!
        implicit none
        integer line,ncol0,ncol,phase,i,j,k
        character string*128
        logical lwrite
        lwrite = .false.
        line = 0
 100    continue
        read(*,'(a)',err=900,end=900) string
        line = line + 1
 101    continue
        if ( index(string,'<table>').ne.0 ) then
            phase = 0
            string = string(index(string,'<table>')+7:)
            if ( lwrite ) print *,'new table'
            goto 101
        elseif ( index(string,'<tr').ne.0 ) then
            if ( phase.eq.0 ) then
                if ( lwrite ) print *,'new header'
                ncol = 0
                phase = 1
            else
                if ( lwrite ) print *,'new row ',ncol,ncol0
                if ( phase.eq.1 ) then
                    if ( lwrite ) print *,'processed header, found '
     +                   ,ncol,' columns'
                    phase = 2
                    ncol0 = ncol
                elseif ( ncol.ne.ncol0 ) then
                    print *,'wrong number of columns at line ',line
                    print *,'expected ',ncol0,' found ',ncol
                endif
                ncol = 0
            endif
            string = string(index(string,'<tr')+3:)
            goto 101
        elseif ( index(string,'<th').ne.0 .or.
     +           index(string,'<td').ne.0 ) then
            if ( index(string,'colspan').ne.0 ) then
                i = index(string,'colspan')
                j = i + 8
                if ( string(j:j).eq.'"' ) j = j + 1
                read(string(j:),*) k
                ncol = ncol + k - 1
                string(i:j) = ' '
                goto 101
            else
                ncol = ncol + 1
                string = string(min(index(string,'<th'),
     +               index(string,'<td'))+3:)
                goto 101
            endif
        endif
        goto 100
 900    continue
        print *,'analysed ',line,' lines'
        end
