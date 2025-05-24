Subset Selection(Best Subset Selection, Forward/Backward Stepwise
Selection); Choosing optimal model(test error rate)- Adjusting training
error(Cp,AIC,BIC,adjusted R^2) and DIRECTLY estimating test error-
Validation and CV
================

## Best Subset Selection

Пример как прогнозировать зарплату бейсболиста на основе различных
статистических данных- с показателями за предыдущий год.
sum(is.na(Hitters\$Salary))- сколько salary пропущенно

``` r
library(ISLR)
fix(Hitters)
names(Hitters)
```

    ##  [1] "AtBat"     "Hits"      "HmRun"     "Runs"      "RBI"       "Walks"    
    ##  [7] "Years"     "CAtBat"    "CHits"     "CHmRun"    "CRuns"     "CRBI"     
    ## [13] "CWalks"    "League"    "Division"  "PutOuts"   "Assists"   "Errors"   
    ## [19] "Salary"    "NewLeague"

``` r
dim(Hitters)
```

    ## [1] 322  20

``` r
sum(is.na(Hitters$Salary))
```

    ## [1] 59

Функция na.omit() удаляет все строки, в которых отсутствуют значения
любой переменной.

``` r
Hitters<- na.omit(Hitters)
dim(Hitters)
```

    ## [1] 263  20

``` r
sum(is.na(Hitters))
```

    ## [1] 0

\#Best subset selection 1\[Идентифицирует subset of P предикторов,
которые мы полагаем влияют на response\]–\> 2\[Обучает модель с помощью
МНК=Least Squares на reduced set of variables\] “)

Функция regsubsets() (из библиотеки leaps) выполняет best subset
selection sub-regsubsets() устанавливает выбор, определяя лучшую модель,
которая содержит заданное число из предсказателей, где лучше всего
количественно с помощью RSS.

``` r
library(leaps)
bsubssel.fit<-regsubsets(Salary~.,Hitters)
summary(bsubssel.fit)
```

    ## Subset selection object
    ## Call: regsubsets.formula(Salary ~ ., Hitters)
    ## 19 Variables  (and intercept)
    ##            Forced in Forced out
    ## AtBat          FALSE      FALSE
    ## Hits           FALSE      FALSE
    ## HmRun          FALSE      FALSE
    ## Runs           FALSE      FALSE
    ## RBI            FALSE      FALSE
    ## Walks          FALSE      FALSE
    ## Years          FALSE      FALSE
    ## CAtBat         FALSE      FALSE
    ## CHits          FALSE      FALSE
    ## CHmRun         FALSE      FALSE
    ## CRuns          FALSE      FALSE
    ## CRBI           FALSE      FALSE
    ## CWalks         FALSE      FALSE
    ## LeagueN        FALSE      FALSE
    ## DivisionW      FALSE      FALSE
    ## PutOuts        FALSE      FALSE
    ## Assists        FALSE      FALSE
    ## Errors         FALSE      FALSE
    ## NewLeagueN     FALSE      FALSE
    ## 1 subsets of each size up to 8
    ## Selection Algorithm: exhaustive
    ##          AtBat Hits HmRun Runs RBI Walks Years CAtBat CHits CHmRun CRuns CRBI
    ## 1  ( 1 ) " "   " "  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 2  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 3  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 4  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 5  ( 1 ) "*"   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 6  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    " "   "*" 
    ## 7  ( 1 ) " "   "*"  " "   " "  " " "*"   " "   "*"    "*"   "*"    " "   " " 
    ## 8  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   " "    " "   "*"    "*"   " " 
    ##          CWalks LeagueN DivisionW PutOuts Assists Errors NewLeagueN
    ## 1  ( 1 ) " "    " "     " "       " "     " "     " "    " "       
    ## 2  ( 1 ) " "    " "     " "       " "     " "     " "    " "       
    ## 3  ( 1 ) " "    " "     " "       "*"     " "     " "    " "       
    ## 4  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 5  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 6  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 7  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 8  ( 1 ) "*"    " "     "*"       "*"     " "     " "    " "

## Интерпретация

