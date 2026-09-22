"""
Unit and Integration Test Suite for MoSJE Business Advisory and Financial Structuring Assistant.
Tests:
1. Scheme Auto-Selection Rules (≤ ₹1.40L vs > ₹1.40L to ₹50L vs > ₹50L)
2. 10% Margin to 90% Concessional Loan Structuring
3. Micro Finance Scheme Amortization (6.5% interest, 3-year tenure, 3-month moratorium)
4. Term Loan Scheme Amortization (8.0% interest, 7-year tenure, 6-month moratorium)
5. Feasibility Engine (Market reach, SWOT, Competitor Saturation, Unit Economics)
6. What-If Stress Testing Engine
7. Multilingual Localization and DPR Generation
"""

import pytest
import pandas as pd
from src.financial_engine import FinancialEngine
from src.feasibility_engine import FeasibilityEngine
from src.advisory_chat import GraminUdyamSathi
from src.dpr_generator import DPRGenerator
from src.i18n import t, LANGUAGES
from src.geo_database import GEO_DATA, BUSINESS_CATALOG

class TestSchemeRoutingAndFinancials:
    """Test suite for Module 2: Financial Calculator and Scheme Router."""

    def test_micro_finance_scheme_routing(self):
        """Test routing when project cost <= 1.40 Lakh (Margin <= 14,000)."""
        engine = FinancialEngine(available_margin=10000.0, business_name="Dairy Farming & Value-Added Milk Products")
        report = engine.generate_complete_financial_report()
        
        # 10% margin -> 1,00,000 project cost
        assert report["capital_structure"]["total_project_cost_inr"] == 100000.0
        assert report["capital_structure"]["eligible_loan_inr"] == 90000.0
        assert report["scheme_details"]["scheme_id"] == "MFS"
        assert report["scheme_details"]["scheme_name"] == "Micro Finance Scheme"
        assert report["scheme_details"]["interest_rate_pct"] == 6.5
        assert report["scheme_details"]["tenure_years"] == 3
        assert report["scheme_details"]["moratorium_months"] == 3

    def test_term_loan_scheme_routing(self):
        """Test routing when project cost > 1.40 Lakh and <= 50.00 Lakh (Margin e.g. 1,00,000)."""
        engine = FinancialEngine(available_margin=100000.0, business_name="Dairy Farming & Value-Added Milk Products")
        report = engine.generate_complete_financial_report()
        
        # 10% margin -> 10,00,000 project cost
        assert report["capital_structure"]["total_project_cost_inr"] == 1000000.0
        assert report["capital_structure"]["eligible_loan_inr"] == 900000.0
        assert report["scheme_details"]["scheme_id"] == "TLS"
        assert report["scheme_details"]["scheme_name"] == "Term Loan Scheme"
        assert report["scheme_details"]["interest_rate_pct"] == 8.0
        assert report["scheme_details"]["tenure_years"] == 7
        assert report["scheme_details"]["moratorium_months"] == 6

    def test_moratorium_in_amortization_schedule(self):
        """Verify that months 1 to moratorium have 0 principal repayment."""
        engine = FinancialEngine(available_margin=14000.0, business_name="Agro-Processing, Flour / Oil Mill & Spice Grinding")
        repay = engine.calculate_repayment_schedules()
        df_monthly = repay["monthly_schedule_df"]
        
        # Check first 3 months have 0 principal
        for m in range(3):
            assert df_monthly.iloc[m]["Principal_Paid_INR"] == 0.0
            assert "Moratorium" in df_monthly.iloc[m]["Status"]
            
        # Month 4 should have active repayment
        assert df_monthly.iloc[3]["Principal_Paid_INR"] > 0.0
        assert "Active" in df_monthly.iloc[3]["Status"]

    def test_capex_opex_split(self):
        """Verify 70% CapEx and 30% OpEx split."""
        engine = FinancialEngine(available_margin=50000.0, business_name="Rural Retail, Kirana & Departmental Supply Hub")
        capex_opex = engine.compute_capex_opex_allocation()
        
        total = capex_opex["total_project_cost"]
        assert total == 500000.0
        assert capex_opex["capex_total_inr"] == 350000.0
        assert capex_opex["opex_total_inr"] == 150000.0
        assert len(capex_opex["capex_breakdown"]) > 0
        assert len(capex_opex["opex_breakdown"]) > 0

    def test_stress_testing_engine(self):
        """Verify What-If sensitivity simulation."""
        engine = FinancialEngine(available_margin=100000.0, business_name="Dairy Farming & Value-Added Milk Products")
        stress = engine.run_stress_test(revenue_shock_pct=20.0, cost_inflation_pct=15.0, dry_spell_months=2)
        
        assert stress["stressed_revenue"] < stress["baseline_revenue"]
        assert stress["stressed_ebitda"] < stress["baseline_ebitda"]
        assert stress["stressed_dscr"] >= 0.0
        assert "Resilience" in stress["resilience_verdict"] or "Vulnerability" in stress["resilience_verdict"]

