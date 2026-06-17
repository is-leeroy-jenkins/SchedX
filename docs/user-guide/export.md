# Export

The Export section creates downloadable CSV files from loaded or derived Schedx outputs.

## 🧭 Purpose

Produce reviewable, portable data extracts for spreadsheet analysis, audit support, notebook workflows, or downstream reporting.

## 📤 Export Types

| Export | File Name | Source |
|---|---|---|
| Raw data | `schedulex_raw.csv` | Loaded dataframe |
| Anomalies | `schedulex_anomalies.csv` | Records labeled `-1` in Anomaly Detection |

## ✅ Export Sequence

1. Confirm the workbook loaded correctly.
2. Review sample rows and feature summary.
3. Run the analytical workflow required for derived outputs.
4. Confirm selected features and parameter values.
5. Inspect displayed results.
6. Download the CSV.
7. Save the export with the source workbook and run notes.

## 🧾 Recommended Run Notes

| Field | Content |
|---|---|
| Source workbook | Workbook name and date |
| Sheet | Worksheet used |
| Section | Schedx workflow used |
| Features | Selected numeric or categorical fields |
| Parameters | Algorithm settings |
| Export file | Downloaded CSV name |
| Reviewer | Analyst or reviewer name |
| Validation | Source or control total checked |

## 🧯 Corrections

| Problem | Correction |
|---|---|
| Raw export unexpected | Return to Overview and confirm loaded workbook. |
| Anomaly export unavailable | Run Anomaly Detection first. |
| CSV encoding issue | Open with UTF-8 support. |
| Export lacks expected fields | Confirm selected dataframe and workflow output before download. |
