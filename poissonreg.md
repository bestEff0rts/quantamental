poisson regression
================

data generation

``` r
PD<-rpois(60, lambda = 5)
PD
```

    ##  [1]  5 11  5 10  5  8  8  3  4  6  3  3  3 10  5  8  4  9  6  5  3  4  6  4  8
    ## [26]  4  3  9  5  6  5  6  9  7  7  3  3  5  2  9  3  4  6  3  4 11  6  3  4  5
    ## [51]  6  4  5  4  7  3  6  2  7  4

``` r
data<-table(PD)
```

plot

``` r
plot(data,cex.axis=0.6,xlab="Counts",ylab="Frequency of counts")
```

![](poissonreg_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

``` r
WPData<-as.data.frame(warpbreaks)
str(WPData)
```

    ## 'data.frame':    54 obs. of  3 variables:
    ##  $ breaks : num  26 30 54 25 70 52 51 26 67 18 ...
    ##  $ wool   : Factor w/ 2 levels "A","B": 1 1 1 1 1 1 1 1 1 1 ...
    ##  $ tension: Factor w/ 3 levels "L","M","H": 1 1 1 1 1 1 1 1 1 2 ...

``` r
summary(WPData)
```

    ##      breaks      wool   tension
    ##  Min.   :10.00   A:27   L:18   
    ##  1st Qu.:18.25   B:27   M:18   
    ##  Median :26.00          H:18   
    ##  Mean   :28.15                 
    ##  3rd Qu.:34.00                 
    ##  Max.   :70.00

``` r
# fix(WPData)
```

Box plot (ящичный график)

``` r
par(mfrow = c(1, 2))
plot(breaks ~ tension, data = WPData, col = "pink",
     varwidth = TRUE, subset = wool == "A", main = "Wool A",ylim=c(8,72))
plot(breaks ~ tension, data = warpbreaks, col = "purple",
     varwidth = TRUE, subset = wool == "B", main = "Wool B",ylim=c(8,72))
```

![](poissonreg_files/figure-gfm/unnamed-chunk-4-1.png)<!-- --> Разделим
данные train test

``` r
dim(WPData)
```

    ## [1] 54  3

``` r
train.indices= sample(nrow(WPData),round(0.75*nrow(WPData)),replace=FALSE)
train.set=WPData[train.indices,]
test.set=WPData[-train.indices,]
# fix(test.set)
```

Обучим модель train data

``` r
pr.fit1 <- glm(breaks ~ wool+tension, data = train.set, family=poisson)
pr.fit1
```

    ## 
    ## Call:  glm(formula = breaks ~ wool + tension, family = poisson, data = train.set)
    ## 
    ## Coefficients:
    ## (Intercept)        woolB     tensionM     tensionH  
    ##      3.6245      -0.1161      -0.2998      -0.4771  
    ## 
    ## Degrees of Freedom: 39 Total (i.e. Null);  36 Residual
    ## Null Deviance:       188.5 
    ## Residual Deviance: 145.3     AIC: 356.4

``` r
exp(coef(pr.fit1))
```

    ## (Intercept)       woolB    tensionM    tensionH 
    ##  37.5052099   0.8903763   0.7409437   0.6206015

``` r
exp(confint(pr.fit1))
```

    ## Выполняю профилирование...

    ##                  2.5 %     97.5 %
    ## (Intercept) 33.5042150 41.8464607
    ## woolB        0.7906111  1.0024209
    ## tensionM     0.6467852  0.8491391
    ## tensionH     0.5304245  0.7249591

``` r
Coef1<-coef(pr.fit1)
Coef1[2]
```

    ##      woolB 
    ## -0.1161112

``` r
exp(Coef1[2])
```

    ##     woolB 
    ## 0.8903763

``` r
summary(pr.fit1)
```

    ## 
    ## Call:
    ## glm(formula = breaks ~ wool + tension, family = poisson, data = train.set)
    ## 
    ## Coefficients:
    ##             Estimate Std. Error z value Pr(>|z|)    
    ## (Intercept)  3.62448    0.05671  63.914  < 2e-16 ***
    ## woolB       -0.11611    0.06054  -1.918   0.0551 .  
    ## tensionM    -0.29983    0.06942  -4.319 1.56e-05 ***
    ## tensionH    -0.47707    0.07966  -5.988 2.12e-09 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## (Dispersion parameter for poisson family taken to be 1)
    ## 
    ##     Null deviance: 188.47  on 39  degrees of freedom
    ## Residual deviance: 145.31  on 36  degrees of freedom
    ## AIC: 356.36
    ## 
    ## Number of Fisher Scoring iterations: 4

``` r
deviance(pr.fit1)/df.residual(pr.fit1)
```

    ## [1] 4.036408

добавим interaction term и обучим новую модель

``` r
pr.fit2=glm(breaks~wool*tension, data = train.set, family=poisson)
pr.fit2
```

    ## 
    ## Call:  glm(formula = breaks ~ wool * tension, family = poisson, data = train.set)
    ## 
    ## Coefficients:
    ##    (Intercept)           woolB        tensionM        tensionH  woolB:tensionM  
    ##         3.7534         -0.4502         -0.6071         -0.5684          0.6635  
    ## woolB:tensionH  
    ##         0.2526  
    ## 
    ## Degrees of Freedom: 39 Total (i.e. Null);  34 Residual
    ## Null Deviance:       188.5 
    ## Residual Deviance: 122.8     AIC: 337.8

``` r
exp(coef(pr.fit2))
```

    ##    (Intercept)          woolB       tensionM       tensionH woolB:tensionM 
    ##     42.6666667      0.6375000      0.5449219      0.5664062      1.9415747 
    ## woolB:tensionH 
    ##      1.2873563

``` r
exp(confint(pr.fit2))
```

    ## Выполняю профилирование...

    ##                     2.5 %     97.5 %
    ## (Intercept)    37.6511620 48.1086222
    ## woolB           0.5165526  0.7832926
    ## tensionM        0.4506638  0.6576521
    ## tensionH        0.4610464  0.6931770
    ## woolB:tensionM  1.4687736  2.5750721
    ## woolB:tensionH  0.9355273  1.7728426

``` r
summary(pr.fit2)
```

    ## 
    ## Call:
    ## glm(formula = breaks ~ wool * tension, family = poisson, data = train.set)
    ## 
    ## Coefficients:
    ##                Estimate Std. Error z value Pr(>|z|)    
    ## (Intercept)     3.75342    0.06250  60.055  < 2e-16 ***
    ## woolB          -0.45020    0.10611  -4.243 2.21e-05 ***
    ## tensionM       -0.60711    0.09635  -6.301 2.95e-10 ***
    ## tensionH       -0.56844    0.10394  -5.469 4.52e-08 ***
    ## woolB:tensionM  0.66350    0.14317   4.634 3.58e-06 ***
    ## woolB:tensionH  0.25259    0.16297   1.550    0.121    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## (Dispersion parameter for poisson family taken to be 1)
    ## 
    ##     Null deviance: 188.47  on 39  degrees of freedom
    ## Residual deviance: 122.75  on 34  degrees of freedom
    ## AIC: 337.81
    ## 
    ## Number of Fisher Scoring iterations: 4

``` r
deviance(pr.fit2)/df.residual(pr.fit2)
```

    ## [1] 3.610371
