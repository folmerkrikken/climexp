function danoprob(wks:graphic,res:logical,field:float,\
                  shadingtype:string,cbar:integer,mycbar:string,\
                  xylint:integer,pmin:integer,cmin:float,cmax:float,\
                  cint:float,proj:string,uncert:integer,prob:float,usefieldf:logical)

;
; NCL script to display an anomaly field similar to GJvO dano GrADS script
;
;		JMA BoM Aug-2011 - now

begin

; print("This is danoprob with args "+shadingtype+" "+cbar+" "+mycbar+" "+xylint+" "+pmin+" "+cmin+" "+cmax+" "+cint+" "+proj+" "+uncert+" "+usefieldf)

; FORCEFULLY ADD CYCLIC POINT
 lon = field&lon
 nlon = dimsizes(lon)
 fieldf = new((/dimsizes(field&lat),dimsizes(lon)+1/),typeof(field))
 fieldf(:,0:nlon/2-1) = field(lat|:,lon|nlon/2:nlon-1)
 fieldf(:,nlon/2:nlon-1) = field(lat|:,lon|0:nlon/2-1)
 fieldf(:,nlon) = field(lat|:,lon|nlon/2)
 replace_ieeenan(prob,prob@_FillValue,0) ; to prevent infinite loop, thanks Julie!
 probf = new((/dimsizes(field&lat),dimsizes(lon)+1/),typeof(field))
 probf(:,0:nlon/2-1) = prob(lat|:,lon|nlon/2:nlon-1)
 probf(:,nlon/2:nlon-1) = prob(lat|:,lon|0:nlon/2-1)
 probf(:,nlon) = prob(lat|:,lon|nlon/2)
 copy_VarAtts(field,fieldf)
 copy_VarCoords_1(field,fieldf)
 copy_VarAtts(prob,probf)
 copy_VarCoords_1(prob,probf)
 lonr = new(nlon+1,typeof(lon))
 lonr(0:nlon/2-1) = lon(nlon/2:nlon-1)-360.
 lonr(nlon/2:nlon-1) = lon(0:nlon/2-1)
 lonr(nlon) = lon(nlon/2)
 fieldf&lon = lonr
 probf&lon = lonr

; LOAD COLORS
 cmap = RGBtoCmap(mycbar)
 gsn_define_colormap(wks,cmap)

; SET CONTOUR INTERVALS
 if (.not.ismissing(cmin).and..not.ismissing(cmax).and.cint.eq.0) then
  cint = (cmax-cmin)/10.
 end if
; if (cmax.eq.30) then
;  res@cnLevelSelectionMode = "ExplicitLevels"
;  res@cnLevels = (/-80.,-40.,-20.,-10.,-5.,-2.5,0.,2.5,5.,10.,20.,40.,80./)
; else
;  res@cnLevelSelectionMode = "ManualLevels"
;  res@cnMinLevelValF = cmin
;  res@cnMaxLevelValF = cmax
;  res@cnLevelSpacingF = cint
; end if
 res@gsnAddCyclic = False

; SET COLOR FILL ON
 if ( shadingtype.eq."shaded".or.shadingtype.eq."shadedcontour")
  res@cnFillOn = True
  res@cnLinesOn = False
  res@cnLineLabelsOn = False
 end if
 if ( shadingtype.eq."grfill")
  res@cnFillOn = True
  res@cnLinesOn = False
  res@cnLineLabelsOn = False
  res@cnFillMode = "RasterFill"
 end if

; FONT HEIGHT FOR LABELS
 res@gsnStringFontHeightF = 0.013

; RESOURCES FOR STIPPLING
 ress = True
 ress@gsnAddCyclic = False
 ress@cnLinesOn = False
 ress@cnLineLabelsOn = False
 ress@cnLevelSelectionMode = "ExplicitLevels"
 ress@cnLevels = (/0.05,4.0/)
 ress@cnFillPatterns = (/-1,10,10/)
 ress@cnInfoLabelOn = False
 ress@tiMainOn = False
 ress@cnFillOn = True
 ress@cnMonoFillPattern = False
 ress@cnFillColor = "black"
 ress@cnMonoFillColor = True
 ress@cnFillScaleF = 0.45         ; add extra density
 ress@lbLabelBarOn = False
 ress@gsnDraw = False
 ress@gsnFrame = False
 ress@gsnCenterString = ""
 ress@gsnLeftString = ""
 ress@gsnRightString = ""

; RESOURCES FOR LIGHTER COLOURS
 sres = res
 ;;;sres@mpOutlineOn = False
 sres@mpFillOn = False
 sres@cnLinesOn = False
 sres@cnLineLabelsOn = False
 sres@cnLevelSelectionMode = "ExplicitLevels"
 delete(sres@cnLevels)
 sres@cnLevels = (/0.01/)
 sres@cnFillColors = (/"blue","white"/)
 sres@gsnDraw = True
 sres@gsnFrame = True
 sres@lbLabelBarOn = False
 sres@gsnCenterString = ""
 sres@gsnLeftString = ""
 sres@gsnRightString = ""

 if (proj.eq."latlon") then
  if ( usefieldf ) then
   plot = gsn_csm_contour_map(wks,fieldf,res)
  else
   plot = gsn_csm_contour_map(wks,field,res)
  end if
 else
  res@gsnPolar = proj
  plot = gsn_csm_contour_map_polar(wks,fieldf,res)
 end if

 if (uncert.eq.1 .and. pmin.lt.100) then
  plot2 = gsn_csm_contour(wks,probf,ress)
  overlay(plot,plot2)
 end if
 if (uncert.eq.2) then
  wks2 = gsn_open_wks("ps","gjlight")
  if (proj.eq."latlon") then
   plot2 = gsn_csm_contour_map(wks2,probf,sres)
  else
   res@gsnPolar = proj
   plot2 = gsn_csm_contour_map_polar(wks2,probf,sres)
  end if
 end if

 return plot
end
