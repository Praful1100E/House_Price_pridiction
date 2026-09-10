# 🏡 Real Estate Marketplace & AI Valuation Platform

An enterprise-grade, high-performance real estate marketplace and intelligence platform built with **Streamlit**, **Scikit-Learn**, and **SQLite**. Features **Buy & Sell Property Marketplace**, **AI Deal Radar**, **AI-Assisted Listing Price Estimator**, single & batch property price prediction, multi-model benchmarking (5 algorithms), exploratory data analysis (EDA), regional market valuations (Himachal Pradesh & Hill Stations), interactive mortgage/EMI financial planning, and persistent SQLite database logging.

---

## ✨ Key Features

1. **🛒 Real Estate Marketplace (Buy Houses)**:
   - **Curated Property Catalog**: Pre-populated with 12+ luxury and residential homes across US and Indian hill station markets (Shimla, Manali, Dharamshala, Beverly Hills, Seattle, Miami, Austin, Lake Tahoe, etc.).
   - **AI Deal Radar**: Compares asking price against our trained ML regression models to detect undervalued "Hot Deals" and fair valuations.
   - **Interactive Property Inspection**: High-resolution photography, detailed specs (BHK, Baths, SqFt, Garage, Year Built, Quality), and amenity badges.
   - **Direct Purchase & Offer Flow**: Submit instant Buy Now purchase orders with escrow verification receipts, negotiate with counter-offers, or schedule in-person/virtual 3D property tours.

2. **🏷️ Sell Houses & AI Listing Studio**:
   - Step-by-step listing wizard with curated luxury architecture photo presets or custom image URLs.
   - **🤖 AI Price Suggester**: Instant model evaluation on custom specs (Living Area, BHK, Quality, District/Region) to recommend fair market asking prices.
   - **Seller Dashboard**: Manage active listings, toggle status (`Available`, `Under Offer`, `Sold`), and view incoming buyer bids and tour appointments.

3. **🏡 Instant AI Valuation Studio**:
   - **Regional Hill Station Valuator**: Calibrated for Indian districts (Shimla, Manali, Dharamshala, Solan, Kasauli, Kullu, etc.) with scenic view multipliers, BHK & age configurations, and ₹ INR Lakhs/Crores display.
   - **Comprehensive Property Valuator**: Advanced multi-variable valuation for global/standard residential properties.
   - **Confidence Range & Valuation Band**: Provides 95% Confidence Interval and Price per Sq. Ft. metrics.
   - **Direct SQLite Saving**: Log predictions with customizable tags and notes.

4. **📊 Market Insights & EDA Dashboard**:
   - Interactive Altair charts: Price distribution (with log scale toggle), Living Area vs Price scatter plots, Median price by neighborhood, and Top correlating features.
   - Missing data audit and dataset summary statistics.

5. **🤖 ML Studio & Multi-Model Benchmarking**:
   - Side-by-side comparison of 5 machine learning models:
     - **Random Forest Regressor**
     - **Gradient Boosting Regressor**
     - **Ridge Regression**
     - **Lasso Regression**
     - **Linear Regression**
   - Evaluation metrics: $R^2$ (Test), $R^2$ (Train/Overfitting check), MAE, RMSE, MAPE.
   - Feature importance rankings and live hyperparameter retraining.

6. **📂 Data Management & SQLite Database**:
   - **Dataset Explorer**: Filter, search, and export training data.
   - **Valuation History Tracker**: View, search, delete, and export past logged valuations to CSV.
   - **Custom Property Portfolio**: Add, view, manage, and delete custom real estate inventory listings.

7. **📁 Batch Inference Engine**:
   - Upload any custom CSV or load pre-packaged `test.csv`.
   - Generates bulk property estimates with low/high valuation bounds and downloads enriched CSV files.

8. **💰 Mortgage & Financial Planner**:
   - Monthly loan EMI calculator with principal vs interest breakdown.
   - Year-by-year loan amortization schedule and interactive payoff curve.
   - Investment Gross & Net Rental Yield calculator.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```

The application will automatically launch in your default web browser at `http://localhost:8501`.

---

## 📁 Project Architecture

```
HousePrice/
├── app.py                      # Main Streamlit Application (Entrypoint)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/                       # Dataset directory
│   ├── train.csv               # Ames Housing training dataset
│   ├── test.csv                # Test dataset for batch prediction
│   ├── sample_submission.csv   # Sample format
│   └── data_description.txt   # Feature documentation
├── database/                   # SQLite database directory
│   └── real_estate.db          # Auto-generated database for logs, marketplace & inquiries
├── models/                     # Saved serialized models & metadata
│   ├── house_price_model.joblib
│   └── data_info.json
├── src/                        # Modular source code
│   ├── __init__.py
│   ├── ui_theme.py             # Glassmorphism dark styling & UI components
│   ├── marketplace_ui.py       # Buy & Sell Marketplace, AI Deal Radar & Offer Studio
│   ├── data_manager.py         # Data loaders, audit, SQLite CRUD & seed data
│   ├── ml_engine.py            # Pipelines, multi-model benchmarks & inference
│   ├── analytics.py            # Interactive Altair data visualizations
│   └── financials.py           # Mortgage EMI & Amortization calculators
└── tests/
    └── test_platform.py        # Automated test suite (15 verification stages)
```
