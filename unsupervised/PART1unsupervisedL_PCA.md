unsupervisedLearning: PCA
================

``` r
states=row.names(USArrests)
states
```

    ##  [1] "Alabama"        "Alaska"         "Arizona"        "Arkansas"      
    ##  [5] "California"     "Colorado"       "Connecticut"    "Delaware"      
    ##  [9] "Florida"        "Georgia"        "Hawaii"         "Idaho"         
    ## [13] "Illinois"       "Indiana"        "Iowa"           "Kansas"        
    ## [17] "Kentucky"       "Louisiana"      "Maine"          "Maryland"      
    ## [21] "Massachusetts"  "Michigan"       "Minnesota"      "Mississippi"   
    ## [25] "Missouri"       "Montana"        "Nebraska"       "Nevada"        
    ## [29] "New Hampshire"  "New Jersey"     "New Mexico"     "New York"      
    ## [33] "North Carolina" "North Dakota"   "Ohio"           "Oklahoma"      
    ## [37] "Oregon"         "Pennsylvania"   "Rhode Island"   "South Carolina"
    ## [41] "South Dakota"   "Tennessee"      "Texas"          "Utah"          
    ## [45] "Vermont"        "Virginia"       "Washington"     "West Virginia" 
    ## [49] "Wisconsin"      "Wyoming"

``` r
names(USArrests)
```

    ## [1] "Murder"   "Assault"  "UrbanPop" "Rape"

``` r
apply(USArrests, 2, mean)
```

    ##   Murder  Assault UrbanPop     Rape 
    ##    7.788  170.760   65.540   21.232

apply() function allows us to apply a function—in this case, the mean()
function—to each row or column of the data set. The second input here
denotes whether we wish to compute the mean of the rows, 1, or the
columns, 2.

``` r
apply(USArrests, 2, var)
```

    ##     Murder    Assault   UrbanPop       Rape 
    ##   18.97047 6945.16571  209.51878   87.72916

*pca*

``` r
pca=prcomp(USArrests, scale=TRUE)
names(pca)
```

    ## [1] "sdev"     "rotation" "center"   "scale"    "x"

By default, the prcomp() function centers the variables to have mean
zero. By using the option scale=TRUE, we scale the variables to have
standard deviation one.

``` r
pca$center
```

    ##   Murder  Assault UrbanPop     Rape 
    ##    7.788  170.760   65.540   21.232

``` r
pca$scale
```

    ##    Murder   Assault  UrbanPop      Rape 
    ##  4.355510 83.337661 14.474763  9.366385

``` r
pca$rotation
```

    ##                 PC1        PC2        PC3         PC4
    ## Murder   -0.5358995 -0.4181809  0.3412327  0.64922780
    ## Assault  -0.5831836 -0.1879856  0.2681484 -0.74340748
    ## UrbanPop -0.2781909  0.8728062  0.3780158  0.13387773
    ## Rape     -0.5434321  0.1673186 -0.8177779  0.08902432

The center and scale components correspond to the means and standard
deviations of the variables that were used for scaling prior to
implementing PCA. The rotation matrix provides the principal component
loadings; each col umn of pr.out\$rotation contains the corresponding
principal component loading vector *plot pc1 and pc2*

``` r
biplot(pca, scale=0)
```

![](PART1unsupervisedL_PCA_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->
biplots unique up to a sign

``` r
pca$rotation=-pca$rotation
pca$x=-pca$x
biplot(pca, scale=0)
```

![](PART1unsupervisedL_PCA_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->
*variance explained by each pc*

``` r
pca$sdev
```

    ## [1] 1.5748783 0.9948694 0.5971291 0.4164494

``` r
pca.var=pca$sdev^2
pca.var
```

    ## [1] 2.4802416 0.9897652 0.3565632 0.1734301

*PVE*

``` r
pve=pca.var/sum(pca.var)
pve
```

    ## [1] 0.62006039 0.24744129 0.08914080 0.04335752

proportion of variance explained by each principal component= variance
explained by each pc the total variance explained by all pc *plot*

``` r
plot(pve, xlab="Principal Component", ylab="Proportion of Variance Explained", ylim=c(0,1),type='b')
```

![](PART1unsupervisedL_PCA_files/figure-gfm/pve%20plot-1.png)<!-- -->

``` r
plot(cumsum(pve), xlab="Principal Component", ylab="Cumulative Proportion of Variance Explained",ylim=c(0,1), type='b')
```

![](PART1unsupervisedL_PCA_files/figure-gfm/pve%20plot-2.png)<!-- -->
(функция cumsum()вычисляет cumulative sum элементов числового вектора)
Наглядно представлено, что PC1- первый основной компонент- объясняет
62,0% дисперсии в данных, следующий основной компонент PC2 объясняет
24,7% дисперсиии, и тд. Что означает, что рассматривать PC3, PC4 и
прочие не рационально тк они(в сумме) объясняют менее 20% общей
дисперсии данных.
