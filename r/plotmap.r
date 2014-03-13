# Map a two dimensional data matrix, with first dimension p being longitude
# and second dimension q being latitude, in either equidistant latitude 
# and longitude projection or stereographic projection 
#
# Description:
#
#      Plot data in a regular latitude and longitude grid with colorbar
#      and contours if requested
#
# Usage:
#
#      plotmapglobal(lon,lat,data,maintit='',legtit='',equi=TRUE,bw=FALSE, 
#                   cont=FALSE,reg=FALSE,..., lonlim=c(0,360), 
#		    latlim=c(50,90),orientation=NULL,
#		    mapdat="world",xmaplim=c(-180,180),ymaplim=c(50,90),
#		    longrds=NULL,latgrds=NULL,n=11)
#
# Arguments:
#
#    lon: A vector of p longitude coordinates in ascending order.
#
#    lat: A vector of q latitude coordinates in ascending order.
#
#   data: A matrix of p rows (longitudes) and q columns (latitudes) that 
#         contains the data values to be plotted.
#
#maintit: A string with the main title of the plot. If not provided 
#         no title is displayed.
#
# legtit: A string with the title of the colourbar. If not provided 
#         no title is displayed.
#
#   cont: Logical. If TRUE adds contours to the image plot. Default is FALSE.
#
#      n: A odd number of colours/intervals for the colourbar. Default is 11.
#
#     bw: Logical. If TRUE produces black, gray and white plot. Default is FALSE.  
#
#   equi: Logical. If FALSE produces stereographic projection plot.
#
#    reg: Logical. To be used only if plotting data in equidistant projection.
#         If TRUE produces a plot using as much ares as possible of the display
#         window. Default is FALSE (addequate to plot global data). 
#
#    ...: Additional arguments passed to `contour'.
#
# latlim: Range of latitudes where data will be plotted. e.g. latlim=c(50,90)
#         or latlim=c(-90,-50)
#  
# lonlim: Range of longitudes where data will be plotted. e.g. lonlim=c(0,360)
#         or lonlim=c(-180,180)
#
# orientation: Orientation parameter of mapproject. For Europe
#              as a whole a reasonable setting is:  orientation=c(45,0,7.5)
#              The latter places the pole of projection to latitude 45 N.
#              For the South Pole use, for example, orientation=c(-90,0,0)
#
# mapdat:  Name of the dataset from which map data is taken from either maps or mpdata
#          packages for producing stereographic plots. Default is "wolrd". Other options
#          could be for example mapdat = "worldHires" plots high resolution map, 
#          mapdat = "none" no map, .
#
#xmaplim and ymaplim: Range of longitudes/latitudes where the map data will be drawn. 
#         In default, the map is drawn for the area of longitude and latitide provided
#         in vectors lon and lat. Sometimes it is useful to define e.g. xmaplim=c(-180,180),
#         ymaplim=c(0,90) i.e. whole hemisphere. But this will be very slow if invoked
#         with madat="worldHires".
#
# Authors:
#
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 2 November 2005
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no>
#
# Examples:
#
#      #Equidistant global plots with UK on the right hand side 
#      plotmap(seq(0,360,2.5),seq(-90,90,2.5),matrix(rnorm(145*73,sd=10),ncol=73,nrow=145),'Example','Random data')
#      plotmap(seq(0,360,2.5),seq(-90,90,2.5),matrix(rnorm(145*73,sd=10),ncol=73,nrow=145),'Example','Random data',bw=T)
#      plotmap(seq(0,360,2.5),seq(-90,90,2.5),abs(matrix(rnorm(145*73,sd=10),ncol=73,nrow=145)),'Example','Random data')
#
#      #Equidistant plots with UK in the centre
#      plotmap(seq(-180,180,2.5),seq(-90,90,2.5),matrix(rnorm(145*73,sd=10),ncol=73,nrow=145),'Example','Random data')
#      plotmap(seq(-180,180,2.5),seq(-90,90,2.5),matrix(rnorm(145*73,sd=10),ncol=73,nrow=145),'Example','Random data',bw=T)
#
#      #Equidistant regional plots 
#      plotmap(seq(-50,50,1),seq(-50,50,1),matrix(rnorm(101*101,sd=10),ncol=101,nrow=101),'Example','Random data',reg=T)
#      plotmap(seq(-50,50,1),seq(-50,50,1),matrix(rnorm(101*101,sd=10),ncol=101,nrow=101),'Example','Random data',reg=T,bw=T)
#      plotmap(seq(0,100,1),seq(-50,50,1),matrix(rnorm(101*101,sd=10),ncol=101,nrow=101),'Example','Random data',reg=T)
#
#      #Stereographic plot for the North Pole     
#      plotmap(seq(-180,180,2.5),seq(60,90,2.5),matrix(rnorm(145*13,sd=10),ncol=13,nrow=145),'Example','Random data',equi=F,lonlim=c(-180,180),latlim=c(60,90),xmaplim=c(-180,180),ymaplim=c(60,90))
#      plotmap(seq(-180,180,2.5),seq(60,90,2.5),matrix(rnorm(145*13,sd=10),ncol=13,nrow=145),'Example','Random data',equi=F,bw=T,lonlim=c(-180,180),latlim=c(60,90),xmaplim=c(-180,180),ymaplim=c(60,90))
#
#      #Stereographic plot for the South Pole     
#      plotmap(seq(-180,180,2.5),seq(-90,-60,2.5),matrix(rnorm(145*13,sd=10),ncol=13,nrow=145),'Example','Random data',equi=F,lonlim=c(-180,180),latlim=c(-90,-60),orientation=c(-90,0,0),xmaplim=c(-180,180),ymaplim=c(-90,-60))
#      plotmap(seq(-180,180,2.5),seq(-90,-60,2.5),matrix(rnorm(145*13,sd=10),ncol=13,nrow=145),'Example','Random data',equi=F,bw=T,lonlim=c(-180,180),latlim=c(-90,-60),orientation=c(-90,0,0),xmaplim=c(-180,180),ymaplim=c(-90,-60))

