# Schedx Architecture

Schedx is organized as a single Streamlit application that combines data loading, exploratory analytics, statistical testing, dimensionality reduction, clustering, anomaly detection, visualization, and export features.

## 🧭 Purpose

This page explains how the application moves from workbook ingestion to analytical output.

## 🧱 Application Layers

| Layer                 | Responsibility                                                               |
|-----------------------|------------------------------------------------------------------------------|
| User Browser          | Presents the Streamlit user interface.                                       |
| Streamlit Sidebar     | Captures file upload, fallback path, and workflow section selection.         |
| Excel Loader          | Reads the uploaded workbook or fallback file path.                           |
| DataFrame Preparation | Identifies numeric and categorical columns and prepares analysis-ready data. |
| Statistical Engines   | Computes descriptive, inferential, and distribution diagnostics.             |
| Feature Engines       | Computes correlations, PCA, LDA, and dimensionality-reduction projections.   |
| Clustering Engines    | Runs k-Means, DBSCAN, and Agglomerative clustering.                          |
| Anomaly Engines       | Runs Isolation Forest, One-Class SVM, LOF, and Elliptic Envelope.            |
| Presentation Layer    | Displays tables, charts, captions, and insights in Streamlit.                |
| Export Layer          | Produces downloadable CSV outputs.                                           |
| Documentation Layer   | Uses MkDocs, Material for MkDocs, and mkdocstrings.                          |

## 🔄 Runtime Flow

1. The user opens the Streamlit application.
2. The sidebar prompts for an Excel workbook or fallback local path.
3. The loader attempts to read sheet `Data`.
4. If sheet `Data` is missing, the loader attempts the first workbook sheet.
5. The app builds numeric and categorical feature lists.
6. The selected sidebar section determines which analytical workflow runs.
7. Tables, charts, and downloadable outputs are rendered in the browser.

## 🧪 Analytical Pipeline

| Stage    | Inputs                          | Outputs                                           |
|----------|---------------------------------|---------------------------------------------------|
| Load     | Excel workbook or fallback path | `pd.DataFrame`                                    |
| Inspect  | Loaded dataframe                | Sample rows, column summary, numeric snapshot     |
| Describe | Numeric columns                 | Expanded descriptive statistics and distributions |
| Test     | Numeric and categorical columns | t-test, Mann-Whitney U, ANOVA, chi-square results |
| Project  | Numeric feature matrix          | PCA, SVD, FA, IPCA, t-SNE, or UMAP coordinates    |
| Cluster  | Numeric feature matrix          | Cluster labels and summaries                      |
| Detect   | Numeric feature matrix          | Inlier/outlier predictions                        |
| Export   | Loaded or labeled dataframe     | CSV download                                      |


## ✅ Design Notes

Schedx favors a traditional Streamlit pattern: load data, expose workflow controls in the sidebar, execute analysis in the selected section, and render results immediately. The documentation should preserve that mental model so users understand the application before reviewing the API reference.
