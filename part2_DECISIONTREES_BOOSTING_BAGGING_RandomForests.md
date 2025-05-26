part 2: DECISION TREES+BOOSTING+BAGGING+Random Forests
================

# Random forests- Леса деревьев принятия решений

Rfs decorrelate trees т.к. when splitting at each node algo cannot use
*majority rule* that leads to trees voting on strongest predicotrs and
thus trees look alike= are correlated (1) Build a number of decison
trees on bootstrapped training dataset; but as building trees each time
considering splitting a tree **random sample of m predictors** is chosen
as a split candidate from a full set of predictors (2) Fresh sample of m
predictors is taken at each splt ($m=\sqrt p$)

\#Lab bagging and Random Forests **bagging = case of a random forest
with m=p**

``` r
library(ISLR)
library(randomForest)
```

    ## randomForest 4.7-1.2

    ## Type rfNews() to see new features/changes/bug fixes.

``` r
library(MASS)
train.set = sample(1:nrow(Boston), nrow(Boston)/2)
boston.test=Boston[-train.set,"medv"]
set.seed(1)
boston.bag<-randomForest(medv~., data=Boston, subset= train.set, mtry=13, importance=TRUE)
boston.bag
```

    ## 
    ## Call:
    ##  randomForest(formula = medv ~ ., data = Boston, mtry = 13, importance = TRUE,      subset = train.set) 
    ##                Type of random forest: regression
    ##                      Number of trees: 500
    ## No. of variables tried at each split: 13
    ## 
    ##           Mean of squared residuals: 14.0808
    ##                     % Var explained: 83.56

*mtry=13* indicates that *all* 13 predictors should be considered for
each split of the tree —in other words, that bagging should be done.

``` r
# on test set 
yhat.bag = predict(boston.bag,newdata=Boston[-train.set,])
plot(yhat.bag, boston.test)
abline(0,1)
```

![](part2_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

``` r
mean((yhat.bag-boston.test)^2)
```

    ## [1] 16.53016

``` r
boston.bag2=randomForest(medv~.,data=Boston,subset=train.set,mtry=13,ntree=25)
yhat.bag<-predict(boston.bag2,newdata=Boston[-train.set,])
mean((yhat.bag-boston.test)^2)
```

    ## [1] 17.0269

\#Random Forests

``` r
set.seed(1)
boston.rf=randomForest(medv~.,data=Boston,subset=train.set,mtry=6,importance=TRUE)
yhat.rf = predict(boston.rf,newdata=Boston[-train.set,])
mean((yhat.rf-boston.test)^2)
```

    ## [1] 16.34185

importance() function, we can view the importance of each importance()
variable.

``` r
importance(boston.rf)
```

    ##           %IncMSE IncNodePurity
    ## crim    16.911266    1592.97945
    ## zn       4.565250      69.21001
    ## indus    7.375220     609.91945
    ## chas     1.114229      27.22581
    ## nox     19.491334    1575.08925
    ## rm      32.956793    7263.45245
    ## age     12.226483     627.91865
    ## dis     11.132227     849.07202
    ## rad      6.109637     138.36109
    ## tax      8.396761     329.06358
    ## ptratio 12.213320     963.76110
    ## black    6.395961     276.89068
    ## lstat   30.596560    6969.93569

*Two measures of variable importance are reported. *%IncMSE\* = mean
decrease of accuracy in predictions on the out of bag samples when a
given variable is excluded from the model. *IncNodePurity* is a measure
of the total decrease in node impurity that results from splits over
that variable, averaged over all trees In the case of regression trees,
the node impurity is measured by the training RSS, and for
classification trees by the deviance.

``` r
varImpPlot(boston.rf)
```

![](part2_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->
The results indicate that across all of the trees considered in the
random forest, the wealth level of the community (lstat) and the house
size (rm) are by far the two most important variables.

\##BOOSTING doesn’t involve bootstrap, each tree is a modified version
of original dataset boosting learns slowly (1) given current model we
fit a decision tree to *residuals* as a response( not to Y response) (2)
add new decision tree into fiited function to update residuals *Boosting
parameters* 1. $B$ - number of trees (determined with CV) 2. $\lambda$-
shrinkage parameter= rate at which boosting learns 3. $d$ - number of
splits (d=1-\> stump(=weak learner)) *Boosting for regression trees* (1)
set $\hat f(x)=0$ and $r~j=y~i$ for all training set (2) for b=1,2…B
repeat: a. fit a tree $\hat f^b$ with d splits (d+1 terminal nodes) b.
update $\hat f$ by adding a shrunken version of a new tree
$\hat f(x) <- \hat f(x) + \lambda*\hat f^b(x)$ c. update residuals
$r~j<-r~i<- \lambda* \hat f^b(x~i)$ (3) output boosted model
$\hat f(x)= \sum \lambda \hat f^b(x)$ \##Boosting

``` r
library(gbm)
```

    ## Loaded gbm 2.2.2

    ## This version of gbm is no longer under development. Consider transitioning to gbm3, https://github.com/gbm-developers/gbm3

``` r
set.seed(1)
boston.boost<-gbm(medv~., data=Boston[train.set,], distribution="gaussian", n.trees=5000, interaction.depth=4)
summary(boston.boost)
```

![](part2_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

    ##             var     rel.inf
    ## lstat     lstat 37.96276780
    ## rm           rm 29.57362353
    ## dis         dis  6.71856938
    ## crim       crim  6.13611101
    ## nox         nox  4.72015642
    ## age         age  4.65225844
    ## ptratio ptratio  3.02031563
    ## black     black  2.95314795
    ## indus     indus  1.49233087
    ## rad         rad  1.21288633
    ## tax         tax  1.04667454
    ## zn           zn  0.49033260
    ## chas       chas  0.02082552

gbm() function, to fit boosted gbm() regression trees to the Boston data
set. We run gbm() with the option distribution=“gaussian” since this is
a regression problem; if it were a binary classification problem, we
would use distribution=“bernoulli”. n.trees=5000 indicates that we want
5000 trees, and the option interaction.depth=4 limits the depth of each
tree.

``` r
 # par(mfrow=c(2,2))
 plot(boston.boost,i="rm")
```

![](part2_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

``` r
 plot(boston.boost,i="lstat")
```

![](part2_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-8-2.png)<!-- -->
lstat and rm are the most important variables. to produce partial
dependence plots for these two variables. illustrate the marginal effect
of the selected variables on the response after integrating out the
other variables. In this case,median house prices are increasing with rm
and decreasing with lstat \#use the boosted model to predict medv on the
test set

``` r
yhat.boost=predict(boston.boost,newdata=Boston[-train.set,],n.trees=5000)
mean((yhat.boost-boston.test)^2)
```

    ## [1] 16.73323

we can perform boosting with a different value of the shrinkage
parameter λ.The default value is 0.001,but this is easily modified.Here
we take λ=0.2.

``` r
boston.boost2=gbm(medv~., data=Boston[train.set,], distribution="gaussian", n.trees=5000, interaction.depth=4,shrinkage=0.2, verbose=F)
yhat.boost=predict(boston.boost,newdata=Boston[-train.set,],n.trees=5000)
mean((yhat.boost-boston.test)^2)
```

    ## [1] 16.73323
