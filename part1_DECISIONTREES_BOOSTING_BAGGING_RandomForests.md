part 1: DECISION TREES+BOOSTING+BAGGING+Random Forests
================

# Терминология

terminal node leaf Tree with 2 leaves= stump **Recurcive binary
splitting**- top-down greedy approach doesnt account for future possible
best splits, best split at each step For any j and s define pair of
half-planes $R~1(j,s)={X|X~j<S}$ $R~2(j,s)={X|X~j>S}$ and seek a and j
to minimize $\sum(y~i-\hat y~r1)^2$+$\sum(y~i-\hat y~r2)^2$ where
$\hat y~r1$- mean response for training observations in R1(j,s)
$\hat y~r2$- mean response for training observations in R2(j,s)

# DECISION TREES Основные идеи

Tree-based methods(Методы основанные на деревьях решений) сегментируют
признаковое пространство(predictor space) и make predictions основанные
на mean of training observations Для quant output- *Regression Trees*
prediction= mean response of training observations that belong to same
terminal node Для qualitative(categorical) output- *Classification
Trees*

# Regression Trees 1. Разделить predictor space(признаковое пространство)

на distinct and non-overlapping regions 2. For every observation that
falls into region make same prediction= mean of response values for
training observations in region “Boxes”(created by decision boundaries)
that minimize $\sum\sum(y~i-\hat y~rj)^2$

# Tree pruning

Fewer splits-\> less risk of overfitting(less variance and better
interpretation at the cost of introducing a little bias) \# *Cost
Complexity pruning(weakest link pruning)*- consider a sequence of trees
indexed by a non-negative tunning parameter \# Building a regression
Tree (1) *recursive binary splitting* on training data(stop only when
each terminal node has reached some number of observations) (2) *cost
complexity pruning* to huge tree to obtain a sequence of best subtrees
as function of $\alpha$- tuning parameter (3) K-fold Cross Validation to
choose $\alpha$ that is divide training observations into K folds and
for each k=1…K a.repeat steps 1 and 2 on all but Kth fold of training
data b.evaluate *mean squared prediction error* on data in left-out Kth
fold as a function of $\alpha$ Average results for each value of
$\alpha$ to min average error (4) rerun subtree from step 2 that
corresponds to chosen value of $\alpha$

(similar to lasso regression) $\sum\sum(y~i-\hat y~rm)^2+\alpha*|T|$ T-
subtree, $T~0$- huge tree $\hat y~rm$- predicted response associated
with Rm, i.e. mean of training observations in Rm $\alpha$- tuning
parameter that controls tree’s complexity and fit to training data

\#Classification Trees Qualitative(categorical) response(Y) predicts
that each observation belongs to most commonly occurring class of
training observations in region to which it belongs *majority vote*
\#*Criterion for Classification trees Pruning* Instead of RSS-\>
*classification error rate* $E=1-max(\hat P~mk)$ $(\hat P~mk)$-
proportion of training observations in Mth region that are from Kth
class *2 Criteria for Building a Classification tree*- *1*.Gini
(impurity) index $G=\sum\hat P~mk(1-\hat P~mk)$ чем меньше G тем более
чистые(pure) i.e node contains predominantly observations from 1 class
and

*2*.Entropy(энтропия- мера неоднороднсоти данных(множества)) Энтропия
Шеннона $S=-\sum P~i*log~2 P~i$ где $P~i=N~i/N$- отношение количесвта
элементов принадлежащих определенному классу к общему числу элементов
(цель обучения классификатора-уменьшить энтропию то есть неоднородность
наблюдений внутри одного класса, но если энтропия=0- переобучение)

Энтропия для отбора разделяющей переменной (splitting terminal node)
*Information Gain(информационный выигрыш)*
$IG= S~0+ N1/N*S~1+ N~2/N*S~2$ показывает количество информации, которое
содержится в делении множества на 2 данных поднабора(S1- энтропия
поднабора 1, N1- количество его элементов) Алгоритм заканчивает работу
когда IG перестает увеличиваться

\#Trees VS Linear Models Regression models:
$f(X)=\beta~0+\sum\beta~1*X~j$ (linear relationships) Regression Trees^
$f(X)=\sum C~m*1~(x принадлежит Rm)$ (non-linear relationships) Compare
with $\hat(Test error)$ using Cross Validation trees’ disadvanatges:
non-robust (small changes in data-\> large change in estimations)

