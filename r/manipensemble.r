manipensemble<-function(y){
data<-array(NA,c(dim(y)[1],dim(y)[2],dim(y)[3]*dim(y)[4]))
j<-1
for (i in 1:dim(y)[4]){
data[,,j:(j+dim(y)[3]-1)]<-y[,,,i]
j<-j+dim(y)[3]
}
invisible(list(data=data))
}
