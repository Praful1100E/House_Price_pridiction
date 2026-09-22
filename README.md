# 🌾 Gramin Udyam AI — MoSJE Hyper-Local Business Advisory & Scheme Assistant

**Problem Statement ID**: 26091  
**Problem Statement Title**: AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs  
**Organization**: Ministry of Social Justice and Empowerment (MoSJE)  
**Department**: Department of Social Justice and Empowerment  
**Theme**: Agriculture, FoodTech & Rural Development  
**Category**: Software  

---

## 🏛️ Executive Background & Problem Context

Under various affirmative empowerment schemes of the **Ministry of Social Justice and Empowerment (MoSJE)** and its apex corporations (**NBCFDC**, **NSFDC**, **NSKFDC**), marginalized rural micro-entrepreneurs are eligible for concessional credit assistance. Beneficiaries contribute a **10% margin capital fraction**, while State Channelizing Agencies (SCAs) provide the remaining **90% as a concessional loan**.

However, rural first-time entrepreneurs frequently face high stagnation rates due to:
1. Lack of formal, hyper-local market research tailored to their specific village/block geography.
2. Poor financial literacy regarding margin calculations, concessional scheme routing, moratorium grace periods, and debt amortization.

**Gramin Udyam AI** democratizes institutional-grade business consulting and financial structuring into an easy-to-use, multilingual, voice-guided assistant.

---

## ✨ Core System Architecture & Modules

### 📍 Module 1: Hyper-Local Business Feasibility Report
1. **Market Reach (5–10 km Radius)**:
   - Immediate population, household counts, and monthly addressable consumer spend.
   - Weekly Rural Haat (पेठ / हाट) frequencies and distance to APMC Mandis.
   - Primary distribution channel mix (Village B2C, Weekly Haats, B2B wholesale, Sub-district Mandis).
2. **Opportunity & Value-Addition Gap Analysis**:
   - Highlighting unserved/underserved local niches.
   - Value-addition gross margin spread (Raw commodity vs packaged/processed goods).
   - Seasonal demand cycles (Harvest liquidity, Festive peaks, Monsoon shifts).
3. **Dynamic SWOT Matrix**:
   - Calibrated for micro-enterprise budget scales (< ₹1.40L vs ₹1.40L–₹50L).
4. **Threats Identification & Rural Mitigations**:
   - Raw material price volatility, power outages, perishable spoilage, single-buyer reliance.
   - Actionable rural mitigation strategies.
5. **Competitor Mapping & Saturation Index**:
   - Estimated density of similar units in the block.
   - Saturation score meter (Low, Moderate, High) and recommended spatial buffer (km).
   - Defensible differentiation strategy.
6. **Product Market Value & Unit Pricing Strategy**:
   - Regional purchasing power calibration.
   - Unit economics (Raw materials, labor, power, unit gross profit, margin %).
   - Daily & monthly production capacity, projected revenue, and Break-Even Point (BEP).
7. **Feasibility Index Scorecard**:
   - 0–100 composite health score across Demand, Financials, Competition, and Operations.

---

### 💰 Module 2: Smart Financial Calculator & Scheme Router
1. **Financial Structuring (10% Margin : 90% Loan)**:
   $$\text{Total Feasible Project Cost} = \frac{\text{Available Margin Capital}}{10\%} = \text{Margin} \times 10$$
   $$\text{Concessional Loan Amount} = \text{Total Project Cost} \times 90\% = \text{Margin} \times 9$$
2. **Rule-Based Scheme Auto-Selection**:
   - **Micro Finance Scheme** (Project Cost $\le$ ₹1.40 Lakh):
     - **Interest Rate**: 6.5% p.a. (Concessional)
     - **Tenure**: 3 Years (36 Months)
     - **Moratorium**: **3 Months** (repayment starts from Month 4)
     - **Max Agency Loan**: ₹1.25 Lakh
   - **Term Loan Scheme** (Project Cost > ₹1.40 Lakh & $\le$ ₹50.00 Lakh):
     - **Interest Rate**: 8.0% p.a. (Concessional)
     - **Tenure**: 7 Years (84 Months)
     - **Moratorium**: **6 Months** (repayment starts from Month 7)
     - **Max Agency Loan**: ₹45.00 Lakh
3. **CapEx vs. OpEx Allocation**:
   - Fixed Capital (CapEx): 70% of project cost (Machinery, Shed, Equipment, Tools).
   - Working Capital (OpEx): 30% of project cost (Raw material inventory, 2-3 months buffer).
4. **Repayment & Moratorium Amortization**:
   - Post-moratorium Monthly Equal Monthly Installments (EMI).
   - Quarterly Repayment Schedule (aligned with SCA post-harvest collection norms).
5. **Financial Viability Indicators**:
   - Debt Service Coverage Ratio (DSCR)
   - Break-Even Point (BEP in ₹ & capacity %)
   - Net Profit Margin % & Payback Period (Months)
   - 3-Year / 7-Year multi-year P&L and cash flow projection table.

---

### 🌟 Institutional MoSJE Value-Adds
- **⚡ What-If Sensitivity & Stress Testing**: Real-time simulation of revenue drops (-10% to -40%), feed/input cost inflation (+10% to +30%), and monsoon dry spells.
- **🤖 Gramin Udyam Sathi (ग्रामीण उद्यम साथी)**: Multilingual AI chatbot providing contextual advice on loan documentation, avoiding village credit (Udhaar) losses, and weekly Haat marketing.
- **📑 Bank-Ready Detailed Project Report (DPR) Generator**: One-click generation and download of printable, bank-compliant DPR with official stamps, executive summary, tables, and statutory document checklist.
- **🌐 10 Indian Regional Languages**: English, Hindi, Marathi, Bengali, Tamil, Telugu, Gujarati, Kannada, Punjabi, Odia.
- **🔊 Web Speech Audio Guidance**: Interactive audio button for rural entrepreneurs with diverse literacy levels.

---

## 📁 Directory Structure

```
HousePrice/
├── app.py                      # Main Streamlit Application (Unified Portal)
├── requirements.txt            # Project dependencies
├── README.md                   # Complete system documentation
├── src/
│   ├── __init__.py
│   ├── i18n.py                 # 10-Language Translation & Localization
│   ├── geo_database.py         # Indian Districts, Demographics & 12 Enterprise Catalogs
│   ├── feasibility_engine.py   # Module 1: 6-Part Feasibility Engine & Scorecard
│   ├── financial_engine.py     # Module 2: Scheme Router, 10%/90% Split, Moratorium & DSCR
│   ├── advisory_chat.py        # Gramin Udyam Sathi AI Advisory Chatbot
│   ├── dpr_generator.py        # Bank-Ready Detailed Project Report (HTML/Print Engine)
│   └── ui_components.py        # Theme styling, KPI Cards & Web Speech Audio simulator
└── tests/
    └── test_assistant.py       # Automated Pytest Suite (9 verification tests)
```

---

## 🚀 Quick Start Guide

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run Verification Test Suite
```bash
python -m pytest tests/test_assistant.py -v
```

### 3. Launch Web Portal
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 👥 Targeted Impact
- **Reduces Rural Business Failure Rate** by replacing anecdotal guesswork with data-backed feasibility.
- **Eliminates Financial Confusion** by automatically mapping 10% available cash to 90% borrowing power and exact repayment obligations.
- **Empowers Marginalized Youth & Artisans** with institutional-grade business consulting at the Gram Panchayat level.
