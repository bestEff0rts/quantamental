Applied#8
================

\##задача a classification tree was applied to the Carseats data set
after converting Sales into a qualitative response variable. Now we will
seek to *predict Sales using regression trees* and related
approaches,treating the response as a *quantitative variable.*

``` r
library(ISLR)
library(MASS)
library(tree)
attach(Carseats)
```

\#1 Split the data set into a training set and a test set

``` r
train.set = sample(1:nrow(Carseats), nrow(Carseats)/2)
test.set=! train.set
```

\#2.Fit a regression tree to the training set. Plot the tree, and
interpret the results. What test MSE do you obtain?

``` r
reg.tree=tree(Sales~., data=Carseats, subset=train.set)
summary(reg.tree)
```

    ## 
    ## Regression tree:
    ## tree(formula = Sales ~ ., data = Carseats, subset = train.set)
    ## Variables actually used in tree construction:
    ## [1] "ShelveLoc"   "Price"       "Age"         "CompPrice"   "Advertising"
    ## [6] "Income"     
    ## Number of terminal nodes:  15 
    ## Residual mean deviance:  2.401 = 444.2 / 185 
    ## Distribution of residuals:
    ##     Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    ## -4.73700 -1.03100 -0.08467  0.00000  1.03200  3.60900

``` r
plot(reg.tree)
text(reg.tree,pretty=0)
```

![](applied8_files/figure-gfm/unnamed-chunk-3-1.png)<!-- --> deviance is
simply the sum of squared errors for the tree \#Use cross-validation in
order to determine the optimal level of tree complexity. Does pruning
the tree improve the test MSE?

``` r
cv=cv.tree(reg.tree)
plot(cv$size,cv$dev,type='b')
```

![](applied8_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->
dev-corresponding to size error rate

``` r
prune=prune.tree(reg.tree,best=5)
plot(prune)
text(prune,pretty=0)
```

![](applied8_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

``` r
summary(prune)
```

    ## 
    ## Regression tree:
    ## snip.tree(tree = reg.tree, nodes = c(6L, 9L, 8L, 7L, 5L))
    ## Variables actually used in tree construction:
    ## [1] "ShelveLoc" "Price"     "Age"      
    ## Number of terminal nodes:  5 
    ## Residual mean deviance:  4.149 = 809 / 195 
    ## Distribution of residuals:
    ##     Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    ## -5.80400 -1.36100 -0.08923  0.00000  1.52200  4.51600

significant decrease in test mse after pruning -Residual mean deviance:
4.41 = 860 / 195 \#Use the bagging approach in order to analyze this
data. What test MSE do you obtain? Use the importance() function to
determine which variables are most important. **bagging = case of a
random forest with m=p**

``` r
library(randomForest)
```

    ## randomForest 4.7-1.2

    ## Type rfNews() to see new features/changes/bug fixes.

``` r
bag=randomForest(Sales~.,data=Carseats, subset=train.set, mtry=13, importance=TRUE)
```

    ## Warning in randomForest.default(m, y, ...): invalid mtry: reset to within valid
    ## range

``` r
bag
```

    ## 
    ## Call:
    ##  randomForest(formula = Sales ~ ., data = Carseats, mtry = 13,      importance = TRUE, subset = train.set) 
    ##                Type of random forest: regression
    ##                      Number of trees: 500
    ## No. of variables tried at each split: 10
    ## 
    ##           Mean of squared residuals: 2.922107
    ##                     % Var explained: 63.09

*mtry=13* indicates that *all* 13 predictors should be considered for
each split of the tree —in other words, that bagging should be done.

``` r
importance(bag)
```

    ##                %IncMSE IncNodePurity
    ## CompPrice   19.2215577    140.754156
    ## Income       5.4749105     87.529096
    ## Advertising 13.8947628     87.083168
    ## Population   1.7238363     62.303117
    ## Price       49.6290026    454.146331
    ## ShelveLoc   55.2246932    457.114686
    ## Age         25.2797308    190.436071
    ## Education   -0.5023275     46.373919
    ## Urban       -0.7009199      7.466987
    ## US           3.4255029      9.435273

\#Use random forests to analyze this data. What test MSE do you obtain?
Use the importance() function to determine which vari ables are most
important. Describe the effect of m,thenumberof variables considered at
each split, on the error rate obtained.

``` r
sales.rf=randomForest(Sales~., data=Carseats, subset=train.set, mtry=6, importance=TRUE)
yhat.rf = predict(sales.rf,newdata=Carseats[-train.set,])
Carseats.test=Carseats[-train.set,"Sales"]
# fix(Carseats)
mean((yhat.rf-Carseats.test)^2)
```

    ## [1] 2.754759

that’s the test MSE

``` r
importance(sales.rf)
```

    ##                %IncMSE IncNodePurity
    ## CompPrice   14.9018431    139.092289
    ## Income       5.1744904     97.083812
    ## Advertising 13.1004020    100.925237
    ## Population   0.5970015     77.242189
    ## Price       46.1593602    422.697899
    ## ShelveLoc   50.8032926    424.063919
    ## Age         22.4953982    191.192119
    ## Education    2.5532359     54.174107
    ## Urban       -0.1482582      7.844396
    ## US           2.6742247     13.606699
