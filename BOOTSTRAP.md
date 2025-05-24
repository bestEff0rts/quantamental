Bootstrap
================

## ПОСТАНОВКА ЗАДАЧИ

X, Y- returns(random quantities) of 2 finanicial assets we wish to
invest in; тогда alpha шт X; 1-alpha= Y; выберем такую alpha чтобы
минимизировать риск( i.e. variance) тогда
$alpha= (Var(Y)-Cov(X,Y))/(Var(X)+Var(Y)-2Cov(X,Y))$

Итог: цель- получить оценку alpha для минимизирования риска при
инвестициях в выбранные 2 инструмента Метод: bootstrap

## Function that outputs the statistic

функция alpha.fn: input- (X,Y) data и ветор(какие observations исп для
estimation)

``` r
library(ISLR)
attach(Portfolio)
dim(Portfolio)
```

    ## [1] 100   2

``` r
alpha.fn<- function(data,index){
  X<-data$X[index]
  Y<-data$Y[index]
  return((var(Y)-cov(X,Y))/(var(X)+var(Y)-2*cov(X,Y)))
  
}
alpha.fn(Portfolio,1:100)
```

    ## [1] 0.5758321

## bootstrap

replace=T значит с возможным повторением(после выбора элемент
возвращается в выборку) для автоматизации исп boot(data,функия которая
возвращает нужную статистику,R= число бутстрап replicates) 1000 бутстрап
estimates for alpha

    ## [1] 0.7368375

    ## 
    ## ORDINARY NONPARAMETRIC BOOTSTRAP
    ## 
    ## 
    ## Call:
    ## boot(data = Portfolio, statistic = alpha.fn, R = 1000)
    ## 
    ## 
    ## Bootstrap Statistics :
    ##      original       bias    std. error
    ## t1* 0.5758321 -0.001695873  0.09366347

\#теперь BOOTSTRAP для estimating accuracy of a linear regression model

``` r
library(boot)
library(ISLR)
attach(Auto)

bt.fn<- function(data,index)
  return(coefficients(lm(mpg~horsepower, data=data, subset=index )))
bt.fn(Auto,1:392)
```

    ## (Intercept)  horsepower 
    ##  39.9358610  -0.1578447

пусть теперь boot() посчитает standard error of 1000 bootstrap estimates
of coef (intercept and slope) note, пока что, модель имеет вид простой
линейной регресии $mpg= intercept+slope*horsepower$ t1- intercept; t2-
slope

``` r
boot(Auto,bt.fn,R=1000)
```

    ## 
    ## ORDINARY NONPARAMETRIC BOOTSTRAP
    ## 
    ## 
    ## Call:
    ## boot(data = Auto, statistic = bt.fn, R = 1000)
    ## 
    ## 
    ## Bootstrap Statistics :
    ##       original        bias    std. error
    ## t1* 39.9358610  0.0412152338 0.832986409
    ## t2* -0.1578447 -0.0005105609 0.007228529

Получаем $SE(\hat{B0}=0.83$ $SE(\hat{B1}=0.007$

``` r
summary(lm(mpg~horsepower, data=Auto))$coef
```

    ##               Estimate  Std. Error   t value      Pr(>|t|)
    ## (Intercept) 39.9358610 0.717498656  55.65984 1.220362e-187
    ## horsepower  -0.1578447 0.006445501 -24.48914  7.031989e-81

``` r
plot(residuals(lm(mpg~horsepower, data=Auto)))
```

![](BOOTSTRAP_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

# РАЗНЫЕ ЗНАЧЕНИЯ standard error estimates BOOTSTRAP И LEAST SQUARES- ПОЧЕМУ?

На самом деле, residuals plot показывает гетероскедастичность а также
нелинейность зависимости между предиктором и outcome; для МНК:
$SE(\hat{B0)}=\sigma^2*[1/n+\bar{x}^2/(\sum_{i=1}^n (x~i-\bar{x})^2)]$
$SE(\hat{B1)}=\sigma^2/(\sum_{i=1}^n (x~i-\bar{x})^2)$

Хотя формула для стандартных ошибок не полагается на то предположение,
что выбор функциональной формы модели- линейной в данном случае-
является верной, оценка для $σ^2$ полагается.

``` r
attach(Auto)
```

    ## Следующие объекты скрыты от Auto (pos = 3):
    ## 
    ##     acceleration, cylinders, displacement, horsepower, mpg, name,
    ##     origin, weight, year

``` r
plot(horsepower,mpg)
lm.fit<-lm(mpg ~ horsepower, data=Auto)
abline(lm.fit,lwd=2, col="yellow")
```

![](BOOTSTRAP_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

``` r
lm.fit.poly2<-lm(mpg~poly(horsepower,2),data=Auto)

lm.fit.poly3<-lm(mpg~poly(horsepower,3), data=Auto)

# lines(lm.fit.poly3, col="green", lwd=3)
```

Мы видим, что существует нелинейная связь в данных

и таким образом остатки (residuals) от линейного соответствия будут
inflated, и так будет $σ^2$. Во-вторых, стандартные формулы предполагают
(несколько нереалистично), что $xi$ являются f исключено, и вся
изменчивость приходит от вариации в ошибках i.The Подход bootstrap не
опирается ни на одно из этих предположений, и поэтому он Скорее всего,
более точная оценка стандартных ошибок X β 0 и X β 1 чем является
функция summary().

``` r
library(ggplot2)
```

    ## 
    ## Присоединяю пакет: 'ggplot2'

    ## Следующий объект скрыт от 'Auto':
    ## 
    ##     mpg

``` r
names(Auto)
```

    ## [1] "mpg"          "cylinders"    "displacement" "horsepower"   "weight"      
    ## [6] "acceleration" "year"         "origin"       "name"

``` r
attach(Auto)
```

    ## Следующий объект скрыт от package:ggplot2:
    ## 
    ##     mpg

    ## Следующие объекты скрыты от Auto (pos = 4):
    ## 
    ##     acceleration, cylinders, displacement, horsepower, mpg, name,
    ##     origin, weight, year

    ## Следующие объекты скрыты от Auto (pos = 5):
    ## 
    ##     acceleration, cylinders, displacement, horsepower, mpg, name,
    ##     origin, weight, year

``` r
ggplot(data=Auto, aes(x=horsepower, y= mpg), geom=point)
```

![](BOOTSTRAP_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->
