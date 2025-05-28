regression, natural and smooting splines
================

*1* Fit wage to age using a regression spline

``` r
library(splines)
spl.fit=lm(wage~bs(age,knots=c(25,40,60)),data=Wage)
```

(regression splines can be fit by constructing an appropriate matrix of
basis functions.) Функция bs() генерирует матрицу базисных функций для
splines с указанным набором knots *2* predict()

``` r
spl.pred=predict(spl.fit,newdata=list(age=age.grid),se=T)
plot(age,wage,col="gray")
lines(age.grid,spl.pred$fit,lwd=2, col="orange")
lines(age.grid,spl.pred$fit+2*spl.pred$se,lty="dashed", col="red")
lines(age.grid,spl.pred$fit-2*spl.pred$se,lty="dashed", col="blue")
```

![](nonLinearSplines_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->
prespecified knots at ages 25, 40, and 60 -\>spline с шестью basis
functions. (например, кубический spline с тремя knots имеет семь
степеней свободы; эти степени свободы =intercept+ шесть basis functions)
*3* df()

``` r
dim(bs(age,knots=c(25,40,60)))
```

    ## [1] 3000    6

``` r
dim(bs(age,df=6))
```

    ## [1] 3000    6

``` r
attr(bs(age,df=6),"knots")
```

    ## [1] 33.75 42.00 51.00

df () produces a spline with knots at uniform quantiles of the data. В
этом случае R выбирает knots at ages 33,8,42,0 и 51,0, которые
соответствуют 25, 50 и 75 percentiles of age

## fit a natural spline

*1* ns()

``` r
ns.fit=lm(wage~ns(age,df=4),data=Wage)
ns.pred=predict(ns.fit,newdata=list(age=age.grid),se=T)
plot(age,wage,col="gray")
lines(age.grid, ns.pred$fit,col="red",lwd=2)
```

![](nonLinearSplines_files/figure-gfm/unnamed-chunk-4-1.png)<!-- --> \##
fit a smoothing splin *1* smooth.spline()

``` r
 sp.fit=smooth.spline(age,wage,df=16)
 sp.fit2=smooth.spline(age,wage,cv=TRUE)
```

    ## Warning in smooth.spline(age, wage, cv = TRUE): кросс-валидация с неуникальными
    ## значениями 'x' выглядит сомнительно

``` r
 sp.fit2$df
```

    ## [1] 6.794596

*2* plot

``` r
plot(age,wage,xlim=age.limits,cex=.5,col="darkgrey")
title("Smoothing Spline")
lines(sp.fit,col="yellow",lwd=2)
lines(sp.fit2,col="orange",lwd=2)
legend("topright",legend=c("16 DF","6.8 DF"),
col=c("yellow","orange"),lty=1,lwd=2,cex=.8)
```

![](nonLinearSplines_files/figure-gfm/unnamed-chunk-6-1.png)<!-- --> \##
local regression *1* loess()

``` r
lr.fit=loess(wage~age,span=.2,data=Wage)
lr.fit2=loess(wage~age,span=.5,data=Wage)
```

*2* plot

``` r
plot(age,wage,xlim=age.limits,cex=.5,col="darkgrey")
title("Local Regression")
lines(age.grid,predict(lr.fit,data.frame(age=age.grid)),col="purple",lwd=2)
lines(age.grid,predict(lr.fit2,data.frame(age=age.grid)),col="green",lwd=2)
legend("topright",legend=c("Span=0.2","Span=0.5"), col=c("purple","green"),lty=1,lwd=2,cex=.8)
```

![](nonLinearSplines_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->
локальная линейная регрессия с использованием spans(диапазоны) 0,2 и
0,5: То есть, каждый район состоит из 20% или 50% наблюдений. The larger
the span, the smoother the fit.
