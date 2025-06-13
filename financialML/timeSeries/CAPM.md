Регрессия временных рядов: CAPM(регрессия доходности аĸции на доходность
рынĸа)
================

``` r
knitr::opts_chunk$set(warning = FALSE, message = FALSE)
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
library(lmtest)
library(PerformanceAnalytics)
```

    ## 
    ## Присоединяю пакет: 'PerformanceAnalytics'

    ## Следующий объект скрыт от 'package:graphics':
    ## 
    ##     legend

``` r
library(tidyverse)
```

    ## ── Attaching core tidyverse packages ──────────────────────── tidyverse 2.0.0 ──
    ## ✔ dplyr     1.1.4     ✔ readr     2.1.5
    ## ✔ forcats   1.0.0     ✔ stringr   1.5.1
    ## ✔ ggplot2   3.5.2     ✔ tibble    3.2.1
    ## ✔ lubridate 1.9.4     ✔ tidyr     1.3.1
    ## ✔ purrr     1.0.4

    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::first()  masks xts::first()
    ## ✖ dplyr::lag()    masks stats::lag()
    ## ✖ dplyr::last()   masks xts::last()
    ## ℹ Use the conflicted package (<http://conflicted.r-lib.org/>) to force all conflicts to become errors

``` r
library(sandwich)
```

\##Регрессия акций AAPL на индекс S&P500

``` r
getSymbols(c("AAPL", "^GSPC"), src = "yahoo", from = "2015-01-01", to = "2023-01-01")
```

    ## [1] "AAPL" "GSPC"

``` r
df <- merge(dailyReturn(AAPL, type = "log"), dailyReturn(GSPC, type = "log")) %>%
  as.data.frame() %>%
  rownames_to_column(var = "Date") %>%
  as_tibble() %>%
  rename(Apple = daily.returns, SP500 = daily.returns.1) %>%
  mutate(Date = as.Date(Date))
# fix(df)


str(df)
```

    ## tibble [2,014 × 3] (S3: tbl_df/tbl/data.frame)
    ##  $ Date : Date[1:2014], format: "2015-01-02" "2015-01-05" ...
    ##  $ Apple: num [1:2014] -1.87e-02 -2.86e-02 9.41e-05 1.39e-02 3.77e-02 ...
    ##  $ SP500: num [1:2014] -0.00034 -0.01845 -0.00893 0.01156 0.01773 ...

визуализация данных

``` r
ggplot(df, aes(x = Date)) +
  geom_line(aes(y = Apple, color = "Apple"), linewidth = 0.5, alpha = 0.8) +
  geom_line(aes(y = SP500, color = "S&P 500"), linewidth = 0.5, alpha = 0.8) +
  labs(title = "Daily Returns: Apple vs S&P 500 (2015-2022)", y = "Return", color = NULL) +
  scale_color_manual(values = c("Apple" = "red", "S&P 500" = "blue")) +
  theme_minimal() +
  theme(legend.position = "top")  
```

![](CAPM_files/figure-gfm/unnamed-chunk-2-1.png)<!-- --> Разделение
данных train test

``` r
split_date <- df$Date[floor(0.8 * nrow(df))]
train.d <- filter(df, Date <= split_date)
test.d <- filter(df, Date > split_date)
str(train.d)
```

    ## tibble [1,611 × 3] (S3: tbl_df/tbl/data.frame)
    ##  $ Date : Date[1:1611], format: "2015-01-02" "2015-01-05" ...
    ##  $ Apple: num [1:1611] -1.87e-02 -2.86e-02 9.41e-05 1.39e-02 3.77e-02 ...
    ##  $ SP500: num [1:1611] -0.00034 -0.01845 -0.00893 0.01156 0.01773 ...

``` r
dim(train.d)+dim(test.d)
```

    ## [1] 2014    6

``` r
library(roll)
library(zoo)
window_size <- 252  # примерно 1 год торговых дней
n <- nrow(df)
#скользящая регрессия: fit CAPM для каждого окна
rolling.fit <- roll_lm(
  x = as.matrix(df$SP500),
  y = as.matrix(df$Apple),
  width = window_size)

betas <- rolling.fit$coefficients[, 2]
alphas <- rolling.fit$coefficients[, 1]
```

