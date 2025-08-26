# 🧮 boogr.py

The `boogr` module defines optimization models for solving scheduling problems using mixed-integer
programming techniques.

## 📘 API Reference

::: boogr

## 🛠️ Key Features

- Constructs and solves constrained scheduling models.
- Encodes task dependencies, time limits, and resource bounds.
- Interfaces with external solvers like Gurobi or CBC.

## 🚀 Example

```
python
from boogr import build_schedule

input_data = {...}  # scheduling problem definition
schedule = build_schedule(input_data)

print(schedule)
```
