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

