"""
UI Styling, Visual Theme, and Custom Interactive Components.
Provides Rural-Tech Green & Gold aesthetics, glassmorphic stat cards,
Speech/Audio accessibility guidance, and responsive badge components.
"""

import streamlit as st

def apply_custom_theme():
    """Injects high-contrast, polished CSS theme tailored for rural enterprise platform."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        }
        
        /* Main background & Container */
        .main {
            background: linear-gradient(135deg, #f7faf7 0%, #edf4ee 100%);
        }
        
        /* Top Navigation Header Card */
        .gov-banner {
            background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 50%, #1565c0 100%);
            color: #ffffff;
            padding: 16px 24px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(27, 94, 32, 0.15);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .gov-banner h2 {
            margin: 0;
            font-size: 22px;
            font-weight: 800;
            color: #ffffff !important;
            letter-spacing: -0.5px;
        }
        
        .gov-banner p {
            margin: 4px 0 0 0;
            font-size: 13px;
            opacity: 0.92;
            color: #e8f5e9;
        }
        
        .badge-pill {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
            display: inline-block;
        }
        
        /* High-Impact Stat Card */
        .stat-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 18px 20px;
            border: 1px solid #e0ebd8;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(46, 125, 50, 0.12);
            border-color: #a5d6a7;
        }
        
        .stat-card-border-green { border-top: 4px solid #2e7d32; }
        .stat-card-border-blue { border-top: 4px solid #1976d2; }
        .stat-card-border-gold { border-top: 4px solid #f57f17; }
        .stat-card-border-purple { border-top: 4px solid #7b1fa2; }
        
        .stat-title {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #556b2f;
            margin-bottom: 6px;
        }
        
        .stat-val {
            font-size: 24px;
            font-weight: 800;
            color: #1a331e;
            line-height: 1.1;
        }
        
        .stat-sub {
            font-size: 12px;
            color: #667085;
            margin-top: 6px;
        }
        
        /* Scheme Highlight Callout */
        .scheme-hero {
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
            border: 2px solid #81c784;
            border-radius: 14px;
            padding: 22px;
            margin: 15px 0 25px 0;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
        }
        
        .scheme-hero h3 {
            margin: 0 0 8px 0;
            color: #1b5e20;
            font-size: 20px;
            font-weight: 800;
        }
        
        /* Audio Guidance Banner */
        .audio-guide-box {
            background: #fff8e1;
            border: 1px solid #ffe082;
            border-left: 5px solid #ffb300;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* SWOT Cards */
        .swot-ui-card {
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
            height: 100%;
        }
        .swot-ui-s { background: #e8f5e9; border: 1px solid #a5d6a7; color: #1b5e20; }
        .swot-ui-w { background: #fff8e1; border: 1px solid #ffe082; color: #f57f17; }
        .swot-ui-o { background: #e1f5fe; border: 1px solid #81d4fa; color: #0277bd; }
        .swot-ui-t { background: #ffebee; border: 1px solid #ffcdd2; color: #c62828; }
        
        .swot-ui-card h4 {
            margin: 0 0 10px 0;
            font-size: 15px;
            font-weight: 800;
        }
        
        .swot-ui-card ul {
            margin: 0;
            padding-left: 18px;
            font-size: 13px;
            color: #333;
        }
        
        .swot-ui-card li {
            margin-bottom: 6px;
        }

        /* Streamlit Tabs Customization */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #e8ede6;
            padding: 6px;
            border-radius: 12px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 600;
            font-size: 14px;
            background-color: transparent;
            border: none;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1b5e20 !important;
            color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(27, 94, 32, 0.25);
        }
    </style>
    """, unsafe_allow_html=True)

def render_gov_header(title: str, subtitle: str, badge_text: str):
    """Renders official MoSJE portal banner."""
    st.markdown(f"""
    <div class="gov-banner">
        <div>
            <h2>🏛️ {title}</h2>
            <p>{subtitle}</p>
        </div>
        <div>
            <span class="badge-pill">🇮🇳 {badge_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stat_card(title: str, value: str, subtitle: str, color_type: str = "green"):
    """Renders polished KPI stat card."""
    border_class = f"stat-card-border-{color_type}"
    st.markdown(f"""
    <div class="stat-card {border_class}">
        <div class="stat-title">{title}</div>
        <div class="stat-val">{value}</div>
        <div class="stat-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_audio_guidance_bar(message: str, lang_code: str = "en"):
    """
    Renders an interactive Web Speech Audio Synthesizer widget for rural users.
    """
    # Safe javascript speech synthesis script
    speech_js = f"""
    <div class="audio-guide-box">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:24px;">🔊</span>
            <div>
                <b style="color:#b78103; font-size:13px;">AUDIO GUIDANCE / ध्वनि सहायता:</b>
                <div style="font-size:13px; color:#444;">{message}</div>
            </div>
        </div>
        <div>
            <button onclick="
                var msg = new SpeechSynthesisUtterance('{message.replace("'", "")}');
                msg.lang = '{lang_code if lang_code in ['en', 'hi'] else 'hi-IN'}';
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            " style="background:#ffb300; color:#000; border:none; padding:6px 14px; border-radius:20px; font-weight:700; cursor:pointer; font-size:12px;">
                ▶ Play Voice / आवाज़ सुनें
            </button>
        </div>
    </div>
    """
    st.markdown(speech_js, unsafe_allow_html=True)

def format_inr(amount: float) -> str:
    """Formats numeric amount into Indian Currency Format."""
    if amount >= 10000000:
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount/100000:.2f} Lakh"
    else:
        return f"₹{amount:,.0f}"
