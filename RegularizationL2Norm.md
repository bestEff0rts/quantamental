Regularization: (L2) Ridge Regression and (L1) the Lasso
================

## убрать NA

``` r
Hitters=na.omit(Hitters)
sum(is.na(Hitters))
```

    ## [1] 0

## Including Code

model.matrix creates a design (or model) matrix, e.g., by expanding
factors to a set of dummy variables (depending on the contrasts) and
expanding interactions similar

\#Используем Lasso и Ridge чтобы прогнозировать Salary

``` r
x=model.matrix(Salary~.,Hitters)[,-1]
y=Hitters$Salary
```

## glmnet()

The glmnet() function has an alpha argument that determines what type of
model is fit. If alpha=0 then a ridge regression model is fit, and if
alpha=1 then a lasso model is fit.

``` r
library(glmnet)
grid=10^seq(10,-2,length=100)
ridge.mod=glmnet(x,y,alpha=0,lambda=grid)
dim(coef(ridge.mod))
```

    ## [1]  20 100

Associated with each value of λ is a vector of ridge regression
coefficients, stored in a matrix that can be accessed by coef().

``` r
ridge.mod$lambda[50]
```

    ## [1] 11497.57

``` r
coef(ridge.mod)[,50]
```

    ##   (Intercept)         AtBat          Hits         HmRun          Runs 
    ## 407.356050200   0.036957182   0.138180344   0.524629976   0.230701523 
    ##           RBI         Walks         Years        CAtBat         CHits 
    ##   0.239841459   0.289618741   1.107702929   0.003131815   0.011653637 
    ##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
    ##   0.087545670   0.023379882   0.024138320   0.025015421   0.085028114 
    ##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
    ##  -6.215440973   0.016482577   0.002612988  -0.020502690   0.301433531

``` r
sqrt(sum(coef(ridge.mod)[-1,50]^2))
```

    ## [1] 6.360612

Ожидаемо,оценки коэффициентов гораздо меньше (L2norm) при использовании
большого значения λ, в сравнении с малым значением λ.

Напротив, вот коэффициенты, когда λ=705, вместе с их L2 Norm. Большая L2
Norm коэффициентов associated with меньшее значение λ.

``` r
ridge.mod$lambda[60]
```

    ## [1] 705.4802

``` r
coef(ridge.mod)[,60]
```

    ##  (Intercept)        AtBat         Hits        HmRun         Runs          RBI 
    ##  54.32519950   0.11211115   0.65622409   1.17980910   0.93769713   0.84718546 
    ##        Walks        Years       CAtBat        CHits       CHmRun        CRuns 
    ##   1.31987948   2.59640425   0.01083413   0.04674557   0.33777318   0.09355528 
    ##         CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists 
    ##   0.09780402   0.07189612  13.68370191 -54.65877750   0.11852289   0.01606037 
    ##       Errors   NewLeagueN 
    ##  -0.70358655   8.61181213

``` r
sqrt(sum(coef(ridge.mod)[-1,60]^2))
```

    ## [1] 57.11001

# predict() for a new value

``` r
predict(ridge.mod,s=50,type="coefficients")[1:20,]
```

    ##   (Intercept)         AtBat          Hits         HmRun          Runs 
    ##  4.876610e+01 -3.580999e-01  1.969359e+00 -1.278248e+00  1.145892e+00 
    ##           RBI         Walks         Years        CAtBat         CHits 
    ##  8.038292e-01  2.716186e+00 -6.218319e+00  5.447837e-03  1.064895e-01 
    ##        CHmRun         CRuns          CRBI        CWalks       LeagueN 
    ##  6.244860e-01  2.214985e-01  2.186914e-01 -1.500245e-01  4.592589e+01 
    ##     DivisionW       PutOuts       Assists        Errors    NewLeagueN 
    ## -1.182011e+02  2.502322e-01  1.215665e-01 -3.278600e+00 -9.496680e+00

\##We now split the samples into a training set and a test set in order
to estimate the test error of ridge regression and the lasso.

``` r
set.seed(1)
train=sample(1:nrow(x), nrow(x)/2)
test=(-train)
y.test=y[test]
```

\#Next we fit a ridge regression model on the training set, and evaluate
its MSE on the test set, using λ = 4.

``` r
 ridge.mod=glmnet(x[train,],y[train],alpha=0,lambda=grid,
 thresh=1e-12)
 ridge.pred=predict(ridge.mod,s=4,newx=x[test,])
 mean((ridge.pred-y.test)^2)
```

    ## [1] 142199.2

That is the test MSE \# CV: instead of arbitrarily choosing λ = 4, it
would be better to use cross-validation to choose the tuning parameter
λ. built-in cross-validation function, cv.glmnet().

``` r
set.seed(1)
cv.out=cv.glmnet(x[train,],y[train],alpha=0)
plot(cv.out)
```

![](RegularizationL2Norm_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->

``` r
bestlam=cv.out$lambda.min
bestlam
```

    ## [1] 326.0828

``` r
ridge.pred=predict(ridge.mod,s=bestlam,newx=x[test,])
mean((ridge.pred-y.test)^2)
```

    ## [1] 139856.6

``` r
ridge.pred4=predict(ridge.mod,s=4,newx=x[test,])
mean((ridge.pred4-y.test)^2)
```

    ## [1] 142199.2

\#improvement! This represents a further improvement over the test MSE
that we got using λ = 4. \#Finally, we refit our ridge regression model
on the full data set, using the value of λ chosen by cross-validation,
and examine the coefficient estimates

``` r
out=glmnet(x,y,alpha=0)
predict(out,type="coefficients",s=bestlam)[1:20,]
```

    ##  (Intercept)        AtBat         Hits        HmRun         Runs          RBI 
    ##  15.44383120   0.07715547   0.85911582   0.60103106   1.06369007   0.87936105 
    ##        Walks        Years       CAtBat        CHits       CHmRun        CRuns 
    ##   1.62444617   1.35254778   0.01134999   0.05746654   0.40680157   0.11456224 
    ##         CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists 
    ##   0.12116504   0.05299202  22.09143197 -79.04032656   0.16619903   0.02941950 
    ##       Errors   NewLeagueN 
    ##  -1.36092945   9.12487765

\#As expected none of the coefficients ar ezero—ridge regression does
not perform variable selection:)
