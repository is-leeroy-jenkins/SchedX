# Data Expectations

Schedx is designed for Schedule-X-style budget datasets stored in Excel workbooks.

## 🧭 Purpose

This page documents the expected workbook layout, field conventions, and data hygiene assumptions used by the application.

## 📘 Workbook

The primary workbook is expected to be:

| Item                          | Value                                 |
|-------------------------------|---------------------------------------|
| File                          | `CombinedSchedules.xlsx`              |
| Preferred sheet               | `Data`                                |
| Fallback sheet                | First worksheet in the workbook       |
| Preferred local path          | `stores/excel/CombinedSchedules.xlsx` |
| Optional environment variable | `SCHEDULEX_COMBINED_PATH`             |

## 🔍 Loader Order

Schedx attempts to load data in this order:

1. Uploaded workbook from the Streamlit sidebar.
2. Sidebar fallback path.
3. `stores/excel/CombinedSchedules.xlsx`.
4. Current working directory equivalent of `stores/excel/CombinedSchedules.xlsx`.
5. Path supplied by `SCHEDULEX_COMBINED_PATH`.

If no usable workbook is found, the loader returns an empty dataframe and the app stops with a warning.

## 📊 Expected Schedule-X Fields

Common Schedule-X fields include:

| Field            | Meaning                                 |
|------------------|-----------------------------------------|
| `PY`             | Prior Year                              |
| `CY`             | Current Year                            |
| `BY`             | Budget Year                             |
| `OY-1`           | Outyear 1                               |
| `OY-2`           | Outyear 2                               |
| `OY-3`           | Outyear 3                               |
| `OY-4`           | Outyear 4                               |
| `OY-5`           | Outyear 5                               |
| `OY-6`           | Outyear 6                               |
| `OY-7`           | Outyear 7                               |
| `OY-8`           | Outyear 8                               |
| `OY-9`           | Outyear 9                               |
| `AgencyCode`     | Agency identifier where present         |
| `BureauCode`     | Bureau identifier where present         |
| `MainAccount`    | Treasury main account where present     |
| `TreasurySymbol` | Treasury account symbol where present   |
| `AccountName`    | Account title where present             |
| `LineName`       | Schedule line description where present |
| `Line`           | Schedule line number where present      |
| `Subfunction`    | Budget subfunction where present        |

## 🧹 Data Hygiene

Schedx uses several defensive data-preparation practices:

| Practice            | Purpose                                                                     |
|---------------------|-----------------------------------------------------------------------------|
| Numeric coercion    | Converts selected features to numeric values for modeling and statistics.   |
| Missing-row removal | Removes incomplete rows before matrix-based operations.                     |
| Boolean exclusion   | Prevents boolean columns from being treated as numeric analysis features.   |
| Standardization     | Scales numeric matrices before PCA, SVD, clustering, and anomaly detection. |
| Empty-data fallback | Prevents downstream failures when no valid records are available.           |

## ✅ Recommended Preparation

Before loading a workbook:

1. Confirm the target sheet is named `Data`.
2. Confirm budget-year and outyear columns are numeric.
3. Remove merged cells from analytical regions.
4. Preserve account and classification identifiers as categorical fields.
5. Validate totals against authoritative OMB or Treasury sources before operational use.
