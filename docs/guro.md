# ⚙️ guro.py

The `guro` module provides an interface to the Gurobi optimization solver, supporting both standard
and custom solver configurations.

## 📘 API Reference

::: guro

## 🛠️ Key Features

- Initializes and configures Gurobi models.
- Manages solver parameters, solution callbacks, and status codes.
- Works in tandem with `boogr` to solve complex scheduling tasks.

## 🚀 Example

```
python
from guro import GurobiSolver

solver = GurobiSolver()
solver.configure(time_limit=60)
results = solver.solve(model)

print(results.status)
```
