'''
  ******************************************************************************************
      Assembly:                Schedule-X
      Filename:                app.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file='app.py' company='Terry D. Eppler'>

	     app.py
	     Copyright ©  2022  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    app.py
  </summary>
  ******************************************************************************************
'''
from __future__ import annotations

import math
import random
from typing import Optional, Sequence, Tuple, Any, Dict

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from scipy import stats
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA, TruncatedSVD, FactorAnalysis, IncrementalPCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import silhouette_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Optional / best-effort imports (fall back if unavailable)
try:
    import plotly.express as px  # type: ignore
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

# Try importing umap and openTSNE / sklearn.manifold TSNE as fallbacks
try:
    import umap  # type: ignore
    UMAP_AVAILABLE = True
except Exception:
    UMAP_AVAILABLE = False

try:
    from sklearn.manifold import TSNE  # type: ignore
    TSNE_AVAILABLE = True
except Exception:
    TSNE_AVAILABLE = False

# -----------------------------------------------------------------------------
# Utility helpers (style and guards)
# -----------------------------------------------------------------------------
def throw_if(name: str, value: Any) -> None:
    """
    Purpose:
    --------
    Guard to raise a ValueError when a required argument is missing or falsy.

    Parameters:
    -----------
    name: str
        Name of the parameter for the error message.
    value: Any
        Value to validate.

    Returns:
    --------
    None
    """
    if not value:
        raise ValueError(f"Required parameter '{name}' is missing or empty.")


def fmt_num(x: float) -> str:
    """Format a number with comma and 3 decimal places where applicable."""
    try:
        if abs(x) >= 1:
            return f"{x:,.3f}"
        return f"{x:.6f}"
    except Exception:
        return str(x)


# -----------------------------------------------------------------------------
# Streamlit page config
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Schedule-X — Analysis", layout="wide")
sns.set_style("whitegrid")


