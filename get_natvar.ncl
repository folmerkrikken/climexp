;**********************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"   
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"   
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"
;************************************************


begin
length_of_period = LENGTH_OF_PERIOD. ;in yrs
var_name = "VAR_NAME"
relative = RELATIVE

uname = systemfunc("uname")
if uname .eq. "Darwin" then
  stat = "stat -L -f %m "
  extracut=""
else
  stat = "stat -L --printf='%Y\n' "
  extracut="|cut -b 3-"
end if

;var_name = (/"hfss","prc","prsn","psl","rlds","rldscs","rlus","rlut","rlutcs","rsdscs","rsdt","rsus" ,"rsuscs","rsut","rsutcs","rtmt","uas","vas"/)
; var_name = (/"tas", "pr"/)
; relative = 0

scenario = (/"piControl"/)

overwrite = "False"

; ** dir_path in series **
dir_path_in_series = "CMIP5/Tglobal/"
; ** dir_path in **
dir_path_in = "CMIP5/monthly/"
; ** dir_path in **
dir_path_out = "./natvar/"

do k=0,dimsizes(var_name)-1 ;loop over var name

if True then
  model = (/"ACCESS1-0","ACCESS1-3","bcc-csm1-1","BNU-ESM","CanESM2","CCSM4","CESM1-BGC","CMCC-CMS","CNRM-CM5","CSIRO-Mk3-6-0","FGOALS-g2","FIO-ESM","GFDL-CM3","GFDL-ESM2G","GFDL-ESM2M","GISS-E2-H","GISS-E2-H","GISS-E2-R","GISS-E2-R","inmcm4","IPSL-CM5A-LR","MIROC5","MIROC-ESM","MPI-ESM-LR","MPI-ESM-MR","MPI-ESM-P","MRI-CGCM3","NorESM1-M" /)
  ens_member = (/"r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p2","r1i1p3","r1i1p2","r1i1p3","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1","r1i1p1" /)
else  ; compute dynamically, this gives a few more models than listed in Annex I Atlas (ACCESS1-0, HadGEM2-ES, MPI-ESM-P)
; co-ordinate numbers with dirs...
model = systemfunc("ls "+dir_path_in+var_name(k)+"/*"+scenario(0)+"*_144.nc | fgrep -v mean | cut -d'/' -f4 | cut -d'_' -f3")
ens_member = systemfunc("ls "+dir_path_in+var_name(k)+"/*"+scenario(0)+"*_144.nc | fgrep -v mean | cut -d'/' -f4 | cut -d'_' -f5")
; print(""+model+" "+ens_member)
end if ; static list or dynamically generated one

do i=0,dimsizes(model)-1 ;loop over models

    print(dir_path_in_series+"global_tas_Amon_"+model(i)+"_"+scenario(0)+"_"+ens_member(i)+"_144.nc")
    in=addfile(dir_path_in_series+"global_tas_Amon_"+model(i)+"_"+scenario(0)+"_"+ens_member(i)+"_144.nc","r")
    var = in->tas
    delete(in)
    dims_contr = dimsizes(var)  
    delete(var)

    print("dims_contr = "+dims_contr)
    if dims_contr .ge. 6000 then ;take only models where contr ge 500*12 months

    if var_name(k).eq."mrso" .or. var_name(k).eq."mrro" .or. var_name(k).eq."mrros" then
        time_resolution = (/"Lmon"/)
    else
        time_resolution = (/"Amon"/)
    end if
      
;check if file new
; ** check if file exist ORIG
    filename=dir_path_in+var_name(k)+"/"+var_name(k)+"_"+time_resolution+"_"+model(i)+"_piControl_"+ens_member(i)+"_144.nc"
      file_exist = isfilepresent(filename)
      if file_exist then
        tmp = systemfunc(stat+filename+extracut) ; bloody 32-bits NCL
        ;;;print("tmp1 = "+tmp)
        date_file= (/stringtoint(tmp)/) 
        delete(tmp)
      else
        date_file = 0
      end if
      delete(file_exist)
      ;;;print("date_file="+date_file)
      
