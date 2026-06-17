![](./images/schedx-project.png)

___

Schedx, also referred to as Schedule-X, is a Streamlit analytics application for exploring Schedule-X-style budget datasets. It loads a `CombinedSchedules.xlsx` workbook, prepares the data for analysis, and supports descriptive statistics, inferential statistics, feature analysis, dimensionality reduction, clustering, anomaly detection, and CSV export workflows.

## 🧭 Purpose

Schedx gives analysts a repeatable interface for inspecting budget-year and outyear data, identifying distribution patterns, testing relationships, projecting high-dimensional features, grouping records, and flagging possible anomalies.

## 🧱 Core Workflows

| Workflow                 | Description                                                                              |
|--------------------------|------------------------------------------------------------------------------------------|
| Data Loading             | Upload `CombinedSchedules.xlsx` or use a fallback local path.                            |
| Overview                 | Inspect sample records, data types, missing values, and numeric summaries.               |
| Descriptive Statistics   | Compute expanded statistics, distribution plots, skewness, kurtosis, and outlier counts. |
| Inferential Statistics   | Run pairwise t-tests, Mann-Whitney U tests, ANOVA, and chi-square tests.                 |
| Feature Analysis         | Review correlations, PCA projections, LDA separation, and optional k-Means clustering.   |
| Dimensionality Reduction | Use PCA, TruncatedSVD, FactorAnalysis, IncrementalPCA, t-SNE, and UMAP where available.  |
| Clustering               | Group records with k-Means, DBSCAN, or Agglomerative clustering.                         |
| Anomaly Detection        | Detect outliers using Isolation Forest, One-Class SVM, LOF, or Elliptic Envelope.        |
| Export                   | Download raw data and anomaly outputs as CSV files.                                      |

## 🏛️ Government Analytics Context

Schedx is useful for analytical exploration of federal budget structures, OMB reporting data, audit preparation, anomaly detection, and exploratory financial modeling.

## 🚀 Quick Start

Install dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

Open the local Streamlit URL shown in the terminal, typically:

    http://localhost:8501

## 📚 Documentation Map

| Page                                      | Purpose                                                                      |
|-------------------------------------------|------------------------------------------------------------------------------|
| [Architecture](architecture.md)           | Explains the application structure and workflow layers.                      |
| [Data Expectations](data-expectations.md) | Describes the expected workbook, sheet, and Schedule-X fields.               |
| [User Guide](user-guide/index.md)         | Provides task-oriented instructions for using the app.                       |
| [API Reference](api/index.md)             | Provides source-generated documentation from `app.py`.                       |
| [Deployment](deployment.md)               | Explains local, Streamlit, Colab, Databricks, and optional Docker workflows. |
| [Development](development.md)             | Documents validation, build, and troubleshooting practices.                  |
