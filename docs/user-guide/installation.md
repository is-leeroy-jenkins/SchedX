# Installation

Schedx runs as a local Streamlit application with Python dependencies installed from `requirements.txt`.

## 🧭 Purpose

Create a reproducible local runtime for the Schedx application and documentation workflow.

## 🧰 Runtime Requirements

| Component | Requirement |
|---|---|
| Python | Python 3.11 or later recommended |
| Application framework | Streamlit |
| Data stack | pandas, NumPy, openpyxl |
| Statistics | SciPy |
| Modeling | scikit-learn |
| Visualization | matplotlib, seaborn, optional Plotly |
| Optional projection | UMAP when `umap-learn` is installed |
| Documentation | MkDocs, Material for MkDocs, mkdocstrings |

## 🖥️ Windows PowerShell Setup

Create a virtual environment:

    python -m venv .venv

Activate the environment:

    .\.venv\Scripts\Activate.ps1

Upgrade packaging tools:

    python -m pip install --upgrade pip wheel setuptools

Install dependencies:

    pip install -r requirements.txt

Run Schedx:

    streamlit run app.py

## ✅ Validation

| Check | Command | Expected Result |
|---|---|---|
| Python runtime | `python --version` | Supported Python version |
| Package install | `pip install -r requirements.txt` | Completed dependency installation |
| Source compile | `python -m py_compile .\app.py` | No syntax errors |
| Streamlit launch | `streamlit run app.py` | Local application URL printed |

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Activation blocked | Run PowerShell with current-user script execution enabled. |
| Streamlit command missing | Activate `.venv` and reinstall dependencies. |
| Import error | Confirm the package is listed in `requirements.txt` and installed in the active environment. |
| Browser does not open | Copy the local Streamlit URL from the terminal into the browser. |
