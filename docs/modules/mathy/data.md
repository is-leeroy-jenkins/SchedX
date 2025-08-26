# 🔗 mathy.clusters

Implements unsupervised learning algorithms for discovering groups or patterns in unlabeled data.

## 📘 API Reference

::: mathy.clusters

## 🛠️ Key Features

- Includes KMeans and similar clustering methods.
- Useful for identifying cohort patterns in scheduling data.
- Supports `.fit()`, `.predict()`, `.fit_predict()` interfaces.

## 🚀 Example

```
python
from mathy.clusters import KMeans

model = KMeans(n_clusters=4)
labels = model.fit_predict(X)
```
