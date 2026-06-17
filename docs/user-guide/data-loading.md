# Data Loading

Schedx loads Schedule-X-style Excel data from a Streamlit upload control or from a local fallback path.

## 🧭 Purpose

Create the dataframe used by all downstream overview, statistics, projection, clustering, anomaly, and export workflows.

## 📥 Accepted Input

| Input | Requirement |
|---|---|
| Workbook | Excel file readable by pandas and openpyxl |
| Preferred filename | `CombinedSchedules.xlsx` |
| Preferred sheet | `Data` |
| Fallback sheet | First worksheet when `Data` is unavailable |
| Sidebar upload | `.xlsx` file |
| Sidebar fallback path | Local filesystem path |
| Environment fallback | `SCHEDULEX_COMBINED_PATH` |

## 🔄 Load Order

1. Uploaded workbook from the sidebar.
2. Sidebar fallback path.
3. `stores/excel/CombinedSchedules.xlsx`.
4. Current-working-directory equivalent of `stores/excel/CombinedSchedules.xlsx`.
5. Path from `SCHEDULEX_COMBINED_PATH`.

## 🧹 Data Preparation

| Preparation | Behavior |
|---|---|
| Sheet selection | Attempts `Data` first and first sheet second. |
| Empty result | Returns an empty dataframe when no source can be read. |
| Numeric detection | Selects numeric columns and excludes booleans. |
| Categorical detection | Selects object and category columns. |
| Matrix workflows | Coerces selected columns to numeric and removes incomplete rows. |

## ✅ Load Verification

| Check | Expected Result |
|---|---|
| Application status | No `No data` warning |
| Sample rows | Records appear in the Overview section |
| Feature summary | Columns show dtype, unique count, and missing count |
| Numeric snapshot | Budget amount fields appear as numeric |
| Sidebar section selector | Analysis sections remain available |

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Empty dataframe | Upload a valid workbook or correct the fallback path. |
| Missing `Data` sheet | Rename the sheet or rely on the first-sheet fallback. |
| Numeric fields absent | Convert amount columns to numeric values in the workbook. |
| Unexpected categories | Confirm identifier columns are stored consistently. |
