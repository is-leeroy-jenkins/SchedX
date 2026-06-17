# Data Overview

The Overview section provides the first inspection layer after data loading.

## 🧭 Purpose

Validate loaded records, column structure, missing values, and numeric summary distributions before running deeper analytical workflows.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Loaded dataframe | Display first 300 rows | Sample table |
| Loaded dataframe | Count data types, unique values, missing values | Feature summary |
| Numeric columns | Compute percentile-rich `describe()` output | Numeric snapshot |

## 📊 Outputs

| Output | Content | Use |
|---|---|---|
| Sample | First 300 records | Confirm workbook and sheet selection |
| Feature summary | dtype, unique count, missing count | Identify usable numeric and categorical fields |
| Numeric snapshot | count, mean, std, min, percentiles, max | Inspect baseline amount distributions |

## ✅ Review Sequence

1. Confirm the sample table contains the expected Schedule-X records.
2. Verify core fields such as `PY`, `CY`, `BY`, and outyears are present.
3. Review missing counts before selecting columns for tests or models.
4. Confirm categorical identifiers are available for grouping and coloring.
5. Confirm numeric fields are present before using projection, clustering, or anomaly detection.

## 🧯 Corrections

| Finding | Correction |
|---|---|
| Wrong records displayed | Check workbook, worksheet, or fallback path. |
| Numeric fields typed as object | Correct workbook formatting or rely on numeric coercion in downstream workflows. |
| High missing counts | Filter or clean source data before matrix-based analysis. |
| Unexpected unique counts | Review identifier consistency and category encoding. |
