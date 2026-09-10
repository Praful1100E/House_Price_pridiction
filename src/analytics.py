"""
Analytics and Visualizations Module for House Price Prediction Platform.
Generates rich, interactive Altair charts matching the dark aesthetic.
"""

from typing import Optional
import altair as alt
import numpy as np
import pandas as pd


def plot_price_distribution(
    df: pd.DataFrame, target_col: str = "SalePrice", use_log: bool = False
) -> Optional[alt.Chart]:
    """Renders an interactive distribution histogram for house prices."""
    if df is None or target_col not in df.columns:
        return None

    plot_df = df[[target_col]].dropna().copy()
    col_name = target_col
    if use_log:
        plot_df["Log_Price"] = np.log1p(plot_df[target_col])
        col_name = "Log_Price"

    chart = (
        alt.Chart(plot_df)
        .mark_bar(opacity=0.75, cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(f"{col_name}:Q", bin=alt.Bin(maxbins=40), title=f"{col_name}"),
            y=alt.Y("count()", title="Property Count"),
            color=alt.value("#38bdf8"),
            tooltip=[
                alt.Tooltip(f"{col_name}:Q", bin=alt.Bin(maxbins=40), title="Price Bin"),
                alt.Tooltip("count()", title="Count"),
            ],
        )
        .properties(height=320)
        .configure_view(strokeWidth=0)
        .interactive()
    )
    return chart


def plot_price_vs_area(
    df: pd.DataFrame, target_col: str = "SalePrice"
) -> Optional[alt.Chart]:
    """Renders a scatter plot of Living Area vs Price, colored by Overall Quality."""
    if df is None or target_col not in df.columns or "GrLivArea" not in df.columns:
        return None

    cols = ["GrLivArea", target_col]
    if "OverallQual" in df.columns:
        cols.append("OverallQual")
    if "Neighborhood" in df.columns:
        cols.append("Neighborhood")

    plot_df = df[cols].dropna()

    chart = (
        alt.Chart(plot_df)
        .mark_circle(size=60, opacity=0.8)
        .encode(
            x=alt.X("GrLivArea:Q", title="Living Area (Sq Ft)"),
            y=alt.Y(f"{target_col}:Q", title=f"Price ({target_col})"),
            color=alt.Color(
                "OverallQual:Q",
                scale=alt.Scale(scheme="viridis"),
                title="Quality (1-10)",
            )
            if "OverallQual" in plot_df.columns
            else alt.value("#38bdf8"),
            tooltip=[
                alt.Tooltip("GrLivArea:Q", title="Sq Ft"),
                alt.Tooltip(f"{target_col}:Q", format="$,.0f", title="Price"),
                alt.Tooltip("OverallQual:Q", title="Quality"),
                alt.Tooltip("Neighborhood:N", title="Neighborhood"),
            ]
            if "Neighborhood" in plot_df.columns
            else [
                alt.Tooltip("GrLivArea:Q", title="Sq Ft"),
                alt.Tooltip(f"{target_col}:Q", format="$,.0f", title="Price"),
            ],
        )
        .properties(height=340)
        .interactive()
    )
    return chart


def plot_price_by_neighborhood(
    df: pd.DataFrame, target_col: str = "SalePrice", top_n: int = 15
) -> Optional[alt.Chart]:
    """Renders a horizontal bar chart showing median price by neighborhood."""
    if df is None or target_col not in df.columns or "Neighborhood" not in df.columns:
        return None

    summary = (
        df.groupby("Neighborhood")[target_col]
        .median()
        .reset_index()
        .sort_values(by=target_col, ascending=False)
        .head(top_n)
    )

    chart = (
        alt.Chart(summary)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X(f"{target_col}:Q", title="Median Sale Price ($)"),
            y=alt.Y("Neighborhood:N", sort="-x", title="Neighborhood"),
            color=alt.Color(
                f"{target_col}:Q",
                scale=alt.Scale(scheme="tealblues"),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Neighborhood:N"),
                alt.Tooltip(f"{target_col}:Q", format="$,.0f", title="Median Price"),
            ],
        )
        .properties(height=340)
        .interactive()
    )
    return chart


def plot_feature_correlations(
    df: pd.DataFrame, target_col: str = "SalePrice", top_n: int = 12
) -> Optional[alt.Chart]:
    """Renders a horizontal bar chart of top features correlating with target."""
    if df is None or target_col not in df.columns:
        return None

    num_df = df.select_dtypes(include=np.number)
    if target_col not in num_df.columns:
        return None

    corrs = (
        num_df.corr()[target_col]
        .drop(target_col, errors="ignore")
        .dropna()
        .sort_values(ascending=False)
    )
    top_corrs = corrs.head(top_n).reset_index()
    top_corrs.columns = ["Feature", "Correlation"]

    chart = (
        alt.Chart(top_corrs)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X("Correlation:Q", title="Pearson Correlation Coefficient", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("Feature:N", sort="-x", title="Feature"),
            color=alt.Color(
                "Correlation:Q",
                scale=alt.Scale(scheme="plasma"),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Feature:N"),
                alt.Tooltip("Correlation:Q", format=".3f"),
            ],
        )
        .properties(height=340)
        .interactive()
    )
    return chart


def plot_missing_values(df: pd.DataFrame) -> Optional[alt.Chart]:
    """Renders a missing value bar chart."""
    if df is None:
        return None

    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame(
        {"Feature": df.columns, "MissingPct": missing_pct}
    ).query("MissingPct > 0").sort_values(by="MissingPct", ascending=False).head(15)

    if missing_df.empty:
        return None

    chart = (
        alt.Chart(missing_df)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X("MissingPct:Q", title="Missing Percentage (%)"),
            y=alt.Y("Feature:N", sort="-x", title="Column Name"),
            color=alt.value("#f43f5e"),
            tooltip=[
                alt.Tooltip("Feature:N"),
                alt.Tooltip("MissingPct:Q", format=".2f", title="% Missing"),
            ],
        )
        .properties(height=320)
        .interactive()
    )
    return chart


def plot_feature_importance_chart(df_imp: pd.DataFrame) -> Optional[alt.Chart]:
    """Plots top feature importances."""
    if df_imp is None or df_imp.empty:
        return None

    chart = (
        alt.Chart(df_imp)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X("Importance:Q", title="Feature Importance Weight"),
            y=alt.Y("Feature:N", sort="-x", title="Feature"),
            color=alt.Color(
                "Importance:Q",
                scale=alt.Scale(scheme="tealblues"),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Feature:N"),
                alt.Tooltip("Importance:Q", format=".4f"),
            ],
        )
        .properties(height=340)
        .interactive()
    )
    return chart
