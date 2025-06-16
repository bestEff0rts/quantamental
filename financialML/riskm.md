RiskManagmentExamples
================

``` r
knitr::opts_chunk$set(echo = TRUE)
library(quantmod) 
```

    ## Загрузка требуемого пакета: xts

    ## Загрузка требуемого пакета: zoo

    ## 
    ## Присоединяю пакет: 'zoo'

    ## Следующие объекты скрыты от 'package:base':
    ## 
    ##     as.Date, as.Date.numeric

    ## Загрузка требуемого пакета: TTR

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

``` r
library(moments) # For skewness and kurtosis 
library(tseries)    # Для теста Харке-Бера
library(energy)     # Для многомерных тестов нормальности 
```

## 

``` r
symbols <- c("AAPL", "MSFT", "JNJ", "JPM", "PG", "HD", "DIS", "MRK", "CSCO")
start.date <- "1993-01-01"
end.date <- "2000-12-31"
stock.data <- list()
for(symbol in symbols) {
getSymbols(symbol, src = "yahoo", from = start.date, to = end.date)
stock.data[[symbol]] <- Ad(get(symbol)) # Use adjusted closing prices
}
rm(list = symbols)
```

logarithmic returns

``` r
calculate_returns <- function(prices, period = "daily") {
logreturns <- diff(log(prices), lag = 1)
logreturns <- na.omit(logreturns)

aggregated_returns <- switch(period,
         daily = logreturns,
         weekly = apply.weekly(logreturns, sum),
         monthly = apply.monthly(logreturns, sum),
         quarterly = apply.quarterly(logreturns, sum))
  
  return(aggregated_returns)
}
```

list store at dif frequencies

``` r
returns <- list(
daily = lapply(stock.data, calculate_returns, "daily"),
weekly = lapply(stock.data, calculate_returns, "weekly"),
monthly = lapply(stock.data, calculate_returns, "monthly"),
quarterly = lapply(stock.data, calculate_returns, "quarterly")
)
```

\##Univariate Normality Tests

``` r
test_univariate_normality <- function(return_series) {
  # Calculate basic statistics
  n <- length(return_series)
  skew <- skewness(return_series)
  kurt <- kurtosis(return_series)
  
  # Jarque-Bera test from tseries package
  jb_test <- jarque.bera.test(return_series)
  list(
    n = n,
    skewness = skew,
    kurtosis = kurt,
    jb_statistic = jb_test$statistic,
    jb_pvalue = jb_test$p.value
  )
}
```

\##Multivariate Normality Tests

``` r
# Prepare multivariate data (daily returns as example)
multivariate_data <- as.matrix(do.call(cbind, returns$daily))

# Energy test for multivariate normality
energy_test <- mvnorm.etest(multivariate_data, R = 999) # R = number of bootstrap replicates
```

QQ-Plot \*выбор distance metric- Если данные имеют корреляцию и разный
масштаб → Махаланобис Если признаки независимы и нормированы → Евклидово
Если важна устойчивость к выбросам → Манхэттен (Расстояние Махаланобиса
учитывает: Ковариационную структуру данных (корреляцию между
признаками). Масштаб (дисперсию) каждого признака (автоматически
нормирует данные).)

``` r
# Calculate squared Mahalanobis distances
cov_matrix <- cov(multivariate_data)
center <- colMeans(multivariate_data)
D_squared <- mahalanobis(multivariate_data, center, cov_matrix)
# QQ-plot against chi-squared distribution
jpeg(file="qqplot.jpeg")
qqplot(qchisq(ppoints(length(D_squared)), df = ncol(multivariate_data)),
D_squared,main = "QQ-Plot of Mahalanobis D-squared vs Chi-squared",
xlab = "Theoretical Chi-squared Quantiles",ylab = "Sample Mahalanobis D-squared")
abline(0, 1, col = "red")
```

\##интерпретация В верхней части графика точки сильно отклоняются вверх,
что указывает на аномально большие расстояния (выбросы). В нижней части
точки ближе к линии, значит центральная часть данных ближе к
нормальности. вывод: данные не являются многомерно нормальными, особенно
из-за fat tails-тяжелых хвостов. results

``` r
# Print multivariate results
cat("\nEnergy Test for Multivariate Normality:\n")
```

    ## 
    ## Energy Test for Multivariate Normality:

``` r
cat("Test Statistic:", energy_test$statistic, "\n")
```

    ## Test Statistic: 31.04

``` r
cat("p-value:", energy_test$p.value, "\n")
```

    ## p-value: 0
