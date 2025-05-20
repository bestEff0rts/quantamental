library(ISLR)
names(Smarket)
dim(Smarket)
summary(Smarket)
# plotting data; dev.off()- остановка записи в pdf/jpeg
pdf("scatterplotmatrix.pdf")
pairs(Smarket)
dev.off()
# cor(df)- matrix with pairwise correlations; исключ 9 колонку т к direction- qualitatuve(categorical)
cor(Smarket[,-9])
attach(Smarket)
# attach(df)- make variables from data frame avaliable by name
plot(Volume)

# Fit Logistic Regression to predict Direction using Lag 1,2,3,4,5+Volume
lr.fit<- glm(Direction ~ Lag1+ Lag2+ Lag3+ Lag4+ Lag5+ Volume, data=Smarket, family="binomial")
summary(lr.fit)
coef(lr.fit)
# to access coefficients- fitted model and 
summary(lr.fit)$coef
# access patricular aspects of model- like p-values for coefficients
summary(lr.fit)$coef[,4]
# только 4 Column- Колонка, то есть p-values
lr.prob<- predict(lr.fit, type="response")
lr.prob
contrasts(Direction)
# т к dummy variable up=1 то lr.prob ( P(Y=1|X) ) это вероятность direction Up
# now convert predicted probabilities into class labels; NOTE [для примера] обучение и тестрование тут исп одну и ту же выборку- trainig error rate не testing пока что
lr.pred<- rep("Down", 1250)
lr.pred[lr.prob>.5]="Up"
# сначала create a vector of 1250 down elements, then all of the elements for which predicted probability>0.5 (P(Y=1|X)) are transformed to UP
table(lr.pred, Direction)
(507+145)/1250
mean(lr.pred==Direction)
# 100-52.2=47.8 = TRAINING error rate; overly optimistic cause trained and tested on same 1250 observations
train<-(Year<2005)
Smarket.2005<-Smarket[!train,] 
dim(Smarket.2005)
Direction.2005=Direction[!train]
# vector train is BOOLEAN  its elements are TRUE and False; used to obtain a subset of rows or columns of a matrix
# example Smarket[train,] picks a submatrix of Smarket corr only to dates before 2005(elements of Train are TRUE)
# ! reverses all of elements of boolean vectors
lr.fit<- glm(Direction~Lag1+Lag2+Lag3+Lag4+Lag5+Volume, data=Smarket, family="binomial", subset=train)
lr.prob<- predict(lr.fit, Smarket.2005, type="response")
lr.pred=rep("Down",252)
lr.pred[lr.prob>.5]="Up"
table(lr.pred, Direction.2005)
mean(lr.pred==Direction.2005)
mean(lr.pred!=Direction.2005)
# that is TEST ERROR rate =52% :( 
library("glmnet")

x.test<- data.matrix(Smarket[,-9])
y.test<-as.factor(data.matrix(Smarket.2005[,9]))
head(x)

x.train<-[,-9]
x.test<-Smarket.2005

y.train<-y[train_rows]
y.test<-y[-train_rows]

lr1.fit<-cv.glmnet(x,y, type.measure ="deviance", aplha=0.5, family="binomial")
lr1.predicted<-predict(lr1.fit,s=lr1.fit$lambda.1se, newx=x.test)

mean((y.test-lr1.predicted)^2)