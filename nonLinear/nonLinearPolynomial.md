non-linear models(Polynomial;Step Function)+ ANOVA для выбора степени
полинома (альтернатива CV)
================

*1* Polynomial Regression and Step Functions

``` r
poly.fit=lm(wage~poly(age,4), data=Wage)
coef(summary(poly.fit))
```

    ##                 Estimate Std. Error    t value     Pr(>|t|)
    ## (Intercept)    111.70361  0.7287409 153.283015 0.000000e+00
    ## poly(age, 4)1  447.06785 39.9147851  11.200558 1.484604e-28
    ## poly(age, 4)2 -478.31581 39.9147851 -11.983424 2.355831e-32
    ## poly(age, 4)3  125.52169 39.9147851   3.144742 1.678622e-03
    ## poly(age, 4)4  -77.91118 39.9147851  -1.951938 5.103865e-02

Этот синтаксис соответствует линейной модели, используя функцию lm(),
чтобы предсказать размер, использующий полиномий четвертой степени в
возрасте: poly(age,4) Функция возвращает матрицу, столбцы которой
являются основанием ортогональных полиномов, другими словами каждый
столбец является линейным ортогональной комбинацией переменных age^1,
age^2, age^3, age^4.

``` r
poly.fit2a=lm(wage~age+I(age^2)+I(age^3)+I(age^4),data=Wage)
coef(summary(poly.fit2a))
```

    ##                  Estimate   Std. Error   t value     Pr(>|t|)
    ## (Intercept) -1.841542e+02 6.004038e+01 -3.067172 0.0021802539
    ## age          2.124552e+01 5.886748e+00  3.609042 0.0003123618
    ## I(age^2)    -5.638593e-01 2.061083e-01 -2.735743 0.0062606446
    ## I(age^3)     6.810688e-03 3.065931e-03  2.221409 0.0263977518
    ## I(age^4)    -3.203830e-05 1.641359e-05 -1.951938 0.0510386498

``` r
# I(x^n)- wrapper or cbind()
poly.fit2b=lm(wage~cbind(age,age^2,age^3,age^4),data=Wage)
coef(summary(poly.fit2b))
```

    ##                                         Estimate   Std. Error   t value
    ## (Intercept)                        -1.841542e+02 6.004038e+01 -3.067172
    ## cbind(age, age^2, age^3, age^4)age  2.124552e+01 5.886748e+00  3.609042
    ## cbind(age, age^2, age^3, age^4)    -5.638593e-01 2.061083e-01 -2.735743
    ## cbind(age, age^2, age^3, age^4)     6.810688e-03 3.065931e-03  2.221409
    ## cbind(age, age^2, age^3, age^4)    -3.203830e-05 1.641359e-05 -1.951938
    ##                                        Pr(>|t|)
    ## (Intercept)                        0.0021802539
    ## cbind(age, age^2, age^3, age^4)age 0.0003123618
    ## cbind(age, age^2, age^3, age^4)    0.0062606446
    ## cbind(age, age^2, age^3, age^4)    0.0263977518
    ## cbind(age, age^2, age^3, age^4)    0.0510386498

*2* predict()

``` r
age.limits=range(age)
age.grid=seq(from=age.limits[1],to=age.limits[2])
length(age.grid)
```

    ## [1] 63

``` r
poly.pred=predict(poly.fit,newdata=list(age=age.grid),se=TRUE)
se=cbind(poly.pred$fit+2*poly.pred$se.fit,poly.pred$poly.fit-2*poly.pred$se.fit)
length(se)
```

    ## [1] 63

create a grid of values for age at which we want predictions *3* plot

``` r
 par(mfrow=c(1,2),mar=c(4.5,4.5,1,1),oma=c(0,0,4,0))
 plot(age,wage,xlim=age.limits,cex=.5,col="darkgrey")
 title("Degree-4 Polynomial",outer=T)
 lines(age.grid,poly.pred$fit,lwd=2,col="blue")
 matlines(age.grid,se,lwd=1,col="red",lty=3)
```

