library(glmnet)
library(ggplot2)
library(cowplot)
library(plotly)

set.seed(42)

n <- 1000
p <- 5000
real_p <- 15

x <- matrix(rnorm(n*p), nrow=n, ncol=p)
y <- apply(x[,1:real_p], 1, sum) + rnorm(n)

train_rows <- sample(1:n, .66*n)
x.train<-x[train_rows, ]
x.test<-x[-train_rows, ]

y.train<-y[train_rows]
y.test<-y[-train_rows]

##Ridge(alpha=0)
alpha0.fit <- cv.glmnet(x.train, y.train, type.measure="mse", alpha=0, family="gaussian")
alpha0.predicted <- predict(alpha0.fit, s=alpha0.fit$lambda.1se, newx=x.test)
mse0 <- mean((y.test - alpha0.predicted)^2)

##Lasso(alpha=1)
alpha1.fit <- cv.glmnet(x.train, y.train, type.measure="mse", alpha=1, family="gaussian")
alpha1.predicted <- predict(alpha1.fit, s=alpha1.fit$lambda.1se, newx=x.test)
mse1 <- mean((y.test - alpha1.predicted)^2)

##Elastic Net (alpha=0.5)
alpha0.5.fit <- cv.glmnet(x.train, y.train, type.measure="mse", alpha=0.5, family="gaussian")
alpha0.5.predicted <- predict(alpha0.5.fit, s=alpha0.5.fit$lambda.1se, newx=x.test)
mse0.5 <- mean((y.test - alpha0.5.predicted)^2)

##alpha от 0 до 1
list.of.fits <- list()
for (i in 0:50) {
  set.seed(42)
  fit.name <- paste0("alpha", i/50)
  list.of.fits[[fit.name]] <- cv.glmnet(x.train, y.train, type.measure="mse", alpha=i/50, family="gaussian")
}

results <- data.frame()
for (i in 0:50) {
  fit.name <- paste0("alpha", i/50)
  predicted <- predict(list.of.fits[[fit.name]], s=list.of.fits[[fit.name]]$lambda.1se, newx=x.test)
  mse <- mean((y.test - predicted)^2)
  temp <- data.frame(alpha=i/50, mse=mse, fit.name=fit.name)
  results <- rbind(results, temp)
}
results
#MSE для разных alpha
mseplot <- ggplot(results, aes(x=alpha, y=mse)) +
  geom_line(color="steelblue", size=1.2) +
  geom_point(color="red", size=2) +
  labs(title="MSE for Different Alpha Values", 
       x="Alpha (0=Ridge, 1=Lasso)", 
       y="Mean Squared Error") +
  theme_minimal()

ggplotly(mseplot) # MSE по alpha

library(plotly)
lambda_values <- c(0, 10, 20, 40)
slope_range <- seq(-2, 2, length.out = 500)
ssr <- 10  # Фиксированное значение SSR

#расчет данных для Ridge penalty
ridge_data <- data.frame(
  slope = rep(slope_range, times = length(lambda_values)),
  lambda = factor(rep(lambda_values, each = length(slope_range)), 
                  levels = c("40", "20", "10", "0")),
  penalty = ssr + rep(lambda_values, each = length(slope_range)) * 
    rep(slope_range, times = length(lambda_values))^2
)

#интерактивный график
plotridge <- plot_ly() %>%
  add_lines(
    data = subset(ridge_data, lambda == "40"),
    x = ~slope, y = ~penalty,
    name = "λ=40", line = list(color = "red", width = 2),
    hoverinfo = "text",
    text = ~paste("λ=40<br>β:", round(slope, 2), "<br>Penalty:", round(penalty, 2))
  ) %>%
  add_lines(
    data = subset(ridge_data, lambda == "20"),
    x = ~slope, y = ~penalty,
    name = "λ=20", line = list(color = "green", width = 2),
    hoverinfo = "text",
    text = ~paste("λ=20<br>β:", round(slope, 2), "<br>Penalty:", round(penalty, 2))
  ) %>%
  add_lines(
    data = subset(ridge_data, lambda == "10"),
    x = ~slope, y = ~penalty,
    name = "λ=10", line = list(color = "blue", width = 2),
    hoverinfo = "text",
    text = ~paste("λ=10<br>β:", round(slope, 2), "<br>Penalty:", round(penalty, 2))
  ) %>%
  add_lines(
    data = subset(ridge_data, lambda == "0"),
    x = ~slope, y = ~penalty,
    name = "λ=0", line = list(color = "black", width = 2),
    hoverinfo = "text",
    text = ~paste("λ=0<br>β:", round(slope, 2), "<br>Penalty:", round(penalty, 2))
  ) %>%
  layout(
    title = list(
      text = "<b>Ridge Penalty: SSR + λ×β²</b>",
      x = 0.5,
      font = list(size = 16)
    ),
    xaxis = list(
      title = "Slope Values (β)",
      range = c(-2, 2),
      tickvals = seq(-2, 2, 1),
      zeroline = FALSE,
      showgrid = TRUE,
      gridcolor = "lightgray"
    ),
    yaxis = list(
      title = "Penalty Value",
      range = c(0, max(ridge_data$penalty) + 5),
      showgrid = TRUE,
      gridcolor = "lightgray"
    ),
    legend = list(
      orientation = "h",
      x = 0.5,
      y = 1.1,
      xanchor = "center"
    ),
    hovermode = "x unified",
    shapes = list(
      list(
        type = "line",
        x0 = 0,
        x1 = 0,
        y0 = 0,
        y1 = max(ridge_data$penalty),
        line = list(color = "gray", dash = "dash")
      )
    ),
    annotations = list(
      list(
        x = 1.5,
        y = max(ridge_data$penalty) * 0.9,
        text = "Парабола сдвигается вверх и сужается с ростом λ",
        showarrow = FALSE,
        font = list(size = 14)
      ),
      list(
        x = 0,
        y = ssr,
        text = "SSR",
        showarrow = FALSE,
        font = list(size = 14),
        yshift = 10
      )
    )
  )
plotridge
