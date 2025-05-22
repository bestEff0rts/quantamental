# QUALITATIVE (categorical) Predictors
library(ISLR)
fix(Carseats)
names(Carseats)
attach(Carseats)
mrg.fit<-lm(Sales~.+Income:Advertising+Price:Age,data=Carseats)
summary(mrg.fit)

contrasts(Shevlock)
# contasts показывает dummy variables
loadlibr<-function(){
  library(car)
  library(glmnet)
  library(ISLR)
  library(MASS)
  print("libraries loaded")
}

# library(glmnet)
# x<-matrix(# fitted())
# lmrg.fit<-cv.glmnet(Sales,Income:Advertising+Price:Age,data=Carseats)