; ** check if file exist RESULT
      outfile=dir_path_out+var_name(k)+"."+model(i)+"."+ens_member(i)+".natvar."+length_of_period+".nc"
      print("outfile="+outfile)
      file_exist = isfilepresent(outfile)
      if file_exist then
              
        tmp = systemfunc(stat+outfile+extracut)
        ;;;print("tmp2 = "+tmp)
        date_period_file= (/stringtoint(tmp)/) 
        delete(tmp)
      else
        date_period_file = 0
      end if
      ;;;print("date_period_file = "+date_period_file)
      
      if overwrite .eq. "True" .or. (date_file - date_period_file) .gt. 0 then ;overwrite

        print(""+var_name(k)+" "+model(i)+" "+ens_member(i))
        in = addfile(dir_path_in+"/"+var_name(k)+"/"+var_name(k)+"_"+time_resolution+"_"+model(i)+"_piControl_"+ens_member(i)+"_144.nc","r")
        time = in->$var_name(k)$&time
                                ;cut the first 100 yr
        start_yr = cd_calendar(time(0),0)
        new_start_yr = (start_yr(0,0) + 100) * 100 + 1
        ind_start = ind(cd_calendar(time,1) .eq. new_start_yr)
        delete(start_yr)
        delete(new_start_yr)
        delete(time)
        
        var = in->$var_name(k)$(ind_start::,:,:)
        time = in->$var_name(k)$&time(ind_start::)
        dims_var = dimsizes(var)
                                ;calc how many periods there are
        nr_periods = floor(dimsizes(time)/(length_of_period*12.))
        yr_possible = dimsizes(time)/(length_of_period*12.)
        rest = yr_possible-nr_periods

        if rest .gt. 0 then
          ind_end = floattointeger((nr_periods*12.) + ind_start)
          var3 = in->$var_name(k)$(ind_end:ind_end+11,:,:)
          delete(ind_end)
        end if
        delete(ind_start)

        print("periods "+nr_periods+" -- remainig "+(decimalPlaces(yr_possible-nr_periods,2,True))+" period")
        print(""+rest)


          var_period_1mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_2mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_3mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_4mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_5mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_6mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_7mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_8mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_9mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_10mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_11mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))
          var_period_12mon = new((/floattointeger(nr_periods)-1,12,dims_var(1),dims_var(2)/),typeof(var))

        var_period_1mon!0 = "period"
        var_period_1mon!1 = "subseason"
        var_period_1mon!2 = "lat"
        var_period_1mon!3 = "lon"
        var_period_1mon&lat = var&lat
        var_period_1mon&lon = var&lon
        copy_VarCoords(var_period_1mon,var_period_2mon)
        copy_VarCoords(var_period_1mon,var_period_3mon)
        copy_VarCoords(var_period_1mon,var_period_4mon)
        copy_VarCoords(var_period_1mon,var_period_5mon)
        copy_VarCoords(var_period_1mon,var_period_6mon)
        copy_VarCoords(var_period_1mon,var_period_7mon)
        copy_VarCoords(var_period_1mon,var_period_8mon)
        copy_VarCoords(var_period_1mon,var_period_9mon)
        copy_VarCoords(var_period_1mon,var_period_10mon)
        copy_VarCoords(var_period_1mon,var_period_11mon)
        copy_VarCoords(var_period_1mon,var_period_12mon)


        do j=0,nr_periods-2 ;loop over periods


         ; *** 1-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+k)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 0 ;change here
              ;print(""+j+" "+l+" "+k+" "+ind_beg+" "+ind_end+" "+dims_var(0))
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_1mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) 
          end do ;loop over sub-month
          delete(tmp)


          ; *** 2-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 1 ;change here
              ;print(""+j+" "+l+" "+ll+" "+ind_beg+" "+ind_end+" "+dims_var(0))
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then
                  print("bal2")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_2mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) 
          end do ;loop over sub-month
          delete(tmp)

          ; *** 3-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 2 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then           
                if rest .eq. 0  then ;change here
                  print("bal3")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_3mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 4-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 3 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if

              if ind_end .ge. dims_var(0) then
                if rest .eq. 0  then ;change here
                  print("bal4")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_4mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 5-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 4 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then ;change here
                  print("bal5")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_5mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 6-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 5 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal6")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_6mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 7-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 6 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal7")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_7mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 8-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 7 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal8")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_8mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 9-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 8 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal9")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_9mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 10-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 9 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal10")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_10mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 11-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 10 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal11")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_11mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)

          ; *** 12-month ****
          tmp = new((/floattointeger(length_of_period),12,dims_var(1),dims_var(2)/),typeof(var))
          tmp!0 = "length_period"
          do l=0,11 ;loop over sub-month
            do ll=0,length_of_period-1 ;loop over length_of_period
                                ;print(""+j+" "+l+" "+ll)
              ind_beg = floattointeger(j*length_of_period*12) + l + (ll*12)
              ind_end = floattointeger(j*length_of_period*12) + l + (ll*12) + 11 ;change here
              
              if ind_end .lt. dims_var(0) then ;we are inside the good range
                tmp(ll,l,:,:) = dim_avg_n_Wrap(var(ind_beg:ind_end,:,:),0)
              end if
              
              if ind_end .ge. dims_var(0) then
                if rest .eq. 0 then 
                  print("bal12")
                  a = var(ind_beg:dims_var(0)-1,:,:)
                  tmp1 = (a)/(dims_var(0) - ind_beg)

                  delete(a)
                  tmp(ll,l,:,:) = (/tmp1(0,:,:)/)
                  delete(tmp1)
                end if
              end if
            end do ;loop over length_of_period
            var_period_12mon(j,l,:,:) = dim_avg_n_Wrap(tmp(:,l,:,:),0) ;change here
          end do ;loop over sub-month
          delete(tmp)



        end do ;loop over periods


        delete(time)
        delete(var)
        ;delete(var2)
        delete(rest)
        delete(dims_var)
        delete(nr_periods)
        

                                ;*** quadratic detrending SEASONAL VALUES ***
        ; *** 1-month ****
        tmp = dtrend_quadratic(var_period_1mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_1mon"
        tmp!3 = "time"
        tmp&lat =  var_period_1mon&lat
        tmp&lon = var_period_1mon&lon
        var_dtrend_1mon = (/var_period_1mon/) ;init
        var_dtrend_1mon = tmp(time|:,period_1mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_1mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_1mon,0)
        tmp_conf = conform(var_dtrend_1mon,tmp,(/1,2,3/))
        var_dtrend_1mon = var_dtrend_1mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_1mon)


        ; *** 2-month ****
        tmp = dtrend_quadratic(var_period_2mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_2mon"
        tmp!3 = "time"
        tmp&lat =  var_period_2mon&lat
        tmp&lon = var_period_2mon&lon
        var_dtrend_2mon = (/var_period_2mon/) ;init
        var_dtrend_2mon = tmp(time|:,period_2mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_2mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_2mon,0)
        tmp_conf = conform(var_dtrend_2mon,tmp,(/1,2,3/))
        var_dtrend_2mon = var_dtrend_2mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_2mon)

        ; *** 3-month ****
        tmp = dtrend_quadratic(var_period_3mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_3mon"
        tmp!3 = "time"
        tmp&lat =  var_period_3mon&lat
        tmp&lon = var_period_3mon&lon
        var_dtrend_3mon = (/var_period_3mon/) ;init
        var_dtrend_3mon = tmp(time|:,period_3mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_3mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_3mon,0)
        tmp_conf = conform(var_dtrend_3mon,tmp,(/1,2,3/))
        var_dtrend_3mon = var_dtrend_3mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_3mon)