Звездочка указывает на то, что данная переменная включена в
соответствующую модель. Например, этот вывод показывает, что лучшая
двухпеременная модель содержит только Hits и CRBI. По умолчанию,
regsubsets() сообщает только результаты до лучшей восьми-переменной
модели. Но nvmax может быть использована, чтобы вернуть так много
переменных, как указано.Например:

``` r
bsubssel.fit<-regsubsets(Salary~.,data=Hitters, nvmax=19)
bss.summary<-summary(bsubssel.fit)
```

Names(summary) показывает AIC(Cp), BIC, RSS, $R^2$,
$R^2 adjusted=1-/(1-R^2)(n-1)/(n-k-1))$ (используется при более чем
одном предикторе, добавляя penalty за усложнение модели)

``` r
names(bss.summary)
```

    ## [1] "which"  "rsq"    "rss"    "adjr2"  "cp"     "bic"    "outmat" "obj"

``` r
bss.summary$rsq
```

    ##  [1] 0.3214501 0.4252237 0.4514294 0.4754067 0.4908036 0.5087146 0.5141227
    ##  [8] 0.5285569 0.5346124 0.5404950 0.5426153 0.5436302 0.5444570 0.5452164
    ## [15] 0.5454692 0.5457656 0.5459518 0.5460945 0.5461159

``` r
which.max(bss.summary$adjr2)
```

    ## [1] 11

``` r
# points(11, bss.summary$adjr2[11], col="red", cex=2, pch=20)
which.min(bss.summary$cp)
```

    ## [1] 10

``` r
# points(10,bss.summary$cp[10],col="red",cex=2,pch=20)
which.min(bss.summary$bic)
```

    ## [1] 6

``` r
# plot(bss.summary$bic,xlab="Number of Variables",ylab="BIC")
# points(6,bss.summary$bic[6],col="red",cex=2,pch=20)
```

## plot(bsubssel.fit, scale=““)

Команда points() работает так же, как команда plot(), но добавляет точки
на уже созданный график.

Функция regsubsets() имеет встроенную команду plot(), которая может
будет использоваться для отображения выбранных переменных для лучшей
модели с заданным числом предикторов (в примере nvmax=19), ранжированных
по BIC,Cp, adjusted $R^2$, или AIC.

``` r
plot(bsubssel.fit,scale="r2")
```

