ECONOMETRICS
================

``` r
knitr::opts_chunk$set(echo = TRUE)
df=read.csv("D:/data/all_stocks_5yr.csv")
str(df)
```

    ## 'data.frame':    619040 obs. of  7 variables:
    ##  $ date  : chr  "2013-02-08" "2013-02-11" "2013-02-12" "2013-02-13" ...
    ##  $ open  : num  15.1 14.9 14.4 14.3 14.9 ...
    ##  $ high  : num  15.1 15 14.5 14.9 15 ...
    ##  $ low   : num  14.6 14.3 14.1 14.2 13.2 ...
    ##  $ close : num  14.8 14.5 14.3 14.7 14 ...
    ##  $ volume: int  8407500 8882000 8126000 10259500 31879900 15628000 11354400 14725200 11922100 6071400 ...
    ##  $ Name  : chr  "AAL" "AAL" "AAL" "AAL" ...

\#добавляем features- : R t — это месячная простая доходность индекса

``` r
library(quantmod)
```

    ## Загрузка требуемого пакета: xts

    ## Загрузка требуемого пакета: zoo

    ## 
    ## Присоединяю пакет: 'zoo'

    ## Следующие объекты скрыты от 'package:base':
    ## 
    ##     as.Date, as.Date.numeric

    ## Загрузка требуемого пакета: TTR

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

``` r
library(TTR)
attach(df)

df$Intraday.Return = (close - open)/open
df$Range = (high - low)/low
df$Close.Return = c(NA, diff(close)/close[-length(close)])

df$Open.Return = c(NA, diff(open)/open[-length(open)])
df$High.Return = c(NA, diff(high)/high[-length(high)])
df$Low.Return = c(NA, diff(low)/low[-length(low)])
df$Volume.Change = c(NA, diff(volume)/volume[-length(volume)])
#скользящие средние
df$SMA10 <- SMA(df$close, n = 10)
df$SMA10 <- na.locf(df$SMA10, na.rm = FALSE)  # Заполнить последним известным значением
df$SMA20 <- SMA(df$close, n = 20)
df$SMA20 <- na.locf(df$SMA20, na.rm = FALSE)  # Заполнить последним известным значением
#labels for classificators- бинарные сигналы (1 если цена выросла, 0 если упала)
df$Price.Dir <- ifelse(df$Close.Return > 0, 1, 0)
df$RSI14 <- RSI(df$close, n = 14)
# MACD индикатор
df$macd <- MACD(df$close)

# df <- df[-1, ]
str(df)
```

    ## 'data.frame':    619040 obs. of  19 variables:
    ##  $ date           : chr  "2013-02-08" "2013-02-11" "2013-02-12" "2013-02-13" ...
    ##  $ open           : num  15.1 14.9 14.4 14.3 14.9 ...
    ##  $ high           : num  15.1 15 14.5 14.9 15 ...
    ##  $ low            : num  14.6 14.3 14.1 14.2 13.2 ...
    ##  $ close          : num  14.8 14.5 14.3 14.7 14 ...
    ##  $ volume         : int  8407500 8882000 8126000 10259500 31879900 15628000 11354400 14725200 11922100 6071400 ...
    ##  $ Name           : chr  "AAL" "AAL" "AAL" "AAL" ...
    ##  $ Intraday.Return: num  -0.0212 -0.0289 -0.0125 0.0252 -0.0636 ...
    ##  $ Range          : num  0.0335 0.0526 0.0291 0.0484 0.1368 ...
    ##  $ Close.Return   : num  NA -0.0197 -0.0131 0.0273 -0.0457 ...
    ##  $ Open.Return    : num  NA -0.0119 -0.0296 -0.0104 0.0448 ...
    ##  $ High.Return    : num  NA -0.00728 -0.03331 0.02963 0.00134 ...
    ##  $ Low.Return     : num  NA -0.0253 -0.0112 0.0106 -0.0765 ...
    ##  $ Volume.Change  : num  NA 0.0564 -0.0851 0.2626 2.1074 ...
    ##  $ SMA10          : num  NA NA NA NA NA ...
    ##  $ SMA20          : num  NA NA NA NA NA NA NA NA NA NA ...
    ##  $ Price.Dir      : num  NA 0 0 1 0 1 0 0 1 1 ...
    ##  $ RSI14          : num  NA NA NA NA NA NA NA NA NA NA ...
    ##  $ macd           : num [1:619040, 1:2] NA NA NA NA NA NA NA NA NA NA ...
    ##   ..- attr(*, "dimnames")=List of 2
    ##   .. ..$ : NULL
    ##   .. ..$ : chr [1:2] "macd" "signal"