Обучение модели линейной регрессии временных рядов train data

``` r
capm.fit <- lm(Apple ~ SP500, data = train.d)
summary(capm.fit)
```

    ## 
    ## Call:
    ## lm(formula = Apple ~ SP500, data = train.d)
    ## 
    ## Residuals:
    ##       Min        1Q    Median        3Q       Max 
    ## -0.075729 -0.006182 -0.000155  0.006239  0.090117 
    ## 
    ## Coefficients:
    ##              Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept) 0.0004191  0.0003152    1.33    0.184    
    ## SP500       1.1813572  0.0269986   43.76   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.01264 on 1609 degrees of freedom
    ## Multiple R-squared:  0.5434, Adjusted R-squared:  0.5431 
    ## F-statistic:  1915 on 1 and 1609 DF,  p-value: < 2.2e-16

``` r
confint(capm.fit)
```

    ##                     2.5 %      97.5 %
    ## (Intercept) -0.0001990425 0.001037262
    ## SP500        1.1284010052 1.234313403

``` r
camp.poly.fit<- lm(Apple~ I(SP500^2), data=df)
summary(camp.poly.fit)
```

    ## 
    ## Call:
    ## lm(formula = Apple ~ I(SP500^2), data = df)
    ## 
    ## Residuals:
    ##       Min        1Q    Median        3Q       Max 
    ## -0.103947 -0.008815 -0.000374  0.009165  0.140140 
    ## 
    ## Coefficients:
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)  0.0012744  0.0004301   2.963  0.00308 ** 
    ## I(SP500^2)  -3.5827637  0.7065306  -5.071 4.32e-07 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 0.01877 on 2012 degrees of freedom
    ## Multiple R-squared:  0.01262,    Adjusted R-squared:  0.01213 
    ## F-statistic: 25.71 on 1 and 2012 DF,  p-value: 4.322e-07

Прогнозирование

``` r
capm.pred<-predict(capm.fit, newdata=test.d)
test.d$pred <- predict(capm.fit, newdata = test.d)

# Оценка качества (MSE, R² на тест data)
mse <- mean((test.d$Apple - test.d$pred)^2)
r2.test <- cor(test.d$Apple, test.d$pred)^2

cat("Test MSE:", mse, "\nTest R²:", r2.test)
```

    ## Test MSE: 0.0001072971 
    ## Test R²: 0.7258407

Диагностика модели

``` r
# Графики остатков
plot(capm.fit)
```

![](CAPM_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->![](CAPM_files/figure-gfm/unnamed-chunk-6-2.png)<!-- -->![](CAPM_files/figure-gfm/unnamed-chunk-6-3.png)<!-- -->![](CAPM_files/figure-gfm/unnamed-chunk-6-4.png)<!-- -->

``` r
# Тест на автокорреляцию (Дарбина-Уотсона)
dwtest(capm.fit)
```

    ## 
    ##  Durbin-Watson test
    ## 
    ## data:  capm.fit
    ## DW = 1.898, p-value = 0.02055
    ## alternative hypothesis: true autocorrelation is greater than 0

``` r
# Тест на гетероскедастичность (Бреуша-Пагана)
bptest(capm.fit)
```

    ## 
    ##  studentized Breusch-Pagan test
    ## 
    ## data:  capm.fit
    ## BP = 4.9582, df = 1, p-value = 0.02597

``` r
# Оценка модели с поправкой Newey-West
coeftest(capm.fit, vcov = NeweyWest(capm.fit, lag = 6))  # lag можно подобрать
```

    ## 
    ## t test of coefficients:
    ## 
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept) 0.00041911 0.00033334  1.2573   0.2088    
    ## SP500       1.18135720 0.04325520 27.3113   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Durbin-Watson test H0: Нет автокорреляции остатков. H1: Положительная
автокорреляция (остатки зависят от предыдущих). вывод: DW \< 2 (и
p-value \< 0.05): Есть положительная автокорреляция

