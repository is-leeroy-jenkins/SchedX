# 🧼 mathy.preprocessors

Provides data transformation utilities to clean, normalize, encode, or scale data prior to modeling
or optimization.

## 📘 API Reference

::: mathy.preprocessors

## 🛠️ Key Features

- Standard scaling and normalization of feature sets.
- Categorical encoding and missing data imputation.
- Designed for modular use in ML pipelines.

## 🚀 Example

```
python
from mathy.preprocessors import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)
```