\#Bagging= Bootstrap+Aggregation reduces variance of a statistical
learnig method Given set of predictors $Z1,..Zn$ with variance
$\sigma^2$ each if we average that decreases variance (average of mean =
$\sigma^2/n$) Bagging step-by-step (1) bootstrap by *taking repeated
samples from one trainig dataset* generate B different bootstrapped
trainig datasets (2) train method on b-th bootstrapped dataset to get
$\hat f^*$ and (3) average all the predictions to obtain
$\hat fbag(x)= 1/B* \sum \hat f^*(x)$

*Bagging for regression trees* (1) construct B regression trees using B
bootstrapped trainig sets (2) average resulting predictions (do not
prune these trees- each one of them has hign variance and low bias and
by averaging their predictions we reduce the variance) *Bagging for
classification trees* For a given test observation record class
predicted by each of B trees take a *majority vote* =overall predicition
is the most commonly ocurring among B predcitors \#OOB Estiamtion
Out-Of-Bag- ~1/3 of observations are not used in a bagged tree To
estimate *Test Error Rate* predict reponses for observations in trees
where it was OOB (regression trees- OOB MSEby *averaging predicted
responses*) (classification trees- OOB classification error y *majotity
vote*) \#Variable Importance Measures Summary of Importance of each
predictor- RSS (bagging regression trees) or Gini Index (bagging
classification trees)

\#Random Forests

\#Boosting

## Алгоритмы AdaBoost,CatBoost, XGBoost

\#lab

``` r
library(tree)
library(ISLR)
attach(Carseats)
High=ifelse(Sales<=8,"No","Yes")
Carseats<-data.frame(Carseats,High)
# fix(Carseats)
```

classification trees to analyze the Carseats data set. Sales is a
*continuous variable*, and so we begin by recoding it as a binary
variable. ifelse() function to create a variable, called ifelse() High,
which takes on a value of Yes if the Sales variable exceeds 8, and takes
on a value of No otherwise. data.frame() function to merge High with the
rest of the Carseats data.

``` r
tree1<-tree(High~.- Sales, Carseats)
```

    ## Warning in tree(High ~ . - Sales, Carseats): в результате преобразования
    ## созданы NA

``` r
# summary(tree.fit)
```

tree() function to fit a classification tree in order to predict High
using all variables but Sales. \#Fitting Regression trees

``` r
library(MASS)
set.seed(1)
train.set = sample(1:nrow(Boston), nrow(Boston)/2)
tree.boston=tree(medv~.,Boston,subset=train.set)
summary(tree.boston)
```

    ## 
    ## Regression tree:
    ## tree(formula = medv ~ ., data = Boston, subset = train.set)
    ## Variables actually used in tree construction:
    ## [1] "rm"    "lstat" "crim"  "age"  
    ## Number of terminal nodes:  7 
    ## Residual mean deviance:  10.38 = 2555 / 246 
    ## Distribution of residuals:
    ##     Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    ## -10.1800  -1.7770  -0.1775   0.0000   1.9230  16.5800

``` r
plot(tree.boston)
text(tree.boston,pretty=0)
```

![](part1_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

use the cv.tree() function to see whether pruning the tree will improve
performance.

``` r
cv.boston=cv.tree(tree.boston)
plot(cv.boston$size,cv.boston$dev,type='b')
```

![](part1_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

if we wish to prune the tree, we could do so as follows, using the
prune.tree() function:

``` r
prune.boston=prune.tree(tree.boston,best=5)
plot(prune.boston)
text(prune.boston,pretty=0)
```

![](part1_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

In keeping with the cross-validation results, we use the unpruned tree
to make predictions on the test set.

``` r
yhat=predict(tree.boston,newdata=Boston[-train.set,])
boston.test=Boston[-train.set,"medv"]
plot(yhat,boston.test)
abline(0,1)
```

![](part1_DECISIONTREES_BOOSTING_BAGGING_RandomForests_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
mean((yhat-boston.test)^2)
```

    ## [1] 35.28688

the test set MSE associated with the regression tree is 25.05. The
square root of the MSE is therefore around 5.005,
