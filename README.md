**Quantamental Research: Financial ML & Statistical Learning**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0+-blue?logo=r)](https://www.r-project.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Tests](https://github.com/bestEff0rts/quantamental/actions/workflows/python-tests.yml/badge.svg)](https://github.com/bestEff0rts/quantamental/actions)


данный проект охватывает ключевые концепции машинного обучения и statistical learning с элементами мат статистики и эконометрики
и предлагает свежий взгляд на имплеменатцию *financial machine learning* на Python и R.

python - Tensorflow/Keras, Statsmodels, mlfinlab, Pandas, NumPy, Scikit-Learn, XGBoost, yfinance
R- glm, e1071, MASS, splines, randomForest, gam, tseries, caret, boot, PortfolioAnalytics, forecast
(см requirements.txt)

модели: 
*Deep Learning* : Sequential models(RNN, LSTM, TCN,  CNN) ; Reinforcement Learning (Deep Q-Networks, Q-Learning)
*сплайны*: regression splines, cubic and natural splines 

*методы опорных векторов*: support vector machines, support vector classifier с ядрами: radial basis kernel, linear kernel

*регрессия*: OLS множественная линейная регрессия, polynomial regression, регрессия с interaction effects, обобщенные аддитивные модели(generalized additive models)

*регуляризация*: L1 (lasso), L2(ridge), elastic-net; partial least squares regression(supervised аналог pca), early stopping(neural networks)

*классификаторы*: logistic regression, naive Bayes
*tree-based*: bart(bayesian additive regression trees), random forests, decision trees, boosting, bagging
*ансамбли*: xgboost, catboost, adaboost, gradient boost

*unsupervised learning*: KNN clustering, Hierarchial clustering, DBSCAN, Isolation Forest
*bayesian*: monte carlo simultion, mcmc (Monte Carlo Markov Chains)

*методы снижения размерности признакового пространства(dimension reduction)*: pca(principal component analysis), pls(partial least squares), lda(linear discriminant analysis), qda(quadratic discriminant analysis)

*эконометирика*: arima, garch, adf-augmented dickey fuller тест на стационарность, Granger Casuality Test

*risk managment*: Var, CVar, EVT (extreme value theorem)

*portfolio managment*: cla(markowitz efficient frontier), capm, cot(commitments of traders) data 

(Список литературы: afml, islp)

Моя активность на GitHub  
[Stats](https://github-readme-stats.vercel.app/api?username=bestEff0rts&show_icons=true&theme=radical)  

[Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=bestEff0rts&layout=compact)  

Как склонировать репозиторий  
```bash
git clone https://github.com/bestEff0rts/quantamental.git
```
Установка
```bash
pip install -r requirements.txt
```