class TestFeasibilityEngine:
    """Test suite for Module 1: Hyper-Local Feasibility Engine."""

    def test_feasibility_generation(self):
        engine = FeasibilityEngine(
            state="Uttar Pradesh",
            district="Varanasi",
            block="Chiraigaon",
            business_name="Dairy Farming & Value-Added Milk Products",
            margin_capital=100000.0
        )
        report = engine.generate_complete_feasibility_report()
        
        # Check market reach
        reach = report["market_reach"]
        assert reach["radius_5km"]["population"] > 0
        assert reach["radius_10km"]["population"] > reach["radius_5km"]["population"]
        assert reach["haat_frequency_weekly"] >= 1
        assert len(reach["distribution_channels"]) >= 3
        
        # Check SWOT
        swot = report["swot_analysis"]
        assert len(swot["strengths"]) >= 3
        assert len(swot["weaknesses"]) >= 3
        assert len(swot["opportunities"]) >= 3
        assert len(swot["threats"]) >= 3
        
        # Check Unit Economics
        pricing = report["unit_pricing_economics"]
        assert pricing["recommended_selling_price_inr"] > pricing["cost_per_unit_inr"]
        assert pricing["profit_per_unit_inr"] > 0
        assert pricing["break_even_units_monthly"] > 0
        
        # Check Scorecard
        score = report["feasibility_scorecard"]
        assert 0 <= score["total_score"] <= 100

class TestDPRAndLocalization:
    """Test suite for DPR generation and i18n localization."""

    def test_dpr_html_generation(self):
        f_engine = FeasibilityEngine("Bihar", "Muzaffarpur", "Kanti", "Food Processing, Pickles, Papad & Spices", 25000.0)
        f_rep = f_engine.generate_complete_feasibility_report()
        
        fin_engine = FinancialEngine(25000.0, "Food Processing, Pickles, Papad & Spices")
        fin_rep = fin_engine.generate_complete_financial_report()
        
        dpr_gen = DPRGenerator(f_rep, fin_rep, "en")
        html_out = dpr_gen.generate_html_dpr()
        
        assert "<html" in html_out
        assert "DETAILED PROJECT REPORT" in html_out
        assert "Food Processing" in html_out
        assert "Capital Expenditure (CapEx) Breakdown" in html_out
        assert "DSCR" in html_out

    def test_i18n_translation(self):
        assert t("project_cost", "hi") == "कुल साध्य परियोजना लागत"
        assert t("loan_amount", "hi") == "रियायती ऋण राशि (90%)"
        assert len(LANGUAGES) == 10

    def test_advisory_chatbot(self):
        bot = GraminUdyamSathi("Madhya Pradesh", "Indore", "Sanwer", "Dairy Farming & Value-Added Milk Products", 50000.0, "Term Loan Scheme", "hi")
        response = bot.respond("ऋण के लिए कौन से दस्तावेज चाहिए?")
        assert "दस्तावेज" in response or "चेकलिस्ट" in response or "Aadhaar" in response