plotmap <- function(lon,lat,data,maintit='',legtit='',equi=TRUE,bw=FALSE, 
                    cont=FALSE,reg=FALSE,..., lonlim=c(0,360), 
		    latlim=c(50,90),orientation=NULL,
		    mapdat="world",xmaplim=c(-180,180),ymaplim=c(50,90),
		    longrds=NULL,latgrds=NULL,
		    n=11) {

rg<-range(data, na.rm=T)

lowerlim <- rg[1]
upperlim <- rg[2]

maximum <- max(abs(c(lowerlim,upperlim)))

if(lowerlim<0) breaks <- seq(-maximum,maximum,(maximum-(-maximum))/n)
else breaks <- seq(lowerlim,upperlim,(upperlim-(lowerlim))/n)

if(!bw){

# check if range includes negative values to use appropriate colour scale
if (rg[1] <0) {
colours = bluered(seq(0,n-1,by=1), "linear", yellow =TRUE)
}
else {
colours = bluered(seq(0,n-1,by=1), "linear", white=0, invert=T)
}

}

else{
if (rg[1] <0) {
colours <- grey(seq(0, 1, length = length(breaks)-1))
colours <- c(colours[1:((n-1)/2)],rev(colours[(((n-1)/2)+1):n]))
}
else {
colours <- grey(seq(0, 1, length = length(breaks)-1))
}


}


if (equi){

#par(mfrow = c(2, 1),mai=c(0.1, 0.5, 1, 0.5))
layout(matrix(1:2, ncol = 1, nrow=2), heights = c(5,1))
par(mar = c(6, 2, 6.5, 0.5))
if (reg) {
layout(matrix(1:2, ncol = 1, nrow=2), heights = c(9,1))
par(mar = c(5, 2, 1.5, 0.5))
}

# plot data
image(lon,lat,data,axes=F, col = colours, xlab = '', ylab = '',breaks=breaks)


if(cont) {contour(lon,lat,data,levels=round(breaks,1),labels=round(breaks,1),add=T,...)}

# check if lon is from 0 to 360 or -180 to 180 to use appropriate world map
if (min(lon)<0){
map('world',interior = FALSE,add = T, lwd=1) # Low resolution world map (lon -180 to 180)
}
else{
map('world2',interior = FALSE,add = T, lwd=1) # Low resolution world map (lon 0 360)
}
box()
map.axes()
title(maintit)


# adding colorbar
#par(mai = c(2.8, 0.5, 0.5, 0.5))
par(mar = c(4.5, 2, 0, 0.5), mgp = c(1.5, 0.3, 0), las = 1)
if (reg) {
par(mar = c(2.5, 2, 0, 0.5), mgp = c(1.5, 0.3, 0), las = 1)
}
image(c(1:n),1, t(t(c(1:n))), axes = F, col = colours,xlab = '', ylab = '')

box()
par(cex = 1.1)



## add the tick marks to the plot without plotting labels
axis(1, at = seq(1.5, length(breaks)-1.5), labels = F)

if(maximum>1){
## add the labels to the plot, without plotting tick marks
axis(1, at = seq(1.5, length(breaks)-1.5), tick = F,
     labels = round(breaks[2:(length(breaks)-1)],1))
}
else{
axis(1, at = seq(1.5, length(breaks)-1.5), tick = F,
     labels = round(breaks[2:(length(breaks)-1)],2))
}
## redifine font size
par(cex = 1.2)
## add the title
title(xlab = legtit)

} #end if equi

else{
layout(matrix(1:2, ncol = 1, nrow=2), heights = c(9,1))
par(mar = c(5, 2, 1.5, 0.5))

#image.map(lon,lat,data,latlim=c(60,90),projection="stereographic",xmaplim=c(-180,180),ymaplim=c(60,90),col=colours,breaks=breaks,longrds=seq(-180,180,by=60),latgrds=seq(60,80,by=10))

image.map(lon,lat,data,latlim=latlim,lonlim=lonlim,projection="stereographic",orientation=orientation,mapdat=mapdat,xmaplim=xmaplim,ymaplim=ymaplim,col=colours,breaks=breaks,longr="no",latgr="no")
title(maintit)

# adding colorbar
#par(mai = c(2.8, 0.5, 0.5, 0.5))
par(mar = c(2.5, 2, 0, 0.5), mgp = c(1.5, 0.3, 0), las = 1)
image(c(1:n),1, t(t(c(1:n))), axes = F, col = colours,xlab = '', ylab = '')

box()
par(cex = 1.1)



## add the tick marks to the plot without plotting labels
axis(1, at = seq(1.5, length(breaks)-1.5), labels = F)

if(maximum>1){
## add the labels to the plot, without plotting tick marks
axis(1, at = seq(1.5, length(breaks)-1.5), tick = F,
     labels = round(breaks[2:(length(breaks)-1)],1))
}
else{
axis(1, at = seq(1.5, length(breaks)-1.5), tick = F,
     labels = round(breaks[2:(length(breaks)-1)],2))
}
## redifine font size
par(cex = 1.2)
## add the title
title(xlab = legtit)

} # end else equi

}
