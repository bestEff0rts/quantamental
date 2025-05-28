NONLINEARapplied
================

## условие

In this exercise, you will further analyze the Wage data set considered
throughout this chapter. (a) Perform *polynomial regression* to predict
wage using age. Use cross-validation to select the optimal degree d for
the polynomial. What degree was chosen, and how does this compare to the
results of hypothesis testing using ANOVA? Make a plot ofthe resulting
polynomial fit to the data. *1* fit wage~poly(age,d)+ select d via CV

``` r
library(boot)
 set.seed(17)
 cv.error.10=rep(0,10)
 for (i in 1:10){
 glm.fit=glm(wage~poly(age,i),data=Wage)
 cv.error.10[i]=cv.glm(Wage,glm.fit,K=10)$delta[1]
 }
 cv.error.10
```

    ##  [1] 1675.109 1601.423 1595.850 1594.073 1593.960 1597.031 1594.023 1594.544
    ##  [9] 1592.573 1593.557

2)  Fit a step function to predict wage using age, and perform cross
    validation to choose the optimal number of cuts. Make a plot of the
    fit obtained.

``` r
table(cut(age,4))
```

    ## 
    ## (17.9,33.5]   (33.5,49]   (49,64.5] (64.5,80.1] 
    ##         750        1399         779          72

``` r
step.fit=lm(wage~cut(age,4),data=Wage)
coef(summary(step.fit))
```

    ##                         Estimate Std. Error   t value     Pr(>|t|)
    ## (Intercept)            94.158392   1.476069 63.789970 0.000000e+00
    ## cut(age, 4)(33.5,49]   24.053491   1.829431 13.148074 1.982315e-38
    ## cut(age, 4)(49,64.5]   23.664559   2.067958 11.443444 1.040750e-29
    ## cut(age, 4)(64.5,80.1]  7.640592   4.987424  1.531972 1.256350e-01

``` r
pred=predict(step.fit,newdata=list(age=age.grid),se=T)
plot(age,wage,col="gray")
lines(age.grid,pred$fit,lwd=2)
```

![](StepFapplied_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->
