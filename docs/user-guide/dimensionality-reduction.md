# Dimensionality Reduction

The Dimensionality Reduction section projects selected numeric fields into lower-dimensional representations.

## 🧭 Purpose

Transform high-dimensional Schedule-X numeric feature matrices into two-dimensional or multi-component projections for visual inspection and structural analysis.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Numeric columns | Numeric coercion | Numeric feature matrix |
| Numeric feature matrix | Missing-row removal | Complete analysis matrix |
| Complete matrix | Standardization | Scaled matrix |
| Scaled matrix | Projection method | Component dataframe |
| Component dataframe | Scatter chart | Two-dimensional visualization |

## 🧰 Methods

| Method | Output Columns | Use |
|---|---|---|
| PCA | `PC1`, `PC2`, ... | Linear variance projection |
| TruncatedSVD | `SVD1`, `SVD2`, ... | Matrix factorization projection |
| FactorAnalysis | `FA1`, `FA2`, ... | Latent-factor projection |
| IncrementalPCA | `IPCA1`, `IPCA2`, ... | Incremental PCA-style projection |
| t-SNE | `TSNE1`, `TSNE2` | Nonlinear local-neighborhood visualization |
| UMAP | `UMAP1`, `UMAP2`, ... | Nonlinear manifold visualization when installed |

## ✅ Review Sequence

1. Select fields with comparable analytical meaning.
2. Start with PCA for interpretability.
3. Review explained variance when PCA is selected.
4. Use SVD or FactorAnalysis for alternative linear structure checks.
5. Use t-SNE or UMAP for exploratory visual grouping.
6. Validate patterns against known account, agency, line, or classification structure.

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Projection empty | Check missing values in selected columns. |
| UMAP unavailable | Install `umap-learn` or choose another method. |
| t-SNE unavailable | Confirm scikit-learn manifold support is installed. |
| Crowded scatter plot | Reduce feature set or filter the dataset before projection. |