; *** 4-month ****
        tmp = dtrend_quadratic(var_period_4mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_4mon"
        tmp!3 = "time"
        tmp&lat =  var_period_4mon&lat
        tmp&lon = var_period_4mon&lon
        var_dtrend_4mon = (/var_period_4mon/) ;init
        var_dtrend_4mon = tmp(time|:,period_4mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_4mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_4mon,0)
        tmp_conf = conform(var_dtrend_4mon,tmp,(/1,2,3/))
        var_dtrend_4mon = var_dtrend_4mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_4mon)

; *** 5-month ****
        tmp = dtrend_quadratic(var_period_5mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_5mon"
        tmp!3 = "time"
        tmp&lat =  var_period_5mon&lat
        tmp&lon = var_period_5mon&lon
        var_dtrend_5mon = (/var_period_5mon/) ;init
        var_dtrend_5mon = tmp(time|:,period_5mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_5mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_5mon,0)
        tmp_conf = conform(var_dtrend_5mon,tmp,(/1,2,3/))
        var_dtrend_5mon = var_dtrend_5mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_5mon)

; *** 6-month ****
        tmp = dtrend_quadratic(var_period_6mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_6mon"
        tmp!3 = "time"
        tmp&lat =  var_period_6mon&lat
        tmp&lon = var_period_6mon&lon
        var_dtrend_6mon = (/var_period_6mon/) ;init
        var_dtrend_6mon = tmp(time|:,period_6mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_6mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_6mon,0)
        tmp_conf = conform(var_dtrend_6mon,tmp,(/1,2,3/))
        var_dtrend_6mon = var_dtrend_6mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_6mon)


