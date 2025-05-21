library(MASS)
library(ISLR)
fix(Boston)
names(Boston)
attach(Boston)
# fit a SIMPLE LINEAR REGRESSION
rg.fit<-lm(medv~lstat)
rg.fit
summary(rg.fit)
names(rg.fit)
coef(rg.fit)
confint(rg.fit)
# confidence intervals for coeff
predict(rg.fit, data.frame(lstat=c(5,10,15)), interval="confidence")
# predictions for a given value of lstat
predict(rg.fit, data.frame(lstat=c(5,10,15)), interval="prediction")
# prediction intervals шире т к включают irreducible error
plot(lstat,medv)
abline(rg.fit, col="red", lwd=3)
res<-residuals(rg.fit)
fitval<-fitted(rg.fit)
plot(fitval,res)
# residual plots индикатор гетероскедастичности(непостоянной дисперсии ошибки) и non-linearity :(

# plot(lstat,medv,col="red")
# plot(lstat,medv,pch=20)
# plot(lstat,medv,pch="+")
# plot(1:20,1:20,pch=1:20)
rstudent(rg.fit)
# studentisized residuals
par(mfrow=c(2,2))
# разделение 2 на 2 для построения неск графиков
plot(predict(rg.fit), residuals(rg.fit))
plot(hatvalues(rg.fit))
which.max(hatvalues(rg.fit))
# observation с индексом 375 имеет наиб leverage statistic

mrg.fit<-lm(medv~.,data=Boston)
summary(mrg.fit)
library(car)
vif(mrg.fit)
# variance inflation factor формула 1/(1-R^2 xj xj) если больше 5-10 МУЛЬТИКОЛЛИНЕАРНОСТЬ(тесная статистическая связь предикторов)
# mrg fit1<-update(mrg fit∼.,-age)
# апдейт у  age huge p-value исключаем

# INTERACTION TERMS синергия предикторов
summary(lm(medv~lstat*age,data=Boston))
# NON LINEAR TRANSFORMATIONS OF PREDICTORS 
mrg.fit2<-lm(medv~lstat+I(lstat^2))
summary(mrg.fit2)
# model improved!!сравниваем linear и quadratic fit через ANOVA
lm.fit=lm(medv~lstat)
anova(lm.fit,mrg.fit2)
par(mfrow=c(2,2))
plot(lm.fit)
# plot(fitted(lm.fit),residuals(lm.fit))
plot(mrg.fit2)
# plot(fitted(mrg.fit2),residuals(mrg.fit2))
lm.fit5<-lm(medv~poly(lstat,5))
# 5th order polynomial
plot(lm.fit5)
