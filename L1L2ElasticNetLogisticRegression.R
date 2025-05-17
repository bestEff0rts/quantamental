library(glmnet)
library(ggplot2)
library(plotly)

set.seed(42)

# 1. Генерация бинарных данных (для логистической регрессии)
n <- 1000
p <- 500
real_p <- 150

x <- matrix(rnorm(n*p), nrow=n, ncol=p)
log_odds <- apply(x[,1:real_p], 1, sum)  # истинные предикторы
prob <- 1/(1 + exp(-log_odds))           # преобразуем в вероятности
y <- rbinom(n, 1, prob)                 # бинарный outcome (0/1)

# 2. Разделение на train/test
train_rows <- sample(1:n, .66*n)
x.train <- x[train_rows, ]
x.test <- x[-train_rows, ]
y.train <- y[train_rows]
y.test <- y[-train_rows]

## Ridge (alpha=0) - логистическая регрессия
alpha0.fit <- cv.glmnet(x.train, y.train, 
                        type.measure = "deviance",  # вместо "mse"
                        alpha = 0, 
                        family = "binomial")       # вместо "gaussian"

## Lasso (alpha=1) - логистическая регрессия
alpha1.fit <- cv.glmnet(x.train, y.train, 
                        type.measure = "deviance",
                        alpha = 1, 
                        family = "binomial")

## Elastic Net (alpha=0.5)
alpha0.5.fit <- cv.glmnet(x.train, y.train, 
                          type.measure = "deviance",
                          alpha = 0.5, 
                          family = "binomial")

# 3. Предсказания и оценка (вероятности)
alpha0.probs <- predict(alpha0.fit, newx=x.test, s="lambda.1se", type="response")
alpha1.probs <- predict(alpha1.fit, newx=x.test, s="lambda.1se", type="response")
alpha0.5.probs <- predict(alpha0.5.fit, newx=x.test, s="lambda.1se", type="response")

# 4. Функция для вычисления девианса
compute_deviance <- function(true, probs) {
  -2*mean(true*log(probs) + (1-true)*log(1-probs))
}

dev0 <- compute_deviance(y.test, alpha0.probs)
dev1 <- compute_deviance(y.test, alpha1.probs)
dev0.5 <- compute_deviance(y.test, alpha0.5.probs)

# 5. Подбор alpha от 0 до 1
list.of.fits <- list()
for (i in 0:50) {
  fit.name <- paste0("alpha", i/50)
  list.of.fits[[fit.name]] <- cv.glmnet(x.train, y.train, 
                                        type.measure = "deviance",
                                        alpha = i/50, 
                                        family = "binomial")
}

# 6. Сбор результатов (по deviance)
results <- data.frame()
for (i in 0:50) {
  fit.name <- paste0("alpha", i/50)
  probs <- predict(list.of.fits[[fit.name]], 
                   newx = x.test, 
                   s = "lambda.1se", 
                   type = "response")
  dev <- compute_deviance(y.test, probs)
  temp <- data.frame(alpha = i/50, deviance = dev, fit.name = fit.name)
  results <- rbind(results, temp)
}
results
# 7. График deviance для разных alpha
dev_plot <- ggplot(results, aes(x = alpha, y = deviance)) +
  geom_line(color = "steelblue", size = 1.2) +
  geom_point(color = "red", size = 2) +
  labs(title = "Deviance for Different Alpha Values", 
       subtitle = "Logistic Regression (binomial family)",
       x = "Alpha (0=Ridge, 1=Lasso)", 
       y = "Deviance") +
  theme_minimal()

ggplotly(dev_plot)