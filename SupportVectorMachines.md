Support Vector Machines
================

## Fit SVM for a given value of cost

\#demonstration: svm() use of this function on a two-dimensional example
so that we can plot the resulting decision boundary. We begin by
generating the observations, which belong to two classes, and checking
whether the classes are linearly separable.

``` r
set.seed(1)
x= matrix(rnorm(20*2), ncol=2)
y=c(rep(-1,10),rep(1,10))
x[y==1,]=x[y==1,] +1
plot(x, col=(3-y))
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->
Classes are not lineary separable

\#Fit SVM

``` r
data=data.frame(x=x,y=as.factor(y))
library(e1071)
svm.fit=svm(y~.,data=data, kernal="linear", cost=10, scale=FALSE)
plot(svm.fit, data)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

for the svm() function to perform classification (as opposed to
SVM-based regression), we must encode the response as a factor variable.
We now create a data frame with the response coded as a factor

The argument scale=FALSE tells the svm() function not to scale each
feature to have mean zero or standard deviation one; depending on the
application, one might prefer to use scale=TRUE.

the second feature is plotted on the x-axis and the first feature is
plotted on the y-axis,in contrast to the behavior of the usual plot()
function in R. The support vectors are plotted as crosses and the
remaining observations are plotted as circles; we see here that there
are seven support vectors. We can determine their identities

``` r
svm.fit$index
```

    ##  [1]  1  4  5  6  8  9 13 14 15 16

``` r
summary(svm.fit)
```

    ## 
    ## Call:
    ## svm(formula = y ~ ., data = data, kernal = "linear", cost = 10, scale = FALSE)
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  radial 
    ##        cost:  10 
    ## 
    ## Number of Support Vectors:  10
    ## 
    ##  ( 6 4 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  -1 1

\#summary() a linear kernel was used with cost=10,and there were 10
support vectors, 6 in one class and 4 in the other.

``` r
svm.fit2=svm(y~.,data=data,cost=0.1, kernel="linear", scale=FALSE)
plot(svm.fit2,data)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->
***Smaller value of cost-\> wider margin (шире)-\> more support
vectors***

\#tune() for CV

``` r
set.seed(1)
tune.cv=tune(svm, y~.,data=data, kernel="linear",ranges=list(cost=c(0.001, 0.01, 0.1, 1,5,10,100)))
summary(tune.cv)
```

    ## 
    ## Parameter tuning of 'svm':
    ## 
    ## - sampling method: 10-fold cross validation 
    ## 
    ## - best parameters:
    ##  cost
    ##   0.1
    ## 
    ## - best performance: 0.05 
    ## 
    ## - Detailed performance results:
    ##    cost error dispersion
    ## 1 1e-03  0.55  0.4377975
    ## 2 1e-02  0.55  0.4377975
    ## 3 1e-01  0.05  0.1581139
    ## 4 1e+00  0.15  0.2415229
    ## 5 5e+00  0.15  0.2415229
    ## 6 1e+01  0.15  0.2415229
    ## 7 1e+02  0.15  0.2415229

By default, tune() performs ten-fold cross-validation. compare SVMs with
a linear kernel,using a range of values of the cost parameter.

# best model?

``` r
best.mod=tune.cv$best.model
summary(tune.cv$best.model)
```

    ## 
    ## Call:
    ## best.tune(METHOD = svm, train.x = y ~ ., data = data, ranges = list(cost = c(0.001, 
    ##     0.01, 0.1, 1, 5, 10, 100)), kernel = "linear")
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  linear 
    ##        cost:  0.1 
    ## 
    ## Number of Support Vectors:  16
    ## 
    ##  ( 8 8 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  -1 1

cost=0.1 results in the lowest cross-validation error rate.The tune()
function stores the best model obtained

# predict()

``` r
x.test=matrix(rnorm(20*2), ncol=2)
y.test=sample(c(-1,1),20, rep=TRUE)
x.test[y.test==1,]=x.test[y.test==1,] + 1
test.dat=data.frame(x=x.test, y=as.factor(y.test))
```

predict the class label on a set of test observations,at any given value
of the cost parameter \#predict class labels on generated test data,
using best model from cv

``` r
y.predicted=predict(best.mod,test.dat)
table(predict=y.predicted, true=test.dat$y)
```

    ##        true
    ## predict -1 1
    ##      -1  9 1
    ##      1   2 8

``` r
summary(best.mod)
```

    ## 
    ## Call:
    ## best.tune(METHOD = svm, train.x = y ~ ., data = data, ranges = list(cost = c(0.001, 
    ##     0.01, 0.1, 1, 5, 10, 100)), kernel = "linear")
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  linear 
    ##        cost:  0.1 
    ## 
    ## Number of Support Vectors:  16
    ## 
    ##  ( 8 8 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  -1 1

\#интерпретация при cost=0.1, 9+8= 17 правильно классифицированы

``` r
# library(pROC)
# roc1=roc(y~.,data=test.dat ,auc=TRUE)
```

\#twoclassesarelinearlyseparable

``` r
 x[y==1,]=x[y==1,]+0.5
 plot(x, col=(y+5)/2, pch=19)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->
