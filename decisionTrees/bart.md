Bayesian Additive Regression Trees(bart)vs bagging vs RF
================

## Summary of Tree Ensemble Methods

*bagging*=bootstrapping+aggregating, sampling with repetition; деревья
выращиваются независимо на основе случайных выборок
наблюдений-\>деревья, как правило, очень похожи друг на друга. Таким
образом, создание пакетов-\> может привести к локальным оптимумам и не
позволит полностью изучить пространство модели.

*random forests*= деревья выращиваются независимо на основе случайных
выборок наблюдений; Однако каждый split (разбиение) на каждом дереве
выполняется с использованием случайного подмножества объектов, тем самым
декорируя деревья -\> более тщательное изучение пространства модели

*boosting*= используютя только исходные данные, никаких случайных
выборок. Деревья выращиваются последовательно, используя подход
“медленного”обучения: каждое новое дерево соответствует сигналу,
оставшемуся от предыдущих деревьев, и shrunken down перед
использованием.

*bart*= используем только исходные данные, последовательно выращиваем
деревья. Однако каждое дерево is perutrbed(подвергается возмущению),
чтобы избежать локальных минимумов и добиться более тщательного изучения
пространства модели.

\##BART

``` r
attach(Boston)
library(BART)
```

    ## Загрузка требуемого пакета: nlme

    ## Загрузка требуемого пакета: survival

# train test datasets

``` r
set.seed(1)
train <-sample(1:nrow(Boston), nrow(Boston) / 2)
x <- Boston[, 1:12]
y <- Boston[, "medv"]

xtrain <- x[train, ]
ytrain <- y[train]
xtest <- x[-train, ]
ytest <- y[-train]
```

# fit bart

``` r
bart.fit <-gbart(xtrain, ytrain, x.test = xtest)
```

    ## *****Calling gbart: type=1
    ## *****Data:
    ## data:n,p,np: 253, 12, 253
    ## y1,yn: 0.213439, -5.486561
    ## x1,x[n*p]: 0.109590, 20.080000
    ## xp1,xp[np*p]: 0.027310, 7.880000
    ## *****Number of Trees: 200
    ## *****Number of Cut Points: 100 ... 100
    ## *****burn,nd,thin: 100,1000,1
    ## *****Prior:beta,alpha,tau,nu,lambda,offset: 2,0.95,0.795495,3,3.71636,21.7866
    ## *****sigma: 4.367914
    ## *****w (weights): 1.000000 ... 1.000000
    ## *****Dirichlet:sparse,theta,omega,a,b,rho,augment: 0,0,1,0.5,1,12,0
    ## *****printevery: 100
    ## 
    ## MCMC
    ## done 0 (out of 1100)
    ## done 100 (out of 1100)
    ## done 200 (out of 1100)
    ## done 300 (out of 1100)
    ## done 400 (out of 1100)
    ## done 500 (out of 1100)
    ## done 600 (out of 1100)
    ## done 700 (out of 1100)
    ## done 800 (out of 1100)
    ## done 900 (out of 1100)
    ## done 1000 (out of 1100)
    ## time: 5s
    ## trcnt,tecnt: 1000,1000

# test error

``` r
yhat.bart <- bart.fit$yhat.test.mean
mean((ytest- yhat.bart)^2)
```

    ## [1] 15.97434

# проверим, сколько раз каждая переменная появлялась в коллекции деревьев.

``` r
names(bart.fit)
```

    ##  [1] "sigma"           "yhat.train"      "yhat.test"       "varcount"       
    ##  [5] "varprob"         "treedraws"       "proc.time"       "hostname"       
    ##  [9] "yhat.train.mean" "sigma.mean"      "LPML"            "yhat.test.mean" 
    ## [13] "ndpost"          "offset"          "varcount.mean"   "varprob.mean"   
    ## [17] "rm.const"

``` r
ord <-order(bart.fit$varcount.mean, decreasing = T)
bart.fit$varcount.mean[ord]
```

    ##   lstat     nox     tax      rm     rad    chas   indus ptratio     age     dis 
    ##  21.638  21.458  20.900  20.725  20.627  20.102  19.640  19.083  18.736  15.417 
    ##      zn    crim 
    ##  15.146  11.891

# сравнение с bagging(same data)

``` r
library(randomForest)
```

    ## randomForest 4.7-1.2

    ## Type rfNews() to see new features/changes/bug fixes.

``` r
set.seed(1)
bag.fit <-randomForest(medv ~ ., data = Boston,  subset = train, mtry = 12, importance = TRUE)
bag.fit
```

    ## 
    ## Call:
    ##  randomForest(formula = medv ~ ., data = Boston, mtry = 12, importance = TRUE,      subset = train) 
    ##                Type of random forest: regression
    ##                      Number of trees: 500
    ## No. of variables tried at each split: 12
    ## 
    ##           Mean of squared residuals: 11.40162
    ##                     % Var explained: 85.17

\#bagging test set

``` r
yhat.bag <-predict(bag.fit, newdata = Boston[-train, ])
boston.test <- Boston[-train, "medv"]
plot(yhat.bag, boston.test)
abline(0, 1)
```

![](bart_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
print("test set MSE associated with the bagged regression tree=")
```

    ## [1] "test set MSE associated with the bagged regression tree="

``` r
mean((yhat.bag- boston.test)^2)
```

    ## [1] 23.41916

# сравнение с random forests

``` r
 rf.fit <-randomForest(medv~., data = Boston, subset = train, ntree = 25)
 yhat.bag <-predict(rf.fit, newdata = Boston[-train, ])
 mean((yhat.bag- boston.test)^2)
```

    ## [1] 19.76028

вывод: с этими данными лучше справляется bart bart test set
mse=$15.97434$ bagging test set mse=$23.41916$ random forests test set
mse= $19.76028$