``` r
str(df[20:40,])
```

    ## 'data.frame':    21 obs. of  19 variables:
    ##  $ date           : chr  "2013-03-08" "2013-03-11" "2013-03-12" "2013-03-13" ...
    ##  $ open           : num  15 14.8 15.1 15.5 16 ...
    ##  $ high           : num  15.2 15.2 15.6 16.2 16.4 ...
    ##  $ low            : num  14.8 14.7 14.9 15.5 15.9 ...
    ##  $ close          : num  14.9 15.1 15.5 15.9 16.2 ...
    ##  $ volume         : int  10593700 6961800 8999100 11380000 8383300 17667700 6514100 11805300 10819800 10740800 ...
    ##  $ Name           : chr  "AAL" "AAL" "AAL" "AAL" ...
    ##  $ Intraday.Return: num  -0.00467 0.01886 0.02378 0.02381 0.0169 ...
    ##  $ Range          : num  0.0243 0.0299 0.0435 0.0465 0.027 ...
    ##  $ Close.Return   : num  0.00675 0.01408 0.02445 0.02645 0.02137 ...
    ##  $ Open.Return    : num  0.01973 -0.00934 0.01953 0.02642 0.02831 ...
    ##  $ High.Return    : num  0.01808 -0.00329 0.0297 0.03846 0.00988 ...
    ##  $ Low.Return     : num  0.02345 -0.00876 0.01632 0.03545 0.02907 ...
    ##  $ Volume.Change  : num  0.161 -0.343 0.293 0.265 -0.263 ...
    ##  $ SMA10          : num  13.9 14.1 14.3 14.6 14.9 ...
    ##  $ SMA20          : num  14 14 14.1 14.2 14.2 ...
    ##  $ Price.Dir      : num  1 1 1 1 1 0 1 1 1 0 ...
    ##  $ RSI14          : num  53.8 56.1 59.9 63.7 66.5 ...
    ##  $ macd           : num [1:21, 1:2] NA NA NA NA NA ...
    ##   ..- attr(*, "dimnames")=List of 2
    ##   .. ..$ : NULL
    ##   .. ..$ : chr [1:2] "macd" "signal"

``` r
data.subset=df[c(1:768),]
str(data.subset)
```

    ## 'data.frame':    768 obs. of  19 variables:
    ##  $ date           : chr  "2013-02-08" "2013-02-11" "2013-02-12" "2013-02-13" ...
    ##  $ open           : num  15.1 14.9 14.4 14.3 14.9 ...
    ##  $ high           : num  15.1 15 14.5 14.9 15 ...
    ##  $ low            : num  14.6 14.3 14.1 14.2 13.2 ...
    ##  $ close          : num  14.8 14.5 14.3 14.7 14 ...
    ##  $ volume         : int  8407500 8882000 8126000 10259500 31879900 15628000 11354400 14725200 11922100 6071400 ...
    ##  $ Name           : chr  "AAL" "AAL" "AAL" "AAL" ...
    ##  $ Intraday.Return: num  -0.0212 -0.0289 -0.0125 0.0252 -0.0636 ...
    ##  $ Range          : num  0.0335 0.0526 0.0291 0.0484 0.1368 ...
    ##  $ Close.Return   : num  NA -0.0197 -0.0131 0.0273 -0.0457 ...
    ##  $ Open.Return    : num  NA -0.0119 -0.0296 -0.0104 0.0448 ...
    ##  $ High.Return    : num  NA -0.00728 -0.03331 0.02963 0.00134 ...
    ##  $ Low.Return     : num  NA -0.0253 -0.0112 0.0106 -0.0765 ...
    ##  $ Volume.Change  : num  NA 0.0564 -0.0851 0.2626 2.1074 ...
    ##  $ SMA10          : num  NA NA NA NA NA ...
    ##  $ SMA20          : num  NA NA NA NA NA NA NA NA NA NA ...
    ##  $ Price.Dir      : num  NA 0 0 1 0 1 0 0 1 1 ...
    ##  $ RSI14          : num  NA NA NA NA NA NA NA NA NA NA ...
    ##  $ macd           : num [1:768, 1:2] NA NA NA NA NA NA NA NA NA NA ...
    ##   ..- attr(*, "dimnames")=List of 2
    ##   .. ..$ : NULL
    ##   .. ..$ : chr [1:2] "macd" "signal"

