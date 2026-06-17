# Inferential Statistics

The Inferential Statistics section computes pairwise and grouped statistical tests for selected numeric and categorical fields.

## 🧭 Purpose

Evaluate differences between numeric fields and associations across categorical classifications in Schedule-X-style data.

## 🧱 Workflow Position

| Input | Process | Output |
|---|---|---|
| Two or more numeric columns | Welch's t-tests | Pairwise t-statistics and p-values |
| Two or more numeric columns | Mann-Whitney U tests | Pairwise U statistics and p-values |
| Numeric columns plus categorical group | One-way ANOVA | F-statistics and p-values |
| Two categorical columns | Chi-square test | Chi-square statistic, p-value, contingency table |

## 🧪 Test Selection

| Test | Use |
|---|---|
| Welch's t-test | Compare means between numeric fields without assuming equal variance. |
| Mann-Whitney U | Compare distributions using a nonparametric rank-based test. |
| ANOVA | Test whether numeric values differ across categories. |
| Chi-square | Test association between two categorical fields. |

## ✅ Review Sequence

1. Select at least two numeric columns for pairwise tests.
2. Use Mann-Whitney U when normality assumptions are weak.
3. Select a categorical grouping field for ANOVA.
4. Select two categorical fields for chi-square.
5. Interpret p-values with analytical context and source-data knowledge.
6. Use results as screening evidence, not final audit conclusions.

## 🧯 Corrections

| Problem | Correction |
|---|---|
| No numeric columns | Confirm amount fields are numeric or coercible. |
| Fewer than two numeric selections | Select at least two fields. |
| No categorical grouping field | Confirm object/category columns are present. |
| Sparse contingency table | Consolidate categories or use a more stable grouping field. |
