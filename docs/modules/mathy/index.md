# 🧠 mathy Package Overview

The `mathy` package is a collection of machine learning and data utilities that support the
analytical core of the SchedX system.

## 📘 Included Submodules

- `classifiers` – Supervised learning models for decision tasks.
- `regressors` – Predictive models for continuous outputs.
- `clusters` – Unsupervised models for grouping tasks.
- `preprocessors` – Tools for transforming raw input data.
- `data` – Loaders, schema checkers, and data managers.

## 🧪 Usage Example

```
python
from mathy.classifiers import DecisionTreeClassifier
from mathy.preprocessors import normalize
from mathy.data import load_schedule_data

X, y = load_schedule_data( "data/input.csv" )
X_norm = normalize( X )

model = DecisionTreeClassifier( )
model.fit( X_norm, y )
```
