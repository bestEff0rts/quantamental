Методы снижения размерности признакового пространства. Dimension
Reduction Methods(PCA, PCR, PLS)
================

\##Терминология Principal Components Analysis трансформирует признаки в
их линейные комбинации и потом использует МНК(LS) в модели линейной
регрессии с новыми признаками. Partial Least Squares явялется Supervised
версией PCA т к учитывает Y response.

Перед нужно *стандартизировать* признаки Это не feature selection
methods, т к PC 1 direction и PLS 1 Direction являются **линейными**
комбинациями ВСЕХ оригинальных предикторов PC 1
ортогонально(перпендикулярно) PC 2= линейная комбинация оргинальных
признаков, которая не коррелирует с PC 1

PC *Loading Scores*- пропорции каждого признака (коэффициенты прямой PC
direction) *Eigen Vectors*- собственные значения вектора, единичный
вектор PC 1 *Eigen Values*- average of Sum of Squared Distances for best
fitted PC line

## Prinicpal Components Regression

``` r
library(pls)
```

    ## 
    ## Присоединяю пакет: 'pls'

    ## Следующий объект скрыт от 'package:stats':
    ## 
    ##     loadings

``` r
library(ISLR)
attach(Hitters)
Hitters=na.omit(Hitters)
sum(is.na(Hitters))
```

    ## [1] 0

``` r
x<-model.matrix(Salary~.,Hitters)[,-1]
y<-Hitters$Salary
train=sample(1:nrow(x), nrow(x)/2)
test=(-train)
y.test=y[test]
```

*apply PCR to the Hitters data, in order to predict Salary*

``` r
pcr.fit=pcr(Salary~.,data=Hitters,scale=TRUE, validation="CV")
summary(pcr.fit)
```

    ## Data:    X dimension: 263 19 
    ##  Y dimension: 263 1
    ## Fit method: svdpc
    ## Number of components considered: 19
    ## 
    ## VALIDATION: RMSEP
    ## Cross-validated using 10 random segments.
    ##        (Intercept)  1 comps  2 comps  3 comps  4 comps  5 comps  6 comps
    ## CV             452    352.1    349.9    349.3    347.5    343.8    342.0
    ## adjCV          452    351.8    349.6    349.0    347.1    343.3    341.2
    ##        7 comps  8 comps  9 comps  10 comps  11 comps  12 comps  13 comps
    ## CV       342.7    343.5    344.6     345.2     346.5     351.5     356.2
    ## adjCV    341.9    342.7    343.7     344.2     345.4     350.1     354.8
    ##        14 comps  15 comps  16 comps  17 comps  18 comps  19 comps
    ## CV        346.4     349.4     341.3     341.7     341.2     345.5
    ## adjCV     344.7     347.7     339.6     339.7     339.2     343.2
    ## 
    ## TRAINING: % variance explained
    ##         1 comps  2 comps  3 comps  4 comps  5 comps  6 comps  7 comps  8 comps
    ## X         38.31    60.16    70.84    79.03    84.29    88.63    92.26    94.96
    ## Salary    40.63    41.58    42.17    43.22    44.90    46.48    46.69    46.75
    ##         9 comps  10 comps  11 comps  12 comps  13 comps  14 comps  15 comps
    ## X         96.28     97.26     97.98     98.65     99.15     99.47     99.75
    ## Salary    46.86     47.76     47.82     47.85     48.10     50.40     50.55
    ##         16 comps  17 comps  18 comps  19 comps
    ## X          99.89     99.97     99.99    100.00
    ## Salary     53.01     53.85     54.61     54.61

Setting scale=TRUE означает has the effect of *standardizing* each
predictor The CV score is provided for each possible number of
components, ranging from M =0onwards. pcr() reports the root mean
squared error; in order to obtain the usual MSE, we must square this
quantity.

``` r
validationplot(pcr.fit,val.type="MSEP")
```