; *** 7-month ****
        tmp = dtrend_quadratic(var_period_7mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_7mon"
        tmp!3 = "time"
        tmp&lat =  var_period_7mon&lat
        tmp&lon = var_period_7mon&lon
        var_dtrend_7mon = (/var_period_7mon/) ;init
        var_dtrend_7mon = tmp(time|:,period_7mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_7mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_7mon,0)
        tmp_conf = conform(var_dtrend_7mon,tmp,(/1,2,3/))
        var_dtrend_7mon = var_dtrend_7mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_7mon)

; *** 8-month ****
        tmp = dtrend_quadratic(var_period_8mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_8mon"
        tmp!3 = "time"
        tmp&lat =  var_period_8mon&lat
        tmp&lon = var_period_8mon&lon
        var_dtrend_8mon = (/var_period_8mon/) ;init
        var_dtrend_8mon = tmp(time|:,period_8mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_8mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_8mon,0)
        tmp_conf = conform(var_dtrend_8mon,tmp,(/1,2,3/))
        var_dtrend_8mon = var_dtrend_8mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_8mon)

; *** 9-month ****
        tmp = dtrend_quadratic(var_period_9mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_9mon"
        tmp!3 = "time"
        tmp&lat =  var_period_9mon&lat
        tmp&lon = var_period_9mon&lon
        var_dtrend_9mon = (/var_period_9mon/) ;init
        var_dtrend_9mon = tmp(time|:,period_9mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_9mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_9mon,0)
        tmp_conf = conform(var_dtrend_9mon,tmp,(/1,2,3/))
        var_dtrend_9mon = var_dtrend_9mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_9mon)

; *** 10-month ****
        tmp = dtrend_quadratic(var_period_10mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_10mon"
        tmp!3 = "time"
        tmp&lat =  var_period_10mon&lat
        tmp&lon = var_period_10mon&lon
        var_dtrend_10mon = (/var_period_10mon/) ;init
        var_dtrend_10mon = tmp(time|:,period_10mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_10mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_10mon,0)
        tmp_conf = conform(var_dtrend_10mon,tmp,(/1,2,3/))
        var_dtrend_10mon = var_dtrend_10mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_10mon)

; *** 11-month ****
        tmp = dtrend_quadratic(var_period_11mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_11mon"
        tmp!3 = "time"
        tmp&lat =  var_period_11mon&lat
        tmp&lon = var_period_11mon&lon
        var_dtrend_11mon = (/var_period_11mon/) ;init
        var_dtrend_11mon = tmp(time|:,period_11mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_11mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_11mon,0)
        tmp_conf = conform(var_dtrend_11mon,tmp,(/1,2,3/))
        var_dtrend_11mon = var_dtrend_11mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_11mon)

