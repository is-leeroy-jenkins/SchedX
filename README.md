###### Schedule-X
![](https://github.com/is-leeroy-jenkins/Sched-X/blob/master/resources/images/git/schedx.png)
___

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-0078FC?style=for-the-badge&logo=github)](https://is-leeroy-jenkins.github.io/schedX/)

## 📊 Features

- **Descriptive Statistics** — `count`, `mean`, `std`, `min/max`, quartiles, **skew**, **kurtosis**.
- **Distributions** — histograms + KDE for PY/CY/BY (optional zero filtering).
- **Normality Testing** — **Shapiro–Wilk** per column with p-values.
- **Confidence Intervals** — mean CIs (95% by default; configurable).
- **Inferential Test** — one-sample **t-test** on CY vs a configurable baseline (default μ₀ = 0).
- **Data Hygiene** — numeric coercion and optional zero exclusion to stabilize analyses.
- **ML Helper** — compact `plot_decision_regions` utility for quick analysis.

## 🎥 Demo

![](https://github.com/is-leeroy-jenkins/SchedX/blob/master/resources/images/schedx-demo.gif)
___

## ☁️ Cloud

<table>
<tr>
<td align="center">
<img width="150" height="1" alt=""><br>
<a href="https://schedx-py.streamlit.app/">
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit App">
</a>
</td>

<td align="center">
<img width="150" height="1" alt=""><br>
<a href="https://sake.ashystone-c8f41cd1.centralus.azurecontainerapps.io">
<img src="https://img.shields.io/badge/Docker-App-2496ED?logo=docker&logoColor=white" alt="Docker App">
</a>
</td>

<td align="center">
<img width="150" height="1" alt=""><br>
<a href="https://chatgpt.com/g/g-67579c62ebf88191b67889476229e498-buddy">
<img src="https://img.shields.io/badge/OpenAI-GPT-412991?logo=openai&logoColor=white" alt="OpenAI GPT">
</a>
</td>

<td align="center">
<img width="150" height="1" alt=""><br>
<a href="https://colab.research.google.com/github/is-leeroy-jenkins/SchedX/blob/master/shedule-x.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
</a>
</td>

<td align="center">
<img width="150" height="1" alt=""><br>
<a href="https://dbc-a0c21f80-7bb3.cloud.databricks.com/editor/notebooks/3169291152437590?o=7474645703081351">
<img src="https://img.shields.io/badge/Databricks%20Repo-SchedX-FF3621?logo=databricks&logoColor=white" alt="Databricks Repo">
</a>
</td>


<td align="center">
<img width="152" height="1" alt=""><br>
<a href="https://leeroy.usw-16.palantirfoundry.com/shares/links/xfdusnf2hi7va">
<img src="https://img.shields.io/badge/Palantir%20Foundry-Repo-101113?logo=palantir&logoColor=white" alt="Repo">
</a>
</td>
</tr>
</table>


## 📈 Table of Contents

- [Data](#-data-expectations)
- [Outputs](#-outputs)
- [Configuration](#-configuration)
- [Requirements](#-requirements)
- [References](#-references)
- [License](#-license)



### Option A — Google Colab (no local setup)


![](https://github.com/is-leeroy-jenkins/SchedX/blob/master/resources/ScheduleX-nb.gif)

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


![](https://github.com/is-leeroy-jenkins/SchedX/blob/master/resources/Schedule-X.gif)
___



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
streamlit run app.py

# specify a port (example)
streamlit run app.py --server.port 8501

# run in headless CI or container (no browser)
streamlit run app.py --server.headless true
```

If your file is named `app.py`, substitute `app.py` for `app_schedule_x.py`.

Streamlit will print the local URL (typically `http://localhost:8501`). Open that URL in your browser.

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


## 📁 Customize Dataset

Replace dataset ingestion cell with:

```python
import pandas as pd
df = pd.read_csv("your_dataset.csv")
X = df.drop("target_column", axis=1)
y = df["target_column"]
```


## 🎶 Fine-Tuning 


| File Name                                                                                                                                                                 | Description                                                                                                            |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| [Balanced Budget and Emergency Deficit Control Act of 1985](https://huggingface.co/datasets/leeroy-jankins/The-Balanced-Budget-And-Emergency-Deficit-Control-Act-of-1985) | Establishes statutory limits on federal spending and deficit control mechanisms, including sequestration procedures.   |
| [Budget Control Act of 2011](https://huggingface.co/datasets/leeroy-jankins/The-Budget-Control-Act-2011)                                                                  | Sets discretionary spending caps and establishes enforcement mechanisms to control federal deficits.                   |
| [Digital Accountability And Transparency Act of 2014](https://huggingface.co/datasets/leeroy-jankins/Data-Act-2014)                                                       | Requires standardized federal spending data and improved transparency through government-wide financial reporting.     |
| [Federal Account Symbols And Titles Book](https://huggingface.co/datasets/leeroy-jankins/FastBook)                                                                        | Defines Treasury account symbols and official titles used for federal budgetary and accounting purposes.               |
| [Federal Acquisition Regulation](https://huggingface.co/datasets/leeroy-jankins/Federal-Acquisition-Regulation)                                                           | Establishes uniform policies and procedures governing the acquisition of goods and services by federal agencies.       |
| [Federal Government Standards For Internal Controls](https://huggingface.co/datasets/leeroy-jankins/Federal-Government-Standards-For-Internal-Controls)                   | Defines the internal control framework for federal agencies to ensure accountability, integrity, and compliance.       |
| [Federal Managers Financial Integrity Act of 1982](https://huggingface.co/datasets/leeroy-jankins/FMFIA-1982)                                                             | Requires agencies to establish internal controls and report annually on their effectiveness.                           |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                 | Provides accounting guidance for the management and reporting of federal trust funds.                                  |
| [Financial Management Regulations DOD 7000-14-R](https://huggingface.co/datasets/leeroy-jankins/DOD-7000-14-Financial-Management-Regulation)                                                                                                                        | Establishes DoD-specific financial management policies, procedures, and accounting requirements.                       |
| [Fiscal Responsibility Act](https://huggingface.co/datasets/leeroy-jankins/The-Fiscal-Responsibility-Act-of-2023)                                                                                                                                                 | Establishes statutory measures intended to improve fiscal discipline and control federal spending.                     |
| [Government Auditing Standards](https://huggingface.co/datasets/leeroy-jankins/Government-Auditing-Standards)                                                                                                                                             | Sets professional standards for audits of government organizations, programs, activities, and functions.               |
| [Government Invoicing User Guide](https://huggingface.co/datasets/leeroy-jankins/Government-Performance-and-Results-Act)                                                                                                                                           | Provides guidance on federal invoicing standards and processes for government transactions.                            |
| [Government Performance and Results Act of 1993](https://huggingface.co/datasets/leeroy-jankins/Government-Performance-and-Results-Act)                                                                                                                            | Requires agencies to engage in strategic planning and performance measurement to improve program effectiveness.        |
| [GPRA Modernization Act of 2010](https://huggingface.co/datasets/leeroy-jankins/The-GPRA-Modernization-Act-Of-2010)                                                                                                                                            | Updates GPRA by strengthening performance management, cross-agency goals, and accountability.                          |
| [OMB Circular A-11 Preparation Submission And Execution Of The Budget](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A-11)                                                                                                      | Provides comprehensive guidance for preparing, submitting, and executing the President’s Budget.                       |
| [OMB Circular A-11 Section 120 Apportionment Process](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A11-Section-120-Apportionment-Process)                                                                                                                       | Defines the apportionment process used to control the rate of obligation of budgetary resources.                       |
| [OMB Circular A-123 Managements Responsibility for Enterprise Risk Management and Internal Control](https://huggingface.co/datasets/leeroy-jankins/OMB-Circular-A-123)                                                                         | Defines management responsibilities for internal control and enterprise risk management across federal agencies.       |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                                                                                       | Establishes requirements for federal agency financial statements and reporting.                                        |
| [Principles Of Federal Appropriations Law Volume One](https://huggingface.co/datasets/leeroy-jankins/Principles-Of-Federal-Appropriations-Law)                                                                                                                       | Authoritative GAO guidance on foundational principles governing the use of federal appropriations.                     |
| [Statements of Federal Federal Financial Accounting Concepts and Standards](https://huggingface.co/datasets/leeroy-jankins/Statements-Of-Federal-Financial-Accounting-Concepts-And-Standards)                                                                                                 | Establishes accounting concepts and standards for federal financial reporting.                                         |
| [The Anti-Deficiency Act PL 97-258](https://huggingface.co/datasets/leeroy-jankins/The-Anti-Deficiency-Act)                                                                                                                                         | Prohibits federal agencies from obligating or expending funds in excess of appropriations or before enactment.         |
| [The Anti-Deficiency Reform and Enforcement Act of 2018](https://huggingface.co/datasets/leeroy-jankins/The-Anti-Deficiency-Reform-And-Enforcement-Act-Of-2018)                                                                                                                    | Strengthens Anti-Deficiency Act enforcement and reporting requirements to improve fiscal accountability.               |
| [The Chief Financial Officers Act of 1990](https://huggingface.co/datasets/leeroy-jankins/The-Chief-Financial-Officers-Act-1990)                                                                                                                                  | Establishes agency Chief Financial Officers and modernizes federal financial management practices.                     |
| [The Congressional Budget and Impoundment Control Act of 1974](https://huggingface.co/datasets/leeroy-jankins/The-Congressional-Budget-And-Impoundment-Control-Act-Of-1974)                                                                                                              | Establishes the congressional budget process and restricts executive impoundment of appropriated funds.                |
| [Statutory Pay As You Go Act of 2010](https://huggingface.co/datasets/leeroy-jankins/Statutory-Pay-As-You-Go-Act-of-2010)                                                                                                                                                   | Authorizes interagency agreements for the provision of goods and services on a reimbursable basis.                     |
| [The Stafford Act](https://huggingface.co/datasets/leeroy-jankins/The-Stafford-Act)                                                                                                                                                          | Provides the statutory framework for federal disaster response and emergency assistance.                               |
| [Federal Trust Fund Accounting Guide](https://huggingface.co/datasets/leeroy-jankins/Federal-Trust-Fund-Accounting-Guide)                                                                                                                                  | Provides additional appropriations authority beyond regular annual funding acts.                                       |
| [Title 2 Code of Federal Regulations – Uniform Administrative Requirements, Cost Principles, and Audit](https://huggingface.co/datasets/leeroy-jankins/Title-2-CFR-Uniform-Administrative-Requirements-Cost-Principles-And-Audit)                                                                     | Establishes uniform administrative, cost, and audit requirements for federal financial assistance.                     |
| [Title 31 Code of Federal Regulations – Money and Finance](https://huggingface.co/datasets/leeroy-jankins/Title-31-CFR-Money-and-Finance)                                                                                                                  | Codifies Treasury and federal financial management regulations governing money and finance.                            |
| [US Standard General Ledger Account Definitions](https://huggingface.co/datasets/leeroy-jankins/US-Standard-General-Ledger-Accounts-And-Definitions)                                                                                                                            | Defines standardized account structures used for federal accounting and financial reporting.                           |

## 🧠 Custom LLM

- [![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Model-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/leeroy-jankins/models)


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