![](draft_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

``` r
plot(bsubssel.fit,scale="adjr2")
```

![](draft_files/figure-gfm/unnamed-chunk-6-2.png)<!-- -->

``` r
plot(bsubssel.fit,scale="Cp")
```

![](draft_files/figure-gfm/unnamed-chunk-6-3.png)<!-- -->

``` r
plot(bsubssel.fit,scale="bic")
```

![](draft_files/figure-gfm/unnamed-chunk-6-4.png)<!-- -->

``` r
?plot.regsubsets.
```

    ## В указанных пакетах и библиотеках нет документации для 'plot.regsubsets.':
    ## можете попробовать '??plot.regsubsets.'

## Интерпретация

Верхняя строка каждого графика содержит черный квадрат для каждой
выбранной переменной в соответствии с оптимальной моделью, связанной с
этой статистикой. Так,мы видим, что несколько моделей имеют BIC около
150

``` r
coef(bsubssel.fit,6)
```

    ##  (Intercept)        AtBat         Hits        Walks         CRBI    DivisionW 
    ##   91.5117981   -1.8685892    7.6043976    3.6976468    0.6430169 -122.9515338 
    ##      PutOuts 
    ##    0.2643076

``` r
bsubssel.fit6<-regsubsets(Salary~.,data=Hitters, nvmax=6)
summary(bsubssel.fit6)
```

    ## Subset selection object
    ## Call: regsubsets.formula(Salary ~ ., data = Hitters, nvmax = 6)
    ## 19 Variables  (and intercept)
    ##            Forced in Forced out
    ## AtBat          FALSE      FALSE
    ## Hits           FALSE      FALSE
    ## HmRun          FALSE      FALSE
    ## Runs           FALSE      FALSE
    ## RBI            FALSE      FALSE
    ## Walks          FALSE      FALSE
    ## Years          FALSE      FALSE
    ## CAtBat         FALSE      FALSE
    ## CHits          FALSE      FALSE
    ## CHmRun         FALSE      FALSE
    ## CRuns          FALSE      FALSE
    ## CRBI           FALSE      FALSE
    ## CWalks         FALSE      FALSE
    ## LeagueN        FALSE      FALSE
    ## DivisionW      FALSE      FALSE
    ## PutOuts        FALSE      FALSE
    ## Assists        FALSE      FALSE
    ## Errors         FALSE      FALSE
    ## NewLeagueN     FALSE      FALSE
    ## 1 subsets of each size up to 6
    ## Selection Algorithm: exhaustive
    ##          AtBat Hits HmRun Runs RBI Walks Years CAtBat CHits CHmRun CRuns CRBI
    ## 1  ( 1 ) " "   " "  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 2  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 3  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 4  ( 1 ) " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 5  ( 1 ) "*"   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 6  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    " "   "*" 
    ##          CWalks LeagueN DivisionW PutOuts Assists Errors NewLeagueN
    ## 1  ( 1 ) " "    " "     " "       " "     " "     " "    " "       
    ## 2  ( 1 ) " "    " "     " "       " "     " "     " "    " "       
    ## 3  ( 1 ) " "    " "     " "       "*"     " "     " "    " "       
    ## 4  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 5  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "       
    ## 6  ( 1 ) " "    " "     "*"       "*"     " "     " "    " "

Однако, модель с наименьшим BIC - это шести-переменная модель, которая
содержит только AtBat,Hits,Walks,CRBI,DivisionW,and PutOuts.

## Forward and Backward Stepwise Selection

1\[FORWARD STEPWISE SELECTION Mo- null model no predictors\]–\>

2\[For k=0..p-1 \]–\>

2.1(Consider all p-k model that augment predictors in Mk with 1
additional predictor)–\>

2.2(Choose best=lowest RSS or highest R^2 and call it Mk+1)–\>

3\[Select a 1 best model among M0,..Mp using AIC, BIC, CV prediction
error, adj R^2\]

## regsubsets()

function to perform forward stepwise or backward stepwise selection,
using the argument method=“forward”or method=“backward”

``` r
fwd.reg.fit<- regsubsets(Salary~., data=Hitters,nvmax=19, method="forward")
summary(fwd.reg.fit)
```

    ## Subset selection object
    ## Call: regsubsets.formula(Salary ~ ., data = Hitters, nvmax = 19, method = "forward")
    ## 19 Variables  (and intercept)
    ##            Forced in Forced out
    ## AtBat          FALSE      FALSE
    ## Hits           FALSE      FALSE
    ## HmRun          FALSE      FALSE
    ## Runs           FALSE      FALSE
    ## RBI            FALSE      FALSE
    ## Walks          FALSE      FALSE
    ## Years          FALSE      FALSE
    ## CAtBat         FALSE      FALSE
    ## CHits          FALSE      FALSE
    ## CHmRun         FALSE      FALSE
    ## CRuns          FALSE      FALSE
    ## CRBI           FALSE      FALSE
    ## CWalks         FALSE      FALSE
    ## LeagueN        FALSE      FALSE
    ## DivisionW      FALSE      FALSE
    ## PutOuts        FALSE      FALSE
    ## Assists        FALSE      FALSE
    ## Errors         FALSE      FALSE
    ## NewLeagueN     FALSE      FALSE
    ## 1 subsets of each size up to 19
    ## Selection Algorithm: forward
    ##           AtBat Hits HmRun Runs RBI Walks Years CAtBat CHits CHmRun CRuns CRBI
    ## 1  ( 1 )  " "   " "  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 2  ( 1 )  " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 3  ( 1 )  " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 4  ( 1 )  " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 5  ( 1 )  "*"   "*"  " "   " "  " " " "   " "   " "    " "   " "    " "   "*" 
    ## 6  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    " "   "*" 
    ## 7  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    " "   "*" 
    ## 8  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    "*"   "*" 
    ## 9  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 10  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 11  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 12  ( 1 ) "*"   "*"  " "   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 13  ( 1 ) "*"   "*"  " "   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 14  ( 1 ) "*"   "*"  "*"   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 15  ( 1 ) "*"   "*"  "*"   "*"  " " "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 16  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 17  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 18  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   "*"   "*"    "*"   " "    "*"   "*" 
    ## 19  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   "*"   "*"    "*"   "*"    "*"   "*" 
    ##           CWalks LeagueN DivisionW PutOuts Assists Errors NewLeagueN
    ## 1  ( 1 )  " "    " "     " "       " "     " "     " "    " "       
    ## 2  ( 1 )  " "    " "     " "       " "     " "     " "    " "       
    ## 3  ( 1 )  " "    " "     " "       "*"     " "     " "    " "       
    ## 4  ( 1 )  " "    " "     "*"       "*"     " "     " "    " "       
    ## 5  ( 1 )  " "    " "     "*"       "*"     " "     " "    " "       
    ## 6  ( 1 )  " "    " "     "*"       "*"     " "     " "    " "       
    ## 7  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 8  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 9  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 10  ( 1 ) "*"    " "     "*"       "*"     "*"     " "    " "       
    ## 11  ( 1 ) "*"    "*"     "*"       "*"     "*"     " "    " "       
    ## 12  ( 1 ) "*"    "*"     "*"       "*"     "*"     " "    " "       
    ## 13  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 14  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 15  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 16  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 17  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"       
    ## 18  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"       
    ## 19  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"

``` r
bwd.reg.fit<- regsubsets(Salary~., data=Hitters, nvmax=19, method="backward")
summary(bwd.reg.fit)
```

    ## Subset selection object
    ## Call: regsubsets.formula(Salary ~ ., data = Hitters, nvmax = 19, method = "backward")
    ## 19 Variables  (and intercept)
    ##            Forced in Forced out
    ## AtBat          FALSE      FALSE
    ## Hits           FALSE      FALSE
    ## HmRun          FALSE      FALSE
    ## Runs           FALSE      FALSE
    ## RBI            FALSE      FALSE
    ## Walks          FALSE      FALSE
    ## Years          FALSE      FALSE
    ## CAtBat         FALSE      FALSE
    ## CHits          FALSE      FALSE
    ## CHmRun         FALSE      FALSE
    ## CRuns          FALSE      FALSE
    ## CRBI           FALSE      FALSE
    ## CWalks         FALSE      FALSE
    ## LeagueN        FALSE      FALSE
    ## DivisionW      FALSE      FALSE
    ## PutOuts        FALSE      FALSE
    ## Assists        FALSE      FALSE
    ## Errors         FALSE      FALSE
    ## NewLeagueN     FALSE      FALSE
    ## 1 subsets of each size up to 19
    ## Selection Algorithm: backward
    ##           AtBat Hits HmRun Runs RBI Walks Years CAtBat CHits CHmRun CRuns CRBI
    ## 1  ( 1 )  " "   " "  " "   " "  " " " "   " "   " "    " "   " "    "*"   " " 
    ## 2  ( 1 )  " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    "*"   " " 
    ## 3  ( 1 )  " "   "*"  " "   " "  " " " "   " "   " "    " "   " "    "*"   " " 
    ## 4  ( 1 )  "*"   "*"  " "   " "  " " " "   " "   " "    " "   " "    "*"   " " 
    ## 5  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    "*"   " " 
    ## 6  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    "*"   " " 
    ## 7  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    "*"   " " 
    ## 8  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   " "    " "   " "    "*"   "*" 
    ## 9  ( 1 )  "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 10  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 11  ( 1 ) "*"   "*"  " "   " "  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 12  ( 1 ) "*"   "*"  " "   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 13  ( 1 ) "*"   "*"  " "   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 14  ( 1 ) "*"   "*"  "*"   "*"  " " "*"   " "   "*"    " "   " "    "*"   "*" 
    ## 15  ( 1 ) "*"   "*"  "*"   "*"  " " "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 16  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 17  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   " "   "*"    "*"   " "    "*"   "*" 
    ## 18  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   "*"   "*"    "*"   " "    "*"   "*" 
    ## 19  ( 1 ) "*"   "*"  "*"   "*"  "*" "*"   "*"   "*"    "*"   "*"    "*"   "*" 
    ##           CWalks LeagueN DivisionW PutOuts Assists Errors NewLeagueN
    ## 1  ( 1 )  " "    " "     " "       " "     " "     " "    " "       
    ## 2  ( 1 )  " "    " "     " "       " "     " "     " "    " "       
    ## 3  ( 1 )  " "    " "     " "       "*"     " "     " "    " "       
    ## 4  ( 1 )  " "    " "     " "       "*"     " "     " "    " "       
    ## 5  ( 1 )  " "    " "     " "       "*"     " "     " "    " "       
    ## 6  ( 1 )  " "    " "     "*"       "*"     " "     " "    " "       
    ## 7  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 8  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 9  ( 1 )  "*"    " "     "*"       "*"     " "     " "    " "       
    ## 10  ( 1 ) "*"    " "     "*"       "*"     "*"     " "    " "       
    ## 11  ( 1 ) "*"    "*"     "*"       "*"     "*"     " "    " "       
    ## 12  ( 1 ) "*"    "*"     "*"       "*"     "*"     " "    " "       
    ## 13  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 14  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 15  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 16  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    " "       
    ## 17  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"       
    ## 18  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"       
    ## 19  ( 1 ) "*"    "*"     "*"       "*"     "*"     "*"    "*"

## Интерпретация

Например, для bwd лучшая модель с 1 предиктором включает только CHmRun.
However,the best seven-variable models identified by forward stepwise
selection,backward stepwise selection,and best subset selection are
different. Коэффициенты для лучшей модели с 7 предикторами

``` r
coef(bsubssel.fit,7)
```

    ##  (Intercept)         Hits        Walks       CAtBat        CHits       CHmRun 
    ##   79.4509472    1.2833513    3.2274264   -0.3752350    1.4957073    1.4420538 
    ##    DivisionW      PutOuts 
    ## -129.9866432    0.2366813

``` r
coef(fwd.reg.fit,7)
```

    ##  (Intercept)        AtBat         Hits        Walks         CRBI       CWalks 
    ##  109.7873062   -1.9588851    7.4498772    4.9131401    0.8537622   -0.3053070 
    ##    DivisionW      PutOuts 
    ## -127.1223928    0.2533404

``` r
coef(bwd.reg.fit,7)
```

    ##  (Intercept)        AtBat         Hits        Walks        CRuns       CWalks 
    ##  105.6487488   -1.9762838    6.7574914    6.0558691    1.1293095   -0.7163346 
    ##    DivisionW      PutOuts 
    ## -116.1692169    0.3028847

\##Choosing Among Models Using the Validation Set Approach and
Cross-Validation

Создаем вектор элементы которого= true если соответствующие наблюдение
входит в train set, а ЛОЖНОЕ - в противном случае. $!$ приводит к
переключению TRUE на FALSE и vice versa

``` r
set.seed(1)
v.train=sample(c(TRUE,FALSE), nrow(Hitters), rep=TRUE)
v.test=(!v.train)
```

Теперь мы применяем regsubsets() к training set to perform best subset
selection \#expression Hitters\[train,\]. we subset the Hitters data
frame directly to access only the training subset of the data, using the
expression $Hitters[train,]$.

``` r
rgfit.best<-regsubsets(Salary~., data=Hitters[v.train,], nvmax=19)
```

now compute the validation set error for the best model of each model
size. We first make a model matrix from the test data

``` r
test.mtrx<-model.matrix(Salary~. ,data=Hitters[v.test,])
val.err<-rep(NA,19)
for (i in 19) {
  coeff=coef(rgfit.best,id=i)
  pred=test.mtrx[,names(coeff)]%*%coeff
  val.err[i]=mean((Hitters$Salary[v.test]-pred)^2)
}
val.err
```

    ##  [1]       NA       NA       NA       NA       NA       NA       NA       NA
    ##  [9]       NA       NA       NA       NA       NA       NA       NA       NA
    ## [17]       NA       NA 142238.2

``` r
set.seed(1)
 train=sample(c(TRUE,FALSE), nrow(Hitters),rep=TRUE)
test=(!train)
regfit.best=regsubsets(Salary~.,data=Hitters[train,],
 nvmax=19)
test.mat=model.matrix(Salary~.,data=Hitters[test,])
 val.errors=rep(NA,19)
  for(i in 1:19){
     coefi=coef(regfit.best,id=i)
 pred=test.mat[,names(coefi)]%*%coefi
  val.errors[i]=mean((Hitters$Salary[test]-pred)^2)
  }
 val.errors
```

    ##  [1] 164377.3 144405.5 152175.7 145198.4 137902.1 139175.7 126849.0 136191.4
    ##  [9] 132889.6 135434.9 136963.3 140694.9 140690.9 141951.2 141508.2 142164.4
    ## [17] 141767.4 142339.6 142238.2

``` r
 which.min(val.errors)
```

    ## [1] 7

``` r
 coef(regfit.best,7)
```

    ##  (Intercept)        AtBat         Hits        Walks        CRuns       CWalks 
    ##   67.1085369   -2.1462987    7.0149547    8.0716640    1.2425113   -0.8337844 
    ##    DivisionW      PutOuts 
    ## -118.4364998    0.2526925

## Function как predict() для regsubsets()

``` r
predict.regsubsets=function(object,newdata,id,...){
 form=as.formula(object$call[[2]])
 mat=model.matrix(form,newdata)
 coefi=coef(object,id=id)
 xvars=names(coefi)
 mat[,xvars]%*%coefi
 }
```

Finally,we perform best subset selection on the full dataset,and select
the best ten-variable model(full datset to obtain more accurate
coefficient estimates) Note that we perform best subset selection on the
full dataset and select the best ten variable model, rather than simply
using the variables that were obtained from the training set, because
the best ten-variable model on the full data  
set may differ from the corresponding model on the training set.

``` r
regfit.best=regsubsets(Salary~.,data=Hitters,nvmax=19)
coef(regfit.best,10)
```

    ##  (Intercept)        AtBat         Hits        Walks       CAtBat        CRuns 
    ##  162.5354420   -2.1686501    6.9180175    5.7732246   -0.1300798    1.4082490 
    ##         CRBI       CWalks    DivisionW      PutOuts      Assists 
    ##    0.7743122   -0.8308264 -112.3800575    0.2973726    0.2831680

\#Интерпретация

\##choosing among the models of different sizes using CV =perform best
subset selection within each of the k training sets

``` r
k=10
set.seed(1)
folds=sample(1:k,nrow(Hitters),replace=TRUE)
cv.errors=matrix(NA,k,19, dimnames=list(NULL, paste(1:19)))
```

# loop that performs cross-validation

``` r
for(j in 1:k){
 best.fit=regsubsets(Salary~.,data=Hitters[folds!=j,],
 nvmax=19)
 for(i in 1:19){
 pred=predict(best.fit,Hitters[folds==j,],id=i)
 cv.errors[j,i]=mean( (Hitters$Salary[folds==j]-pred)^2)
 }
 }
```

This has given us a 10×19 matrix, of which the (i,j)th element
corresponds to the test MSE for the ith cross-validation fold for the
best j-variable model. We use the apply() function to average over the
columns of this apply() matrix in order to obtain a vector for which the
jth element is the cross validation error for the j-variable model.

``` r
mean.cv.errors=apply(cv.errors,2,mean)
mean.cv.errors
```

    ##        1        2        3        4        5        6        7        8 
    ## 149821.1 130922.0 139127.0 131028.8 131050.2 119538.6 124286.1 113580.0 
    ##        9       10       11       12       13       14       15       16 
    ## 115556.5 112216.7 113251.2 115755.9 117820.8 119481.2 120121.6 120074.3 
    ##       17       18       19 
    ## 120084.8 120085.8 120403.5

``` r
plot(mean.cv.errors,type='b')
```

![](draft_files/figure-gfm/unnamed-chunk-18-1.png)<!-- -->

CV выбирает 10-variable model. We now perform best subset selection on
the full data set in order to obtain the 11-variable model.

``` r
 reg.best=regsubsets(Salary~.,data=Hitters, nvmax=19)
 coef(reg.best,11)
```

    ##  (Intercept)        AtBat         Hits        Walks       CAtBat        CRuns 
    ##  135.7512195   -2.1277482    6.9236994    5.6202755   -0.1389914    1.4553310 
    ##         CRBI       CWalks      LeagueN    DivisionW      PutOuts      Assists 
    ##    0.7852528   -0.8228559   43.1116152 -111.1460252    0.2894087    0.2688277