``` r
train.set=data.subset[c(1:512),]
test.set=data.subset[c(512:768),]
attach(df)
```

    ## Следующие объекты скрыты от df (pos = 3):
    ## 
    ##     close, date, high, low, Name, open, volume

``` r
is.factor(Price.Dir)
```

    ## [1] FALSE

``` r
lm.fit=lm(Intraday.Return~open+high+low+close+volume+Intraday.Return+Range+Close.Return+Open.Return+High.Return+Low.Return+Volume.Change+SMA10 +SMA20 +RSI14, data=test.set)
```

    ## Warning in model.matrix.default(mt, mf, contrasts): отклик появился справа и
    ## поэтому был удален

    ## Warning in model.matrix.default(mt, mf, contrasts): проблема с термом 6 в
    ## 'model.matrix': не присвоены колонки

``` r
summary(lm.fit)
```

    ## 
    ## Call:
    ## lm(formula = Intraday.Return ~ open + high + low + close + volume + 
    ##     Intraday.Return + Range + Close.Return + Open.Return + High.Return + 
    ##     Low.Return + Volume.Change + SMA10 + SMA20 + RSI14, data = test.set)
    ## 
    ## Residuals:
    ##        Min         1Q     Median         3Q        Max 
    ## -0.0052019 -0.0008871 -0.0000176  0.0009319  0.0063007 
    ## 
    ## Coefficients:
    ##                 Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)   -3.099e-03  2.897e-03  -1.070 0.285812    
    ## open          -2.208e-02  5.005e-04 -44.124  < 2e-16 ***
    ## high          -2.666e-04  1.811e-03  -0.147 0.883076    
    ## low           -3.816e-04  1.745e-03  -0.219 0.827102    
    ## close          2.252e-02  4.862e-04  46.314  < 2e-16 ***
    ## volume         2.010e-11  2.252e-11   0.893 0.373011    
    ## Range          1.668e-02  6.775e-02   0.246 0.805721    
    ## Close.Return   2.972e-03  1.533e-02   0.194 0.846494    
    ## Open.Return   -4.791e-02  1.350e-02  -3.548 0.000466 ***
    ## High.Return    4.765e-02  1.598e-02   2.983 0.003150 ** 
    ## Low.Return     5.954e-03  1.340e-02   0.444 0.657101    
    ## Volume.Change -7.471e-04  3.637e-04  -2.054 0.041016 *  
    ## SMA10          3.031e-05  1.529e-04   0.198 0.843024    
    ## SMA20          1.845e-04  2.043e-04   0.903 0.367373    
    ## RSI14          5.086e-05  4.382e-05   1.161 0.246936    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.001813 on 242 degrees of freedom
    ## Multiple R-squared:  0.9921, Adjusted R-squared:  0.9916 
    ## F-statistic:  2165 on 14 and 242 DF,  p-value: < 2.2e-16

``` r
attach(data.subset)
```

    ## Следующие объекты скрыты от df (pos = 3):
    ## 
    ##     close, Close.Return, date, high, High.Return, Intraday.Return, low,
    ##     Low.Return, macd, Name, open, Open.Return, Price.Dir, Range, RSI14,
    ##     SMA10, SMA20, volume, Volume.Change

    ## Следующие объекты скрыты от df (pos = 4):
    ## 
    ##     close, date, high, low, Name, open, volume

``` r
lm.fit2=lm(Intraday.Return ~ open + close + Open.Return + High.Return + 
   Volume.Change, data = test.set)
summary(lm.fit2)
```

    ## 
    ## Call:
    ## lm(formula = Intraday.Return ~ open + close + Open.Return + High.Return + 
    ##     Volume.Change, data = test.set)
    ## 
    ## Residuals:
    ##        Min         1Q     Median         3Q        Max 
    ## -0.0051720 -0.0009119 -0.0001357  0.0008330  0.0076238 
    ## 
    ## Coefficients:
    ##                 Estimate Std. Error  t value Pr(>|t|)    
    ## (Intercept)    0.0005450  0.0011995    0.454   0.6500    
    ## open          -0.0224815  0.0001816 -123.810  < 2e-16 ***
    ## close          0.0224757  0.0001822  123.350  < 2e-16 ***
    ## Open.Return   -0.0482326  0.0082045   -5.879 1.31e-08 ***
    ## High.Return    0.0512462  0.0114229    4.486 1.10e-05 ***
    ## Volume.Change -0.0004217  0.0001965   -2.146   0.0328 *  
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.001818 on 251 degrees of freedom
    ## Multiple R-squared:  0.9917, Adjusted R-squared:  0.9916 
    ## F-statistic:  6026 on 5 and 251 DF,  p-value: < 2.2e-16

