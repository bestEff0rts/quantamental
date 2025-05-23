# RESAMPLING METHODS: CV and BOOTSTRAP
loadlibr()
set.seed(1)
# (1) VALIDATION APPROACH# TRAINING SET=random sampling 196 observations out of all 392
train<-sample(392,196)
lr.fit1<-lm(mpg~horsepower,data=Auto,subset=train)
attach(Auto)
mean((mpg-predict(lr.fit1,Auto))[-train]^2)
# MSE только НЕ для training set
# теперь POLYNOMIAL linar regression
lr.fit2<-lm(mpg~poly(horsepower,2), data=Auto, subset=train)
mean((mpg-predict(lr.fit2,Auto))[-train]^2)
lr.fit3<-lm(mpg~poly(horsepower,3),data=Auto, subset=train)
mean((mpg-predict(lr.fit2,Auto))[-train]^2)
# different trainig set- DIFFERENT MSE (random sampling)
set.seed(2)
train2<-sample(392,196)
lr.fit1<-lm(mpg~horsepower,data=Auto,subset=train2)
attach(Auto)
mean((mpg-predict(lr.fit1,Auto))[-train2]^2)
# MSE только НЕ для training set
# теперь POLYNOMIAL linar regression
lr.fit2<-lm(mpg~poly(horsepower,2), data=Auto, subset=train)
mean((mpg-predict(lr.fit2,Auto))[-train2]^2)
lr.fit3<-lm(mpg~poly(horsepower,3),data=Auto, subset=train)
mean((mpg-predict(lr.fit2,Auto))[-train2]^2)

# LEAVE ONE OUT CV
library(boot)
glm.fit<-glm(mpg~horsepower,data=Auto)
cv.err<- cv.glm(Auto,glm.fit)
cv.err$delta
# cv error; adjusted cv estimate
cv.err$seed
# now POLYNOMIAL fits still LeaveOneOut CV
cv.error<-rep(0,5)
for (i in 1:5){
  glm.poly.fit<-glm(mpg~poly(horsepower,i), data=Auto)
  cv.error[i]<-cv.glm(Auto,glm.poly.fit)$delta[1]
}
cv.error

# K FOLD CV
set.seed(17)
cv.error.10<-rep(0,10)
for (i in 1:10){
  glm.poly.fit<-glm(mpg~poly(horsepower,i), data= Auto)
  cv.error.10[i]<- cv.glm(Auto,glm.poly.fit)$delta[1]
}
cv.error.10
