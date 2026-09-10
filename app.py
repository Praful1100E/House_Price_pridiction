"""
Main Streamlit Application: Real Estate Intelligence & House Price Prediction Platform.
Features an ultra-modern Dark Glassmorphic UI, Multi-Model ML Studio, SQLite Persistence,
Exploratory Data Analytics, Batch Prediction, and Mortgage Financial Planner.
"""

from datetime import datetime
import io
import json
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# Internal Modules
from src.analytics import (
    plot_feature_correlations,
    plot_feature_importance_chart,
    plot_missing_values,
    plot_price_by_neighborhood,
    plot_price_distribution,
    plot_price_vs_area,
)
from src.data_manager import (
    add_custom_property,
    clear_all_prediction_history,
    delete_custom_property,
    delete_prediction_log,
    get_custom_properties,
    get_dataset_summary,
    get_missing_values_summary,
    get_prediction_history,
    init_db,
    load_dataset,
    save_prediction_log,
)
from src.financials import (
    calculate_investment_yield,
    calculate_mortgage_emi,
    generate_amortization_schedule,
    plot_amortization_chart,
)
from src.marketplace_ui import (
    render_buy_marketplace,
    render_sell_property_form,
)
from src.ml_engine import (
    HP_MARKET_DATA,
    benchmark_all_models,
    extract_feature_importances,
    format_currency,
    load_trained_pipeline,
    predict_single_property,
    save_trained_pipeline,
    train_single_model,
)
from src.ui_theme import (
    apply_theme,
    render_hero_header,
    render_metric_card,
    render_price_prediction_card,
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Real Estate Marketplace & AI Valuation Suite",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply UI Theme
apply_theme()
init_db()

# ----------------------------------------------------
# Global State & Dataset Initialization
# ----------------------------------------------------
if "df" not in st.session_state:
    st.session_state["df"] = load_dataset("train.csv")

if "pipe" not in st.session_state or "data_info" not in st.session_state:
    # Try loading pre-saved model, otherwise train default model automatically
    loaded_pipe, loaded_info = load_trained_pipeline()
    if loaded_pipe is not None:
        st.session_state["pipe"] = loaded_pipe
        st.session_state["data_info"] = loaded_info
    elif st.session_state["df"] is not None:
        try:
            p, m, d = train_single_model(
                st.session_state["df"],
                target_col="SalePrice",
                model_name="Random Forest Regressor",
            )
            st.session_state["pipe"] = p
            st.session_state["metrics"] = m
            st.session_state["data_info"] = d
            save_trained_pipeline(p, d)
        except Exception as e:
            st.warning(f"Initial model auto-train notice: {e}")

# ----------------------------------------------------
# Sidebar Controls & System Status
# ----------------------------------------------------
with st.sidebar:
    st.markdown("### 🏰 Real Estate AI")
    st.caption("AI-Powered Luxury Marketplace & Intelligence Platform")
    st.markdown("---")

    # Global Currency Preference
    st.markdown("#### 🌐 Currency Display")
    currency_pref = st.radio(
        "Preferred Currency",
        options=["USD ($)", "INR (₹)"],
        index=0,
        horizontal=True,
    )
    is_inr_mode = "INR" in currency_pref

    st.markdown("---")
    st.markdown("#### 📊 Marketplace Status")
    if st.session_state.get("df") is not None:
        num_rows = len(st.session_state["df"])
        st.success(f"● Market Benchmark: {num_rows:,} Transactions")
    else:
        st.error("● Market Data: Offline")

    if st.session_state.get("pipe") is not None:
        model_name = st.session_state.get("data_info", {}).get(
            "model_name", "Random Forest"
        )
        st.success(f"● Valuation Engine: {model_name}")
    else:
        st.warning("● Valuation Engine: Offline")

    st.markdown("---")
    st.markdown("#### 💎 Platform Highlights")
    st.markdown(
        """
        - 🏡 **Curated Estates**: Verified luxury & hill stations
        - ⚡ **AI Deal Radar**: Instant fair price benchmarking
        - 🔒 **Escrow Ready**: Instant purchase order flow
        - 📈 **ROI Planner**: Interactive EMI & rental cashflow
        """
    )

    st.markdown("---")
    st.caption(f"Local Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("Enterprise Real Estate Suite")


# ----------------------------------------------------
# Top Hero Banner
# ----------------------------------------------------
render_hero_header(
    title="Real Estate Marketplace & AI Valuation Suite",
    subtitle="Explore & buy luxury properties, list houses with AI Price Recommenders, instant valuation engine, and mortgage analytics.",
    badge_text="v3.0 Live Marketplace",
)

# ----------------------------------------------------
# Navigation Tabs
# ----------------------------------------------------
tab_buy, tab_sell, tab_valuation, tab_eda, tab_ml, tab_finance = st.tabs(
    [
        "🛒 Buy Houses",
        "🏷️ Sell a House",
        "🏡 AI Valuation Studio",
        "📊 Market Insights & Analytics",
        "🤖 ML Intelligence Studio",
        "💰 Mortgage & ROI Planner",
    ]
)

# ====================================================
# TAB 1: BUY HOUSES (MARKETPLACE)
# ====================================================
with tab_buy:
    render_buy_marketplace(
        pipe=st.session_state.get("pipe"),
        data_info=st.session_state.get("data_info"),
        global_is_inr=is_inr_mode,
    )

# ====================================================
# TAB 2: SELL A HOUSE (LISTING STUDIO)
# ====================================================
with tab_sell:
    render_sell_property_form(
        pipe=st.session_state.get("pipe"),
        data_info=st.session_state.get("data_info"),
        global_is_inr=is_inr_mode,
    )

# ====================================================
# TAB 3: VALUATION STUDIO
# ====================================================
with tab_valuation:
    st.markdown("### 🧮 Instant Property Valuation")
    st.caption(
        "Configure property specifications to generate an instant market price estimate with confidence bounds."
    )

    if st.session_state.get("pipe") is None or st.session_state.get("data_info") is None:
        st.warning("Please train or load a model from the ML Benchmarks tab to enable valuation.")
    else:
        # Market Mode Selection
        val_mode = st.radio(
            "Select Valuation Engine Mode:",
            [
                "🏔️ Regional Indian Market (Himachal Pradesh & Hill Stations)",
                "🏙️ Comprehensive Property Valuator (Standard Model)",
            ],
            horizontal=True,
        )
        is_hp_mode = "Regional" in val_mode

        st.markdown("---")

        with st.form("valuation_form"):
            if is_hp_mode:
                c1, c2, c3 = st.columns(3)
                with c1:
                    district = st.selectbox(
                        "District / Region",
                        HP_MARKET_DATA["districts"],
                        index=0,
                        help="Select the hill station / district",
                    )
                    area_sqft = st.number_input(
                        "Built-up Living Area (Sq Ft)",
                        min_value=300,
                        max_value=12000,
                        value=1800,
                        step=50,
                    )
                    bhk = st.slider("Bedrooms (BHK)", 1, 8, 3)

                with c2:
                    bathrooms = st.slider("Bathrooms", 1, 6, 2)
                    property_age = st.number_input(
                        "Property Age (Years)", 0, 80, 5, step=1
                    )
                    view_type = st.selectbox(
                        "Scenic View & Location Grade",
                        list(HP_MARKET_DATA["view_multipliers"].keys()),
                        index=0,
                    )

                with c3:
                    overall_condition = st.select_slider(
                        "Construction & Finish Quality",
                        options=[
                            "Standard / Economy",
                            "Good / Semi-Furnished",
                            "Premium / Luxury",
                            "Ultra Luxury / Villa",
                        ],
                        value="Premium / Luxury",
                    )
                    garage_cars = st.slider("Covered Parking / Garage Capacity", 0, 4, 1)
                    notes_input = st.text_input("Property Label / Notes (Optional)", "Hilltop Villa")

            else:
                c1, c2, c3 = st.columns(3)
                with c1:
                    overall_qual = st.slider("Overall Material & Finish Quality (1-10)", 1, 10, 7)
                    area_sqft = st.number_input("Above Ground Living Area (GrLivArea sq ft)", 400, 6000, 1750, step=50)
                    total_bsmt_sf = st.number_input("Basement Area (Sq Ft)", 0, 4000, 950, step=50)

                with c2:
                    bedrooms = st.slider("Bedrooms Above Ground", 1, 7, 3)
                    bathrooms = st.slider("Full Bathrooms", 1, 5, 2)
                    garage_cars = st.slider("Garage Car Capacity", 0, 4, 2)

                with c3:
                    year_built = st.number_input("Year Built", 1880, datetime.now().year, 2012, step=1)
                    neighborhoods = sorted(
                        [
                            "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst",
                            "NWAmes", "OldTown", "BrkSide", "Sawyer", "NAmes", "SawyerW",
                            "IDOTRR", "MeadowV", "Edwards", "Timber", "Gilbert", "StoneBr",
                            "ClearCr", "NPkVill", "Blmngtn", "BrDale", "SWISU", "Blueste", "NridgHt"
                        ]
                    )
                    neighborhood = st.selectbox("Neighborhood", neighborhoods, index=neighborhoods.index("CollgCr") if "CollgCr" in neighborhoods else 0)
                    notes_input = st.text_input("Property Label / Notes (Optional)", "Suburban Residence")

            submit_val = st.form_submit_button("🚀 Calculate Market Valuation", use_container_width=True)

        if submit_val:
            current_year = datetime.now().year
            if is_hp_mode:
                # Map HP inputs to model features
                qual_mapping = {
                    "Standard / Economy": 4,
                    "Good / Semi-Furnished": 6,
                    "Premium / Luxury": 8,
                    "Ultra Luxury / Villa": 10,
                }
                mapped_qual = qual_mapping.get(overall_condition, 7)
                mapped_year = current_year - property_age

                input_dict = {
                    "GrLivArea": area_sqft,
                    "OverallQual": mapped_qual,
                    "YearBuilt": mapped_year,
                    "FullBath": bathrooms,
                    "TotRmsAbvGrd": bhk + 2,
                    "GarageCars": garage_cars,
                    "TotalBsmtSF": area_sqft * 0.4,
                }

                result = predict_single_property(
                    pipeline=st.session_state["pipe"],
                    data_info=st.session_state["data_info"],
                    input_features=input_dict,
                    is_regional_hp=True,
                    district=district,
                    view_type=view_type,
                )
                location_label = f"{district} ({view_type})"
                pred_price = result["predicted_price"]
                low_price = result["low_bound"]
                high_price = result["high_bound"]
                curr_symbol = "INR"

            else:
                input_dict = {
                    "GrLivArea": area_sqft,
                    "OverallQual": overall_qual,
                    "YearBuilt": year_built,
                    "FullBath": bathrooms,
                    "TotRmsAbvGrd": bedrooms + 2,
                    "GarageCars": garage_cars,
                    "TotalBsmtSF": total_bsmt_sf,
                    "Neighborhood": neighborhood,
                }
                result = predict_single_property(
                    pipeline=st.session_state["pipe"],
                    data_info=st.session_state["data_info"],
                    input_features=input_dict,
                    is_regional_hp=False,
                )
                location_label = neighborhood
                pred_price = result["predicted_price"]
                low_price = result["low_bound"]
                high_price = result["high_bound"]
                curr_symbol = "USD"

            # Store in session state for financial calculator pre-fill
            st.session_state["latest_prediction"] = {
                "price": pred_price,
                "currency": curr_symbol,
                "sqft": area_sqft,
            }

            # Display Valuation Result
            st.markdown("---")
            render_price_prediction_card(
                price_str=result["formatted_price"],
                confidence_str=f"Estimated Range (95% CI): {result['formatted_range']}",
                currency_label="INR (₹)" if curr_symbol == "INR" else "USD ($)",
                disclaimer="Valuation calibrated with multi-variable Scikit-Learn regression engine.",
            )

            # Quick Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                price_per_sqft = pred_price / area_sqft if area_sqft > 0 else 0
                render_metric_card(
                    "Price per Sq. Ft.",
                    f"{'₹' if curr_symbol == 'INR' else '$'} {price_per_sqft:,.1f} / sqft",
                    delta="Market Competitive",
                    delta_type="pos",
                )
            with m2:
                render_metric_card(
                    "Property Size",
                    f"{area_sqft:,.0f} Sq Ft",
                    delta=f"{bhk if is_hp_mode else bedrooms} BHK | {bathrooms} Baths",
                    delta_type="info",
                )
            with m3:
                render_metric_card(
                    "Location Index",
                    location_label,
                    delta="Regional Adjustment Applied" if is_hp_mode else "Standard Market",
                    delta_type="info",
                )

            # Save to Portfolio Shortlist Button
            st.markdown(" ")
            col_save, col_empty = st.columns([1, 2])
            with col_save:
                if st.button("⭐ Save Valuation to Portfolio", use_container_width=True):
                    saved = save_prediction_log(
                        property_mode="Regional HP" if is_hp_mode else "Standard",
                        location=location_label,
                        area_sqft=float(area_sqft),
                        bedrooms=int(bhk if is_hp_mode else bedrooms),
                        bathrooms=float(bathrooms),
                        overall_qual=int(mapped_qual if is_hp_mode else overall_qual),
                        year_built=int(mapped_year if is_hp_mode else year_built),
                        model_used=st.session_state["data_info"].get("model_name", "Random Forest"),
                        predicted_price=pred_price,
                        low_bound=low_price,
                        high_bound=high_price,
                        currency=curr_symbol,
                        notes=notes_input,
                    )
                    if saved:
                        st.success("✨ Valuation estimate saved to your portfolio!")


# ====================================================
# TAB 2: MARKET INSIGHTS & EDA
# ====================================================
with tab_eda:
    st.markdown("### 📊 Market Exploratory Data Analysis (EDA)")
    st.caption("Interactive visual distributions, correlations, and dataset statistics.")

    df = st.session_state.get("df")
    if df is None or df.empty:
        st.warning("No dataset loaded. Please upload or load train.csv.")
    else:
        summary = get_dataset_summary(df, "SalePrice")

        # Top Summary KPIs
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_metric_card("Total Properties", f"{summary.get('rows', 0):,}", delta="Ames Housing Records")
        with k2:
            med_price = summary.get("target_stats", {}).get("median", 0)
            render_metric_card("Median Price", f"${med_price:,.0f}", delta="Central Value")
        with k3:
            avg_area = df["GrLivArea"].mean() if "GrLivArea" in df.columns else 0
            render_metric_card("Avg Living Area", f"{avg_area:,.0f} sqft", delta="Mean Floor Area")
        with k4:
            render_metric_card("Features Count", f"{summary.get('columns', 0)} Cols", delta=f"{summary.get('missing_pct', 0)}% Missing cells")

        st.markdown("---")

        # Visual Analytics Charts
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### 📈 Sale Price Distribution")
            use_log = st.checkbox("Apply Log Transform (Normal Distribution View)", value=False)
            chart_dist = plot_price_distribution(df, "SalePrice", use_log=use_log)
            if chart_dist:
                st.altair_chart(chart_dist, use_container_width=True)

        with col_c2:
            st.markdown("#### 🎯 Living Area vs. Sale Price (Quality Coded)")
            chart_scatter = plot_price_vs_area(df, "SalePrice")
            if chart_scatter:
                st.altair_chart(chart_scatter, use_container_width=True)

        col_c3, col_c4 = st.columns(2)
        with col_c3:
            st.markdown("#### 🏘️ Median Price by Neighborhood")
            chart_neigh = plot_price_by_neighborhood(df, "SalePrice", top_n=12)
            if chart_neigh:
                st.altair_chart(chart_neigh, use_container_width=True)

        with col_c4:
            st.markdown("#### 🔗 Top Features Correlating with Price")
            chart_corr = plot_feature_correlations(df, "SalePrice", top_n=10)
            if chart_corr:
                st.altair_chart(chart_corr, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🚨 Missing Data Audit")
        missing_df = get_missing_values_summary(df)
        if not missing_df.empty:
            cm1, cm2 = st.columns([1, 1])
            with cm1:
                chart_missing = plot_missing_values(df)
                if chart_missing:
                    st.altair_chart(chart_missing, use_container_width=True)
            with cm2:
                st.dataframe(missing_df.head(15), use_container_width=True, height=320)
        else:
            st.success("✨ Zero missing values found across all dataset features!")


# ====================================================
# TAB 3: ML MODEL BENCHMARKS
# ====================================================
with tab_ml:
    st.markdown("### 🤖 Machine Learning Model Benchmarking & Studio")
    st.caption("Compare 5 algorithms, evaluate cross-validation metrics, and inspect feature importance weights.")

    df = st.session_state.get("df")
    if df is None:
        st.warning("Please ensure dataset is loaded to train and benchmark models.")
    else:
        # Multi-model Benchmark Runner
        col_bench_btn, col_bench_split = st.columns([1, 2])
        with col_bench_btn:
            run_bench = st.button("⚡ Run Full Model Benchmark (5 Algorithms)", use_container_width=True)
        with col_bench_split:
            test_split_pct = st.slider("Test Partition Split Size", 0.10, 0.35, 0.20, 0.05)

        if run_bench or "benchmark_df" not in st.session_state:
            with st.spinner("Training and benchmarking models..."):
                bench_df = benchmark_all_models(
                    df,
                    target_col="SalePrice",
                    test_size=test_split_pct,
                )
                st.session_state["benchmark_df"] = bench_df

        st.markdown("#### 🏆 Algorithm Performance Comparison")
        if "benchmark_df" in st.session_state:
            st.dataframe(
                st.session_state["benchmark_df"],
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("---")

        # Model Retraining & Fine-tuning
        st.markdown("#### ⚙️ Train & Set Active Model")
        ct1, ct2, ct3 = st.columns(3)
        with ct1:
            selected_model_type = st.selectbox(
                "Choose Algorithm",
                [
                    "Random Forest Regressor",
                    "Gradient Boosting Regressor",
                    "Ridge Regression",
                    "Lasso Regression",
                    "Linear Regression",
                ],
            )
        with ct2:
            rand_seed = st.number_input("Random State Seed", 1, 999, 42)
        with ct3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            train_now = st.button("🚀 Train & Activate Model", use_container_width=True)

        if train_now:
            with st.spinner(f"Training {selected_model_type}..."):
                p, m, d = train_single_model(
                    df,
                    target_col="SalePrice",
                    model_name=selected_model_type,
                    test_size=test_split_pct,
                    random_state=rand_seed,
                )
                st.session_state["pipe"] = p
                st.session_state["metrics"] = m
                st.session_state["data_info"] = d
                save_trained_pipeline(p, d)
                st.success(f"{selected_model_type} trained successfully! (R²: {m['R2_Score']:.3f}, MAE: ${m['MAE']:,.0f})")

        # Active Model Feature Importances
        st.markdown("---")
        st.markdown("#### 🔍 Active Model Feature Importance")
        if st.session_state.get("pipe") is not None and st.session_state.get("data_info") is not None:
            imp_df = extract_feature_importances(
                st.session_state["pipe"],
                st.session_state["data_info"],
                top_n=15,
            )
            if not imp_df.empty:
                col_i1, col_i2 = st.columns([2, 1])
                with col_i1:
                    chart_imp = plot_feature_importance_chart(imp_df)
                    if chart_imp:
                        st.altair_chart(chart_imp, use_container_width=True)
                with col_i2:
                    st.dataframe(imp_df, use_container_width=True, height=340)
            else:
                st.info("Feature importance weights not available for the active model type.")


# ====================================================
# TAB 6: MORTGAGE & ROI PLANNER
# ====================================================
with tab_finance:
    st.markdown("### 💰 Mortgage & Real Estate Investment Planner")
    st.caption("Calculate monthly loan EMI, amortization schedules, and investment rental yields.")

    # Auto-populate from latest prediction if available
    default_price = 350000.0
    if "latest_prediction" in st.session_state:
        default_price = float(st.session_state["latest_prediction"]["price"])

    col_fin1, col_fin2 = st.columns(2)

    with col_fin1:
        st.markdown("#### 🏦 Loan & EMI Calculator")
        prop_val = st.number_input(
            "Property Valuation Price",
            min_value=10000.0,
            value=default_price,
            step=10000.0,
            help="Total cost of the property",
        )
        down_pct = st.slider("Down Payment Percentage (%)", 5.0, 50.0, 20.0, 5.0)
        int_rate = st.slider("Annual Interest Rate (%)", 3.0, 15.0, 8.5, 0.25)
        tenure_yrs = st.slider("Loan Tenure (Years)", 5, 30, 20, 5)

        mortgage_res = calculate_mortgage_emi(
            property_price=prop_val,
            down_payment_pct=down_pct,
            interest_rate_annual=int_rate,
            loan_term_years=tenure_yrs,
        )

        st.markdown("##### 📊 Loan Summary")
        fm1, fm2 = st.columns(2)
        with fm1:
            render_metric_card(
                "Monthly EMI",
                f"${mortgage_res['monthly_emi']:,.0f}" if not is_inr_mode else f"₹{mortgage_res['monthly_emi']:,.0f}",
                delta=f"{tenure_yrs} Years Tenure",
                delta_type="info",
            )
        with fm2:
            render_metric_card(
                "Total Interest Payable",
                f"${mortgage_res['total_interest']:,.0f}" if not is_inr_mode else f"₹{mortgage_res['total_interest']:,.0f}",
                delta=f"Principal: ${mortgage_res['principal']:,.0f}",
                delta_type="info",
            )

    with col_fin2:
        st.markdown("#### 📈 Investment Yield & Cashflow")
        monthly_rent = st.number_input(
            "Expected Monthly Rental Income",
            min_value=0.0,
            value=prop_val * 0.005,
            step=500.0,
        )
        annual_maintenance = st.number_input(
            "Annual Maintenance / Taxes / Insurance",
            min_value=0.0,
            value=prop_val * 0.01,
            step=500.0,
        )

        yield_res = calculate_investment_yield(
            property_price=prop_val,
            monthly_rent=monthly_rent,
            annual_expenses=annual_maintenance,
        )

        st.markdown("##### 💵 Return Metrics")
        fy1, fy2 = st.columns(2)
        with fy1:
            render_metric_card(
                "Gross Rental Yield",
                f"{yield_res['gross_yield']:.2f}%",
                delta=f"Annual: ${yield_res['annual_gross_rent']:,.0f}",
                delta_type="pos",
            )
        with fy2:
            render_metric_card(
                "Net Rental Yield",
                f"{yield_res['net_yield']:.2f}%",
                delta=f"Net Cashflow: ${yield_res['annual_net_income']:,.0f}",
                delta_type="pos",
            )

    st.markdown("---")
    st.markdown("#### 📅 Loan Amortization Schedule & Payoff Curve")
    amort_df = generate_amortization_schedule(
        principal=mortgage_res["principal"],
        interest_rate_annual=int_rate,
        loan_term_years=tenure_yrs,
    )

    if not amort_df.empty:
        col_am1, col_am2 = st.columns([1, 1])
        with col_am1:
            chart_amort = plot_amortization_chart(amort_df)
            if chart_amort:
                st.altair_chart(chart_amort, use_container_width=True)
        with col_am2:
            st.dataframe(amort_df, use_container_width=True, height=300)
