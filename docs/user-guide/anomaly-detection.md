# Anomaly Detection

The Anomaly Detection section identifies records with atypical numeric feature patterns.

## 🧭 Purpose

Screen Schedule-X records for unusual amounts, combinations, or trajectories using selected numeric features.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Numeric feature selection | Numeric coercion and missing-row removal | Complete feature matrix |
| Complete feature matrix | Standardization | Scaled matrix |
| Scaled matrix | Anomaly detector | Inlier and outlier predictions |
| Outlier predictions | Filter anomaly records | Review table and CSV download |

## 🧰 Detectors

| Method | Parameters | Output Labels |
|---|---|---|
| Isolation Forest | `n_estimators` | `1` inlier, `-1` anomaly |
| One-Class SVM | `nu` | `1` inlier, `-1` anomaly |
| Local Outlier Factor | `n_neighbors`, `contamination` | `1` inlier, `-1` anomaly |
| Elliptic Envelope | `contamination` | `1` inlier, `-1` anomaly |

## ✅ Review Sequence

1. Select numeric fields that represent the pattern under review.
2. Choose a detector aligned to the expected anomaly shape.
3. Set method parameters conservatively.
4. Review the anomaly count.
5. Inspect flagged records.
6. Compare anomalies against known program, account, or policy changes.
7. Download anomaly CSV only after confirming the selected feature set.

## 🧯 Corrections

| Problem | Correction |
|---|---|
| No anomalies | Adjust parameters or select different features. |
| Too many anomalies | Lower contamination or review feature selection. |
| Empty results | Check missing values after numeric coercion. |
| False positives | Validate against account context and authoritative sources. |
