        program lightcolour
!
!       compute GrADS rgb colours from thepostscript ones
!       and add a lighter shaed
!
        implicit none
        integer i,j
        real cols(3,2:15),fac
        data cols
     +       /0.98,0.24,0.24
     +       ,0.00,0.86,0.00
     +       ,0.12,0.24,1.00
     +       ,0.00,0.78,0.78
     +       ,0.94,0.00,0.51
     +       ,0.90,0.86,0.19
     +       ,0.94,0.51,0.16
     +       ,0.63,0.00,0.78
     +       ,0.63,0.90,0.19
     +       ,0.00,0.63,1.00
     +       ,0.90,0.69,0.18
     +       ,0.00,0.82,0.55
     +       ,0.51,0.00,0.86
     +       ,0.67,0.67,0.67/

        print *,'give factor to make colour slighter:'
        read(*,*) fac
        do i=2,15
            print '(a,i2,3i4,a)','''set rgb ',i+50,
     +           (nint((fac-1+cols(j,i))/fac*255),j=1,3),''''
        end do
        print '(a,i2,3i4,a)','''set rgb ',70,
     +           (nint((fac-1+0.87)/fac*255),j=1,3),''''
        end
