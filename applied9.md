Applied#9
================

\#This problem involves the OJ data set which is part of the ISLR
package.

``` r
library(ISLR)
library(tree)
attach(OJ)
dim(OJ)
```

    ## [1] 1070   18

\#1.Create a training set containing a random sample of 800
observations, and a test set containing the remaining observations.

``` r
set.seed(2)
train.set=sample(1:nrow(OJ), 800)
OJ.test=OJ[-train.set,]
dim(OJ)
```

    ## [1] 1070   18

``` r
length(train.set)
```

    ## [1] 800

``` r
dim(OJ.test)
```

    ## [1] 270  18

\#2.Fit a tree to the training data, with Purchase as the response and
the other variables as predictors. Use the summary() function to produce
summary statistics about the tree, and describe the results obtained.
What is the training error rate? How many terminal nodes does the tree
have?

``` r
tree.fit=tree(Purchase~., data=OJ, subset=train.set)
summary(tree.fit)
```

    ## 
    ## Classification tree:
    ## tree(formula = Purchase ~ ., data = OJ, subset = train.set)
    ## Variables actually used in tree construction:
    ## [1] "LoyalCH"   "PriceDiff"
    ## Number of terminal nodes:  9 
    ## Residual mean deviance:  0.7009 = 554.4 / 791 
    ## Misclassification error rate: 0.1588 = 127 / 800

``` r
plot(tree.fit)
text(tree.fit, pretty=0)
```

![](applied9_files/figure-gfm/unnamed-chunk-3-1.png)<!-- --> training
error rate=Residual mean deviance: 0.7463 = 591.8 / 793 7 terminal nodes
\#3.Type in the name of the tree object in order to get a detailed text
output. Pick one of the terminal nodes, and interpret the information
displayed.

``` r
tree.fit
```

    ## node), split, n, deviance, yval, (yprob)
    ##       * denotes terminal node
    ## 
    ##  1) root 800 1068.00 CH ( 0.61250 0.38750 )  
    ##    2) LoyalCH < 0.5036 359  422.80 MM ( 0.27577 0.72423 )  
    ##      4) LoyalCH < 0.280875 172  127.60 MM ( 0.12209 0.87791 )  
    ##        8) LoyalCH < 0.035047 56   10.03 MM ( 0.01786 0.98214 ) *
    ##        9) LoyalCH > 0.035047 116  106.60 MM ( 0.17241 0.82759 ) *
    ##      5) LoyalCH > 0.280875 187  254.10 MM ( 0.41711 0.58289 )  
    ##       10) PriceDiff < 0.05 73   71.36 MM ( 0.19178 0.80822 ) *
    ##       11) PriceDiff > 0.05 114  156.30 CH ( 0.56140 0.43860 ) *
    ##    3) LoyalCH > 0.5036 441  311.80 CH ( 0.88662 0.11338 )  
    ##      6) LoyalCH < 0.737888 168  191.10 CH ( 0.74405 0.25595 )  
    ##       12) PriceDiff < 0.265 93  125.00 CH ( 0.60215 0.39785 )  
    ##         24) PriceDiff < -0.35 12   10.81 MM ( 0.16667 0.83333 ) *
    ##         25) PriceDiff > -0.35 81  103.10 CH ( 0.66667 0.33333 ) *
    ##       13) PriceDiff > 0.265 75   41.82 CH ( 0.92000 0.08000 ) *
    ##      7) LoyalCH > 0.737888 273   65.11 CH ( 0.97436 0.02564 )  
    ##       14) PriceDiff < -0.39 11   12.89 CH ( 0.72727 0.27273 ) *
    ##       15) PriceDiff > -0.39 262   41.40 CH ( 0.98473 0.01527 ) *

\#5 Predict the response on the test data, and produce a confusion
matrix comparing the test labels to the predicted test labels. What is
the test error rate?

``` r
yhat.tree = predict(tree.fit,newdata=OJ.test, type="class")
pur.test=OJ[-train.set,"Purchase"]
length(yhat.tree)
```

    ## [1] 270

``` r
length(pur.test)
```

    ## [1] 270

``` r
table(yhat.tree,pur.test)
```

    ##          pur.test
    ## yhat.tree  CH  MM
    ##        CH 148  37
    ##        MM  15  70

Интерпретация confusion matrix: (событие А= Purchase CH; CH=Event,MM=No
Event) test Error
Rate=$(FP+FN)/(TP+TN+FP+FN)$=(69+43)/(114+69+43+44)=0.4148148 TP
Rate=$TP/(TP+FN)$=114/(114+43)=0.7261146 FP
Rate=$FP/(FP+TN)$=69/(69+44)=0.6106195
Sensitivity=$TP/(TP+FN)$=114/(114+43)=0.7261146
Specificity=$TN/(FP+TN)$=44/(44+69)=0.3893805

*6* Apply the cv.tree() function to the training set in order to
determine the optimal tree size. ответ: 9- optimal tree size (g) Produce
a plot with tree size on the x-axis and cross-validated classification
error rate on the y-axis.

``` r
cv.oj=cv.tree(tree.fit)
plot(cv.oj$size,cv.oj$dev,type='b')
```

![](applied9_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

9.  This problem involves the OJ data set which is part of the ISLR
    package.

<!-- -->

1)  Create a training set containing a random sample of 800 obser
    vations, and a test set containing the remaining observations.

2)  Fit a tree to the training data, with Purchase as the response and
    the other variables as predictors. Use the summary() function to
    produce summary statistics about the tree, and describe the results
    obtained. What is the training error rate? How many terminal nodes
    does the tree have?

3)  Type in the name of the tree object in order to get a detailed text
    output. Pick one of the terminal nodes, and interpret the
    information displayed.

4)  Create a plot of the tree, and interpret the results.

5)  Predict the response on the test data, and produce a confusion
    matrix comparing the test labels to the predicted test labels. What
    is the test error rate?

6)  Apply the cv.tree() function to the training set in order to
    determine the optimal tree size.

7)  Which tree size corresponds to the lowest cross-validated
    classification error rate? ответ: prunning wont improve
    results(residual deviance=cv error rate won’t decrease)

``` r
prune.oj=prune.tree(tree.fit,best=5)
plot(prune.oj)
text(prune.oj,pretty=0)
```

![](applied9_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
summary(prune.oj)
```

    ## 
    ## Classification tree:
    ## snip.tree(tree = tree.fit, nodes = c(7L, 4L, 6L))
    ## Variables actually used in tree construction:
    ## [1] "LoyalCH"   "PriceDiff"
    ## Number of terminal nodes:  5 
    ## Residual mean deviance:  0.7692 = 611.5 / 795 
    ## Misclassification error rate: 0.1688 = 135 / 800

1)  Produce a pruned tree corresponding to the optimal tree size
    obtained using cross-validation. If cross-validation does not lead
    to selection of a pruned tree, then create a pruned tree with five
    terminal nodes.
