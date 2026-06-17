# Clustering

The Clustering section groups records based on selected numeric feature patterns.

## 🧭 Purpose

Assign Schedule-X records to similarity groups using standardized numeric feature matrices.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Numeric feature selection | Numeric coercion and missing-row removal | Complete feature matrix |
| Complete feature matrix | Standardization | Scaled feature matrix |
| Scaled feature matrix | Clustering algorithm | Cluster labels |
| Cluster labels | Summary and projection | Counts, sample labels, PCA chart |

## 🧰 Algorithms

| Algorithm | Parameters | Label Behavior |
|---|---|---|
| k-Means | `k clusters` | Assigns each record to one of `k` clusters |
| DBSCAN | `eps`, `min_samples` | Assigns dense-region clusters and possible noise labels |
| Agglomerative | `n_clusters` | Assigns hierarchical clusters by fixed count |

## 📊 Outputs

| Output | Content |
|---|---|
| Cluster Membership | Selected features plus assigned cluster label |
| Cluster Counts | Number of records per cluster |
| PCA Projection | PC1 versus PC2 scatter colored by cluster |
| Silhouette Score | Separation score when valid and computable |

## ✅ Review Sequence

1. Select numeric fields representing a coherent analytical profile.
2. Start with k-Means for simple grouping.
3. Use DBSCAN when irregular cluster shape or noise detection is needed.
4. Use Agglomerative clustering for hierarchical grouping behavior.
5. Review cluster counts for imbalance.
6. Inspect feature summaries for practical interpretability.
7. Treat clusters as analytical groupings, not authoritative classifications.

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Empty labels | Check selected columns for missing or nonnumeric values. |
| One dominant cluster | Adjust selected features or algorithm parameters. |
| Many DBSCAN noise records | Increase `eps` or reduce feature noise. |
| Silhouette unavailable | Confirm more than one non-noise cluster exists. |
