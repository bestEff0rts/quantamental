NAIVE BAYES classificator
================

\##1-Обучить модель Naive Bayes to Smarket data

``` r
library(e1071)
train <- (Year < 2005)
Smarket.2005 <- Smarket[!train, ]
dim(Smarket.2005)
```

    ## [1] 252   9

``` r
Direction.2005 <- Direction[!train]
nb.fit <-naiveBayes(Direction~Lag1 + Lag2, data = Smarket, subset = train)
nb.fit
```

    ## 
    ## Naive Bayes Classifier for Discrete Predictors
    ## 
    ## Call:
    ## naiveBayes.default(x = X, y = Y, laplace = laplace)
    ## 
    ## A-priori probabilities:
    ## Y
    ##     Down       Up 
    ## 0.491984 0.508016 
    ## 
    ## Conditional probabilities:
    ##       Lag1
    ## Y             [,1]     [,2]
    ##   Down  0.04279022 1.227446
    ##   Up   -0.03954635 1.231668
    ## 
    ##       Lag2
    ## Y             [,1]     [,2]
    ##   Down  0.03389409 1.239191
    ##   Up   -0.03132544 1.220765

Output Содержит оцененное mean значение и стандартное отклонение для
каждой переменной в каждом классе Так, mean for Lag1 is 0.04279022 for
Direction=Down, sd=1.227446 По умолчанию, эта реализация модели
байесовского классификатора позволяет получить количественный признак,
используя гауссово распределение. Однако для оценки распределений также
может быть использован метод kernel density- плотности ядра.

``` r
mean(Lag1[train][Direction[train] == "Down"])
```

    ## [1] 0.04279022

``` r
sd(Lag1[train][Direction[train] == "Down"])
```

    ## [1] 1.227446

*predict()* на test data

``` r
 nb.class <-predict(nb.fit, Smarket.2005)
 table(nb.class, Direction.2005)
```

    ##         Direction.2005
    ## nb.class Down  Up
    ##     Down   28  20
    ##     Up     83 121

Confusion matrix, TP=121, TN=28, TP Rate=121/(121+20)=0.858156; FP Rate=
83/(83+28)= 0.7477477

``` r
mean(nb.class == Direction.2005)
```

    ## [1] 0.5912698

Naive Bayes с этими данными дает точные прогнозы в течение В 59%
случаев.

``` r
 nb.preds <-predict(nb.fit, Smarket.2005, type = "raw")
 nb.preds[1:5, ]
```

    ##           Down        Up
    ## [1,] 0.4873164 0.5126836
    ## [2,] 0.4762492 0.5237508
    ## [3,] 0.4653377 0.5346623
    ## [4,] 0.4748652 0.5251348
    ## [5,] 0.4901890 0.5098110

Функция predict() также может генерировать оценки вероятности того, что
каждое наблюдение относится к определенному классу.
