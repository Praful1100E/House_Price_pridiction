"""
UI Theme and Custom Styling for the House Price Prediction & Real Estate Intelligence Platform.
Provides Glassmorphism Dark styling, custom metrics cards, glowing badges, and responsive containers.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-main: #0a0f18;
    --bg-secondary: #0f172a;
    --card-bg: rgba(15, 23, 42, 0.75);
    --card-border: rgba(56, 189, 248, 0.15);
    --card-hover-border: rgba(56, 189, 248, 0.4);
    --primary: #38bdf8;
    --primary-glow: rgba(56, 189, 248, 0.25);
    --accent-purple: #a855f7;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --input-bg: #1e293b;
}

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text-main) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #090d16;
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* Header & Banner Styling */
.hero-container {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 50%, rgba(14, 116, 144, 0.2) 100%);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 20px 0 var(--primary-glow);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

.hero-container::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #38bdf8 60%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    color: var(--text-muted);
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 800px;
    line-height: 1.6;
}

/* Glassmorphic Metric Cards */
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: var(--card-hover-border);
    box-shadow: 0 12px 28px rgba(56, 189, 248, 0.15);
}

.metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.02em;
}

.metric-delta-pos {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--accent-emerald);
    margin-top: 0.3rem;
}

.metric-delta-info {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--primary);
    margin-top: 0.3rem;
}

/* Prediction Result Card */
.price-result-box {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 2px solid rgba(16, 185, 129, 0.4);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);
    backdrop-filter: blur(12px);
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}

.price-result-box .val-title {
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6ee7b7;
    margin-bottom: 0.5rem;
}

.price-result-box .val-price {
    font-size: 3.2rem;
    font-weight: 900;
    color: #34d399;
    letter-spacing: -0.03em;
    text-shadow: 0 0 25px rgba(52, 211, 153, 0.4);
    line-height: 1.1;
    margin: 0.5rem 0;
}

.price-result-box .val-sub {
    font-size: 0.95rem;
    color: var(--text-muted);
}

/* Badges and Chips */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.8rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-cyan { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
.badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
.badge-emerald { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

/* UI Form Inputs & Overrides */
.stTextInput>div>div>input, .stNumberInput input, .stSelectbox>div>div>div {
    background-color: var(--input-bg) !important;
    color: var(--text-main) !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stTextInput>div>div>input:focus, .stNumberInput input:focus, .stSelectbox>div>div>div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px var(--primary-glow) !important;
}

/* Streamlit Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #38bdf8 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5) !important;
}

/* Secondary Button Style */
.secondary-btn .stButton > button {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    box-shadow: none !important;
}
.secondary-btn .stButton > button:hover {
    background: #334155 !important;
    border-color: #64748b !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.6);
    padding: 8px;
    border-radius: 14px;
    border: 1px solid rgba(56, 189, 248, 0.1);
}

.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 10px;
    color: var(--text-muted) !important;
    font-weight: 600;
    padding: 0 16px;
    background-color: transparent;
    border: none !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e293b;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #090d16 !important;
    border-right: 1px solid rgba(56, 189, 248, 0.1) !important;
}

/* Tooltip / Info box */
.info-card {
    background: rgba(30, 41, 59, 0.5);
    border-left: 4px solid var(--primary);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: var(--text-main);
    font-size: 0.92rem;
}

/* Marketplace Property Cards */
.prop-card-container {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.prop-card-container:hover {
    transform: translateY(-4px);
    border-color: var(--card-hover-border);
    box-shadow: 0 16px 36px rgba(56, 189, 248, 0.2);
}

.prop-img-wrapper {
    position: relative;
    width: 100%;
    height: 220px;
    overflow: hidden;
}

.prop-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.prop-card-container:hover .prop-img-wrapper img {
    transform: scale(1.04);
}

.prop-badge-overlay {
    position: absolute;
    top: 12px;
    left: 12px;
    display: flex;
    gap: 6px;
    z-index: 2;
}

.prop-status-overlay {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 2;
}

.prop-price-tag {
    font-size: 1.55rem;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: -0.02em;
    margin: 0.4rem 0;
}

.prop-specs-row {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-muted);
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.prop-amenity-chip {
    display: inline-block;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    color: #cbd5e1;
    margin-right: 4px;
    margin-bottom: 4px;
}

.receipt-box {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}
</style>
"""


