# read data from file soi.txt
soi <- read.table("soi.txt",header=T)

# creates a vector called soits with the time series of the SOI
soits<-NULL
for(i in 1:dim(soi)[1])
  soits <- c(soits,as.numeric(soi[i,2:13]))

png("soi.png")
# plot the time series  
plot(soits,type="l")
dev.off()