![](nonLinearPolynomial_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->
plot the data and add the fit from the degree-4 polynomial.

\##Hypothesis testing: which degree of polynomial to choose?
(alternative to CV) *1* fit models from linear to poly(age,5) and seek
simplest model sufficient to explain wage and age relationship

``` r
ln.fit= lm(wage~age, data=Wage)
poly2.fit=lm(wage~poly(age,2), data=Wage)
poly3.fit=lm(wage~poly(age,3), data=Wage)
poly4.fit=lm(wage~poly(age,4), data=Wage)
poly5.fit=lm(wage~poly(age,5), data=Wage)
```

*2* anova()

``` r
anova(ln.fit,poly2.fit,poly3.fit,poly4.fit,poly5.fit)
```

    ## Analysis of Variance Table
    ## 
    ## Model 1: wage ~ age
    ## Model 2: wage ~ poly(age, 2)
    ## Model 3: wage ~ poly(age, 3)
    ## Model 4: wage ~ poly(age, 4)
    ## Model 5: wage ~ poly(age, 5)
    ##   Res.Df     RSS Df Sum of Sq        F    Pr(>F)    
    ## 1   2998 5022216                                    
    ## 2   2997 4793430  1    228786 143.5931 < 2.2e-16 ***
    ## 3   2996 4777674  1     15756   9.8888  0.001679 ** 
    ## 4   2995 4771604  1      6070   3.8098  0.051046 .  
    ## 5   2994 4770322  1      1283   0.8050  0.369682    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

analysis of variance using F-test, $H~0$: model $M~0$ is sufficient to
explain the data against the $H~1$ alternative hypothesis that a more
complex model M2 is required. (netsed Models= the predictors in M1 must
be a subset of the predictors in M2) *result* The $p-value=< 2.2e-16$
comparing the linear Model 1 to the quadratic Model 2 is essentially
zero(\<10−15)=linear fit is not sufficient (reject the null hypothesis
$H~0$). p-value comparing the quadratic Model 2 to the cubic Model 3 is
very low ($0.001679 **$), so the quadratic fit is also insufficient. The
p-value comparing the cubic and degree-4 polynomials,Model 3 and Model
4,=\$ 0.051046\$, while the degree-5 polynomial Model 5 seems
unnecessary because its p-value is $0.37$.

Вывод:cubic or quadratic polynomial- reasonable fit to the data

## Задача: predict whether an individual earns \> \$250,000 per year.

*1* create the appropriate response vector+apply the glm() function
using family=“binomial” in order to fit a polynomial logistic regression
model

``` r
bin.fit=glm(I(wage>250)~poly(age,4),data=Wage,family=binomial)
```

*2* predict()

``` r
bin.pred=predict(bin.fit,newdata=list(age=age.grid),se=T)
bin.fit
```

    ## 
    ## Call:  glm(formula = I(wage > 250) ~ poly(age, 4), family = binomial, 
    ##     data = Wage)
    ## 
    ## Coefficients:
    ##   (Intercept)  poly(age, 4)1  poly(age, 4)2  poly(age, 4)3  poly(age, 4)4  
    ##        -4.301         71.964        -85.773         34.163        -47.401  
    ## 
    ## Degrees of Freedom: 2999 Total (i.e. Null);  2995 Residual
    ## Null Deviance:       730.5 
    ## Residual Deviance: 701.2     AIC: 711.2

*3* transform to calculate confidence intervals

``` r
pfit=exp(bin.pred$fit)/(1+exp(bin.pred$fit))
se.bands.logit = cbind(bin.pred$fit+2*bin.pred$se.fit, bin.pred$fit-2*bin.pred$se.fit)
se.bands = exp(se.bands.logit)/(1+exp(se.bands.logit))
length(se.bands)
```

    ## [1] 126

``` r
length(age.grid)
```

    ## [1] 63

we get predictions and standard errors for logit model
($log (Pr(Y =1|X)/(1 −Pr(Y =1|X)) =Xβ,$) in form of $X\hat β$ to obtain
confidence intervals for $Pr(Y =1|X)$, we use the transformation
$Pr(Y =1|X)= exp(Xβ)/(1+exp(Xβ))$

*4* plot()

``` r
plot(age,I(wage>250),xlim=age.limits,type="n",ylim=c(0,.2))
points(jitter(age), I((wage>250)/5),cex=.5,pch="|",col="darkgrey")
lines(age.grid,pfit,lwd=2, col="blue")
length(pfit)
```

    ## [1] 63

``` r
length(age.grid)
```

    ## [1] 63

``` r
length(se.bands)
```

    ## [1] 126

``` r
se1=se.bands[-c(64:126)]
length(se1)
```

    ## [1] 63

``` r
lines(age.grid,se1,lwd=1,col="green",lty=3)
```

![](nonLinearPolynomial_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->
*Step function* fit

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

cut() автоматически выбирает $age$ cutpoints: 33.5; 49; 64.5 Функция
cut() возвращает ordered categorical variable; Функция lm() создаетт set
of dummy variables(фиктивные переменные) для регрессии.

*predict()*

``` r
step.pred=predict(step.fit, newdata=list(age=age.grid),se=T)
```

*plot()*

``` r
par(mfrow=c(1,2),mar=c(4.5,4.5,1,1),oma=c(0,0,4,0))
plot(age,wage,xlim=age.limits,cex=.5,col="darkgrey")
title("Step Function",outer=T)
lines(age.grid,step.pred$fit,lwd=2,col="blue")
matlines(age.grid,se,lwd=3,col="green",lty=3)
```

![](nonLinearPolynomial_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->
