parte1 <- read.csv("salida.txt")
attach(parte1)

#Parte 1.1

#Histograma de A
a<- parte1$tpo_cola_taquilla_prom
l <- length(a)
m<- mean(a) #X barra
s<- sqrt(var(a)) #Desviacion
res<-m-(1.96*(s/sqrt(100))) # valor menor del intervalo
res2<-m+(1.96*(s/sqrt(100))) #valor mayor del intervalo
clases <- seq(min(a),max(a),length.out=25)
h<- hist(a,prob=T,labels=F,breaks=clases,main="Histograma")
normal<-function(x)dnorm(x,m,s)
curve(normal,add=T)
