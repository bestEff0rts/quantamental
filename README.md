ML + econometrics

1- Ridge Lasso Elastic-Net Regression(Regularisation, Shrinkage methods- Методы сжатия)
Ridge Regression (L2 Norm)- small sample sizes meaning Least Squares not applicable; introduces small ammount of bias for a significant drop in variance for better long-term predictions
Ridge Penalty: minimizes SSR+ lambda x (slope)^2
Assimptotocally to zero, i.e. cannot remove factors; 
When Ridge Regression is applied to Logistic Regression, it optimizes the sum of the likelihoods not ssr(sum of squared residuals); also type.measure= deviance not mse and family= not gaussian but binomial
For complex models combining 2 or more datasets Ridge Regression penalty contains parameters for the slope^2 and all the parameters^2 except for y-intercept (it's not scaled by the measurements- that's why y-intercept not included into the Ridge penalty)

// Гребневая регрессия (L2 Norm)-коррекция для снижения мультиколлинеарности среди предикторов, при неэффективности МНК; дает смещенные оценки но с меньшей дисперсией, вводит небольшую степень отклонения для значительного снижения вариации в целях улучшения долгосрочных прогнозов= увеличивает эффективность оценок
Штраф: минимизирует SSR + lambda x (slope)^2
Ассиимптотично стремится к 0, т.е. не может удалить факторы
Когда регрессия Ridge применяется к логистической регрессии, она оптимизирует сумму вероятностей не ssr (сумма квадратичных остатков)
Для сложных моделей, объединяющих 2 или более наборов данных, содержит параметры для slope^2 и всех параметров^2 за исключением у-intercept (не масштабируется по измерениям)

Lasso(L1 Norm) Regression
может удалить предиктор
Minimizes: SSR + lambda*|slope|

Elastic-Net Regression- separate lambdas for each penalty(L1;L2) -calculated using CV(cross validation))- different combinations
=L1+L2 Penalty
lambda1=1 lambda2=0 Lasso (pick 1 correlated predictor and eliminate others)
lambda1=0 lambda2=1 Ridge (shrinks all the correlated paaremters together)
lambda1>0 lambda2>0 Elastic-Net (groups and shrinks correlated variables' parameters and leaves them in equation or removes them all at once)
Источники: Elements of Statistical Learning Hastie; Introduction to statistical learning in R

library(glmnet) #generalized linear models
cv glmnet- lambda*[alpha*Lasso Penalty+(1-alpha)*Ridge Penalty]
alpha=0 Only Ridge; alpha=1 Only Lasso
0<alpha<1 Elastic Net Regression
Lambda=0 Least Squares/Maximum Likelihood
Test different values for lambda and alpha

10-Fold Cross Validation - default but 
(Purged K-Fold CV:
Разбиваем данные на K блоков по времени
Добавляем "очищающий" период (purged) между train и test)
[ Train Fold 1 ] | [ Purge ] | [ Test Fold 1 ] |........ [ Test Fold k] 

\\\\\\Добавление визуализации
Lasso может обнулить фактор(предиктор) то есть его исключить, Ridge- нет
При построении графика x-axis slope values; y-axis- penalty; Ridge- парабола с преломлением в нуле при увеличении lambda; Lasso- нет преломления в нуле
