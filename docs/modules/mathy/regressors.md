# 📈 mathy.regressors

Provides regression models for predicting continuous values such as durations, costs, or priority
scores.

## 📘 API Reference

::: mathy.regressors

## 🛠️ Key Features

- Supports linear, ridge, and polynomial regression.
- API supports `.fit()`, `.predict()`, `.score()`.
- Commonly used in scheduling predictions and time estimation.

## 🚀 Example

```
python
from mathy.regressors import LinearRegressor

model = LinearRegressor()
model.fit(X_train, y_train)
output = model.predict(X_test)
```
