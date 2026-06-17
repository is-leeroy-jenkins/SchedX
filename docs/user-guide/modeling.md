# Modeling

Schedx provides exploratory modeling workflows for projection, grouping, class separation, and anomaly screening.

## 🧭 Purpose

Identify structure, separation, similarity, and atypical records in Schedule-X-style budget data using numeric feature matrices derived from selected columns.

## 🧱 Source-Grounded Methods

| Method | Schedx Location | Analytical Role |
|---|---|---|
| PCA | Feature Analysis, Dimensionality Reduction | Linear variance projection |
| TruncatedSVD | Dimensionality Reduction | Matrix factorization projection |
| FactorAnalysis | Dimensionality Reduction | Latent-factor projection |
| IncrementalPCA | Dimensionality Reduction | Incremental PCA-style projection |
| t-SNE | Dimensionality Reduction | Nonlinear local-neighborhood visualization |
| UMAP | Dimensionality Reduction | Nonlinear manifold visualization when installed |
| Linear Discriminant Analysis | Feature Analysis | Categorical class-separation projection |
| k-Means | Feature Analysis, Clustering | Fixed-count similarity grouping |
| DBSCAN | Clustering | Density-based grouping and noise identification |
| Agglomerative clustering | Clustering | Hierarchical fixed-count grouping |
| Isolation Forest | Anomaly Detection | Tree-based outlier screening |
| One-Class SVM | Anomaly Detection | Boundary-based novelty screening |
| Local Outlier Factor | Anomaly Detection | Local-density outlier screening |
| Elliptic Envelope | Anomaly Detection | Robust covariance outlier screening |

## 🔄 Shared Processing Pattern

| Stage | Operation |
|---|---|
| Feature selection | User selects numeric columns in the Streamlit section. |
| Numeric coercion | Selected fields are converted to numeric values. |
| Missing-value handling | Rows with missing selected values are removed for matrix operations. |
| Standardization | Feature matrices are scaled with `StandardScaler`. |
| Estimator execution | The selected scikit-learn or optional estimator is fit or applied. |
| Output rendering | Results are displayed as tables, charts, labels, counts, or downloads. |

## 📊 Projection Workflows

| Workflow | Output |
|---|---|
| PCA | Component dataframe and fitted PCA model |
| TruncatedSVD | Component dataframe |
| FactorAnalysis | Component dataframe |
| IncrementalPCA | Component dataframe |
| t-SNE | Two-component dataframe |
| UMAP | Component dataframe when UMAP is installed |

## 🧩 Grouping Workflows

| Workflow | Output |
|---|---|
| k-Means | Cluster labels indexed to rows used for clustering |
| DBSCAN | Cluster or noise labels indexed to rows used for clustering |
| Agglomerative clustering | Cluster labels indexed to rows used for clustering |

## 🚨 Anomaly Workflows

| Workflow | Output |
|---|---|
| Isolation Forest | `1` for inlier and `-1` for anomaly |
| One-Class SVM | `1` for inlier and `-1` for anomaly |
| Local Outlier Factor | `1` for inlier and `-1` for anomaly |
| Elliptic Envelope | `1` for inlier and `-1` for anomaly |

## ✅ Modeling Sequence

1. Confirm loaded data in the Overview section.
2. Inspect missing values and numeric field availability.
3. Run Descriptive Statistics before matrix-based workflows.
4. Review correlations before selecting projection or clustering features.
5. Use PCA for the first projection pass.
6. Use clustering only after selecting coherent numeric features.
7. Use anomaly detection as a screening workflow.
8. Validate results against agency, account, line, and budget-context knowledge.

## 🧯 Interpretation Controls

| Control | Requirement |
|---|---|
| Feature coherence | Selected fields must describe a comparable analytical profile. |
| Missingness | High missingness reduces matrix representativeness. |
| Scaling | Standardization changes magnitude interpretation. |
| Class targets | LDA requires meaningful categorical targets. |
| Cluster labels | Cluster assignments require analytical validation. |
| Anomaly labels | Outlier flags require source-data review. |
