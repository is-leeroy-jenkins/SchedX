# Forecasting

Schedx supports multi-year Schedule-X trajectory analysis using prior-year, current-year, budget-year, and outyear fields.

## 🧭 Purpose

Analyze budget profiles across `PY`, `CY`, `BY`, and `OY-1` through `OY-9` fields through descriptive review, projection, clustering, and anomaly screening.

## 🧱 Source-Grounded Scope

| Capability | Status |
|---|---|
| Multi-year field analysis | Supported through selected numeric columns |
| Outyear profile comparison | Supported through descriptive statistics, projection, clustering, and anomaly detection |
| Formal time-series forecasting model | Not implemented in `app.py` |
| ARIMA, exponential smoothing, or Prophet | Not implemented in `app.py` |
| Forecast export | Not implemented as a dedicated output |

## 📈 Schedule-X Time Fields

| Field | Position |
|---|---|
| `PY` | Prior Year |
| `CY` | Current Year |
| `BY` | Budget Year |
| `OY-1` | Outyear 1 |
| `OY-2` | Outyear 2 |
| `OY-3` | Outyear 3 |
| `OY-4` | Outyear 4 |
| `OY-5` | Outyear 5 |
| `OY-6` | Outyear 6 |
| `OY-7` | Outyear 7 |
| `OY-8` | Outyear 8 |
| `OY-9` | Outyear 9 |

## 🔄 Trajectory Analysis Pattern

| Stage | Operation | Output |
|---|---|---|
| Field selection | Select `PY`, `CY`, `BY`, and outyear fields | Multi-year numeric feature set |
| Descriptive review | Compute expanded statistics | Distribution and outlier profile |
| Projection | Run PCA or related methods | Two-dimensional trajectory structure |
| Grouping | Run clustering on multi-year fields | Similar trajectory groups |
| Screening | Run anomaly detection on multi-year fields | Unusual trajectory records |
| Export | Download raw or anomaly CSV | Reviewable extract |

## ✅ Recommended Trajectory Sequence

1. Select `PY`, `CY`, `BY`, and available outyear fields.
2. Review missing values and numeric coercion behavior.
3. Compare central tendency and dispersion across time fields.
4. Inspect outlier counts for each year field.
5. Use PCA to identify dominant multi-year variance patterns.
6. Use clustering to group similar budget trajectories.
7. Use anomaly detection to flag unusual multi-year profiles.
8. Validate flagged records against policy, program, and account context.

## 🧯 Interpretation Controls

| Control | Requirement |
|---|---|
| Outyear availability | Missing outyear fields reduce trajectory completeness. |
| Account comparability | Compare records within meaningful agency, account, or line contexts. |
| Scale effects | Standardized matrices emphasize relative pattern rather than raw magnitude. |
| Policy changes | Known program changes can appear as statistical anomalies. |
| Formal forecasts | Export data to a dedicated forecasting model when predictive estimates are required. |