def apply_theme():
    """Injects the custom Dark Glassmorphic CSS into the Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero_header(
    title="Real Estate Intelligence Platform",
    subtitle="AI-Powered Valuation Engine, Exploratory Analytics & Property Portfolio Manager",
    badge_text="v2.5 AI Powered",
):
    """Renders the top hero banner with gradient typography and neon styling."""
    html = f"""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <span class="badge badge-cyan">{badge_text}</span>
            <div style="display: flex; gap: 8px;">
                <span class="badge badge-emerald">● Marketplace Live</span>
                <span class="badge badge-purple">AI Valuation Engine</span>
            </div>
        </div>
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = "", delta_type: str = "pos"):
    """Renders a modern glassmorphic KPI card."""
    delta_class = "metric-delta-pos" if delta_type == "pos" else "metric-delta-info"
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    html = f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_price_prediction_card(
    price_str: str,
    confidence_str: str,
    currency_label: str = "USD",
    disclaimer: str = "Based on machine learning regression pipeline",
):
    """Renders the focal price prediction container."""
    html = f"""
    <div class="price-result-box">
        <div class="val-title">Estimated Market Valuation ({currency_label})</div>
        <div class="val-price">{price_str}</div>
        <div style="font-weight: 600; color: #a7f3d0; margin-bottom: 0.4rem;">{confidence_str}</div>
        <div class="val-sub">{disclaimer}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_deal_badge(deal_score: float, price_diff_pct: float):
    """
    Renders an AI Deal Score badge indicating if a property is undervalued, fair, or premium.
    price_diff_pct: (Asking Price - AI Estimated Fair Value) / AI Fair Value * 100
    """
    if price_diff_pct < -8.0:
        return f'<span class="badge badge-emerald">🔥 Hot Deal ({abs(price_diff_pct):.0f}% Under AI Val)</span>'
    elif price_diff_pct > 12.0:
        return f'<span class="badge badge-purple">✨ Luxury Premium (+{price_diff_pct:.0f}%)</span>'
    else:
        return '<span class="badge badge-cyan">⚖️ Fair Market Value</span>'


def render_transaction_receipt(
    order_id: str,
    property_title: str,
    buyer_name: str,
    buyer_email: str,
    amount_formatted: str,
    transaction_type: str,
    tour_date: str = "",
):
    """Renders a verified digital transaction confirmation receipt."""
    tour_html = f"<div><strong>Scheduled Tour Date:</strong> {tour_date}</div>" if tour_date else ""
    html = f"""
    <div class="receipt-box">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(56, 189, 248, 0.2); padding-bottom: 0.8rem; margin-bottom: 1rem;">
            <div style="font-size: 1.1rem; font-weight: 800; color: #34d399;">✅ Transaction Confirmation</div>
            <span class="badge badge-emerald">CONFIRMED #{order_id}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.92rem;">
            <div><strong>Property:</strong> {property_title}</div>
            <div><strong>Transaction Type:</strong> {transaction_type}</div>
            <div><strong>Buyer / Client:</strong> {buyer_name}</div>
            <div><strong>Contact Email:</strong> {buyer_email}</div>
            <div><strong>Amount / Offer:</strong> <span style="color: #38bdf8; font-weight: 700;">{amount_formatted}</span></div>
            {tour_html}
        </div>
        <div style="margin-top: 1rem; font-size: 0.82rem; color: #94a3b8; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 0.6rem;">
            🔒 Verified via Real Estate AI Escrow & Listing Protocol. A confirmation copy has been queued to {buyer_email}.
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