barely linearly separable. We fit the support vector classifier and plot
the resulting hyperplane, using a very large value of costs (no
observations are misclassified)

``` r
dat=data.frame(x=x,y=as.factor(y))
svm.fit3=svm(y~.,data=dat, kernel="linear", cost=1e5)
summary(svm.fit3)
```

    ## 
    ## Call:
    ## svm(formula = y ~ ., data = dat, kernel = "linear", cost = 1e+05)
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  linear 
    ##        cost:  1e+05 
    ## 
    ## Number of Support Vectors:  3
    ## 
    ##  ( 1 2 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  -1 1

``` r
plot(svm.fit3,dat)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-11-1.png)<!-- -->
\#int No training errors and only 3 support vectors. However,the margin
is very narrow **большое значение cost-\> узкая(narrow) margin-\>
меньшеее кол-во support vectors** (because the observations that are not
support vectors, indicated as circles,are very close to the decision
boundary). It seems likely that this model will perform poorly on test
data. *overfit= small bias, lots of variance*

``` r
svm.fit4=svm(y~., data=dat,kernel="linear", cost= 1)
summary(svm.fit4)
```

    ## 
    ## Call:
    ## svm(formula = y ~ ., data = dat, kernel = "linear", cost = 1)
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  linear 
    ##        cost:  1 
    ## 
    ## Number of Support Vectors:  7
    ## 
    ##  ( 4 3 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  -1 1

``` r
plot(svm.fit4, dat)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->
\#int 1 misclassification, however we also obtain a much wider margin
and make use of seven support vectors. It seems likely that this model
will perform better on test data *trade-off- little bias in for a
significant reduction in variance*

## Support Vector Machine (non-linear kernel)

generate data with a non-linear class boundary

``` r
set.seed(1)
x=matrix(rnorm(200*2), ncol=2)
x[1:100,]=x[1:100,]+3
x[101:150,]=x[101:150,]-3
y=c(rep(1,150),rep(2,50))
dat=data.frame(x=x,y=as.factor(y))
plot(x, col=y)
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-13-1.png)<!-- -->
The data is randomly split into training and testing groups. Radial
Kernel $E^-\gamma*(a-b)^2$ $\gamma=1$

``` r
train=sample(200,100)
svm.nl.fit=svm(y~., data=dat[train,], kernel="radial", gamma=1, cost=1)
plot(svm.nl.fit, dat[train,])
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-14-1.png)<!-- -->
\#int SVM has a non-linear boundary.

