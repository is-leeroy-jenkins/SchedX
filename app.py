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

import io
import json
from typing import Optional, Sequence

import numpy as np
import openpyxl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from sklearn.decomposition import PCA, IncrementalPCA, TruncatedSVD, FactorAnalysis
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from scipy import stats

# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def load_excel_from_path_or_upload( uploaded_file: Optional[io.BytesIO], fallback_path: Optional[str] ) -> pd.DataFrame:
    """
    
	    Purpose:
	    --------
	    Load an Excel dataset either from an uploaded file (Streamlit uploader)
	    or from a fallback local path (if present).
	
	    Parameters:
	    -----------
	    uploaded_file: Optional[io.BytesIO]
	        A file-like object from st.file_uploader.
	    fallback_path: Optional[str]
	        Local filesystem path to attempt if uploaded_file is None.
	
	    Returns:
	    --------
	    pd.DataFrame: DataFrame loaded from the notebook's 'Data' sheet.
	    
    """
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name="Data")
            return df
        except Exception as ex:
            st.error(f"Failed to read uploaded file as Excel: {ex}")
            raise
    if fallback_path:
        try:
            df = pd.read_excel(fallback_path, sheet_name="Data")
            return df
        except FileNotFoundError:
            st.warning(
                f"Fallback path not found: {fallback_path}. Please upload an Excel "
                "file using the uploader above."
            )
            return pd.DataFrame()
        except Exception as ex:
            st.error(f"Failed to read fallback Excel: {ex}")
            raise
    return pd.DataFrame()