# -----------------------------------------------------------------------------
# Data loading and basic column selection
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)
def load_excel(uploaded_file: Optional[io.BytesIO], fallback_path: Optional[str]) -> pd.DataFrame:
    """
    Purpose:
    --------
    Load the Excel workbook either from an uploaded file or a local fallback path.
    Expects a sheet named 'Data' (as the notebook does). Returns DataFrame.

    Parameters:
    -----------
    uploaded_file: Optional[io.BytesIO]
        BytesIO from Streamlit uploader.
    fallback_path: Optional[str]
        Local path to attempt if uploader is empty.

    Returns:
    --------
    pd.DataFrame
    """
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name="Data")
        return df
    if fallback_path:
        df = pd.read_excel(fallback_path, sheet_name="Data")
        return df
    return pd.DataFrame()


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return numeric column names (excluding booleans)."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def categorical_columns(df: pd.DataFrame) -> list[str]:
    """Return object/categorical column names."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


# -----------------------------------------------------------------------------
# Extended descriptive statistics
# -----------------------------------------------------------------------------
def safe_mad(series: pd.Series, scaled: bool = False) -> float:
    """
    Purpose:
    --------
    Compute the Median Absolute Deviation (MAD) robustly without depending on
    SciPy version. Returns unscaled MAD by default. If `scaled=True`, returns
    the consistency-corrected MAD (approx *1.4826) for normal distributions.

    Parameters:
    -----------
    series: pd.Series
        Numeric series (may contain NaNs).
    scaled: bool
        If True, return MAD scaled for normal consistency.

    Returns:
    --------
    float: MAD (or np.nan if no values).
    """
    arr = np.asarray(series.dropna(), dtype=float)
    if arr.size == 0:
        return float("nan")
    mad = float(np.median(np.abs(arr - np.median(arr))))
    if scaled:
        return mad * 1.4826
    return mad


# Replace the existing expanded_descriptive function with this:
def expanded_descriptive(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    """
    Purpose:
    --------
    Compute an expanded descriptive statistics DataFrame for the requested
    numeric columns. Uses a safe fallback for MAD if SciPy lacks the function.

    Parameters:
    -----------
    df: pd.DataFrame
        Source dataframe.
    cols: Sequence[str]
        Numeric columns to analyze.

    Returns:
    --------
    pd.DataFrame
        Table of descriptive metrics for each column.
    """
    metrics: Dict[str, Dict[str, float]] = {}
    for c in cols:
        series = pd.to_numeric(df[c], errors="coerce")
        n = int(series.count())
        missing = int(series.isna().sum())

        mean = float(series.mean()) if n else float("nan")
        median = float(series.median()) if n else float("nan")
        std = float(series.std(ddof=1)) if n else float("nan")

        # MAD: try SciPy first (if available), otherwise use safe_mad()
        try:
            # some SciPy versions expose median_absolute_deviation
            mad_val = stats.median_absolute_deviation(series.dropna())
            # stats.median_absolute_deviation may return ndarray/scalar; coerce
            mad = float(np.asarray(mad_val).item())
        except Exception:
            mad = float(safe_mad(series, scaled=False))

        skew = float(series.skew()) if n else float("nan")
        kurt = float(series.kurtosis()) if n else float("nan")
        cv = float(std / mean) if mean and not math.isnan(mean) else float("nan")
        q1 = float(series.quantile(0.25)) if n else float("nan")
        q3 = float(series.quantile(0.75)) if n else float("nan")
        iqr = q3 - q1
        p99 = float(series.quantile(0.99)) if n else float("nan")
        p01 = float(series.quantile(0.01)) if n else float("nan")
        minimum = float(series.min()) if n else float("nan")
        maximum = float(series.max()) if n else float("nan")
        # Outlier counts by IQR rule and Z-score
        outlier_iqr = int(((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum()) if n else 0
        zscores = (series - mean) / std if n and std and not math.isnan(std) else pd.Series(dtype=float)
        outlier_z = int((zscores.abs() > 3).sum()) if not zscores.empty else 0
        # Basic distribution fit stats (KS test vs normal)
        ks_stat, ks_pval = (float("nan"), float("nan"))
        try:
            clean = series.dropna()
            if clean.size > 8:
                ks_stat, ks_pval = stats.kstest((clean - clean.mean()) / clean.std(ddof=1), "norm")
        except Exception:
            ks_stat, ks_pval = (float("nan"), float("nan"))

        metrics[c] = {
            "count": n,
            "missing": missing,
            "mean": mean,
            "median": median,
            "std": std,
            "mad": mad,
            "cv": cv,
            "skewness": skew,
            "kurtosis": kurt,
            "min": minimum,
            "1%": p01,
            "25%": q1,
            "75%": q3,
            "99%": p99,
            "max": maximum,
            "IQR": iqr,
            "outliers_iqr": outlier_iqr,
            "outliers_z": outlier_z,
            "ks_stat": ks_stat,
            "ks_pval": ks_pval,
        }

    table = pd.DataFrame.from_dict(metrics, orient="index")
    preferred = [
        "count", "missing", "mean", "median", "std", "mad", "cv",
        "skewness", "kurtosis", "min", "1%", "25%", "75%", "99%", "max",
        "IQR", "outliers_iqr", "outliers_z", "ks_stat", "ks_pval",
    ]
    cols_ordered = [c for c in preferred if c in table.columns] + [c for c in table.columns if c not in preferred]
    return table[cols_ordered]


# -----------------------------------------------------------------------------
# Inferential statistics utilities
# -----------------------------------------------------------------------------
def pairwise_ttests(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    """
    Purpose:
    --------
    Compute pairwise Welch's t-tests for the provided numeric columns.

    Parameters:
    -----------
    df: pd.DataFrame
    cols: Sequence[str]

    Returns:
    --------
    pd.DataFrame
        Multi-index table with (colA, colB) vs (t-stat, p-value).
    """
    rows = []
    for i, a in enumerate(cols):
        for b in cols[i+1:]:
            s1 = pd.to_numeric(df[a], errors="coerce").dropna()
            s2 = pd.to_numeric(df[b], errors="coerce").dropna()
            if len(s1) < 3 or len(s2) < 3:
                tstat, p = float("nan"), float("nan")
            else:
                tstat, p = stats.ttest_ind(s1, s2, equal_var=False, nan_policy="omit")
            rows.append({"var1": a, "var2": b, "tstat": float(tstat), "pvalue": float(p)})
    if not rows:
        return pd.DataFrame(columns=["var1", "var2", "tstat", "pvalue"])
    return pd.DataFrame(rows)


def anova_test(df: pd.DataFrame, numeric_cols: Sequence[str], cat_col: str) -> pd.DataFrame:
    """
    Purpose:
    --------
    Run one-way ANOVA for each numeric column grouping by categorical column.

    Returns a DataFrame of F-stat and p-value.
    """
    rows = []
    for nc in numeric_cols:
        try:
            groups = [g.dropna().values for _, g in df.groupby(cat_col)[nc]]
            if len(groups) < 2:
                f, p = float("nan"), float("nan")
            else:
                f, p = stats.f_oneway(*groups)
        except Exception:
            f, p = float("nan"), float("nan")
        rows.append({"feature": nc, "F": float(f), "pvalue": float(p)})
    return pd.DataFrame(rows)


def chi2_categorical(df: pd.DataFrame, cat1: str, cat2: str) -> Tuple[float, float, pd.DataFrame]:
    """
    Purpose:
    --------
    Compute chi-square and return the contingency table as well.

    Returns:
    --------
    chi2, pvalue, contingency_table
    """
    ct = pd.crosstab(df[cat1], df[cat2])
    chi2, p, dof, expected = stats.chi2_contingency(ct.fillna(0).astype(int))
    return float(chi2), float(p), ct


# -----------------------------------------------------------------------------
# Dimensionality reduction & clustering wrappers
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)
def compute_pca(df: pd.DataFrame, cols: Sequence[str], n_components: int = 2) -> Tuple[pd.DataFrame, PCA]:
    """
    Purpose:
    --------
    Compute PCA on selected numeric columns. Coerce each column to numeric,
    drop rows with any NaNs, standardize, then fit PCA.

    Returns:
    --------
    (components_dataframe, fitted_pca_model)
    """
    throw_if("cols", cols)
    # Coerce each column individually to numeric (works for multi-column input)
    Xdf = df[list(cols)].apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if Xdf.shape[0] == 0:
        # Return empty DataFrame and a PCA object (with random_state but not fitted)
        return pd.DataFrame(), PCA(n_components=n_components, random_state=0)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xdf)
    pca = PCA(n_components=n_components, random_state=0)
    comps = pca.fit_transform(Xs)
    comps_df = pd.DataFrame(comps,
                            columns=[f"PC{i+1}" for i in range(comps.shape[1])],
                            index=Xdf.index)
    return comps_df, pca


@st.cache_data(ttl=600)
def compute_truncated_svd(df: pd.DataFrame, cols: Sequence[str], n_components: int = 2) -> pd.DataFrame:
    """
    Purpose:
    --------
    Compute truncated SVD projection for numeric columns.
    """
    Xdf = df[list(cols)].apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if Xdf.shape[0] == 0:
        return pd.DataFrame()
    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xdf)
    svd = TruncatedSVD(n_components=n_components, random_state=0)
    comps = svd.fit_transform(Xs)
    return pd.DataFrame(comps,
                        columns=[f"SVD{i+1}" for i in range(n_components)],
                        index=Xdf.index)


@st.cache_data(ttl=600)
def compute_factor_analysis(df: pd.DataFrame, cols: Sequence[str], n_components: int = 2) -> pd.DataFrame:
    """
    Purpose:
    --------
    Compute Factor Analysis projection for numeric columns.
    """
    Xdf = df[list(cols)].apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if Xdf.shape[0] == 0:
        return pd.DataFrame()
    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xdf)
    fa = FactorAnalysis(n_components=n_components, random_state=0)
    comps = fa.fit_transform(Xs)
    return pd.DataFrame(comps,
                        columns=[f"FA{i+1}" for i in range(n_components)],
                        index=Xdf.index)

@st.cache_data(ttl=600)
def run_clustering(df: pd.DataFrame, cols: Sequence[str], method: str, **kwargs) -> pd.Series:
    """
    Purpose:
    --------
    Run clustering on selected numeric columns and return a Series of labels
    indexed to the rows used for clustering.
    """
    Xdf = df[list(cols)].apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if Xdf.shape[0] == 0:
        return pd.Series(dtype=int)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(Xdf)
    method = method.lower()
    if method == "kmeans":
        k = int(kwargs.get("k", 3))
        model = KMeans(n_clusters=k, random_state=0)
        labels = model.fit_predict(Xs)
    elif method == "dbscan":
        eps = float(kwargs.get("eps", 0.5))
        min_samples = int(kwargs.get("min_samples", 5))
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(Xs)
    elif method in ("agglo", "agglomerative", "agglomerativeclustering"):
        n = int(kwargs.get("n_clusters", 3))
        model = AgglomerativeClustering(n_clusters=n)
        labels = model.fit_predict(Xs)
    else:
        raise ValueError(f"Unknown clustering method '{method}'")
    return pd.Series(labels, index=Xdf.index, name="cluster")


# -----------------------------------------------------------------------------
# Anomaly detection wrapper
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)
def detect_anomalies(df: pd.DataFrame, cols: Sequence[str], method: str, **kwargs) -> pd.Series:
    """
    Purpose:
    --------
    Run anomaly detection on selected numeric columns and return Series of
    predictions indexed to the rows used (1 for inlier, -1 for outlier).
    """
    Xdf = df[list(cols)].apply(pd.to_numeric, errors="coerce").dropna(axis=0)
    if Xdf.shape[0] == 0:
        return pd.Series(dtype=int)

    scaler = StandardScaler()
    X = scaler.fit_transform(Xdf)
    method = method.lower()
    if method == "isolation_forest":
        clf = IsolationForest(random_state=0, n_estimators=int(kwargs.get("n_estimators", 100)))
        preds = clf.fit_predict(X)
    elif method == "one_class_svm":
        clf = OneClassSVM(kernel="rbf", nu=float(kwargs.get("nu", 0.05)), gamma="scale")
        preds = clf.fit_predict(X)
    elif method == "lof":
        clf = LocalOutlierFactor(n_neighbors=int(kwargs.get("n_neighbors", 20)),
                                 contamination=float(kwargs.get("contamination", 0.05)))
        preds = clf.fit_predict(X)
    elif method == "elliptic":
        clf = EllipticEnvelope(contamination=float(kwargs.get("contamination", 0.05)), random_state=0)
        clf.fit(X)
        preds = clf.predict(X)
    else:
        raise ValueError(f"Unknown anomaly method '{method}'")
    return pd.Series(preds, index=Xdf.index, name="anomaly")


# -----------------------------------------------------------------------------
# Plot helpers
# -----------------------------------------------------------------------------
def style_dataframe(df: pd.DataFrame, precision: int = 3) -> pd.DataFrame:
    """
    Purpose:
    --------
    Return a pandas Styler-applied DataFrame for nicer display in Streamlit.
    """
    styled = df.copy()
    # Format floats with reasonable precision
    float_cols = styled.select_dtypes(include=[np.floating]).columns
    for c in float_cols:
        styled[c] = styled[c].map(lambda x: (f"{x:,.{precision}f}" if pd.notna(x) else ""))
    return styled


def show_styled_table(df: pd.DataFrame, height: int = 350) -> None:
    """
    Purpose:
    --------
    Present a dataframe in Streamlit with a subtle gradient to highlight magnitudes.

    Notes:
    ------
    Uses pandas Styler for background_gradient; st.dataframe renders it nicely.
    """
    if df.empty:
        st.info("No rows to show.")
        return
    # Use Styler background gradient on numeric columns
    sty = df.style.background_gradient(axis=0, cmap="Blues").format(na_rep="", precision=4)
    st.dataframe(sty, height=height)


def scatter_plot(df: pd.DataFrame, x: str, y: str, hue: Optional[str] = None, size: Optional[str] = None) -> None:
    """
    Purpose:
    --------
    Draw a scatter plot with distinct markers/colors per hue series (if provided),
    and show a short textual insight.

    Parameters:
    -----------
    df: pd.DataFrame
    x: str
    y: str
    hue: Optional[str]
    size: Optional[str]
    """
    df_plot = df[[x, y] + ([hue] if hue else []) + ([size] if size else [])].dropna()
    insight = ""
    # compute simple metrics
    corr = float(df_plot[x].corr(df_plot[y])) if not df_plot[[x, y]].dropna().empty else float("nan")
    insight = f"Pearson correlation between **{x}** and **{y}**: {corr:.3f}"
    if PLOTLY_AVAILABLE:
        px_args = dict(x=x, y=y, hover_data=df_plot.columns.tolist())
        if hue is not None:
            fig = px.scatter(df_plot, color=hue, symbol=hue, **px_args)
        else:
            fig = px.scatter(df_plot, **px_args)
        if size is not None:
            fig.update_traces(marker=dict(size=6), selector=dict(mode="markers"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(insight)
    else:
        # matplotlib fallback with jitter and distinct markers
        fig, ax = plt.subplots(figsize=(7, 5))
        if hue is not None:
            groups = df_plot.groupby(hue)
            markers = ["o", "s", "^", "P", "X", "D", "v", "<", ">"]
            for i, (name, g) in enumerate(groups):
                # jitter small amount to reduce overplot
                xvals = g[x].values + np.random.normal(0, 0.0, size=len(g))
                yvals = g[y].values + np.random.normal(0, 0.0, size=len(g))
                marker = markers[i % len(markers)]
                ax.scatter(xvals, yvals, label=str(name), marker=marker, edgecolors="k",
                           linewidths=0.4, alpha=0.85, s=40)
            ax.legend(title=hue, bbox_to_anchor=(1.02, 1), loc="upper left")
        else:
            ax.scatter(df_plot[x], df_plot[y], s=30, edgecolors="k", alpha=0.7)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} vs {x}")
        st.pyplot(fig)
        st.markdown(insight)


def histogram_with_insight(series: pd.Series, bins: int = 30) -> None:
    """
    Purpose:
    --------
    Plot a histogram and provide quick textual insight on skewness/outliers.

    Parameters:
    -----------
    series: pd.Series
    bins: int
    """
    s = series.dropna()
    if s.empty:
        st.info("No data to plot.")
        return
    skew = s.skew()
    kurt = s.kurtosis()
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    n_out_iqr = int(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum())
    insight = f"Skewness: {skew:.3f}; Kurtosis: {kurt:.3f}; IQR outliers: {n_out_iqr}"
    if PLOTLY_AVAILABLE:
        fig = px.histogram(s, nbins=bins, marginal="box", title="Histogram (with marginal boxplot)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(insight)
    else:
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(s, bins=bins, kde=True, edgecolor="k", ax=ax)
        ax.set_title("Histogram")
        st.pyplot(fig)
        st.markdown(insight)


# -----------------------------------------------------------------------------
# App layout and main logic
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("Schedule-X")
    uploaded = st.file_uploader("Upload CombinedSchedules.xlsx (sheet 'Data')", type=["xlsx"])
    fallback_path = st.text_input("Fallback local path (optional)", value="")
    st.markdown("---")
    section = st.radio("Section", [
        "Overview",
        "Descriptive Statistics",
        "Inferential Statistics",
        "Feature Analysis",
        "Dimensionality Reduction",
        "Clustering",
        "Anomaly Detection",
        "Export",
    ])
    st.markdown("---")
    st.caption("Refactor: multi-selects, richer stats, multiple algorithms, and improved visuals.")


# Load dataframe
try:
    df = load_excel(uploaded, fallback_path)
except Exception as ex:
    st.error(f"Failed to load dataset: {ex}")
    st.stop()

if df.empty:
    st.warning("No data loaded. Upload an Excel 'CombinedSchedules.xlsx' with sheet named 'Data'.")
    st.stop()

# Show overview with improved table display
if section == "Overview":
    st.header("Data Overview")
    st.markdown("### Sample (first 300 rows)")
    # present a styled sample table
    sample = df.head(300).reset_index(drop=True)
    show_styled_table(sample, height=400)

    st.markdown("### Column summary")
    col_summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_unique": df.nunique(dropna=True),
        "n_missing": df.isna().sum(),
    })
    show_styled_table(col_summary, height=350)

    st.markdown("### Quick numeric snapshot")
    num_cols = numeric_columns(df)
    if num_cols:
        snapshot = df[num_cols].describe(percentiles=[0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]).T
        show_styled_table(snapshot, height=420)
    else:
        st.info("No numeric columns detected in the dataset.")


# Descriptive Statistics
elif section == "Descriptive Statistics":
    st.header("Descriptive Statistics — Expanded")
    num_cols = numeric_columns(df)
    if not num_cols:
        st.info("No numeric columns available.")
    else:
        # multi-select prepopulated with up to 6 numeric columns
        default = num_cols[:6]
        chosen = st.multiselect("Select numeric columns (multi-select)", num_cols, default=default)
        if not chosen:
            st.info("Choose one or more numeric columns to compute statistics.")
        else:
            # compute expanded descriptive statistics
            with st.spinner("Computing expanded descriptive statistics..."):
                desc = expanded_descriptive(df, chosen)
            st.subheader("Expanded descriptive statistics")
            show_styled_table(desc, height=480)

            st.subheader("Distribution preview and insights")
            # allow multi-preview of histograms (show 2 per row)
            cols_per_row = 2
            for i, col in enumerate(chosen):
                if i % cols_per_row == 0:
                    cols = st.columns(cols_per_row)
                with cols[i % cols_per_row]:
                    st.markdown(f"**{col}**")
                    histogram_with_insight(pd.to_numeric(df[col], errors="coerce"), bins=st.slider(f"bins_{col}", 10, 200, 40, key=f"bins_{col}"))


# Inferential Statistics
elif section == "Inferential Statistics":
    st.header("Inferential Statistics — Expanded")
    num_cols = numeric_columns(df)
    cat_cols = categorical_columns(df)
    if not num_cols:
        st.info("No numeric columns available for inferential tests.")
    else:
        default_num = num_cols[:6]
        chosen_num = st.multiselect("Numeric columns (tests run pairwise / multi)", num_cols, default=default_num)
        st.markdown("#### Pairwise Welch's t-tests (for each column pair)")
        if len(chosen_num) < 2:
            st.info("Select at least two numeric columns for pairwise t-tests.")
        else:
            tdf = pairwise_ttests(df, chosen_num)
            show_styled_table(tdf, height=280)
            st.caption("Small p-values suggest significant mean differences. Use with context.")

        st.markdown("#### Non-parametric tests (Mann–Whitney U)")
        if len(chosen_num) >= 2:
            rows = []
            for i, a in enumerate(chosen_num):
                for b in chosen_num[i+1:]:
                    s1 = pd.to_numeric(df[a], errors="coerce").dropna()
                    s2 = pd.to_numeric(df[b], errors="coerce").dropna()
                    try:
                        u, p = stats.mannwhitneyu(s1, s2, alternative="two-sided")
                    except Exception:
                        u, p = float("nan"), float("nan")
                    rows.append({"var1": a, "var2": b, "U": float(u), "pvalue": float(p)})
            mw = pd.DataFrame(rows)
            show_styled_table(mw, height=240)
        else:
            st.info("Select at least two numeric columns.")

        st.markdown("#### ANOVA vs a categorical grouping (one-way ANOVA)")
        if cat_cols:
            grouping = st.selectbox("Choose categorical grouping column (for ANOVA)", ["(none)"] + cat_cols)
            if grouping != "(none)":
                anova_df = anova_test(df, chosen_num, grouping)
                show_styled_table(anova_df, height=300)
                st.caption("F-statistics and p-values for group differences across categories.")
        else:
            st.info("No categorical columns available to run ANOVA.")

        st.markdown("#### Categorical association (Chi-square test)")
        if len(cat_cols) >= 2:
            cat1, cat2 = st.multiselect("Select two categorical columns for chi-square", cat_cols, default=cat_cols[:2])
            if isinstance(cat1, str) and isinstance(cat2, str) and cat1 != cat2:
                chi2, p, ct = chi2_categorical(df, cat1, cat2)
                st.write(f"Chi-square: **{chi2:.3f}**; p-value: **{p:.3g}**")
                st.write("Contingency table:")
                show_styled_table(ct, height=250)
            else:
                st.info("Select two different categorical columns.")


# Feature Analysis (formerly Feature Correlations)
elif section == "Feature Analysis":
    st.header("Feature Analysis — correlations, PCA/LDA, cluster-aware summaries")
    num_cols = numeric_columns(df)
    cat_cols = categorical_columns(df)
    if not num_cols:
        st.info("No numeric columns found.")
    else:
        chosen = st.multiselect("Numeric feature columns", num_cols, default=num_cols[:8])
        if not chosen:
            st.info("Select numeric features to analyze.")
        else:
            # Correlation matrix + heatmap
            st.subheader("Correlation matrix (Pearson / Spearman)")
            corr_method = st.selectbox("Method", ["pearson", "spearman", "kendall"], index=0)
            corr = df[chosen].corr(method=corr_method)
            show_styled_table(corr, height=360)
            st.caption("Values near ±1 indicate strong linear associations (Pearson).")

            # PCA summary & plot
            st.subheader("PCA (explained variance and 2D projection)")
            n_pca = st.slider("PCA components", 2, min(10, max(2, len(chosen))), value=2)
            comps_df, pca_model = compute_pca(df, chosen, n_components=n_pca)
            ev = pd.Series(pca_model.explained_variance_ratio_, index=[f"PC{i+1}" for i in range(len(pca_model.explained_variance_ratio_))])
            st.markdown("Explained variance ratio:")
            st.bar_chart(ev)
            # 2D scatter of first two components
            if "PC1" in comps_df.columns and "PC2" in comps_df.columns:
                temp = comps_df.copy()
                # if categorical target present, allow color mapping
                target = None
                if cat_cols:
                    target = st.selectbox("Optional categorical target for coloring", ["(none)"] + cat_cols)
                    if target and target != "(none)":
                        temp[target] = df.loc[temp.index, target]
                if PLOTLY_AVAILABLE:
                    fig = px.scatter(temp, x="PC1", y="PC2", color=target if target and target != "(none)" else None,
                                     hover_data=temp.columns.tolist(), title="PCA: PC1 vs PC2")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    scatter_plot(pd.concat([temp.reset_index(drop=True), df.loc[temp.index].reset_index(drop=True)], axis=1),
                                 "PC1", "PC2", hue=(target if target and target != "(none)" else None))
                # interpretation
                st.markdown(f"**Interpretation:** PC1 explains {ev.iloc[0]:.2%} of variance; PC2 explains {ev.iloc[1]:.2%}.")

            # LDA (if categorical target chosen)
            if cat_cols:
                st.subheader("Linear Discriminant Analysis (LDA)")
                lda_target = st.selectbox("Choose categorical target for LDA", ["(none)"] + cat_cols)
                if lda_target != "(none)":
                    # prepare data
                    mask = df[chosen + [lda_target]].dropna().index
                    if len(mask) < 10:
                        st.info("Not enough rows without missing values to run LDA.")
                    else:
                        X = pd.to_numeric(df.loc[mask, chosen], errors="coerce").astype(float)
                        le = LabelEncoder()
                        y = le.fit_transform(df.loc[mask, lda_target].astype(str))
                        lda = LinearDiscriminantAnalysis(n_components=min(len(np.unique(y)) - 1, 2))
                        try:
                            transformed = lda.fit_transform(X, y)
                            ld_df = pd.DataFrame(transformed, index=mask, columns=[f"LD{i+1}" for i in range(transformed.shape[1])])
                            if PLOTLY_AVAILABLE and ld_df.shape[1] >= 2:
                                fig = px.scatter(ld_df, x="LD1", y="LD2", color=df.loc[mask, lda_target].astype(str),
                                                 hover_data=[lda_target], title="LDA projection")
                                st.plotly_chart(fig, use_container_width=True)
                            elif ld_df.shape[1] >= 2:
                                scatter_plot(pd.concat([ld_df.reset_index(drop=True), df.loc[mask].reset_index(drop=True)], axis=1),
                                             "LD1", "LD2", hue=lda_target)
                            st.markdown("LDA projects features to maximize class separation; inspect loadings for feature influence.")
                        except Exception as e:
                            st.error(f"LDA failed: {e}")

            # k-Means feature clustering (feature-space clustering)
            st.subheader("k-Means (feature-space cluster summary)")
            run_k = st.checkbox("Run k-Means clustering on selected features", value=False)
            if run_k:
                k = st.slider("k clusters", 2, 12, 3)
                labels = run_clustering(df, chosen, "kmeans", k=k)
                # show cluster sizes and top feature means per cluster
                counts = labels.value_counts().sort_index()
                st.write("Cluster counts:")
                st.table(counts)
                # attach labels to df for cluster-level summaries
                merged = df.loc[labels.index, chosen].copy()
                merged["cluster"] = labels.values
                cluster_summary = merged.groupby("cluster").agg(["mean", "std", "count"])
                # flatten multiindex columns
                cluster_summary.columns = ["_".join(col).strip() for col in cluster_summary.columns.values]
                show_styled_table(cluster_summary, height=420)
                # silhouette if possible
                try:
                    sil = silhouette_score(pd.to_numeric(df.loc[labels.index, chosen], errors="coerce").dropna(), labels[labels.index])
                    st.caption(f"Silhouette score: {sil:.3f} (higher is better separation)")
                except Exception:
                    pass


# Dimensionality Reduction (multiple techniques)
elif section == "Dimensionality Reduction":
    st.header("Dimensionality Reduction — multiple techniques")
    num_cols = numeric_columns(df)
    if not num_cols:
        st.info("No numeric columns.")
    else:
        chosen = st.multiselect("Numeric columns to use", num_cols, default=num_cols[:8])
        if not chosen:
            st.info("Select numeric features.")
        else:
            method = st.selectbox("Method", ["PCA", "TruncatedSVD", "FactorAnalysis", "IncrementalPCA", "t-SNE (sklearn)", "UMAP (if available)"])
            n_components = st.slider("Components to compute", 2, min(10, max(2, len(chosen))), value=2)
            if method == "PCA":
                comps, model = compute_pca(df, chosen, n_components)
                st.markdown("Explained variance ratio:")
                ev = pd.Series(model.explained_variance_ratio_, index=[f"PC{i+1}" for i in range(len(model.explained_variance_ratio_))])
                st.bar_chart(ev)
            elif method == "TruncatedSVD":
                comps = compute_truncated_svd(df, chosen, n_components=n_components)
            elif method == "FactorAnalysis":
                comps = compute_factor_analysis(df, chosen, n_components=n_components)
            elif method == "IncrementalPCA":
                ipca = IncrementalPCA(n_components=n_components)
                X = pd.to_numeric(df[chosen], errors="coerce").dropna(axis=0)
                Xs = StandardScaler().fit_transform(X)
                comps_vals = ipca.fit_transform(Xs)
                comps = pd.DataFrame(comps_vals, columns=[f"IPCA{i+1}" for i in range(n_components)], index=X.index)
            elif method == "t-SNE (sklearn)":
                if not TSNE_AVAILABLE:
                    st.info("scikit-learn TSNE is unavailable.")
                    comps = pd.DataFrame()
                else:
                    X = pd.to_numeric(df[chosen], errors="coerce").dropna(axis=0)
                    Xs = StandardScaler().fit_transform(X)
                    tsne = TSNE(n_components=2, init="pca", random_state=0)
                    comps_vals = tsne.fit_transform(Xs)
                    comps = pd.DataFrame(comps_vals, columns=[f"TSNE{i+1}" for i in range(2)], index=X.index)
            elif method == "UMAP (if available)":
                if not UMAP_AVAILABLE:
                    st.info("UMAP not installed; select another technique.")
                    comps = pd.DataFrame()
                else:
                    X = pd.to_numeric(df[chosen], errors="coerce").dropna(axis=0)
                    Xs = StandardScaler().fit_transform(X)
                    reducer = umap.UMAP(n_components=n_components, random_state=0)
                    comps_vals = reducer.fit_transform(Xs)
                    comps = pd.DataFrame(comps_vals, columns=[f"UMAP{i+1}" for i in range(n_components)], index=X.index)
            # show 2D scatter if possible
            if comps is not None and not comps.empty and comps.shape[1] >= 2:
                temp = comps.copy()
                if PLOTLY_AVAILABLE:
                    fig = px.scatter(temp.reset_index(drop=True), x=temp.columns[0], y=temp.columns[1],
                                     hover_data=temp.columns.tolist(), title=f"{method}: {temp.columns[0]} vs {temp.columns[1]}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # create synthetic df with original columns for hue possibilities
                    scatter_plot(pd.concat([temp.reset_index(drop=True), df.loc[temp.index].reset_index(drop=True)], axis=1),
                                 temp.columns[0], temp.columns[1])
                st.markdown("Interpretation: Inspect explained variance (PCA) or cluster separation for projection quality.")
            else:
                st.info("Projection returned less than two components or failed.")


# Clustering tab (multiple clustering options and better visualizations)
elif section == "Clustering":
    st.header("Clustering — multiple algorithms")
    num_cols = numeric_columns(df)
    if not num_cols:
        st.info("No numeric columns.")
    else:
        chosen = st.multiselect("Features to cluster on", num_cols, default=num_cols[:6])
        if not chosen:
            st.info("Select features.")
        else:
            method = st.selectbox("Algorithm", ["kMeans", "DBSCAN", "Agglomerative"])
            if method == "kMeans":
                k = st.slider("k clusters", 2, 12, 3)
                labels = run_clustering(df, chosen, "kmeans", k=k)
            elif method == "DBSCAN":
                eps = st.number_input("eps", value=0.5, format="%.3f")
                min_samples = st.number_input("min_samples", value=5, step=1)
                labels = run_clustering(df, chosen, "dbscan", eps=eps, min_samples=int(min_samples))
            else:
                n = st.slider("n_clusters", 2, 12, 3)
                labels = run_clustering(df, chosen, "agglo", n_clusters=n)
            if labels.empty:
                st.info("Clustering produced no labels (check data).")
            else:
                st.subheader("Cluster membership (sample)")
                sample_l = pd.concat([df.loc[labels.index, chosen], labels.rename("cluster")], axis=1)
                show_styled_table(sample_l.head(300), height=420)
                st.subheader("Cluster counts")
                st.table(labels.value_counts().sort_index())
                # 2D projection for cluster visualization via PCA
                try:
                    comps, pca_model = compute_pca(df.loc[labels.index], chosen, n_components=2)
                    comps["cluster"] = labels.values
                    if PLOTLY_AVAILABLE:
                        fig = px.scatter(comps.reset_index(drop=True), x="PC1", y="PC2", color="cluster", title="Clusters (PCA projection)")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        scatter_plot(pd.concat([comps.reset_index(drop=True), df.loc[labels.index].reset_index(drop=True)], axis=1),
                                     "PC1", "PC2", hue="cluster")
                    # silhouette if valid
                    if len(set(labels.values)) > 1 and -1 not in set(labels.values):
                        try:
                            sil = silhouette_score(pd.to_numeric(df.loc[labels.index, chosen], errors="coerce").dropna(), labels[labels.index])
                            st.caption(f"Silhouette score: {sil:.3f}")
                        except Exception:
                            pass
                except Exception:
                    pass


# Anomaly Detection tab (multiple options)
elif section == "Anomaly Detection":
    st.header("Anomaly Detection — multiple detectors")
    num_cols = numeric_columns(df)
    if not num_cols:
        st.info("No numeric columns.")
    else:
        chosen = st.multiselect("Numeric columns for anomaly detection", num_cols, default=num_cols[:6])
        if not chosen:
            st.info("Select numeric columns.")
        else:
            method = st.selectbox("Anomaly method", ["isolation_forest", "one_class_svm", "lof", "elliptic"])
            params = {}
            if method == "isolation_forest":
                params["n_estimators"] = st.slider("n_estimators", 20, 1000, 100)
            elif method == "one_class_svm":
                params["nu"] = st.slider("nu", 0.001, 0.5, 0.05, format="%.3f")
            elif method == "lof":
                params["n_neighbors"] = st.slider("n_neighbors", 5, 100, 20)
                params["contamination"] = st.slider("contamination", 0.001, 0.5, 0.05, format="%.3f")
            else:
                params["contamination"] = st.slider("contamination", 0.001, 0.5, 0.05, format="%.3f")
            results = detect_anomalies(df, chosen, method, **params)
            if results.empty:
                st.info("Anomaly detection returned no results.")
            else:
                # attach labels to df and display anomalies table (top 300)
                df_out = df.loc[results.index].copy()
                df_out["anomaly"] = results.values
                anomalies = df_out[df_out["anomaly"] == -1]
                st.subheader(f"Anomalies detected: {len(anomalies)}")
                if len(anomalies) > 0:
                    show_styled_table(anomalies.head(300), height=420)
                    st.download_button("Download anomalies CSV", anomalies.to_csv(index=False).encode("utf-8"),
                                       file_name="schedulex_anomalies.csv", mime="text/csv")
                else:
                    st.info("No anomalies found for selected parameters.")


# Export tab
elif section == "Export":
    st.header("Export — Save processed artifacts")
    st.markdown("You can download the raw sheet or processed outputs generated in other tabs.")
    st.download_button("Download raw data CSV", df.to_csv(index=False).encode("utf-8"),
                       file_name="schedulex_raw.csv", mime="text/csv")
    st.caption("Run Clustering or Anomaly Detection first to generate labeled CSV exports.")


# End
st.markdown("---")
st.caption("Schedule-X viewer — refined by Bro. Use plotly (install with 'plotly') for hover tooltips.")


