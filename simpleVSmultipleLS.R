stats.data<- data.frame(
  s=c(1.4,2.6,1.0,3.7,5.5,3.2,3.0,4.9,6.3),
  w=c(0.9,1.8,2.4,3.5,3.9,4.4,5.1,5.6,6.3),
  t=c(0.7,1.3,0.7,2.0,3.6,3.0,2.9,3.9,4.0)
)
stats.data
plot(stats.data$w, stats.data$s)
simple.regression<- lm(s~ w, data=stats.data)
summary(simple.regression)
abline(simple.regression, col="green", lwd=2)
plot(stats.data)
multiple.regression<- lm(s~w+t, data=stats.data)
summary(multiple.regression)