; *** 12-month ****
        tmp = dtrend_quadratic(var_period_12mon(lat|:,lon|:,subseason|:,period|:),0)
        tmp!0 = "lat"
        tmp!1 = "lon"
        tmp!2 = "period_12mon"
        tmp!3 = "time"
        tmp&lat =  var_period_12mon&lat
        tmp&lon = var_period_12mon&lon
        var_dtrend_12mon = (/var_period_12mon/) ;init
        var_dtrend_12mon = tmp(time|:,period_12mon|:,lat|:,lon|:)
        ;printVarSummary(var_dtrend_12mon)
        delete(tmp)
                                ;add mean
        tmp = dim_avg_n_Wrap(var_period_12mon,0)
        tmp_conf = conform(var_dtrend_12mon,tmp,(/1,2,3/))
        var_dtrend_12mon = var_dtrend_12mon + tmp_conf
        delete(tmp)
        delete(tmp_conf)
        delete(var_period_12mon)






                                ;calc mean and std dev
        var_dtrend_1mon_avg = dim_avg_n_Wrap(var_dtrend_1mon,0)
        var_dtrend_1mon_std = dim_stddev_n_Wrap(var_dtrend_1mon,0)
        delete(var_dtrend_1mon)

        var_dtrend_2mon_avg = dim_avg_n_Wrap(var_dtrend_2mon,0)
        var_dtrend_2mon_std = dim_stddev_n_Wrap(var_dtrend_2mon,0)
        delete(var_dtrend_2mon)

        var_dtrend_3mon_avg = dim_avg_n_Wrap(var_dtrend_3mon,0)
        var_dtrend_3mon_std = dim_stddev_n_Wrap(var_dtrend_3mon,0)
        delete(var_dtrend_3mon)

        var_dtrend_4mon_avg = dim_avg_n_Wrap(var_dtrend_4mon,0)
        var_dtrend_4mon_std = dim_stddev_n_Wrap(var_dtrend_4mon,0)
        delete(var_dtrend_4mon)

        var_dtrend_5mon_avg = dim_avg_n_Wrap(var_dtrend_5mon,0)
        var_dtrend_5mon_std = dim_stddev_n_Wrap(var_dtrend_5mon,0)
        delete(var_dtrend_5mon)

        var_dtrend_6mon_avg = dim_avg_n_Wrap(var_dtrend_6mon,0)
        var_dtrend_6mon_std = dim_stddev_n_Wrap(var_dtrend_6mon,0)
        delete(var_dtrend_6mon)

        var_dtrend_7mon_avg = dim_avg_n_Wrap(var_dtrend_7mon,0)
        var_dtrend_7mon_std = dim_stddev_n_Wrap(var_dtrend_7mon,0)
        delete(var_dtrend_7mon)

        var_dtrend_8mon_avg = dim_avg_n_Wrap(var_dtrend_8mon,0)
        var_dtrend_8mon_std = dim_stddev_n_Wrap(var_dtrend_8mon,0)
        delete(var_dtrend_8mon)

        var_dtrend_9mon_avg = dim_avg_n_Wrap(var_dtrend_9mon,0)
        var_dtrend_9mon_std = dim_stddev_n_Wrap(var_dtrend_9mon,0)
        delete(var_dtrend_9mon)

        var_dtrend_10mon_avg = dim_avg_n_Wrap(var_dtrend_10mon,0)
        var_dtrend_10mon_std = dim_stddev_n_Wrap(var_dtrend_10mon,0)
        delete(var_dtrend_10mon)

        var_dtrend_11mon_avg = dim_avg_n_Wrap(var_dtrend_11mon,0)
        var_dtrend_11mon_std = dim_stddev_n_Wrap(var_dtrend_11mon,0)
        delete(var_dtrend_11mon)

        var_dtrend_12mon_avg = dim_avg_n_Wrap(var_dtrend_12mon,0)
        var_dtrend_12mon_std = dim_stddev_n_Wrap(var_dtrend_12mon,0)
        delete(var_dtrend_12mon)
        
        file_exist = isfilepresent(dir_path_out+var_name(k)+"."+model(i)+"."+ens_member(i)+".natvar.nc")
        if file_exist then
          a= systemfunc("rm "+outfile)
          delete(a)
        end if