``` r
summary(svm.nl.fit)
```

    ## 
    ## Call:
    ## svm(formula = y ~ ., data = dat[train, ], kernel = "radial", gamma = 1, 
    ##     cost = 1)
    ## 
    ## 
    ## Parameters:
    ##    SVM-Type:  C-classification 
    ##  SVM-Kernel:  radial 
    ##        cost:  1 
    ## 
    ## Number of Support Vectors:  18
    ## 
    ##  ( 11 7 )
    ## 
    ## 
    ## Number of Classes:  2 
    ## 
    ## Levels: 
    ##  1 2

\#int **bias variance flexibility trade-off** We can see from the figure
that there are a fair number of training errors in this SVM fit.
*increase the value of cost-\> reduce num of training errors(margin
narrow-узкая) but risk of overfitting*; this comes at the price of a
more irregular decision boundary (high variance) that seems to be at
risk of overfitting the data.

\#cost= 1e5(huge)

``` r
svm.nl.fit2=svm(y~., data=dat[train,], kernel="radial",gamma=1,cost=1e5)
plot(svm.nl.fit2, dat[train,])
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-16-1.png)<!-- -->
\#tune() = Cross Validation for Radial Kernel’s parameters to find best
$\gamma$ and $cost$

``` r
set.seed(1)
tune.nl.cv=tune(svm, y~., data=dat[train,], kernel="radial", ranges=list(cost=c(0.1,1,10,100,1000),  gamma=c(0.1,0.2,0.3,0.4,0.5,1,2,3,4,6,7,8,9,10)))
summary(tune.nl.cv)
```

    ## 
    ## Parameter tuning of 'svm':
    ## 
    ## - sampling method: 10-fold cross validation 
    ## 
    ## - best parameters:
    ##  cost gamma
    ##    10   0.1
    ## 
    ## - best performance: 0.01 
    ## 
    ## - Detailed performance results:
    ##     cost gamma error dispersion
    ## 1  1e-01   0.1  0.27 0.15670212
    ## 2  1e+00   0.1  0.02 0.04216370
    ## 3  1e+01   0.1  0.01 0.03162278
    ## 4  1e+02   0.1  0.03 0.04830459
    ## 5  1e+03   0.1  0.03 0.04830459
    ## 6  1e-01   0.2  0.27 0.15670212
    ## 7  1e+00   0.2  0.02 0.04216370
    ## 8  1e+01   0.2  0.03 0.04830459
    ## 9  1e+02   0.2  0.03 0.04830459
    ## 10 1e+03   0.2  0.04 0.05163978
    ## 11 1e-01   0.3  0.26 0.15776213
    ## 12 1e+00   0.3  0.01 0.03162278
    ## 13 1e+01   0.3  0.03 0.04830459
    ## 14 1e+02   0.3  0.03 0.04830459
    ## 15 1e+03   0.3  0.04 0.05163978
    ## 16 1e-01   0.4  0.09 0.11972190
    ## 17 1e+00   0.4  0.01 0.03162278
    ## 18 1e+01   0.4  0.02 0.04216370
    ## 19 1e+02   0.4  0.03 0.04830459
    ## 20 1e+03   0.4  0.04 0.05163978
    ## 21 1e-01   0.5  0.03 0.04830459
    ## 22 1e+00   0.5  0.01 0.03162278
    ## 23 1e+01   0.5  0.02 0.04216370
    ## 24 1e+02   0.5  0.03 0.04830459
    ## 25 1e+03   0.5  0.04 0.05163978
    ## 26 1e-01   1.0  0.02 0.04216370
    ## 27 1e+00   1.0  0.02 0.04216370
    ## 28 1e+01   1.0  0.03 0.04830459
    ## 29 1e+02   1.0  0.03 0.04830459
    ## 30 1e+03   1.0  0.04 0.05163978
    ## 31 1e-01   2.0  0.05 0.05270463
    ## 32 1e+00   2.0  0.02 0.04216370
    ## 33 1e+01   2.0  0.03 0.04830459
    ## 34 1e+02   2.0  0.04 0.05163978
    ## 35 1e+03   2.0  0.04 0.05163978
    ## 36 1e-01   3.0  0.07 0.09486833
    ## 37 1e+00   3.0  0.02 0.04216370
    ## 38 1e+01   3.0  0.03 0.04830459
    ## 39 1e+02   3.0  0.04 0.05163978
    ## 40 1e+03   3.0  0.04 0.05163978
    ## 41 1e-01   4.0  0.15 0.11785113
    ## 42 1e+00   4.0  0.02 0.04216370
    ## 43 1e+01   4.0  0.03 0.04830459
    ## 44 1e+02   4.0  0.04 0.05163978
    ## 45 1e+03   4.0  0.04 0.05163978
    ## 46 1e-01   6.0  0.26 0.15776213
    ## 47 1e+00   6.0  0.02 0.04216370
    ## 48 1e+01   6.0  0.03 0.04830459
    ## 49 1e+02   6.0  0.03 0.04830459
    ## 50 1e+03   6.0  0.03 0.04830459
    ## 51 1e-01   7.0  0.27 0.15670212
    ## 52 1e+00   7.0  0.02 0.04216370
    ## 53 1e+01   7.0  0.03 0.04830459
    ## 54 1e+02   7.0  0.03 0.04830459
    ## 55 1e+03   7.0  0.03 0.04830459
    ## 56 1e-01   8.0  0.27 0.15670212
    ## 57 1e+00   8.0  0.02 0.04216370
    ## 58 1e+01   8.0  0.03 0.04830459
    ## 59 1e+02   8.0  0.03 0.04830459
    ## 60 1e+03   8.0  0.03 0.04830459
    ## 61 1e-01   9.0  0.27 0.15670212
    ## 62 1e+00   9.0  0.02 0.04216370
    ## 63 1e+01   9.0  0.03 0.04830459
    ## 64 1e+02   9.0  0.03 0.04830459
    ## 65 1e+03   9.0  0.03 0.04830459
    ## 66 1e-01  10.0  0.27 0.15670212
    ## 67 1e+00  10.0  0.02 0.04216370
    ## 68 1e+01  10.0  0.03 0.04830459
    ## 69 1e+02  10.0  0.03 0.04830459
    ## 70 1e+03  10.0  0.03 0.04830459

*best parameters* cost=1, $\gamma=0.5$ \## predict()

``` r
table(true=dat[-train,"y"], pred=predict(tune.nl.cv$best.model,
 newdata=dat[-train,]))