studentized Breusch-Pagan test H0: Гомоскедастичность (постоянная
дисперсия остатков). H1: Гетероскедастичность вывод: p-value \< 0.05 →
Отклоняется нулевая гипотеза о гомоскедастичности. Пробуем оценить
модели с поправкой Newey-West, преобразования(Логарифмирование:
log(abs(returns) + 1)) или weighted least squares(Взвешенная регрессия)

``` r
library(caret)
#Функция для расчета MSE с заданным lag
calculate_mse <- function(lag, train_data, test_data) {
  model <- lm(Apple ~ SP500, data = train_data)
  predictions <- predict(model, newdata = test_data)
  mse <- mean((test_data$Apple - predictions)^2)
  return(mse)
}
lags <- 1:10 #претенденты для lag
#Time Series Cross-Validation
time_slices <- createTimeSlices(1:nrow(df), initialWindow = 1000, horizon = 252, fixedWindow = FALSE)
mse_values <- sapply(lags, function(lag) {
  mse <- mean(sapply(time_slices$train, function(idx) {
    train <- df[idx, ]
    test <- df[-idx, ]
    calculate_mse(lag, train, test)
  }))
  return(mse)
})
#оптимальный lag
optimal_lag <- lags[which.min(mse_values)]
cat("Optimal lag for Newey-West:", optimal_lag)
```

    ## Optimal lag for Newey-West: 1

``` r
#оценка модели с оптимальным lag
library(sandwich)
library(lmtest)

capm.fit <- lm(Apple ~ SP500, data = df)
nw_vcov <- NeweyWest(capm.fit, lag = optimal_lag) 
coeftest(capm.fit, vcov = nw_vcov)
```

    ## 
    ## t test of coefficients:
    ## 
    ##               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept) 0.00039102 0.00028901   1.353   0.1762    
    ## SP500       1.20790144 0.03103907  38.916   <2e-16 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

интерпретация α = 0 не отвергается (p=0.1762 \> 0.05). Акция не
показывает значимой избыточной доходности (α) после учета рыночного
риска. β = 1.21 значимо отличается от 0 (p ≈ 0). Акция более волатильна,
чем рынок (β \> 1).

Тест Чоу

``` r
library(strucchange)
sctest(Apple ~ SP500, data = df, type = "Chow", point = 0.5)
```

    ## 
    ##  Chow test
    ## 
    ## data:  Apple ~ SP500
    ## F = 1.0101, p-value = 0.3644

интерпретация: есть ли структурный сдвиг в регрессионной модели в
выбранной точке? (H₀): Нет структурного изменения (модель стабильна на
всём периоде). (H₁): Есть структурный сдвиг (параметры α и β изменились
в определённой точке) p-value = 0.3644 \> 0.05 → Не отвергается H₀.
Вывод: Нет статистически значимых доказательств структурного сдвига в
CAPM модели для акции Apple в тестируемой точке.

Кумулятивный тест (CUSUM):

``` r
# jpeg(file="chh.jpeg")
plot(efp(Apple ~ SP500, data = df, type = "OLS-CUSUM"))
```

![](CAPM_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

``` r
# dev.off()
```

Проверяет постепенные изменения параметров. Колебания внутри
границ-модель стабильна

Визуализация регрессии

``` r
ggplot(df, aes(x = SP500, y = Apple)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", color = "blue") +
  labs(title = "CAPM Regression: Apple vs S&P 500",
       x = "S&P 500 Returns", 
       y = "Apple Returns") +
  theme_minimal()
```

![](CAPM_files/figure-gfm/unnamed-chunk-9-1.png)<!-- --> Интерпретация
результатов

``` r
cat("Alpha (intercept):", coef(capm.fit)[1], "\n")
```

    ## Alpha (intercept): 0.000391025

``` r
cat("Beta (slope):", coef(capm.fit)[2], "\n")
```

    ## Beta (slope): 1.207901

``` r
#R^2
rsq <- summary(capm.fit)$r.squared
cat("R-squared:", rsq, "\n")
```

    ## R-squared: 0.5819012

``` r
#Tracking Error (sd residuals=стандартное отклонение остатков)
tracking_error <- sd(residuals(capm.fit))
cat("Tracking Error:", tracking_error, "\n")
```

    ## Tracking Error: 0.01221026
