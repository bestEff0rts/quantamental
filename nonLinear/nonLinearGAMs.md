GAMs
================

\##задача wage~ year+age using natural spline, treating education as a
qualitative predictor *1* lm()

``` r
library(gam)
```

    ## Загрузка требуемого пакета: splines

    ## Загрузка требуемого пакета: foreach

    ## Loaded gam 1.22-5

``` r
gam.fit1= lm(wage~ns(year,4)+ns(age,5)+education, data=Wage)
```

т.к. это просто большая линейная регрессионная модель с использованием
соответствующих basis functions, о исп функцию lm() *2* Fit the model
$wage=β0+f1(year)+f2(age)+f3(education)+\epsilon$ using smoothing
splines

``` r
gam.fit.m3=gam(wage~s(year,4)+s(age,5)+education,data=Wage)
```

Функция s() из gam library= use a smoothing spline. функция year должна
иметь 4 df(degrees of freedom), функция age -5 df Переменная education
-qualitative,converted into four dummy variables. Используем gam() to
fit a GAM using these components. (all terms are fit simultaneously,
taking each other into account to explain the response) *3* plot

``` r
par(mfrow=c(1,3))
plot(gam.fit.m3, se=TRUE,col="blue")
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

``` r
plot.Gam(gam.fit1, se=TRUE, col="red")
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-3-2.png)<!-- --> *4*
ANOVA

``` r
gam.fit.m1=gam(wage~s(age,5)+education,data=Wage)
gam.fit.m2=gam(wage~year+s(age,5)+education,data=Wage)
anova(gam.fit.m1, gam.fit.m2,gam.fit.m3,test="F")
```

    ## Analysis of Deviance Table
    ## 
    ## Model 1: wage ~ s(age, 5) + education
    ## Model 2: wage ~ year + s(age, 5) + education
    ## Model 3: wage ~ s(year, 4) + s(age, 5) + education
    ##   Resid. Df Resid. Dev Df Deviance       F    Pr(>F)    
    ## 1      2990    3711731                                  
    ## 2      2989    3693842  1  17889.2 14.4771 0.0001447 ***
    ## 3      2986    3689770  3   4071.1  1.0982 0.3485661    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

($H~0$: M0- простая модель- адекватна) Чтобы выбрать между тремя
моделями $M~1$ GAM без year; $M~2$ GAM usimg linear function of year;
$M~3$ GAM using a spline function of year используем Analysis of
Variance(ANOVA) $p-value=0.0001448 ***$ -\> отвергаем нулевую гипотезу
что M1 лучше M2 (GAM с линейной функцией года лучше, чем GAM, который не
включает год вообще) $p-value=0.3485661$ -\> нет оснований полагать, что
линейная функция year необходима Вывод: основываясь на результатах
ANOVA, модель M2 предпочтительна *5* summary()

``` r
summary(gam.fit.m3)
```

    ## 
    ## Call: gam(formula = wage ~ s(year, 4) + s(age, 5) + education, data = Wage)
    ## Deviance Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -119.43  -19.70   -3.33   14.17  213.48 
    ## 
    ## (Dispersion Parameter for gaussian family taken to be 1235.69)
    ## 
    ##     Null Deviance: 5222086 on 2999 degrees of freedom
    ## Residual Deviance: 3689770 on 2986 degrees of freedom
    ## AIC: 29887.75 
    ## 
    ## Number of Local Scoring Iterations: NA 
    ## 
    ## Anova for Parametric Effects
    ##              Df  Sum Sq Mean Sq F value    Pr(>F)    
    ## s(year, 4)    1   27162   27162  21.981 2.877e-06 ***
    ## s(age, 5)     1  195338  195338 158.081 < 2.2e-16 ***
    ## education     4 1069726  267432 216.423 < 2.2e-16 ***
    ## Residuals  2986 3689770    1236                      
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Anova for Nonparametric Effects
    ##             Npar Df Npar F  Pr(F)    
    ## (Intercept)                          
    ## s(year, 4)        3  1.086 0.3537    
    ## s(age, 5)         4 32.380 <2e-16 ***
    ## education                            
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Значения р-value для года и возраста соответствуют нулевой гипотезе
линейной взаимосвязи против альтернативы нелинейной связи Большие
р-values для year соответствует выводу из ANOVA: линейная функция
является адекватной для этого year Однако есть доказательства того, что
для age необходим нелинейная функция.

*6* predict()

``` r
gam.pred=predict(gam.fit.m2,newdata=Wage)
```

\#other possible GAM building blocks

``` r
gam.lo.fit=gam(wage~s(year,df=4)+lo(age,span=0.7)+education,data=Wage)
plot.Gam(gam.lo.fit, se=TRUE, col="pink", lwd=2)
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-7-2.png)<!-- -->![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-7-3.png)<!-- -->
Чтобы использовать local regression fits as building blocks in a
GAM-*lo()* в примере используется local regression for the age term,with
a span of 0.7

*lo() to create interactions before calling gam()*

``` r
gam.int.fit=gam(wage~lo(year,age,span=0.5)+education, data=Wage)
```

    ## Warning in lo.wam(x, z, wz, fit$smooth, which, fit$smooth.frame, bf.maxit, :
    ## liv too small.  (Discovered by lowesd)

    ## Warning in lo.wam(x, z, wz, fit$smooth, which, fit$smooth.frame, bf.maxit, : lv
    ## too small.  (Discovered by lowesd)

    ## Warning in lo.wam(x, z, wz, fit$smooth, which, fit$smooth.frame, bf.maxit, :
    ## liv too small.  (Discovered by lowesd)

    ## Warning in lo.wam(x, z, wz, fit$smooth, which, fit$smooth.frame, bf.maxit, : lv
    ## too small.  (Discovered by lowesd)

пример: two-term model, first term= interaction between year and age,
fit by a local regression surface. *plot*

``` r
library(akima)
plot(gam.int.fit)
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-9-2.png)<!-- -->
\##fit a logistic regression GAM функция *I()*чтобы создать *binary
response variable*+ family=binomial

``` r
log.rg.gam=gam(I(wage>250)~year+s(age,df=5)+education,family="binomial",data=Wage)
par(mfrow=c(1,3))
plot(log.rg.gam,se=T,col="green")
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

``` r
table(education,I(wage>250))
```

    ##                     
    ## education            FALSE TRUE
    ##   1. < HS Grad         268    0
    ##   2. HS Grad           966    5
    ##   3. Some College      643    7
    ##   4. College Grad      663   22
    ##   5. Advanced Degree   381   45

fit a *logistic regression GAM* using all but this category

``` r
gam.lr.s=gam(I(wage>250)~year+s(age,df=5)+education,family="binomial",data=Wage,subset=(education!="1. < HS Grad"))
plot(gam.lr.s,se=T,col="green")
```

![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-12-2.png)<!-- -->![](nonLinearGAMs_files/figure-gfm/unnamed-chunk-12-3.png)<!-- -->