mon1_name = stringtochar((/"J","F","M","A","M","J","J","A","S","O","N","D"/))
mon1_name!0="period_1mon"
mon1_name!1="nchar1"
;printVarSummary(mon1_name)
mon2_name = stringtochar((/"JF","FM","MA","AM","MJ","JJ","JA","AS","SO","ON","ND","DJ"/))
mon2_name!0="period_2mon"
mon2_name!1="nchar2"
;printVarSummary(mon2_name)
mon3_name = stringtochar((/"JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ","DJF"/))
mon3_name!0="period_3mon"
mon3_name!1="nchar3"

mon4_name = stringtochar((/"JFMA","FMAM","MAMJ","AMJJ","MJJA","JJAS","JASO","ASON","SOND","ONDJ","NDJF","DJFM"/))
mon4_name!0="period_4mon"
mon4_name!1="nchar4"

mon5_name = stringtochar((/"JFMAM","FMAMJ","MAMJJ","AMJJA","MJJAS","JJASO","JASON","ASOND","SONDJ","ONDJF","NDJFM","DJFMA"/))
mon5_name!0="period_5mon"
mon5_name!1="nchar5"

mon6_name = stringtochar((/"JFMAMJ","FMAMJJ","MAMJJA","AMJJAS","MJJASO","JJASON","JASOND","ASONDJ","SONDJF","ONDJFM","NDJFMA","DJFMAM"/))
mon6_name!0="period_6mon"
mon6_name!1="nchar6"

mon7_name = stringtochar((/"JFMAMJJ","FMAMJJA","MAMJJAS","AMJJASO","MJJASON","JJASOND","JASONDJ","ASONDJF","SONDJFM","ONDJFMA","NDJFMAM","DJFMAMJ"/))
mon7_name!0="period_7mon"
mon7_name!1="nchar7"

mon8_name = stringtochar((/"JFMAMJJA","FMAMJJAS","MAMJJASO","AMJJASON","MJJASOND","JJASONDJ","JASONDJF","ASONDJFM","SONDJFMA","ONDJFMAM","NDJFMAMJ","DJFMAMJJ"/))
mon8_name!0="period_8mon"
mon8_name!1="nchar8"

mon9_name = stringtochar((/"JFMAMJJAS","FMAMJJASO","MAMJJASON","AMJJASOND","MJJASONDJ","JJASONDJF","JASONDJFM","ASONDJFMA","SONDJFMAM","ONDJFMAMJ","NDJFMAMJJ","DJFMAMJJA"/))
mon9_name!0="period_9mon"
mon9_name!1="nchar9"

mon10_name = stringtochar((/"JFMAMJJASO","FMAMJJASON","MAMJJASOND","AMJJASONDJ","MJJASONDJF","JJASONDJFM","JASONDJFMA","ASONDJFMAM","SONDJFMAMJ","ONDJFMAMJJ","NDJFMAMJJA","DJFMAMJJAS"/))
mon10_name!0="period_10mon"
mon10_name!1="nchar10"

mon11_name = stringtochar((/"JFMAMJJASON","FMAMJJASOND","MAMJJASONDJ","AMJJASONDJF","MJJASONDJFM","JJASONDJFMA","JASONDJFMAM","ASONDJFMAMJ","SONDJFMAMJJ","ONDJFMAMJJA","NDJFMAMJJAS","DJFMAMJJASO"/))
mon11_name!0="period_11mon"
mon11_name!1="nchar11"

