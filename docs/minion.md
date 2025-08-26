# 🤖 minion.py

The `minion` module acts as an orchestration layer that coordinates between data preprocessing,
model inference, and optimization tasks.

## 📘 API Reference

::: minion

## 🛠️ Key Features

- Central hub for executing full ML-to-schedule workflows.
- Connects preprocessing, modeling, and solving in one pass.
- Supports configuration-based pipeline execution.

## 🚀 Example

```
python
from minion import execute_pipeline

results = execute_pipeline(input_data="resources/sample.json")
print(results)
```