```

    ##     pred
    ## true  1  2
    ##    1 69  8
    ##    2  0 23

We can view the test set predictions for this model by applying the
predict() function to the **test data: *newdata==dat\[-train,\]* (index
set)** \#int правильно классифицированны = из

\##ROC Curves

``` r
library(ROCR)
rocplot=function(pred, truth, ...){
 predob = prediction(pred, truth)
 perf = performance(predob, "tpr", "fpr")
 plot(perf,...)}
```

write a short function to plot an ROC curve *given a vector containing a
numerical score for each observation, pred* and *a vector containing the
class label for each observation, truth.*

\#note SVMs and support vector classifiers *output class labels for each
observation.* However, it is also possible to obtain *fitted values for
each observation* =numerical scores used to obtain the class labels.

the sign of the fitted value determines on which *side of the decision
boundary* the observation lies.

**relationship between the fitted value and the class prediction** for a
given observation = if the fitted value \> zero-\> the observation is
assigned to one class, and if it is \< zero-\> it is assigned to the
other.

``` r
svm.fit.opt=svm(y~., data=dat[train,], kernel="radial", cost=10, gamma=0.1, decision.values=T)
fitted=attributes(predict(svm.fit.opt,dat[train,],decision.values=TRUE))$decision.values
```

In order to obtain the fitted values for a given SVM model fit, we use
decision.values=TRUE when fitting svm(). Then the predict() function
will output the fitted values \# ROC curve

``` r
rocplot(fitted,dat[-train,"y"])
```

![](SupportVectorMachines_files/figure-gfm/unnamed-chunk-22-1.png)<!-- -->