mon12_name = stringtochar((/"JFMAMJJASOND","FMAMJJASONDJ","MAMJJASONDJF","AMJJASONDJFM","MJJASONDJFMA","JJASONDJFMAM","JASONDJFMAMJ","ASONDJFMAMJJ","SONDJFMAMJJA","ONDJFMAMJJAS","NDJFMAMJJASO","DJFMAMJJASON"/))
mon12_name!0="period_12mon"
mon12_name!1="nchar12"




        fout = addfile(outfile,"c")

        fout->var_1mon_avg = var_dtrend_1mon_avg
        fout->var_1mon_std = var_dtrend_1mon_std

        fout->var_2mon_avg = var_dtrend_2mon_avg
        fout->var_2mon_std = var_dtrend_2mon_std

        fout->var_3mon_avg = var_dtrend_3mon_avg
        fout->var_3mon_std = var_dtrend_3mon_std

        fout->var_4mon_avg = var_dtrend_4mon_avg
        fout->var_4mon_std = var_dtrend_4mon_std

        fout->var_5mon_avg = var_dtrend_5mon_avg
        fout->var_5mon_std = var_dtrend_5mon_std

        fout->var_6mon_avg = var_dtrend_6mon_avg
        fout->var_6mon_std = var_dtrend_6mon_std

        fout->var_7mon_avg = var_dtrend_7mon_avg
        fout->var_7mon_std = var_dtrend_7mon_std

        fout->var_8mon_avg = var_dtrend_8mon_avg
        fout->var_8mon_std = var_dtrend_8mon_std

        fout->var_9mon_avg = var_dtrend_9mon_avg
        fout->var_9mon_std = var_dtrend_9mon_std

        fout->var_10mon_avg = var_dtrend_10mon_avg
        fout->var_10mon_std = var_dtrend_10mon_std

        fout->var_11mon_avg = var_dtrend_11mon_avg
        fout->var_11mon_std = var_dtrend_11mon_std

        fout->var_12mon_avg = var_dtrend_12mon_avg
        fout->var_12mon_std = var_dtrend_12mon_std



        fout->period_1mon = mon1_name;(/"J","F","M","A","M","J","J","A","S","O","N","D"/)
        fout->period_2mon = mon2_name
        fout->period_3mon = mon3_name
        fout->period_4mon = mon4_name
        fout->period_5mon = mon5_name
        fout->period_6mon = mon6_name
        fout->period_7mon = mon7_name
        fout->period_8mon = mon8_name
        fout->period_9mon = mon9_name
        fout->period_10mon = mon10_name
        fout->period_11mon = mon11_name
        fout->period_12mon = mon12_name


        delete(fout)
        delete(file_exist)

        delete(var_dtrend_1mon_avg)
        delete(var_dtrend_1mon_std)
        delete(var_dtrend_2mon_avg)
        delete(var_dtrend_2mon_std)
        delete(var_dtrend_3mon_avg)
        delete(var_dtrend_3mon_std)
      
      end if ;overwrite

    end if;take only models where contr ge 500 yr
    
  end do ;loop over models
  
  delete(model)
  delete(ens_member)
  if isvar("files") then
    delete(files)
  end if
  
;*****************************
;calc final value
print("calc final values")
files = systemfunc("ls "+dir_path_out+var_name(k)+".*.natvar."+length_of_period+".nc")
print(""+files)

;open to get dimensions
in = addfile(files(0),"r")
tmp = in->var_1mon_std
lat = in->var_1mon_std&lat
lon = in->var_1mon_std&lon
dims = dimsizes(tmp)

period_1mon = in->period_1mon
period_2mon = in->period_2mon
period_3mon = in->period_3mon
period_4mon = in->period_4mon
period_5mon = in->period_5mon
period_6mon = in->period_6mon
period_7mon = in->period_7mon
period_8mon = in->period_8mon
period_9mon = in->period_9mon
period_10mon = in->period_10mon
period_11mon = in->period_11mon
period_12mon = in->period_12mon

delete(in)
delete(tmp)
var_std = new((/dimsizes(files),12,12,dims(1),dims(2)/),float) ;files,periods,nr period,lat,lon
var_avg = new((/dimsizes(files),12,12,dims(1),dims(2)/),float) ;files,periods,nr period,lat,lon

delete(dims)

do i=0,dimsizes(files)-1
  in = addfile(files(i),"r")

var_avg(i,0,:,:,:) = in->var_1mon_avg
var_std(i,0,:,:,:) = in->var_1mon_std

var_avg(i,1,:,:,:) = (/in->var_2mon_avg/)
var_std(i,1,:,:,:) = (/in->var_2mon_std/)

