# 🧠 SchedX

**SchedX** is a modular, notebook-driven scheduling assistant enhanced by machine learning and
optimization components. It combines analytical modules (`mathy`), optimization logic (`guro`,
`boogr`), and a rich visual interface via Jupyter Notebook.

## 🔍 Project Highlights

- 📘 **Notebook Interface**: Explore and interact with scheduling algorithms via `schedule-x.ipynb`.
- 🧮 **Mathy Module**: Custom-built machine learning tools (classifiers, regressors, clusterers,
  preprocessors).
- 📊 **Optimization**: Leverages linear and mixed-integer programming for complex scheduling
  constraints.
- 🔗 **Modular Design**: All components are isolated and reusable across different applications.

## 📂 Folder Structure

| Folder/File        | Purpose                                  |
|--------------------|-------------------------------------------|
| `mathy/`           | Analytics and modeling modules            |
| `boogr.py`         | Optimization solver or engine             |
| `guro.py`          | Gurobi-specific implementation            |
| `minion.py`        | Utility logic (interface or middleware)   |
| `resources/`       | Linked files used in notebooks            |
| `schedule-x.ipynb` | Interactive notebook interface            |

## 🚀 Getting Started

Install dependencies:

```
bash
pip install -r requirements.txt
```