def smart_select_numeric(df: pd.DataFrame) -> list[str]:
    """Return a list of numeric columns useful for plotting / modeling."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.histplot(df[column].dropna(), bins=bins, ax=ax, kde=True)
    ax.set_title(f"Histogram — {column}")
    return fig


def plot_box(df: pd.DataFrame, column: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.boxplot(x=df[column].dropna(), ax=ax)
    ax.set_title(f"Boxplot — {column}")
    return fig


def correlation_heatmap(df: pd.DataFrame, method: str = "pearson") -> plt.Figure:
    numeric = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = numeric.corr(method=method)
    sns.heatmap(corr, annot=False, ax=ax, cmap="coolwarm", center=0)
    ax.set_title(f"{method.title()} Correlation")
    return fig


def compute_basic_stats(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    return df[cols].describe().T


def run_pca_and_plot(df: pd.DataFrame, n_components: int = 2) -> tuple[pd.DataFrame, plt.Figure]:
    numeric = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
    numeric = numeric.dropna(axis=0, how="any")
    scaler = StandardScaler()
    Xs = scaler.fit_transform(numeric)
    pca = PCA(n_components=n_components)
    comps = pca.fit_transform(Xs)
    comp_df = pd.DataFrame(comps, columns=[f"PC{i+1}" for i in range(n_components)])
    fig, ax = plt.subplots(figsize=(6, 5))
    if n_components >= 2:
        ax.scatter(comp_df["PC1"], comp_df["PC2"], s=20, alpha=0.7)
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
    ax.set_title("PCA scatter")
    return comp_df, fig


def run_kmeans(df: pd.DataFrame, k: int = 3) -> pd.Series:
    numeric = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
    idx_keep = numeric.dropna(axis=0).index
    scaler = StandardScaler()
    Xs = scaler.fit_transform(numeric.loc[idx_keep])
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = pd.Series(kmeans.fit_predict(Xs), index=idx_keep, name="kmeans_label")
    return labels


def run_anomaly_detector(df: pd.DataFrame, method: str, **kwargs) -> pd.Series:
    """
    Purpose:
    --------
    Run an anomaly detection algorithm on numeric columns and return a Series
    with index matching df.index and values {1: inlier, -1: outlier}.

    Parameters:
    -----------
    df: DataFrame
    method: name string among {'isolation_forest','one_class_svm','lof','elliptic'}
    kwargs: algorithm-specific parameters.

    Returns:
    --------
    pd.Series with results.
    """
    numeric = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
    numeric = numeric.dropna(axis=0)
    if numeric.shape[0] == 0:
        return pd.Series(dtype=int)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(numeric)

    if method == "isolation_forest":
        clf = IsolationForest(random_state=0, n_estimators=kwargs.get("n_estimators", 100))
        preds = clf.fit_predict(Xs)
    elif method == "one_class_svm":
        clf = OneClassSVM(nu=kwargs.get("nu", 0.05), kernel="rbf", gamma="scale")
        preds = clf.fit_predict(Xs)
    elif method == "lof":
        # LOF uses negative_outlier_factor_, but fit_predict returns -1 for outliers
        clf = LocalOutlierFactor(n_neighbors=kwargs.get("n_neighbors", 20), contamination=kwargs.get("contamination", 0.05))
        preds = clf.fit_predict(Xs)
    elif method == "elliptic":
        clf = EllipticEnvelope(contamination=kwargs.get("contamination", 0.05), random_state=0)
        clf.fit(Xs)
        preds = clf.predict(Xs)
    else:
        raise ValueError("Unknown method")
    return pd.Series(preds, index=numeric.index)


# ---------------------------------------------------------------------
# Streamlit layout and main
# ---------------------------------------------------------------------
st.set_page_config(page_title="Schedule-X: Exploratory App", layout="wide")

st.sidebar.title("Schedule-X")
uploaded = st.sidebar.file_uploader("Upload CombinedSchedules.xlsx (sheet 'Data')", type=["xlsx"])
# Notebook referenced a fallback path; we'll provide an optional local fallback.
fallback_path_input = st.sidebar.text_input(
    "Fallback local Excel path (optional)",
    value="/stores/excel/CombinedSchedules.xlsx",
)

st.sidebar.markdown("---")
section = st.sidebar.radio(
    "Section",
    [
        "Overview / Data",
        "Descriptive Statistics",
        "Inferential Statistics",
        "Dimensionality Reduction",
        "Clustering",
        "Anomaly Detection",
        "Correlation Analysis",
        "Export",
    ],
)

# Load dataset
df = load_excel_from_path_or_upload(uploaded, fallback_path_input)
if df.empty:
    st.warning("No dataframe loaded. Upload the Excel or provide a valid fallback path.")
    if st.button("Show example schema"):
        st.write(
            {
                "Expected sheet": "Data",
                "Columns (examples)": [
                    "CombinedSchedulesId",
                    "MainAccount",
                    "TreasurySymbol",
                    "AccountName",
                    "LineName",
                    "Line",
                    "PY",
                    "CY",
                    "BY",
                    "OY-1",
                    "OY-2",
                ],
            }
        )
    st.stop()

# Present simple overview
if section == "Overview / Data":
    st.header("Schedule-X: Data Overview")
    st.write("Dataframe shape:", df.shape)
    st.subheader("Sample rows")
    st.dataframe(df.head(200))
    st.subheader("Column types")
    st.write(df.dtypes)
    numeric_cols = smart_select_numeric(df)
    st.subheader("Numeric columns detected")
    st.write(numeric_cols)

# Descriptive Stats
elif section == "Descriptive Statistics":
    st.header("Descriptive Statistics")
    numeric_cols = smart_select_numeric(df)
    if not numeric_cols:
        st.info("No numeric columns found for descriptive statistics.")
    else:
        sel = st.multiselect("Select numeric columns to summarize", numeric_cols, default=numeric_cols[:6])
        if sel:
            st.write("Summary statistics")
            st.dataframe(compute_basic_stats(df, sel))
            st.markdown("**Column histograms & boxplots**")
            col = st.selectbox("Column for plots", sel)
            bins = st.slider("Histogram bins", 5, 100, 30)
            st.pyplot(plot_histogram(df, col, bins))
            st.pyplot(plot_box(df, col))

# Inferential Statistics (simple)
elif section == "Inferential Statistics":
    st.header("Inferential Statistics (basic)")
    numeric_cols = smart_select_numeric(df)
    if len(numeric_cols) < 1:
        st.info("Not enough numeric columns for inferential tests.")
    else:
        col1 = st.selectbox("Numeric column (sample 1)", numeric_cols, index=0)
        # If there is any other numeric column, allow second selection for t-test
        if len(numeric_cols) > 1:
            col2 = st.selectbox("Numeric column (sample 2)", numeric_cols, index=min(1, len(numeric_cols)-1))
        else:
            col2 = col1
        st.subheader("Two-sample t-test")
        # dropna pairs
        s1 = df[col1].dropna()
        s2 = df[col2].dropna()
        try:
            tstat, pval = stats.ttest_ind(s1, s2, equal_var=False)
            st.write(f"T-statistic: {tstat:.4f}, p-value: {pval:.4g}")
        except Exception as ex:
            st.error(f"T-test failed: {ex}")

        st.subheader("Mann-Whitney U test")
        try:
            ustat, upval = stats.mannwhitneyu(s1, s2, alternative="two-sided")
            st.write(f"U-statistic: {ustat:.4f}, p-value: {upval:.4g}")
        except Exception as ex:
            st.error(f"Mann-Whitney test failed: {ex}")

# Dimensionality Reduction
elif section == "Dimensionality Reduction":
    st.header("Dimensionality Reduction")
    numeric_cols = smart_select_numeric(df)
    if not numeric_cols:
        st.info("No numeric columns available for PCA.")
    else:
        ncomp = st.slider("PCA components", 2, min(10, len(numeric_cols)), value=2)
        comp_df, fig = run_pca_and_plot(df, n_components=ncomp)
        st.pyplot(fig)
        st.write("Explained variance (first components):")
        try:
            scaler = StandardScaler()
            numeric = df.select_dtypes(include=[np.number]).dropna(axis=1, how="all").dropna(axis=0)
            Xs = scaler.fit_transform(numeric)
            pca = PCA(n_components=ncomp)
            pca.fit(Xs)
            ev = pd.Series(pca.explained_variance_ratio_, index=[f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))])
            st.bar_chart(ev)
        except Exception:
            st.info("Explained variance could not be computed for the selected parameters.")

# Clustering
elif section == "Clustering":
    st.header("K-Means Clustering")
    numeric_cols = smart_select_numeric(df)
    if not numeric_cols:
        st.info("No numeric columns available for clustering.")
    else:
        k = st.slider("k (clusters)", 2, 12, 3)
        labels = run_kmeans(df, k=k)
        if labels.empty:
            st.info("K-Means could not run due to insufficient rows after dropping NAs.")
        else:
            st.write("Cluster counts")
            st.write(labels.value_counts().sort_index())
            # merge labels into a copy of df for presentation
            df_with_labels = df.copy()
            df_with_labels.loc[labels.index, "kmeans_label"] = labels
            st.dataframe(df_with_labels.head(200))
            st.download_button(
                "Download clustered sample (CSV)",
                df_with_labels.to_csv(index=False).encode("utf-8"),
                file_name="schedulex_clustered.csv",
                mime="text/csv",
            )

# Anomaly Detection
elif section == "Anomaly Detection":
    st.header("Anomaly Detection")
    method = st.selectbox("Method", ["isolation_forest", "one_class_svm", "lof", "elliptic"])
    if method == "isolation_forest":
        n_est = st.slider("n_estimators", 20, 500, 100)
        params = {"n_estimators": n_est}
    elif method == "one_class_svm":
        nu = st.slider("nu (upper bound for outlier fraction)", 0.001, 0.5, 0.05, format="%.3f")
        params = {"nu": nu}
    elif method == "lof":
        n_neighbors = st.slider("n_neighbors", 5, 50, 20)
        cont = st.slider("contamination", 0.001, 0.5, 0.05, format="%.3f")
        params = {"n_neighbors": n_neighbors, "contamination": cont}
    else:
        cont = st.slider("contamination", 0.001, 0.5, 0.05, format="%.3f")
        params = {"contamination": cont}

    results = run_anomaly_detector(df, method, **params)
    if results.empty:
        st.info("Anomaly detector returned no results; maybe not enough numeric rows.")
    else:
        st.write("Outlier counts:")
        st.write((results == -1).sum())
        # attach to df and show sample of anomalies
        df_out = df.copy()
        df_out.loc[results.index, "anomaly_label"] = results
        st.subheader("Sample outliers (anomaly_label == -1)")
        anomalies = df_out[df_out["anomaly_label"] == -1]
        st.dataframe(anomalies.head(200))
        st.download_button(
            "Download anomalies (CSV)",
            anomalies.to_csv(index=False).encode("utf-8"),
            file_name="schedulex_anomalies.csv",
            mime="text/csv",
        )

# Correlation Analysis
elif section == "Correlation Analysis":
    st.header("Correlation Analysis")
    numeric_cols = smart_select_numeric(df)
    if not numeric_cols:
        st.info("No numeric columns available for correlation analysis.")
    else:
        method_corr = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"])
        fig = correlation_heatmap(df, method=method_corr)
        st.pyplot(fig)

# Export
elif section == "Export":
    st.header("Export processed data")
    st.write("If you have run clustering or anomaly detection, use the Export tools to download CSVs.")
    st.download_button(
        "Download raw sheet as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="schedulex_raw_data.csv",
        mime="text/csv",
    )
    st.write("Tip: run Clustering or Anomaly Detection sections to attach computed labels")

# End of app
st.sidebar.markdown("---")
st.sidebar.caption("Converted from Schedule-X notebook. Use controls to reproduce the notebook analyses.")


