# Descriptive Statistics

The Descriptive Statistics section computes expanded statistics and distribution diagnostics for selected numeric columns.

## 🧭 Purpose

Quantify central tendency, dispersion, distribution shape, missingness, and outlier prevalence for Schedule-X numeric fields.

## 🧱 Workflow Position

| Input           | Process                                  | Output                  |
|-----------------|------------------------------------------|-------------------------|
| Numeric columns | Select one or more fields                | Analysis feature set    |
| Selected fields | Compute expanded descriptive metrics     | Statistics table        |
| Selected fields | Plot histograms                          | Distribution charts     |
| Selected fields | Compute skewness, kurtosis, IQR outliers | Interpretation captions |

## 📊 Metrics

| Metric         | Definition                                                |
|----------------|-----------------------------------------------------------|
| `count`        | Non-null observation count                                |
| `missing`      | Missing observation count                                 |
| `mean`         | Arithmetic average                                        |
| `median`       | Middle value                                              |
| `std`          | Sample standard deviation                                 |
| `mad`          | Median absolute deviation                                 |
| `cv`           | Standard deviation divided by mean                        |
| `skewness`     | Distribution asymmetry                                    |
| `kurtosis`     | Tail weight and peak behavior                             |
| `min`          | Minimum value                                             |
| `1%`           | First percentile                                          |
| `25%`          | First quartile                                            |
| `75%`          | Third quartile                                            |
| `99%`          | Ninety-ninth percentile                                   |
| `max`          | Maximum value                                             |
| `IQR`          | Third quartile minus first quartile                       |
| `outliers_iqr` | Count outside `Q1 - 1.5*IQR` or `Q3 + 1.5*IQR`            |
| `outliers_z`   | Count with absolute Z-score greater than 3                |
| `ks_stat`      | Kolmogorov-Smirnov statistic against normal approximation |
| `ks_pval`      | Kolmogorov-Smirnov p-value                                |

## ✅ Review Sequence

1. Select core budget fields first.
2. Compare `mean` and `median` for skew.
3. Review `missing` before test selection.
4. Review `std`, `mad`, and `cv` for dispersion.
5. Inspect `outliers_iqr` and `outliers_z` before clustering or anomaly screening.
6. Use histograms to identify heavy tails, spikes, and concentration near zero.

## 🧯 Corrections

| Finding             | Correction                                                                    |
|---------------------|-------------------------------------------------------------------------------|
| Empty selection     | Select at least one numeric column.                                           |
| Extreme skewness    | Review whether zeros, account closures, or large programs dominate the field. |
| High outlier counts | Validate source data and run anomaly detection for targeted review.           |
| Unstable `cv`       | Check whether the mean is near zero.                                          |
