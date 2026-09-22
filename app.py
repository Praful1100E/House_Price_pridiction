"""
Gramin Udyam AI — MoSJE Hyper-Local Business Advisory and Financial Structuring Assistant
Problem Statement ID: 26091
Organization: Ministry of Social Justice and Empowerment (MoSJE)
Department: Department of Social Justice and Empowerment
Theme: Agriculture, FoodTech & Rural Development
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from src.i18n import LANGUAGES, TRANSLATIONS, t
from src.geo_database import GEO_DATA, BUSINESS_CATALOG
from src.feasibility_engine import FeasibilityEngine
from src.financial_engine import FinancialEngine
from src.advisory_chat import GraminUdyamSathi
from src.dpr_generator import DPRGenerator
from src.ui_components import (
    apply_custom_theme,
    render_gov_header,
    render_stat_card,
    render_audio_guidance_bar,
    format_inr
)

# Page configuration
st.set_page_config(
    page_title="Gramin Udyam AI — MoSJE Business & Financial Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom UI theme
apply_custom_theme()

# --- SIDEBAR: Profile & Parameters ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=65)
    st.markdown("### 🇮🇳 **MoSJE Enterprise Portal**")
    
    # Language Selector
    selected_lang_name = st.selectbox(
        "🌐 **Choose Language / भाषा चुनें**",
        options=list(LANGUAGES.values()),
        index=0
    )
    # Get lang code
    lang_code = [k for k, v in LANGUAGES.items() if v == selected_lang_name][0]
    
    st.divider()
    st.markdown(f"#### 📍 **{t('sidebar_inputs', lang_code)}**")
    
    # State selection
    state_list = list(GEO_DATA.keys())
    selected_state = st.selectbox(t("state_label", lang_code), state_list, index=0)
    
    # District selection
    dist_list = list(GEO_DATA[selected_state]["districts"].keys())
    selected_district = st.selectbox(t("district_label", lang_code), dist_list, index=0)
    
    # Block selection
    block_list = GEO_DATA[selected_state].get("blocks", ["Block-1", "Block-2"])
    selected_block = st.selectbox(t("block_label", lang_code), block_list, index=0)
    
    st.divider()
    
    # Business Category Selection
    biz_list = list(BUSINESS_CATALOG.keys())
    selected_biz = st.selectbox(
        t("business_category_label", lang_code),
        biz_list,
        index=0
    )
    
    st.divider()
    
    # Available Margin Capital Input (10% promoter contribution)
    st.markdown(f"#### 💵 **{t('margin_capital_label', lang_code)}**")
    
    # Quick preset buttons
    col_p1, col_p2, col_p3 = st.columns(3)
    preset_val = None
    with col_p1:
        if st.button("₹14,000\n(Micro)", use_container_width=True):
            preset_val = 14000
    with col_p2:
        if st.button("₹1,00,000\n(Term)", use_container_width=True):
            preset_val = 100000
    with col_p3:
        if st.button("₹2,50,000\n(Growth)", use_container_width=True):
            preset_val = 250000

    default_margin = preset_val if preset_val is not None else 100000.0
    
    margin_capital = st.number_input(
        "Enter Margin Money (₹):",
        min_value=5000.0,
        max_value=10000000.0,
        value=float(default_margin),
        step=5000.0,
        format="%.0f"
    )
    
    # Audio guidance toggle
    audio_enabled = st.checkbox("🔊 Enable Audio Guidance (ध्वनि सहायता)", value=True)
    
    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px; color:#666;'>"
        "<b>MoSJE Concessional Credit Guidelines:</b><br>"
        "• Margin Requirement: 10%<br>"
        "• SCA Loan Assistance: 90%<br>"
        "• Micro Finance (≤ ₹1.40L): 6.5% p.a.<br>"
        "• Term Loan (₹1.40L–₹50L): 8.0% p.a."
        "</div>",
        unsafe_allow_html=True
    )

# --- EXECUTE ENGINES ---
feasibility_eng = FeasibilityEngine(
    state=selected_state,
    district=selected_district,
    block=selected_block,
    business_name=selected_biz,
    margin_capital=margin_capital
)
feasibility_data = feasibility_eng.generate_complete_feasibility_report()

financial_eng = FinancialEngine(
    available_margin=margin_capital,
    business_name=selected_biz
)
financial_data = financial_eng.generate_complete_financial_report()

# --- TOP BANNER ---
render_gov_header(
    title=t("app_title", lang_code),
    subtitle=t("tagline", lang_code),
    badge_text=t("ministry_badge", lang_code)
)

# Audio Guidance Bar
if audio_enabled:
    scheme_name_current = financial_data['scheme_details']['scheme_name']
    proj_cost_lakhs = financial_data['capital_structure']['total_project_cost_inr'] / 100000.0
    voice_text = (
        f"आपकी ₹{margin_capital:,.0f} मार्जिन पूंजी पर कुल ₹{proj_cost_lakhs:.2f} लाख का प्रोजेक्ट तैयार किया गया है। "
        f"इसके तहत {scheme_name_current} में 90% रियायती ऋण प्राप्त होगा।"
        if lang_code == "hi" else
        f"Based on your ₹{margin_capital:,.0f} margin capital, your feasible enterprise scale is ₹{proj_cost_lakhs:.2f} Lakhs under {scheme_name_current}."
    )
    render_audio_guidance_bar(voice_text, lang_code)

# --- TOP SUMMARY KPI STRIP ---
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1:
    render_stat_card(
        title=t("project_cost", lang_code),
        value=format_inr(financial_data["capital_structure"]["total_project_cost_inr"]),
        subtitle=f"Margin: {format_inr(margin_capital)} (10%)",
        color_type="green"
    )
with col_k2:
    render_stat_card(
        title=t("loan_amount", lang_code),
        value=format_inr(financial_data["capital_structure"]["eligible_loan_inr"]),
        subtitle=f"Concessional Credit (90%)",
        color_type="blue"
    )
with col_k3:
    scheme_d = financial_data["scheme_details"]
    render_stat_card(
        title=t("selected_scheme", lang_code),
        value=f"{scheme_d['scheme_id']}",
        subtitle=f"{scheme_d['interest_rate_pct']}% p.a. • {scheme_d['tenure_years']} Yrs",
        color_type="gold"
    )
with col_k4:
    rep = financial_data["repayment"]
    render_stat_card(
        title=t("monthly_emi", lang_code),
        value=f"₹{rep['monthly_emi_post_moratorium']:,.0f}",
        subtitle=f"Grace Period: {scheme_d['moratorium_months']} Mo.",
        color_type="purple"
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN NAVIGATION TABS ---
tab_feas, tab_fin, tab_stress, tab_chat, tab_dpr, tab_scheme_guide = st.tabs([
    t("tab_feasibility", lang_code),
    t("tab_financials", lang_code),
    t("tab_stress_test", lang_code),
    t("tab_ai_chat", lang_code),
    t("tab_dpr", lang_code),
    t("tab_schemes", lang_code)
])

# ==============================================================================
# TAB 1: HYPER-LOCAL FEASIBILITY & MARKET STRATEGY (Module 1)
# ==============================================================================
with tab_feas:
    st.markdown(f"### 📍 **Module 1: Hyper-Local Business Feasibility — {selected_biz}**")
    st.caption(f"Location: {selected_block}, {selected_district} ({selected_state}) • Regional Purchasing Power Index: {feasibility_data['location_summary']['purchasing_power_index']}x")
    
    # Feasibility Score & Health Banner
    f_score = feasibility_data["feasibility_scorecard"]
    col_sb1, col_sb2 = st.columns([1.2, 2.8])
    with col_sb1:
        st.markdown(f"""
        <div style="background:#f1f8e9; border:2px solid #81c784; border-radius:12px; padding:18px; text-align:center;">
            <div style="font-size:12px; font-weight:700; color:#2e7d32; text-transform:uppercase;">Overall Feasibility Score</div>
            <div style="font-size:44px; font-weight:900; color:#1b5e20;">{f_score['total_score']}<span style="font-size:22px;">/100</span></div>
            <div style="font-size:14px; font-weight:700; color:#388e3c;">{f_score['rating']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_sb2:
        st.markdown("**Score Components & Verification:**")
        cols_sc = st.columns(4)
        idx = 0
        for comp_name, comp_val in f_score["breakdown"].items():
            with cols_sc[idx % 4]:
                st.metric(label=comp_name, value=comp_val)
            idx += 1
        st.info(f"💡 **AI Appraisal Summary:** {f_score['summary']}")

    st.markdown("---")
    
    # 1. Market Reach (5-10 km radius)
    st.markdown(f"#### 🌐 **{t('market_reach_title', lang_code)}**")
    reach = feasibility_data["market_reach"]
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown(f"""
        <div class="stat-card stat-card-border-green">
            <div class="stat-title">Immediate Radius (5 km)</div>
            <div class="stat-val">{reach['radius_5km']['population']:,}</div>
            <div class="stat-sub"><b>{reach['radius_5km']['households']:,}</b> Rural Households<br>Monthly Spend: ₹{reach['radius_5km']['monthly_addressable_spend_inr']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_r2:
        st.markdown(f"""
        <div class="stat-card stat-card-border-blue">
            <div class="stat-title">Catchment Radius (10 km)</div>
            <div class="stat-val">{reach['radius_10km']['population']:,}</div>
            <div class="stat-sub"><b>{reach['radius_10km']['households']:,}</b> Rural Households<br>Monthly Spend: ₹{reach['radius_10km']['monthly_addressable_spend_inr']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_r3:
        st.markdown(f"""
        <div class="stat-card stat-card-border-gold">
            <div class="stat-title">Rural Haats & Mandi Proximity</div>
            <div class="stat-val">{reach['haat_frequency_weekly']} Haats/Wk</div>
            <div class="stat-sub">Nearest APMC Mandi: <b>{reach['mandi_distance_km']} km</b><br>Connectivity: All-Weather Pucca Road</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Distribution Channels Chart
    df_channels = pd.DataFrame(reach["distribution_channels"])
    col_ch1, col_ch2 = st.columns([1.5, 1])
    with col_ch1:
        st.markdown("##### 📦 Primary Distribution Channels Mix (%)")
        bar_chart = alt.Chart(df_channels).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5).encode(
            x=alt.X('share_pct:Q', title='Target Sales Share (%)'),
            y=alt.Y('channel:N', sort='-x', title='Channel'),
            color=alt.Color('share_pct:Q', scale=alt.Scale(scheme='greens'), legend=None),
            tooltip=['channel', 'share_pct', 'description']
        ).properties(height=200)
        st.altair_chart(bar_chart, use_container_width=True)
    with col_ch2:
        st.markdown("##### 🎯 Channel Execution Blueprint")
        for ch in reach["distribution_channels"]:
            st.markdown(f"• **{ch['channel']}** ({ch['share_pct']}%): *{ch['description']}*")

    st.markdown("---")

    # 2. Opportunity & Value Addition Gap Analysis
    st.markdown(f"#### 💡 **{t('opportunity_title', lang_code)}**")
    opp = feasibility_data["opportunity_analysis"]
    col_op1, col_op2 = st.columns(2)
    with col_op1:
        st.markdown("##### 🌟 High-Potential Local Niches in this Block:")
        for niche in opp["niche_opportunities"]:
            st.markdown(f"✅ **{niche}**")
        st.info(opp["agro_climate_alignment"])
    with col_op2:
        gap = opp["value_addition_gap"]
        st.markdown("##### 📈 Value-Addition Profit Spread vs Raw Commodity:")
        st.markdown(f"""
        <div style="background:#e8f5e9; border:1px solid #a5d6a7; padding:14px; border-radius:8px;">
            <div>• <b>Baseline Sale:</b> {gap['standard_product']}</div>
            <div>• <b>Value-Added Line:</b> <span style="color:#1b5e20; font-weight:bold;">{gap['value_added_product']}</span></div>
            <div style="margin-top:6px; color:#2e7d32; font-weight:bold;">💰 Profit Margin Boost: {gap['profit_margin_gain']}</div>
            <div style="font-size:12px; color:#555; margin-top:6px;">{gap['action_recommendation']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Dynamic SWOT Analysis
    st.markdown(f"#### 🧭 **{t('swot_title', lang_code)}**")
    swot = feasibility_data["swot_analysis"]
    col_sw1, col_sw2 = st.columns(2)
    with col_sw1:
        st.markdown("""<div class="swot-ui-card swot-ui-s"><h4>🟢 STRENGTHS (ताकत)</h4><ul>""" +
                    "".join([f"<li>{s}</li>" for s in swot['strengths']]) +
                    """</ul></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="swot-ui-card swot-ui-o"><h4>🔵 OPPORTUNITIES (अवसर)</h4><ul>""" +
                    "".join([f"<li>{o}</li>" for o in swot['opportunities']]) +
                    """</ul></div>""", unsafe_allow_html=True)
    with col_sw2:
        st.markdown("""<div class="swot-ui-card swot-ui-w"><h4>🟡 WEAKNESSES (कमजोरी)</h4><ul>""" +
                    "".join([f"<li>{w}</li>" for w in swot['weaknesses']]) +
                    """</ul></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="swot-ui-card swot-ui-t"><h4>🔴 THREATS (जोखिम)</h4><ul>""" +
                    "".join([f"<li>{t}</li>" for t in swot['threats']]) +
                    """</ul></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 4. Threats & Mitigations Table
    st.markdown(f"#### 🛡️ **{t('threats_title', lang_code)}**")
    threats_df = pd.DataFrame(feasibility_data["threats_mitigation"])
    st.dataframe(
        threats_df.rename(columns={"threat": "Identified Local Risk", "mitigation": "Prescribed Rural Mitigation", "risk_level": "Severity"}),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # 5. Competitor Density & Saturation Mapping
    st.markdown(f"#### 🗺️ **{t('competitor_title', lang_code)}**")
    comp = feasibility_data["competitor_mapping"]
    col_cp1, col_cp2, col_cp3 = st.columns(3)
    with col_cp1:
        st.metric(
            label="Estimated Similar Units in Block",
            value=f"{comp['estimated_competitors_in_block']} Units",
            delta=comp["saturation_status"]
        )
    with col_cp2:
        st.metric(
            label="Block Saturation Score",
            value=f"{comp['saturation_score_pct']}%",
            delta="Safe Operating Band" if comp['saturation_score_pct'] < 70 else "High Saturation"
        )
    with col_cp3:
        st.metric(
            label="Recommended Spatial Buffer",
            value=comp["recommended_spatial_buffer_km"],
            help="Minimum buffer distance from nearest similar existing business"
        )
    st.success(f"🎯 **Differentiation Roadmap:** {comp['differentiation_strategy']}")

    st.markdown("---")

    # 6. Product Market Value & Unit Pricing Strategy
    st.markdown(f"#### 🏷️ **{t('pricing_title', lang_code)}**")
    pricing = feasibility_data["unit_pricing_economics"]
    col_pr1, col_pr2, col_pr3, col_pr4 = st.columns(4)
    with col_pr1:
        st.metric("Production Cost per Unit", f"₹{pricing['cost_per_unit_inr']:,.1f}")
    with col_pr2:
        st.metric("Recommended Selling Price", f"₹{pricing['recommended_selling_price_inr']:,.1f}")
    with col_pr3:
        st.metric("Gross Profit per Unit", f"₹{pricing['profit_per_unit_inr']:,.1f}", delta=f"{pricing['gross_margin_pct']}% Margin")
    with col_pr4:
        st.metric("Break-Even Monthly Sales", f"{pricing['break_even_units_monthly']:,} Units", help=f"Achieved in ~{pricing['break_even_operating_days_per_month']} operating days/month")

    st.markdown(f"📊 **Monthly Volume & Revenue Projection:** Capacity: **{pricing['monthly_production_units']:,}** {pricing['unit_name']}s/month | Projected Revenue: **₹{pricing['monthly_revenue_inr']:,.0f}** | Estimated Net Operating Income: **₹{pricing['monthly_net_operating_income_inr']:,.0f}/mo**")


# ==============================================================================
# TAB 2: FINANCIAL CALCULATOR & SCHEME ROUTER (Module 2)
# ==============================================================================
with tab_fin:
    st.markdown(f"### 💰 **Module 2: Smart Financial Calculator & Scheme Router**")
    
    # Financial Structuring Callout
    cap = financial_data["capital_structure"]
    scheme = financial_data["scheme_details"]
    
    st.markdown(f"""
    <div class="scheme-hero">
        <h3>🏛️ {scheme['category_badge']}</h3>
        <div style="font-size:15px; color:#2e7d32; font-weight:600; margin-bottom:8px;">{scheme['scheme_name']} ({scheme['scheme_name_hi']})</div>
        <p style="margin:0; font-size:13px; color:#444;">{scheme['description']}</p>
        <div style="display:flex; gap:20px; margin-top:14px; flex-wrap:wrap;">
            <div style="background:#ffffff; padding:8px 16px; border-radius:8px; border:1px solid #c8e6c9;"><b>Interest Rate:</b> <span style="color:#1b5e20;">{scheme['interest_rate_pct']}% p.a. (Concessional)</span></div>
            <div style="background:#ffffff; padding:8px 16px; border-radius:8px; border:1px solid #c8e6c9;"><b>Tenure:</b> {scheme['tenure_years']} Years ({scheme['tenure_months']} Months)</div>
            <div style="background:#ffffff; padding:8px 16px; border-radius:8px; border:1px solid #c8e6c9;"><b>Moratorium Period:</b> <span style="color:#d84315; font-weight:bold;">{scheme['moratorium_months']} Months Grace Period</span></div>
            <div style="background:#ffffff; padding:8px 16px; border-radius:8px; border:1px solid #c8e6c9;"><b>Max Agency Loan Cap:</b> ₹{scheme['max_loan_cap']/100000:,.2f} Lakh</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Capital Split Diagram
    col_cs1, col_cs2 = st.columns([1, 1.4])
    with col_cs1:
        st.markdown("##### 🥧 10% Margin vs 90% Loan Capital Split")
        df_split = pd.DataFrame([
            {"Category": "Promoter Margin (10%)", "Amount": cap["available_margin_inr"]},
            {"Category": "SCA Concessional Loan (90%)", "Amount": cap["eligible_loan_inr"]}
        ])
        donut = alt.Chart(df_split).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Amount", type="quantitative"),
            color=alt.Color(field="Category", type="nominal", scale=alt.Scale(range=["#f57f17", "#2e7d32"])),
            tooltip=["Category", alt.Tooltip("Amount:Q", format=",.0f")]
        ).properties(height=220)
        st.altair_chart(donut, use_container_width=True)
        
    with col_cs2:
        st.markdown("##### 📑 Capital Structuring Breakdown")
        st.markdown(f"""
        - **Your 10% Cash Margin Money:** ₹{cap['available_margin_inr']:,.2f}
        - **Total Feasible Enterprise Scale (Margin / 10%):** **₹{cap['total_project_cost_inr']:,.2f}**
        - **State Channelizing Agency 90% Loan:** **₹{cap['eligible_loan_inr']:,.2f}**
        - **Beneficiary Target Group:** {scheme['target_group']}
        """)
        st.info("💡 Under MoSJE / SCA lending rules, prompt repayment enables micro-entrepreneurs to qualify for next-tier expansion loans up to ₹50 Lakh.")

    st.markdown("---")

    # CapEx vs OpEx Breakdown
    st.markdown("#### 🏗️ **Capital Allocation: CapEx (Fixed 70%) vs OpEx (Working Capital 30%)**")
    capex_opex = financial_data["capex_opex"]
    
    col_co1, col_co2 = st.columns(2)
    with col_co1:
        st.markdown(f"##### 🛠️ Fixed Capital Outlay (CapEx) — ₹{capex_opex['capex_total_inr']:,.0f}")
        df_cx = pd.DataFrame(capex_opex["capex_breakdown"])
        st.dataframe(
            df_cx.rename(columns={"item": "Asset / Machinery Item", "percentage_of_capex": "Share %", "allocated_amount_inr": "Estimated Cost (₹)"}),
            use_container_width=True,
            hide_index=True
        )
    with col_co2:
        st.markdown(f"##### 📦 Working Capital & Buffer (OpEx) — ₹{capex_opex['opex_total_inr']:,.0f}")
        df_ox = pd.DataFrame(capex_opex["opex_breakdown"])
        st.dataframe(
            df_ox.rename(columns={"item": "Operational Expense Category", "percentage_of_opex": "Share %", "allocated_amount_inr": "Allocated Buffer (₹)"}),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # Repayment & Moratorium Amortization Schedules
    st.markdown("#### 📅 **Repayment Schedule & Moratorium Breakdown**")
    repay = financial_data["repayment"]
    
    col_rp1, col_rp2, col_rp3 = st.columns(3)
    with col_rp1:
        st.metric("Post-Moratorium Monthly EMI", f"₹{repay['monthly_emi_post_moratorium']:,.0f}", help=f"Active from Month {scheme['moratorium_months'] + 1} to Month {scheme['tenure_months']}")
    with col_rp2:
        st.metric("Quarterly SCA Repayment Norm", f"₹{repay['quarterly_installment_post_moratorium']:,.0f}", help="SCA post-harvest quarterly repayment cycle")
    with col_rp3:
        st.metric("Total Interest Payable", f"₹{repay['total_interest_payable_monthly']:,.0f}", delta=f"Subsidized {scheme['interest_rate_pct']}% p.a.")

    # Amortization Table View
    schedule_toggle = st.radio("Select Schedule View:", ["Quarterly Repayment Schedule (SCA Standard)", "Monthly Amortization Schedule (Full)"], horizontal=True)
    if "Quarterly" in schedule_toggle:
        st.dataframe(repay["quarterly_schedule_df"], use_container_width=True, hide_index=True)
    else:
        st.dataframe(repay["monthly_schedule_df"], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Financial Viability & Multi-Year Projection
    st.markdown("#### 📈 **Multi-Year Financial Viability & DSCR Analysis**")
    viab = financial_data["viability"]
    
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    with col_v1:
        st.metric("Debt Service Coverage (DSCR)", f"{viab['dscr']}x", delta=viab["dscr_verdict"])
    with col_v2:
        st.metric("Net Profit Margin", f"{viab['net_profit_margin_pct']}%", delta=f"₹{viab['net_annual_profit_inr']:,.0f}/yr")
    with col_v3:
        st.metric("Break-Even Revenue (BEP)", f"₹{viab['bep_revenue_inr']:,.0f}", help=f"Reaches BEP at {viab['bep_utilization_pct']}% capacity")
    with col_v4:
        st.metric("Payback Period", f"{viab['payback_period_months']} Months", help="Estimated capital recovery timeline")

    st.markdown("##### 📊 Multi-Year Projected Cash Flow & Debt Servicing Table")
    st.dataframe(viab["multi_year_projection_df"], use_container_width=True, hide_index=True)


# ==============================================================================
# TAB 3: WHAT-IF SCENARIO STRESS TESTING
# ==============================================================================
with tab_stress:
    st.markdown("### ⚡ **Interactive What-If Scenario Stress Testing**")
    st.caption("Simulate real-world rural risks (seasonal dry spells, revenue drops, feed/input price inflation) to test debt solvency.")

    col_st1, col_st2, col_st3 = st.columns(3)
    with col_st1:
        rev_shock = st.slider("🔻 Revenue Drop / Market Price Crash (%):", 0, 40, 15, step=5)
    with col_st2:
        cost_shock = st.slider("🔺 Raw Material & Feed Price Inflation (%):", 0, 40, 10, step=5)
    with col_st3:
        dry_months = st.slider("🌦️ Monsoon / Seasonal Lean Slump (Months):", 0, 4, 1, step=1)

    # Run stress test simulation
    stress_results = financial_eng.run_stress_test(
        revenue_shock_pct=float(rev_shock),
        cost_inflation_pct=float(cost_shock),
        dry_spell_months=dry_months
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric(
            label="Stressed Gross Revenue",
            value=f"₹{stress_results['stressed_revenue']:,.0f}",
            delta=f"-{rev_shock}% Shock" if rev_shock > 0 else "Baseline"
        )
    with col_res2:
        st.metric(
            label="Stressed Operating EBITDA",
            value=f"₹{stress_results['stressed_ebitda']:,.0f}",
            delta=f"Baseline: ₹{stress_results['baseline_ebitda']:,.0f}"
        )
    with col_res3:
        st.metric(
            label="Stressed DSCR Debt Coverage",
            value=f"{stress_results['stressed_dscr']}x",
            delta="Solvent" if stress_results['stressed_dscr'] >= 1.2 else "Risk Alert",
            delta_color="normal" if stress_results['stressed_dscr'] >= 1.2 else "inverse"
        )

    st.markdown(f"""
    <div style="background:#f9fbe7; border:2px solid #dce775; padding:18px; border-radius:10px; margin-top:15px;">
        <h4 style="margin:0 0 8px 0; color:#33691e;">🛡️ Stress Resilience Verdict:</h4>
        <div style="font-size:15px; font-weight:700;">{stress_results['resilience_verdict']}</div>
        <div style="font-size:13px; color:#555; margin-top:6px;">
            Under this stress scenario, your projected annual retained cash flow is <b>₹{stress_results['stressed_net_cash_flow']:,.0f}</b> after full debt servicing.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 4: GRAMIN UDYAM SATHI (AI ADVISORY CHATBOT)
# ==============================================================================
with tab_chat:
    st.markdown("### 🤖 **Gramin Udyam Sathi (ग्रामीण उद्यम साथी) — AI Advisory Hub**")
    st.caption("Ask questions in your language regarding bank applications, cost reduction, scheme norms, and marketing strategies.")

    advisor = GraminUdyamSathi(
        state=selected_state,
        district=selected_district,
        block=selected_block,
        business_name=selected_biz,
        margin_capital=margin_capital,
        scheme_name=financial_data['scheme_details']['scheme_name'],
        lang=lang_code
    )

    # Quick prompt buttons
    st.markdown("##### ⚡ Quick Suggested Questions (त्वरित प्रश्न):")
    suggested = advisor.get_suggested_prompts()
    cols_q = st.columns(len(suggested))
    clicked_q = None
    for idx, prompt_item in enumerate(suggested):
        with cols_q[idx]:
            if st.button(prompt_item["q"], key=f"q_btn_{idx}", use_container_width=True):
                clicked_q = prompt_item["q"]

    # Chat history state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # If button clicked, process it
    if clicked_q:
        ans = advisor.respond(clicked_q)
        st.session_state.chat_history.append({"user": clicked_q, "bot": ans})

    # User input box
    user_query = st.chat_input("Type your question here (e.g. How to get loan documents or market milk in weekly haat?)...")
    if user_query:
        ans = advisor.respond(user_query)
        st.session_state.chat_history.append({"user": user_query, "bot": ans})

    # Render chat conversation
    if not st.session_state.chat_history:
        # Default welcome message
        st.info("👋 Welcome to **Gramin Udyam Sathi**! Click any quick suggestion above or type your question in the chat box below.")
    else:
        for chat_msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat_msg["user"])
            with st.chat_message("assistant", avatar="🌾"):
                st.markdown(chat_msg["bot"])


# ==============================================================================
# TAB 5: BANK-READY DETAILED PROJECT REPORT (DPR)
# ==============================================================================
with tab_dpr:
    st.markdown("### 📑 **Bank-Ready Detailed Project Report (DPR) Generator**")
    st.caption("Official format compliant with MoSJE, State Channelizing Agencies (SCAs), and Lead District Banks.")

    dpr_gen = DPRGenerator(feasibility_data, financial_data, lang_code)
    html_dpr_content = dpr_gen.generate_html_dpr()

    col_dl1, col_dl2 = st.columns([1, 2])
    with col_dl1:
        st.download_button(
            label="📥 Download Official Bank-Ready DPR (HTML / Print)",
            data=html_dpr_content,
            file_name=f"MoSJE_DPR_{selected_biz.replace(' ', '_')}_{selected_district}.html",
            mime="text/html",
            use_container_width=True
        )
    with col_dl2:
        st.success("✅ Certified Bank-Ready: Includes Executive Summary, 5-10km Catchment, CapEx/OpEx, Multi-Year P&L, DSCR, and Verification Seal.")

    st.markdown("---")
    st.markdown("#### 👁️ **Live DPR Document Preview:**")
    st.components.v1.html(html_dpr_content, height=850, scrolling=True)


# ==============================================================================
# TAB 6: MoSJE SCHEME GUIDELINES & SCA ROADMAP
# ==============================================================================
with tab_scheme_guide:
    st.markdown("### 🏛️ **MoSJE Scheme Guidelines & State Channelizing Agency (SCA) Directory**")
    
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        st.markdown("""
        #### 🏢 **Apex Financing Corporations under MoSJE:**
        1. **NBCFDC** (National Backward Classes Finance & Development Corporation):
           - Concessional loan schemes for backward classes living below double the poverty line.
           - Micro Finance schemes up to ₹1.40 Lakh @ 6.5% p.a.
           - Term Loan schemes up to ₹50 Lakh @ 8.0% p.a.
        2. **NSFDC** (National Scheduled Castes Finance & Development Corporation):
           - Concessional credit empowerment for Scheduled Caste micro-entrepreneurs.
        3. **NSKFDC** (National Safai Karamcharis Finance & Development Corporation):
           - Special credit and mechanized sanitation enterprise loan facilities.
        """)
    with col_sc2:
        st.markdown("""
        #### 📋 **Step-by-Step SCA Application Roadmap:**
        1. **Step 1: Feasibility & Margin Finalization**
           - Finalize 10% margin cash deposit and select business category.
        2. **Step 2: Generate Bank-Ready DPR**
           - Download the comprehensive DPR from Tab 5 of this assistant.
        3. **Step 3: Submit to District SCA Office / DIC**
           - Submit application dossier with Aadhaar, Caste Certificate, Land/Panchayat NOC, and 2 Quotations.
        4. **Step 4: Joint Field Appraisal & Sanction**
           - SCA officer verifies location; loan sanctioned with statutory 3-6 month moratorium.
        5. **Step 5: Direct Disbursement & Asset Purchase**
           - Funds disbursed directly for CapEx machinery and working capital buffer.
        """)

    st.markdown("---")
    st.markdown("""
    #### 📞 **State Channelizing Agency (SCA) Liaison Support & Helpdesk:**
    - **Toll-Free National Helpline:** `1800-180-2121` (MoSJE Rural Enterprise Cell)
    - **Official MoSJE Portal:** [socialjustice.gov.in](https://socialjustice.gov.in)
    - **District Offices:** District Industries Centre (DIC) & District Social Welfare Officer in every District Collectorate.
    """)