![](dimensionreductionPLSPCR_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->
\#interpretation наим root mean square error при n of
components=16;(m=19 - least squares) % of variance explained= amount of
information about the predictors or the response that is captured using
M principal components

Другими словами, если число M совпадает с числом p изначальных
компонентов(предикторов), % of variance explained- 100%

\##perform PCR on the training data and evaluate its test set
performance.

``` r
set.seed(1)
pcr.fit1=pcr(Salary~., data=Hitters,subset=train,scale=TRUE,
 validation="CV")
validationplot(pcr.fit,val.type="MSEP")
```

![](dimensionreductionPLSPCR_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->
Оказалось, что наименьшая cross-validation error при использовании M =7
компонент. Чтобы рассчитать *test MSE*:

``` r
pred.pcr<-predict(pcr.fit,x[test,],ncomp=7)
mean((pred.pcr-y.test)^2)
```

    ## [1] 142202

``` r
pcr.fit=pcr(y~x,scale=TRUE,ncomp=7)
summary(pcr.fit)
```

    ## Data:    X dimension: 263 19 
    ##  Y dimension: 263 1
    ## Fit method: svdpc
    ## Number of components considered: 7
    ## TRAINING: % variance explained
    ##    1 comps  2 comps  3 comps  4 comps  5 comps  6 comps  7 comps
    ## X    38.31    60.16    70.84    79.03    84.29    88.63    92.26
    ## y    40.63    41.58    42.17    43.22    44.90    46.48    46.69

## Patrial Least Squares

``` r
set.seed(1)
pls.fit<-plsr(Salary~., data=Hitters,subset=train,scale=TRUE,
 validation="CV")
summary(pls.fit)
```

    ## Data:    X dimension: 131 19 
    ##  Y dimension: 131 1
    ## Fit method: kernelpls
    ## Number of components considered: 19
    ## 
    ## VALIDATION: RMSEP
    ## Cross-validated using 10 random segments.
    ##        (Intercept)  1 comps  2 comps  3 comps  4 comps  5 comps  6 comps
    ## CV             367    279.2    281.7    291.8    301.1    306.2    312.1
    ## adjCV          367    278.7    280.9    290.2    298.7    303.4    308.8
    ##        7 comps  8 comps  9 comps  10 comps  11 comps  12 comps  13 comps
    ## CV       316.2    324.9    323.5     326.4     325.8     324.8     326.7
    ## adjCV    312.6    320.5    319.0     321.9     321.3     320.3     322.1
    ##        14 comps  15 comps  16 comps  17 comps  18 comps  19 comps
    ## CV        329.2     334.6     329.7     330.3     330.7     343.1
    ## adjCV     324.2     329.3     324.6     325.2     325.6     337.1
    ## 
    ## TRAINING: % variance explained
    ##         1 comps  2 comps  3 comps  4 comps  5 comps  6 comps  7 comps  8 comps
    ## X         35.28    56.67    66.22    72.15    78.19    83.50    86.70    89.28
    ## Salary    46.45    47.99    49.36    50.41    51.25    51.84    52.44    53.22
    ##         9 comps  10 comps  11 comps  12 comps  13 comps  14 comps  15 comps
    ## X         91.91     94.79     96.92     97.79     98.31     98.54     99.24
    ## Salary    53.79     54.01     54.25     54.48     54.70     55.02     55.09
    ##         16 comps  17 comps  18 comps  19 comps
    ## X          99.36     99.78     99.98     100.0
    ## Salary     55.26     55.27     55.28      55.3

Наименьшая cross-validation error- при only M=2 partial least squares
directions Чтобы оценить corresponding test set MSE.

``` r
 pls.pred=predict(pls.fit,x[test,],ncomp=2)
 mean((pls.pred-y.test)^2)
```

    ## [1] 169973.2

Test MSE PLS немного выше чем the test MSE PCR. Теперь PLS на полный
датасет, используя M=2(полученное путем кросс-валидации)

``` r
 pls.fit=plsr(Salary~., data=Hitters,scale=TRUE,ncomp=2)
 summary(pls.fit)
```

    ## Data:    X dimension: 263 19 
    ##  Y dimension: 263 1
    ## Fit method: kernelpls
    ## Number of components considered: 2
    ## TRAINING: % variance explained
    ##         1 comps  2 comps
    ## X         38.08    51.03
    ## Salary    43.05    46.40

the percentage of variance in Salary that the two-component PLS fit
explains, 46.40%, is almost as much as that explained using the initial
seven-component model PCR fit, 46.69%. Процент дисперсии Salary, которое
PLS объясняет,- %, практически равен проценту объясненной 7-компонентной
PCR моделью.( %) Это связано с тем, что PCR нацелен на максимизацию
amount of variance объясненной предикторами, а PLS ищет направление
которое объясняет variance и для предикторов и для response.