``` r
lm.fit3=lm(Intraday.Return ~ open+close+Open.Return+High.Return*
    Volume.Change, data = test.set)
summary(lm.fit3)
```

    ## 
    ## Call:
    ## lm(formula = Intraday.Return ~ open + close + Open.Return + High.Return * 
    ##     Volume.Change, data = test.set)
    ## 
    ## Residuals:
    ##        Min         1Q     Median         3Q        Max 
    ## -0.0053584 -0.0009347 -0.0000631  0.0007807  0.0062714 
    ## 
    ## Coefficients:
    ##                             Estimate Std. Error  t value Pr(>|t|)    
    ## (Intercept)                5.259e-05  1.193e-03    0.044  0.96488    
    ## open                      -2.259e-02  1.826e-04 -123.720  < 2e-16 ***
    ## close                      2.260e-02  1.840e-04  122.792  < 2e-16 ***
    ## Open.Return               -4.738e-02  8.087e-03   -5.859 1.46e-08 ***
    ## High.Return                5.536e-02  1.134e-02    4.883 1.87e-06 ***
    ## Volume.Change             -2.493e-04  2.022e-04   -1.233  0.21857    
    ## High.Return:Volume.Change -2.027e-02  6.871e-03   -2.950  0.00348 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.001791 on 250 degrees of freedom
    ## Multiple R-squared:  0.992,  Adjusted R-squared:  0.9918 
    ## F-statistic:  5177 on 6 and 250 DF,  p-value: < 2.2e-16

``` r
lm.fit4=lm(Intraday.Return ~ I(open^2) + I(close^2) + Open.Return + High.Return, data=test.set)
summary(lm.fit4)
```

    ## 
    ## Call:
    ## lm(formula = Intraday.Return ~ I(open^2) + I(close^2) + Open.Return + 
    ##     High.Return, data = test.set)
    ## 
    ## Residuals:
    ##        Min         1Q     Median         3Q        Max 
    ## -0.0107725 -0.0019047  0.0000795  0.0018160  0.0125300 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  6.207e-04  1.168e-03   0.531    0.596    
    ## I(open^2)   -2.485e-04  3.944e-06 -63.010  < 2e-16 ***
    ## I(close^2)   2.483e-04  3.972e-06  62.512  < 2e-16 ***
    ## Open.Return -9.158e-02  1.554e-02  -5.893 1.21e-08 ***
    ## High.Return  1.003e-01  2.156e-02   4.649 5.38e-06 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.003611 on 252 degrees of freedom
    ## Multiple R-squared:  0.9673, Adjusted R-squared:  0.9668 
    ## F-statistic:  1864 on 4 and 252 DF,  p-value: < 2.2e-16

``` r
anova(lm.fit3,lm.fit4)
```

    ## Analysis of Variance Table
    ## 
    ## Model 1: Intraday.Return ~ open + close + Open.Return + High.Return * 
    ##     Volume.Change
    ## Model 2: Intraday.Return ~ I(open^2) + I(close^2) + Open.Return + High.Return
    ##   Res.Df       RSS Df  Sum of Sq      F    Pr(>F)    
    ## 1    250 0.0008021                                   
    ## 2    252 0.0032851 -2 -0.0024831 386.99 < 2.2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Model 2(lm.fit4) с quadratic term сильно лучше т к p-value\< 2.2e-16
\*\*\*- из anova

``` r
plot(lm.fit4)
```