var_avg(i,2,:,:,:) = (/in->var_3mon_avg/)
var_std(i,2,:,:,:) = (/in->var_3mon_std/)

var_avg(i,3,:,:,:) = (/in->var_4mon_avg/)
var_std(i,3,:,:,:) = (/in->var_4mon_std/)

var_avg(i,4,:,:,:) = (/in->var_5mon_avg/)
var_std(i,4,:,:,:) = (/in->var_5mon_std/)

var_avg(i,5,:,:,:) = (/in->var_6mon_avg/)
var_std(i,5,:,:,:) = (/in->var_6mon_std/)

var_avg(i,6,:,:,:) = (/in->var_7mon_avg/)
var_std(i,6,:,:,:) = (/in->var_7mon_std/)

var_avg(i,7,:,:,:) = (/in->var_8mon_avg/)
var_std(i,7,:,:,:) = (/in->var_8mon_std/)

var_avg(i,8,:,:,:) = (/in->var_9mon_avg/)
var_std(i,8,:,:,:) = (/in->var_9mon_std/)

var_avg(i,9,:,:,:) = (/in->var_10mon_avg/)
var_std(i,9,:,:,:) = (/in->var_10mon_std/)

var_avg(i,10,:,:,:) = (/in->var_11mon_avg/)
var_std(i,10,:,:,:) = (/in->var_11mon_std/)

var_avg(i,11,:,:,:) = (/in->var_12mon_avg/)
var_std(i,11,:,:,:) = (/in->var_12mon_std/)


end do
delete(files)

if relative .eq. 1 then
    if var_name .eq. "pr" .or. var_name .eq. "evspsbl" .or. var_name .eq. "pme" then
        var_std = 10000000*var_std
        var_avg = 10000000*var_avg
    end if
    ;;;var_std = var_std / where(var_avg.ne.0, var_avg, var_std*1e-10) ; does not work... (sign may be wrong also)
    var_std = var_std * var_avg / (abs(var_avg)+0.0001*(var_std+0.0001))^2
    var_std = var_std 
end if

var_std_median = dim_median_n(var_std,0)

var_std_median = var_std_median * sqrt(2.)

var_std_median!0 = "clusters"
var_std_median!1 = "period"
var_std_median!2 = "lat"
var_std_median!3 = "lon"
var_std_median&lat = lat
var_std_median&lon = lon


cluster_name = stringtochar((/"1mon","2mon","3mon","4mon","5mon","6mon","7mon","8mon","9mon","10mon","11mon","12mon"/))
cluster_name!0="clusters_mon"
cluster_name!1="nchar_cluster"

printVarSummary(var_std_median)

if relative .eq. 1 then
  file_exist = isfilepresent(dir_path_out+var_name(k)+"_relative.nc")
  if file_exist then
    a= systemfunc("rm "+dir_path_out+var_name(k)+"_relative.nc")
    delete(a)
  end if
end if

if relative .eq. 0 then
  file_exist = isfilepresent(dir_path_out+var_name(k)+".nc")
  if file_exist then
    a= systemfunc("rm "+dir_path_out+var_name(k)+".nc")
    delete(a)
  end if
end if


if relative .eq. 0 then
  fout = addfile(dir_path_out+var_name(k)+"."+length_of_period+".nc","c")
end if
if relative .eq. 1 then
  fout = addfile(dir_path_out+var_name(k)+"_relative"+"."+length_of_period+".nc","c")
end if

fout->var_std = var_std_median

fout->clusters_mon = cluster_name

fout->period_1mon = period_1mon
fout->period_2mon = period_2mon
fout->period_3mon = period_3mon
fout->period_4mon = period_4mon
fout->period_5mon = period_5mon
fout->period_6mon = period_6mon
fout->period_7mon = period_7mon
fout->period_8mon = period_8mon
fout->period_9mon = period_9mon
fout->period_10mon = period_10mon
fout->period_11mon = period_11mon
fout->period_12mon = period_12mon

delete(var_std)
delete(var_avg)
delete(var_std_median)


end do ;;loop over var name




end
