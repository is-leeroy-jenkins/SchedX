# User Guide

Schedx provides a Streamlit interface for loading Schedule-X-style budget data, inspecting dataframe structure, computing statistical diagnostics, projecting numeric feature matrices, clustering records, screening anomalies, and exporting CSV outputs.

## 🧭 Purpose

Operate the Schedx analytical workflow from workbook ingestion through reviewable outputs.

## 🧱 Workflow Position

| Step | Page | Output |
|---|---|---|
| 1 | [Installation](installation.md) | Local Python and Streamlit runtime |
| 2 | [Data Loading](data-loading.md) | Loaded dataframe |
| 3 | [Data Overview](overview.md) | Sample rows, feature summary, numeric snapshot |
| 4 | [Descriptive Statistics](descriptive-statistics.md) | Distribution diagnostics and summary metrics |
| 5 | [Inferential Statistics](inferential-statistics.md) | Test statistics, p-values, contingency tables |
| 6 | [Feature Analysis](feature-analysis.md) | Correlations, PCA, LDA, k-Means summaries |
| 7 | [Dimensionality Reduction](dimensionality-reduction.md) | Two-dimensional projection tables and charts |
| 8 | [Clustering](clustering.md) | Cluster labels, counts, summaries, projections |
| 9 | [Anomaly Detection](anomaly-detection.md) | Inlier and outlier labels |
| 10 | [Export](export.md) | CSV downloads |

## ✅ Operating Sequence

1. Start the Streamlit application.
2. Load `CombinedSchedules.xlsx`.
3. Confirm the dataframe loaded correctly.
4. Select the analytical section from the sidebar.
5. Select numeric or categorical columns required by the workflow.
6. Review generated tables, charts, and captions.
7. Adjust parameters only when the analytical rationale is clear.
8. Export reviewable outputs after validating selected columns and results.

## 🔗 Related Pages

| Page | Scope |
|---|---|
| [Modeling](modeling.md) | Projection, grouping, class-separation, and anomaly-screening methods available in `app.py`. |
| [Forecasting](forecasting.md) | Multi-year trajectory analysis using `PY`, `CY`, `BY`, and outyear fields. |
