# 🧪 mathy.classifiers

Implements classification models used for supervised learning tasks such as categorizing events,
predicting labels, or validating constraints.

## 📘 API Reference

::: mathy.classifiers

## 🛠️ Key Features

- Wraps decision trees, forests, and possibly ensemble methods.
- Simplified `.fit()` / `.predict()` interface.
- Can be integrated with preprocessors for pipelines.

## 🚀 Example

```
python
from mathy.classifiers import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
