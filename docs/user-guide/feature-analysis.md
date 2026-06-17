# Feature Analysis

The Feature Analysis section supports correlation review, PCA projection, LDA class separation, and optional k-Means grouping.

## 🧭 Purpose

Identify relationships, dominant variation patterns, class separation, and feature-driven group structure in selected numeric Schedule-X fields.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Numeric feature set | Correlation matrix | Pearson, Spearman, or Kendall correlations |
| Numeric feature set | PCA | Explained variance and component projection |
| Numeric feature set plus categorical target | LDA | Discriminant projection |
| Numeric feature set | k-Means | Cluster counts and feature summaries |

## 🔗 Correlation Methods

| Method | Analytical Use |
|---|---|
| Pearson | Linear association between numeric fields |
| Spearman | Monotonic rank association |
| Kendall | Rank association with conservative behavior |

## 📉 PCA Output

| Output | Use |
|---|---|
| Explained variance ratio | Identify how much variance each component captures. |
| PC1 versus PC2 projection | Visualize high-level record structure. |
| Optional categorical coloring | Compare projection patterns across categories. |

## 🎯 LDA Output

| Requirement | Constraint |
|---|---|
| Categorical target | At least two target classes |
| Numeric rows | Enough complete numeric records after coercion |
| Component count | Limited by class count and projection dimension |

## ✅ Review Sequence

1. Select comparable numeric fields.
2. Review correlation matrix before projection.
3. Run PCA and inspect explained variance.
4. Use categorical coloring where meaningful.
5. Run LDA only when the selected categorical target is analytically valid.
6. Use k-Means summaries to compare average feature profiles by cluster.

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Empty feature set | Select at least one numeric field. |
| PCA projection empty | Check missing values after numeric coercion. |
| LDA target invalid | Select a categorical field with at least two classes. |
| Weak cluster separation | Adjust selected features or cluster count. |
