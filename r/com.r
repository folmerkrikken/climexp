#R-new CMD BATCH [options] infile [outfile]
#R-new CMD BATCH com.r exit.out

source("brierscore.r")
source("likelihood.r")

data<-read.table("ECMWF.txt")

png("t.png")
likelihood(data)
dev.off()

brierscore(data[,3],data[,4:12],mean(data[,3]))
