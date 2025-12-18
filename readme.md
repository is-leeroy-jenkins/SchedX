###### Schedule-X
![](https://github.com/is-leeroy-jenkins/Sched-X/blob/master/resources/images/git/schedx.png)
___
#### A machine-learning pipeline for Combined Schedule (X) reporting.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/is-leeroy-jenkins/SchedX/blob/master/shedule-x.ipynb)

## 📊 Features

- **Descriptive Statistics** — `count`, `mean`, `std`, `min/max`, quartiles, **skew**, **kurtosis**.
- **Distributions** — histograms + KDE for PY/CY/BY (optional zero filtering).
- **Normality Testing** — **Shapiro–Wilk** per column with p-values.
- **Confidence Intervals** — mean CIs (95% by default; configurable).
- **Inferential Test** — one-sample **t-test** on CY vs a configurable baseline (default μ₀ = 0).
- **Data Hygiene** — numeric coercion and optional zero exclusion to stabilize analyses.
- **ML Helper** — compact `plot_decision_regions` utility for quick analysis.



## 📈 Table of Contents

- [Data](#-data-expectations)
- [Outputs](#-outputs)
- [Configuration](#-configuration)
- [Requirements](#-requirements)
- [References](#-references)
- [License](#-license)



## 🎯 Quickstart

### Option A — Google Colab (no local setup)

1. Click the **Open In Colab** badge above.
2. Upload your CSV or mount Google Drive.
3. Set `DATA_PATH` near the top of the notebook.
4. **Runtime → Run all**.

### Option B — Local (conda or venv)

```
bash
# 1) Create environment
conda create -n schedx python=3.11 -y
conda activate schedx

# 2) Install dependencies
pip install -U pip wheel setuptools
pip install pandas numpy scipy matplotlib seaborn scikit-learn jupyter

# 3) Launch Jupyter
jupyter notebook
```

Open `ipynb/schedule-x.ipynb` and run cells top-to-bottom.


## Installation & Run — Clone, Build, and Run the Streamlit App

Follow these steps to clone the repository, create an isolated environment, install dependencies, and run the Schedule-X Streamlit app.

> Replace `<REPO_URL>` below with the repository HTTPS or SSH URL that contains the app files (e.g., `https://github.com/you/your-repo.git`).
> The app filename in these instructions is `app_schedule_x.py`. If your repo uses `app.py`, replace that name when running Streamlit.

---

### 1) Clone the repository

```bash
# HTTPS
git clone <REPO_URL> schedulex-app
cd schedulex-app

# or SSH
git clone git@github.com:you/your-repo.git schedulex-app
cd schedulex-app
```

---

### 2) Recommended Python version

Use a modern CPython version. **Recommended:** Python 3.11 or 3.12.
Verify:

```bash
python --version
# or
python3 --version
```

---

### 3) Create and activate a virtual environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

> If you prefer `venv` named `env` or `.env`, the commands are the same—just be consistent.

---

### 4) Install pinned dependencies

Assumes `requirements.txt` is present in the repo root (the file produced previously).

```bash
pip install -r requirements.txt
```

If you want a lightweight install for development (editable install) include:

```bash
pip install -r requirements.txt
pip install -e .
```

(Only needed if the repo provides a `setup.py` / `pyproject.toml` and you intend to develop the package.)

---

### 5) Run the Streamlit app

```bash
# default
streamlit run app_schedule_x.py

# specify a port (example)
streamlit run app_schedule_x.py --server.port 8501

# run in headless CI or container (no browser)
streamlit run app_schedule_x.py --server.headless true
```

If your file is named `app.py`, substitute `app.py` for `app_schedule_x.py`.

Streamlit will print the local URL (typically `http://localhost:8501`). Open that URL in your browser.

---

### 6) Using the app — datasets & options

* The app expects the main data on an Excel sheet named `Data` (same behavior as the original notebook).
* On first load use either:

  * the **Upload** control in the sidebar to upload `CombinedSchedules.xlsx`, or
  * set a **Fallback local Excel path** (sidebar text box) pointing to the file on disk (e.g., `/stores/excel/CombinedSchedules.xlsx`).
* Sections available from the sidebar: Overview, Descriptive Statistics, Inferential Statistics,
  Dimensionality Reduction, Clustering, Anomaly Detection, Correlation, Export.

---

### 7) Quick troubleshooting / tips

* **Import errors after `pip install`** — confirm you activated the virtual environment where packages were installed. Re-run `python -m pip install -r requirements.txt`.
* **Large Excel files** — increase system memory or pre-filter the workbook; Streamlit apps are memory-limited by the host environment.
* **Missing sheet name** — open the Excel file and confirm the sheet named `Data` exists, or change the sheet name in the script where `pd.read_excel(..., sheet_name="Data")` is called.
* **Port in use** — change the port with `--server.port` or stop the process using the port.
* **Windows PowerShell script execution blocked** — if running `Activate.ps1` fails, you may need to set execution policy (run PowerShell as Administrator):

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

---

### 8) Optional: Run with Docker

A minimal Docker workflow (assumes a `Dockerfile` exists in repo). Example commands:

```bash
# build
docker build -t schedulex:latest .

# run (map port 8501)
docker run --rm -p 8501:8501 schedulex:latest
```

If you want, I can produce a Dockerfile pinned to a specific Python base image and the above `requirements.txt`.

---

### 9) Developer / reproducibility notes

* For heavy transforms, add `@st.cache_data` or `@st.cache_resource` decorators to expensive functions to speed interactive usage.
* Save intermediate model artifacts (PCA, trained detectors) if you want reproducible exports; the app currently computes on demand.
* If you want CI checks, add a `requirements-dev.txt` with `pytest`, `flake8` / `ruff`, and a GitHub Actions workflow to run tests on push.


## 📊 Regression

- Linear, Ridge, Lasso, ElasticNet
- Decision Tree, Random Forest, Gradient Boosting
- SVR, KNN, MLP Regressor, Bayesian Ridge, Huber Regressor

## ✅ Classification

- Logistic Regression, Perceptron, SVM, KNN
- Decision Tree, Random Forest, Extra Trees, AdaBoost, Gradient Boosting
- MLP Classifier, Naive Bayes

## 📊 Diagnostics & Evaluation

- Scatter plots, residuals, precision-recall, ROC curves
- Confusion matrices, ANOVA tests, statistical fitting
- PCA visualizations and correlation heatmaps

## 📁 Data & Engineering

- Excel and CSV ingestion
- Imputation (`SimpleImputer`, `KNNImputer`)
- Scaling (`StandardScaler`, `MinMaxScaler`, `RobustScaler`)
- Feature creation via polynomial expansion
- Dimensionality reduction and outlier detection

## 🏛️ Government Use 

- 📉 Budget Execution forecasting
- 🏛️ OMB Reporting (MAX A-11 Data Entry )
- 🧮 Audit prep and  anomaly detection

## 🔎 Data Expectations

The notebook is designed for **Schedule-X** style datasets with numeric columns for:

- **PY** — Prior Year
- **CY** — Current Year
- **BY** — Budget Year
- **OY-1** — Out Year 1
    >through
- **OY-9** — Out Year 9

A minimal table might look like:

| agency | bureau | account | PY      | CY      | BY      | OY-1      | OY-9 |
|-------:|:------:|:-------:|--------:|--------:|--------:|----------:|-----:|
| 001    | 10     | 1234    | 1050.25 | 1101.00 | 1149.90 |           |      |
| 001    | 20     | 5678    |  450.00 |  465.75 |  480.50 |           |      |

**Notes**

- Column names are configurable (see [Configuration](#-configuration)).
- The loader coerces specified columns to numeric.
- Optional zero filtering is available to avoid distorting distributions and tests.



## 📏 Outputs

- **Summary Frames** — PY/CY/BY metrics with skew/kurtosis (copy-ready).
- **Distribution Plots** — histograms + KDE overlays per column.
- **Normality Table** — Shapiro–Wilk statistic and p-value with quick interpretation.
- **Confidence Intervals** — mean CIs with lower/upper bounds.
- **t-Test Readout** — t-statistic, degrees of freedom, p-value, and concise summary.

> Pro tip: Right-click plots in Jupyter → “Save image as…” to drop charts directly into briefings.




#### Install with:

```
bash
pip install -r requirements.txt
```



## 🧩 References

- **USAspending.gov**  – [Federal Accounts](https://www.usaspending.gov/federal_account)
- **OMB Circular A-11:** - [Dataset](https://www.kaggle.com/datasets/terryeppler/omb-circular-a-11)
- **Principles of Federal Appropriations Law:** - [Dataset](https://www.kaggle.com/datasets/terryeppler/principles-of-federal-appropriations-law)

> **Disclaimer**: This is for analytical exploration, research, and education purposes.  
> It is **not** an official OMB/Treasury product; validate against authoritative sources before use.


## ⚙️  Imports and Setup
```
  import pandas as pd
  import numpy as np
  from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
  from sklearn.impute import SimpleImputer, KNNImputer
  
  # Work with numeric and nominal subsets
  X_numeric = df_numeric.copy()
  X_nominal = df_nominal.copy()

```

## 📏  Scaling (Numeric Columns)
- a) StandardScaler → centers data around mean 0, std 1.
- b) MinMaxScaler → rescales data to [0,1].
```
  scaler_standard = StandardScaler()
  scaler_minmax = MinMaxScaler()
  
  scaled_standard = scaler_standard.fit_transform(X_numeric)
  scaled_minmax = scaler_minmax.fit_transform(X_numeric)
  
  df_standard_scaled = pd.DataFrame(scaled_standard, columns=X_numeric.columns)
  df_minmax_scaled = pd.DataFrame(scaled_minmax, columns=X_numeric.columns)
  
  print("StandardScaler Preview:\n", df_standard_scaled.head())
  print("MinMaxScaler Preview:\n", df_minmax_scaled.head())

```

## 🔖  Encoding (Nominal Columns)
- LabelEncoder: Converts categories → integers (good for ordinal/categorical with hierarchy).
- OneHotEncoder: Expands categories into binary dummy variables (best for nominal IDs).
```
  # Label Encoding (example on MainAccount)
  label_encoder = LabelEncoder()
  X_nominal['MainAccount_LE'] = label_encoder.fit_transform(X_nominal['MainAccount'])
  
  # OneHot Encoding (on AgencyCode, MainAccount)
  onehot_encoder = OneHotEncoder(sparse_output=False, drop='first')
  onehot_encoded = onehot_encoder.fit_transform(df_excel[['AgencyCode','MainAccount']])
  
  df_onehot = pd.DataFrame(
      onehot_encoded, 
      columns=onehot_encoder.get_feature_names_out(['AgencyCode','MainAccount'])
  )
  
  print("Label Encoded Preview:\n", X_nominal[['MainAccount','MainAccount_LE']].head())
  print("OneHot Encoded Preview:\n", df_onehot.head())

```

## 🛠️ Imputation (Missing Values)
- SimpleImputer: Replace missing values with mean/median/most_frequent/constant.
- KNNImputer: Replace missing values based on nearest neighbors (handles anomalies better).
```
  # SimpleImputer (mean)
  simple_imputer = SimpleImputer(strategy='mean')
  df_simple_imputed = pd.DataFrame(
      simple_imputer.fit_transform(X_numeric),
      columns=X_numeric.columns
  )
  
  # KNN Imputer
  knn_imputer = KNNImputer(n_neighbors=5)
  df_knn_imputed = pd.DataFrame(
      knn_imputer.fit_transform(X_numeric),
      columns=X_numeric.columns
  )
  
  print("Simple Imputer Preview:\n", df_simple_imputed.head())
  print("KNN Imputer Preview:\n", df_knn_imputed.head())


```

## 1️⃣ StandardScaler (Z-score normalization)
- Centers around mean = 0 and scales by std = 1.
- Useful when data has large magnitude differences.
```
  import matplotlib.pyplot as plt
  import seaborn as sns
  
  # Apply StandardScaler
  scaler_standard = StandardScaler()
  scaled_standard = scaler_standard.fit_transform(df_numeric)
  df_standard_scaled = pd.DataFrame(scaled_standard, columns=df_numeric.columns)

```

## 2️⃣ MinMaxScaler (Normalization)
- Rescales to [0,1].
- Preserves shape of distribution but compresses range.
```
  scaler_minmax = MinMaxScaler()
  scaled_minmax = scaler_minmax.fit_transform(df_numeric)
  df_minmax_scaled = pd.DataFrame(scaled_minmax, columns=df_numeric.columns)


```

## 3️⃣ LabelEncoder
- Maps categories → integers.
- Example: MainAccount 0103 → 0.
- Caution: Implies ordinal relationships that don’t exist.
```
  label_encoder = LabelEncoder()
  encoded_main = label_encoder.fit_transform(df_nominal['MainAccount'])


```

## ⚙️ Dimensionality Reduction

```
  # --- PCA ---
  pca = PCA(n_components=2)
  X_pca = pca.fit_transform(X_scaled)
  
  # --- Incremental PCA ---
  ipca = IncrementalPCA(n_components=2, batch_size=10)
  X_ipca = ipca.fit_transform(X_scaled)
  
  # --- Truncated SVD ---
  tsvd = TruncatedSVD(n_components=2)
  X_tsvd = tsvd.fit_transform(X_scaled)
  
  # --- Factor Analysis ---
  fa = FactorAnalysis(n_components=2)
  X_fa = fa.fit_transform(X_scaled)
  
  # --- Isomap ---
  isomap = Isomap(n_components=2)
  X_isomap = isomap.fit_transform(X_scaled)
  
  # --- t-SNE (nonlinear, heavy) ---
  tsne = TSNE(n_components=2, random_state=42, perplexity=30)
  X_tsne = tsne.fit_transform(X_scaled)


```

## 🎯 Configuration

- Set these variables near the top of the notebook:

```
python
# ---- Configuration ----
DATA_PATH  = "your_data.csv"   # Path to CSV
COL_PY     = "PY"
COL_CY     = "CY"
COL_BY     = "BY"
DROP_ZEROS = True              # Exclude zeros for plots/tests
ALPHA      = 0.05              # Significance level
CI_LEVEL   = 0.95              # Confidence interval level
MU_0       = 0.0               # Baseline for one-sample t-test on CY
```

**Tips**

- Use policy-relevant baselines for `MU_0` (e.g., enacted/planned levels) when zero is not
  meaningful.
- Filter the DataFrame by agency/account before running stats to produce slice-specific results.

## 📦 Dependencies

| Package       | Description                          | Link                                               |
|---------------|--------------------------------------|----------------------------------------------------|
| numpy         | Numerical computing                   | [numpy.org](https://numpy.org/)                    |
| pandas        | Data manipulation                     | [pandas.pydata.org](https://pandas.pydata.org/)    |
| matplotlib    | Plotting                              | [matplotlib.org](https://matplotlib.org/)          |
| seaborn       | Statistical plots                     | [seaborn.pydata.org](https://seaborn.pydata.org/)  |
| scikit-learn  | Machine learning models               | [scikit-learn.org](https://scikit-learn.org/)      |
| xgboost       | Extreme gradient boosting             | [xgboost.readthedocs.io](https://xgboost.readthedocs.io/) |
| statsmodels   | Statistical modeling & ANOVA          | [statsmodels.org](https://www.statsmodels.org/)    |
| openpyxl      | Excel I/O                             | [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/) |
| fitz (PyMuPDF)| PDF parsing                           | [pymupdf.readthedocs.io](https://pymupdf.readthedocs.io/) |
| loguru        | Logging                               | [github.com/Delgan/loguru](https://github.com/Delgan/loguru) |

## 📝 License

#### Sched-X is published under the MIT General Public License v3 [here](https://github.com/is-leeroy-jenkins/Sched-X/blob/master/LICENSE.txt).





