appliedUnsupervisedLearning
================

\##задача a gene expression data set (Ch10Ex11.csv) that consists of 40
tissue samples with measurements on 1,000 genes. The first 20 samples
are from healthy patients, while the second 20 are from a diseased group

``` r
data=read.csv("C:/Users/Huawei/Downloads/Ch10Ex11.csv", header=F)
dim(data) 
```

    ## [1] 1000   40

``` r
# Транспонируем данные, так как нам нужно кластеризовать образцы (столбцы исходных данных)
samples_data <- t(data)
# fix(samples_data)

# Функция для вычисления корреляционного расстояния
cor_dist <- function(x) {
  as.dist(1 - cor(t(x)))
}
# метки групп (первые 20 - здоровые, следующие 20 - больные)
groups <- factor(c(rep("Healthy", 20), rep("Diseased", 20)))
```

*2* Apply hierarchical clustering to the samples using correlation based
distance, and plot the dendrogram.

``` r
hc.complete=hclust(cor_dist(samples_data), method="complete")
hc.average=hclust(cor_dist(samples_data), method="average")
hc.single=hclust(cor_dist(samples_data), method="single")
par(mfrow=c(1,3))
plot(hc.complete,main="Полная связь",labels = groups, xlab="", sub="", cex=.9)
plot(hc.average, main="Средняя связь", xlab="",labels = groups, sub="", cex=.9)
plot(hc.single, main="Одиночная связь", xlab="", labels = groups, sub="",cex=.9)
```

![](appliedHClustering_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->
