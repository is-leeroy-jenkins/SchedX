# Development

This page documents the validation workflow for maintaining Schedx and its MkDocs documentation.

## 🧭 Purpose

Schedx documentation should build cleanly, render correctly, and remain aligned with the behavior of `app.py`.

## 🧪 Source Validation

Compile the main application:

    python -m py_compile .\app.py

Compile the project:

    python -m compileall .

Run the Streamlit app:

    streamlit run app.py

## 📚 Documentation Build

Build the documentation site:

    mkdocs build

Serve the documentation locally:

    mkdocs serve

## ✅ MkDocs Quality Gates

| Gate | Expected Result |
|---|---|
| Python compile | `app.py` compiles without syntax errors. |
| MkDocs build | Site builds without missing-page warnings. |
| mkdocstrings import | `app.py` imports for API rendering. |
| griffe parsing | Docstrings render without malformed-section warnings. |
| Navigation | Every generated Markdown page is listed in `mkdocs.yml`. |
| CSS | Dark-mode styling loads from `assets/css/schedx.css`. |
| JS | Documentation enhancements load from `assets/js/schedx.js`. |

## 🧾 Docstring Standard

Use Google-style docstrings for public functions.

Preferred format:

    """Compute expanded descriptive statistics for selected numeric columns.

    Purpose:
        Builds a statistics table for numeric Schedule-X fields, including central
        tendency, dispersion, shape, outlier counts, and normality diagnostics.

    Args:
        df: Source dataframe containing Schedule-X records.
        cols: Numeric columns to summarize.

    Returns:
        pd.DataFrame: Descriptive statistics indexed by column name.
    """

Avoid underline-style sections such as:

    Purpose:
    --------

Avoid malformed return sections such as:

    Returns:
        Output value.

Use an explicit return type description:

    Returns:
        pd.DataFrame: Descriptive statistics indexed by column name.

## 🧯 Build Warning Corrections

| Warning | Cause | Fix |
|---|---|---|
| Page exists but is not in nav | A Markdown file exists outside `mkdocs.yml` navigation. | Add it to `nav` or delete the unused file. |
| Nav page not found | `mkdocs.yml` references a missing file. | Create the file or remove the nav entry. |
| Failed to get name-description pair | A docstring section is malformed. | Use `name: description` under `Args:` or `Attributes:`. |
| No type or annotation for returned value | Return type is missing or unclear. | Add a return annotation or explicit `Returns:` type. |
| mkdocstrings import failure | The API target cannot be imported. | Install dependencies and check top-level Streamlit execution behavior. |

## 🔁 Recommended Change Sequence

1. Modify source or documentation.
2. Compile `app.py`.
3. Build MkDocs.
4. Fix griffe or nav warnings.
5. Run `mkdocs serve`.
6. Inspect API, tables, code blocks, search, and navigation.
7. Commit only after the app and documentation both validate.