![](exampl1_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->![](exampl1_files/figure-gfm/unnamed-chunk-7-2.png)<!-- -->![](exampl1_files/figure-gfm/unnamed-chunk-7-3.png)<!-- -->![](exampl1_files/figure-gfm/unnamed-chunk-7-4.png)<!-- -->

## Example 1.

Consider the monthly simple returns of the CRSP equal-weighted index
from January 1926 to December 2008 for 996 observations. Denote the
series by Rt. The sample par tial autocorrelationfunction(PACF)ofRt
shows significant serial correlations at lags 1 so that an AR(1) model
is used for the mean equation. The squared series of the AR(3) residuals
suggests that the conditional heteroscedasticity might depend on lags 1,
3 and 8 of the resid uals. Therefore, we employ the special bilinear
model

``` r
Rt <- ts(df$Close.Return, frequency = 12)
sum(is.na(Rt))
```

    ## [1] 1

``` r
Rt<-na.omit(Rt)
# Rt <- ts(df, start=c(1,619040), frequency = 12)
pacf=pacf(Rt, main = "PACF of Monthly Simple Returns")
```

![](exampl1_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

``` r
plot(pacf)
```

![](exampl1_files/figure-gfm/unnamed-chunk-8-2.png)<!-- --> выходит за
синие линии- пределы confidence intervals- p=1 (1 лаг)

``` r
# Автоматический подбор порядка
best_ar <- ar(Rt, method = "ols", order.max = 20)
print(best_ar$order) # Рекомендуемый порядок AR
```

    ## [1] 1

``` r
# fit
ar.fit <- arima(Rt, order = c(1, 0, 0))  # AR(3) # model <- ar(Rt, order.max = 3, method = "ols")
names(ar.fit)
```

    ##  [1] "coef"      "sigma2"    "var.coef"  "mask"      "loglik"    "aic"      
    ##  [7] "arma"      "residuals" "call"      "series"    "code"      "n.cond"   
    ## [13] "nobs"      "model"

``` r
ar.fit
```

    ## 
    ## Call:
    ## arima(x = Rt, order = c(1, 0, 0))
    ## 
    ## Coefficients:
    ##           ar1  intercept
    ##       -0.0025      5e-04
    ## s.e.   0.0013      1e-04
    ## 
    ## sigma^2 estimated as 0.002167:  log likelihood = 1020356,  aic = -2040705

``` r
#проверка residuals
Box.test(ar.fit$residuals, lag = 20, type = "Ljung-Box")
```

    ## 
    ##  Box-Ljung test
    ## 
    ## data:  ar.fit$residuals
    ## X-squared = 23.606, df = 20, p-value = 0.26

``` r
plot(ar.fit$residuals)
```

![](exampl1_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

``` r
# диагностический график

par(mfrow = c(3, 1))
plot.ts(ar.fit$residuals, main = "Standardized Residuals")
acf(ar.fit$residuals, lag.max = 30, main = "ACF of Residuals")
pacf(ar.fit$residuals, lag.max = 30, main = "PACF of Residuals")
```

![](exampl1_files/figure-gfm/unnamed-chunk-10-2.png)<!-- -->

``` r
shapiro.test(ar.fit$residuals[1:5000])  # Проверка нормальности
```

    ## 
    ##  Shapiro-Wilk normality test
    ## 
    ## data:  ar.fit$residuals[1:5000]
    ## W = 0.6905, p-value < 2.2e-16

``` r
library(FinTS)
ArchTest(ar.fit$residuals)  # Проверка ARCH-эффектов
```

    ## 
    ##  ARCH LM-test; Null hypothesis: no ARCH effects
    ## 
    ## data:  ar.fit$residuals
    ## Chi-squared = 0.00045161, df = 12, p-value = 1

``` r
# График квантиль-квантиль
qqnorm(ar.fit$residuals)
qqline(ar.fit$residuals, col = "red")
```

![](exampl1_files/figure-gfm/unnamed-chunk-10-3.png)<!-- -->
Нормальность W=0.69, p\<2.2e-16 Не нормальное распределение
(преобразовать данные) Гетероскедастичность p=1, χ²≈0 Однородная
дисперсия (ARCH-тест: p-value = 1 ⇒ отсутствие ARCH-эффектов;
Chi-squared ≈ 0 ⇒ нет кластеров волатильности)

``` r
# predict
ar.pred <- predict(ar.fit, n.ahead = 5)
print(ar.pred)
```

    ## $pred
    ##                Jan Feb Mar Apr May Jun Jul Aug          Sep          Oct
    ## 51587                                          0.0005238022 0.0005429641
    ## 51588 0.0005429155                                                      
    ##                Nov          Dec
    ## 51587 0.0005429154 0.0005429155
    ## 51588                          
    ## 
    ## $se
    ##              Jan Feb Mar Apr May Jun Jul Aug        Sep        Oct        Nov
    ## 51587                                        0.04655001 0.04655016 0.04655016
    ## 51588 0.04655016                                                             
    ##              Dec
    ## 51587 0.04655016
    ## 51588

``` r
ar.pred$se
```

    ##              Jan Feb Mar Apr May Jun Jul Aug        Sep        Oct        Nov
    ## 51587                                        0.04655001 0.04655016 0.04655016
    ## 51588 0.04655016                                                             
    ##              Dec
    ## 51587 0.04655016
    ## 51588

``` r
names(ar.pred)
```

    ## [1] "pred" "se"

теперь сохраним predictions ar модели и ее residuals (для дальнейшего
использования в ml моделях в качестве features/target variable)
