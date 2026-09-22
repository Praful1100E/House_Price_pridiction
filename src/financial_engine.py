"""
Module 2: Smart Financial Calculator & Scheme Router.
Implements:
- 10% Margin to 90% Loan Capital Structuring
- Rule-based Scheme Auto-Selection (Micro Finance Scheme vs. Term Loan Scheme)
- Exact Moratorium Period (3-month / 6-month) and Post-Moratorium Amortization
- Monthly EMI and Quarterly Repayment Schedules (SCA norms)
- CapEx vs OpEx Allocation & Working Capital Reserve
- Financial Viability Metrics (DSCR, Break-Even Point, Net Profit, Payback Period)
- What-If Stress Testing Engine
"""

import math
from typing import Dict, Any, List
import pandas as pd
from src.geo_database import BUSINESS_CATALOG

class FinancialEngine:
    """Smart Financial Calculator and MoSJE Scheme Router."""

    def __init__(self, available_margin: float, business_name: str, custom_project_cost: float = None):
        self.available_margin = float(available_margin)
        self.business_name = business_name
        
        # Calculate feasible project cost and loan eligibility (10% / 90% rule)
        if custom_project_cost and custom_project_cost > 0:
            self.project_cost = float(custom_project_cost)
            self.margin_amount = self.available_margin
        else:
            self.project_cost = self.available_margin * 10.0
            self.margin_amount = self.available_margin

        # Resolve Scheme & Constraints
        self.scheme_info = self._route_scheme()
        self.loan_amount = min(self.scheme_info["max_loan_cap"], self.project_cost * 0.90)
        
        # Resolve business template
        self.biz_data = BUSINESS_CATALOG.get(business_name, list(BUSINESS_CATALOG.values())[0])

    def _route_scheme(self) -> Dict[str, Any]:
        """
        Auto-routes project to official MoSJE / SCA Scheme:
        Logic A: Project Cost <= 1.40 Lakh -> Micro Finance Scheme (6.5% interest, 3-yr tenure, 3-mo moratorium)
        Logic B: Project Cost > 1.40 Lakh and <= 50.00 Lakh -> Term Loan Scheme (8.0% interest, 7-yr tenure, 6-mo moratorium)
        Logic C: Project Cost > 50.00 Lakh -> Mega Project (SCA cap 45 Lakh + Co-financing)
        """
        if self.project_cost <= 140000:
            return {
                "scheme_id": "MFS",
                "scheme_name": "Micro Finance Scheme",
                "scheme_name_hi": "सूक्ष्म वित्त योजना (Micro Finance Scheme)",
                "target_group": "Targeted marginalized rural micro-entrepreneurs & SHG members",
                "interest_rate_pct": 6.5,
                "tenure_years": 3,
                "tenure_months": 36,
                "moratorium_months": 3,
                "moratorium_quarters": 1,
                "max_loan_cap": 125000.0,
                "agency_share_pct": 90.0,
                "promoter_share_pct": 10.0,
                "category_badge": "🟢 Micro Finance Tier (≤ ₹1.40 Lakh)",
                "description": "Tailored for small rural units up to ₹1.40 Lakh with 6.5% concessional interest and 3-month moratorium."
            }
        elif self.project_cost <= 5000000:
            return {
                "scheme_id": "TLS",
                "scheme_name": "Term Loan Scheme",
                "scheme_name_hi": "सावधि ऋण योजना (Term Loan Scheme)",
                "target_group": "Individual micro & small entrepreneurs, technicians, artisans",
                "interest_rate_pct": 8.0,
                "tenure_years": 7,
                "tenure_months": 84,
                "moratorium_months": 6,
                "moratorium_quarters": 2,
                "max_loan_cap": 4500000.0,
                "agency_share_pct": 90.0,
                "promoter_share_pct": 10.0,
                "category_badge": "🔵 Term Loan Tier (₹1.40 Lakh – ₹50.00 Lakh)",
                "description": "Designed for scalable rural enterprises up to ₹50 Lakh with 8.0% interest and 6-month moratorium."
            }
        else:
            return {
                "scheme_id": "MEGA",
                "scheme_name": "Term Loan Scheme (Syndicated / Co-Financed)",
                "scheme_name_hi": "सावधि ऋण योजना (सिंडिकेटेड / सह-वित्तपोषित)",
                "target_group": "Large rural processing plants & agro-clusters",
                "interest_rate_pct": 8.0,
                "tenure_years": 7,
                "tenure_months": 84,
                "moratorium_months": 6,
                "moratorium_quarters": 2,
                "max_loan_cap": 4500000.0,
                "agency_share_pct": 90.0,
                "promoter_share_pct": 10.0,
                "category_badge": "🟣 High-Value Composite Enterprise (> ₹50.00 Lakh)",
                "description": "Project cost exceeds ₹50 Lakh. SCA maximum loan capped at ₹45 Lakh; remaining balance funded via bank consortium/promoter equity."
            }

    def compute_capex_opex_allocation(self) -> Dict[str, Any]:
        """
        Divides project cost into CapEx (Fixed Capital ~ 70%) and OpEx (Working Capital ~ 30%)
        with itemized breakdowns from the business archetype.
        """
        capex_total = self.project_cost * 0.70
        opex_total = self.project_cost * 0.30
        
        raw_capex = self.biz_data.get("capex_items", [])
        raw_opex = self.biz_data.get("opex_items", [])
        
        capex_items = []
        for item in raw_capex:
            cost = (item["pct"] / 100.0) * capex_total
            capex_items.append({
                "item": item["item"],
                "percentage_of_capex": item["pct"],
                "allocated_amount_inr": round(cost, 2)
            })
            
        opex_items = []
        for item in raw_opex:
            cost = (item["pct"] / 100.0) * opex_total
            opex_items.append({
                "item": item["item"],
                "percentage_of_opex": item["pct"],
                "allocated_amount_inr": round(cost, 2)
            })
            
        return {
            "total_project_cost": self.project_cost,
            "capex_total_inr": capex_total,
            "capex_share_pct": 70.0,
            "opex_total_inr": opex_total,
            "opex_share_pct": 30.0,
            "capex_breakdown": capex_items,
            "opex_breakdown": opex_items
        }

    def calculate_repayment_schedules(self) -> Dict[str, Any]:
        """
        Computes exact Monthly EMI and Quarterly Repayment schedules
        factoring in the 3-month or 6-month moratorium grace periods.
        """
        P = self.loan_amount
        annual_rate = self.scheme_info["interest_rate_pct"]
        total_months = self.scheme_info["tenure_months"]
        moratorium_months = self.scheme_info["moratorium_months"]
        active_repayment_months = total_months - moratorium_months
        
        # Monthly Rate
        r_month = (annual_rate / 100.0) / 12.0
        
        # Standard Equal Monthly Installment post-moratorium
        if r_month > 0 and active_repayment_months > 0:
            monthly_emi = P * (r_month * ((1 + r_month) ** active_repayment_months)) / (((1 + r_month) ** active_repayment_months) - 1)
        else:
            monthly_emi = P / active_repayment_months if active_repayment_months > 0 else 0
            
        # Quarterly calculation (SCA norms)
        total_quarters = self.scheme_info["tenure_years"] * 4
        moratorium_quarters = self.scheme_info["moratorium_quarters"]
        active_quarters = total_quarters - moratorium_quarters
        r_quarter = (annual_rate / 100.0) / 4.0
        
        if r_quarter > 0 and active_quarters > 0:
            quarterly_installment = P * (r_quarter * ((1 + r_quarter) ** active_quarters)) / (((1 + r_quarter) ** active_quarters) - 1)
        else:
            quarterly_installment = P / active_quarters if active_quarters > 0 else 0

        # Build Month-by-Month Amortization Table
        balance = P
        monthly_schedule = []
        total_interest_paid_monthly = 0.0
        
        for m in range(1, total_months + 1):
            if m <= moratorium_months:
                # During moratorium: Zero principal repayment
                interest_accrued = balance * r_month
                monthly_schedule.append({
                    "Month": m,
                    "Status": "Moratorium Grace Period",
                    "Installment_INR": 0.0,
                    "Principal_Paid_INR": 0.0,
                    "Interest_Paid_INR": round(interest_accrued, 2),
                    "Closing_Balance_INR": round(balance, 2)
                })
            else:
                interest = balance * r_month
                principal = monthly_emi - interest
                if balance - principal < 1.0 or m == total_months:
                    principal = balance
                    monthly_emi_adj = principal + interest
                else:
                    monthly_emi_adj = monthly_emi
                    
                balance = max(0.0, balance - principal)
                total_interest_paid_monthly += interest
                
                monthly_schedule.append({
                    "Month": m,
                    "Status": "Active Repayment",
                    "Installment_INR": round(monthly_emi_adj, 2),
                    "Principal_Paid_INR": round(principal, 2),
                    "Interest_Paid_INR": round(interest, 2),
                    "Closing_Balance_INR": round(balance, 2)
                })

        # Build Quarter-by-Quarter Amortization Table (SCA standard)
        balance_q = P
        quarterly_schedule = []
        total_interest_paid_quarterly = 0.0
        
        for q in range(1, total_quarters + 1):
            if q <= moratorium_quarters:
                interest_accrued = balance_q * r_quarter
                quarterly_schedule.append({
                    "Quarter": f"Q{q} (Yr {(q-1)//4 + 1})",
                    "Status": "Moratorium Grace Period",
                    "Quarterly_Due_INR": 0.0,
                    "Principal_INR": 0.0,
                    "Interest_INR": round(interest_accrued, 2),
                    "Closing_Balance_INR": round(balance_q, 2)
                })
            else:
                interest = balance_q * r_quarter
                principal = quarterly_installment - interest
                if balance_q - principal < 1.0 or q == total_quarters:
                    principal = balance_q
                    installment_adj = principal + interest
                else:
                    installment_adj = quarterly_installment
                    
                balance_q = max(0.0, balance_q - principal)
                total_interest_paid_quarterly += interest
                
                quarterly_schedule.append({
                    "Quarter": f"Q{q} (Yr {(q-1)//4 + 1})",
                    "Status": "Active Repayment",
                    "Quarterly_Due_INR": round(installment_adj, 2),
                    "Principal_INR": round(principal, 2),
                    "Interest_INR": round(interest, 2),
                    "Closing_Balance_INR": round(balance_q, 2)
                })

        return {
            "monthly_emi_post_moratorium": round(monthly_emi, 2),
            "quarterly_installment_post_moratorium": round(quarterly_installment, 2),
            "total_principal_borrowed": P,
            "total_interest_payable_monthly": round(total_interest_paid_monthly, 2),
            "total_interest_payable_quarterly": round(total_interest_paid_quarterly, 2),
            "total_repayment_amount": round(P + total_interest_paid_monthly, 2),
            "monthly_schedule_df": pd.DataFrame(monthly_schedule),
            "quarterly_schedule_df": pd.DataFrame(quarterly_schedule)
        }

    def compute_viability_metrics(self) -> Dict[str, Any]:
        """
        Computes Debt Service Coverage Ratio (DSCR), Break-Even Point (BEP),
        Net Profit Margin %, Payback Period, and Multi-Year Cash Flow Projections.
        """
        repayment = self.calculate_repayment_schedules()
        annual_debt_service = repayment["monthly_emi_post_moratorium"] * 12.0
        
        # Estimate annual operations based on scale
        scale_factor = max(1.0, math.sqrt(self.project_cost / 100000.0))
        ue = self.biz_data.get("unit_economics", {})
        daily_units = int(ue.get("daily_output_litres_per_animal", 15.0) * scale_factor)
        annual_units = daily_units * 312 # 312 operating days
        
        selling_price = ue.get("selling_price_liquid", 65.0)
        unit_cost = ue.get("cost_per_unit_liquid", 40.0)
        
        annual_revenue = annual_units * selling_price
        annual_cogs = annual_units * unit_cost
        annual_gross_profit = annual_revenue - annual_cogs
        
        # Fixed operational overheads (Electricity, maintenance, Panchayat cess, insurance)
        annual_fixed_overhead = (self.project_cost * 0.04) + 36000
        annual_net_operating_income = annual_gross_profit - annual_fixed_overhead  # EBITDA
        
        # Average annual interest expense
        avg_annual_interest = repayment["total_interest_payable_monthly"] / self.scheme_info["tenure_years"]
        annual_depreciation = (self.project_cost * 0.70) * 0.10 # 10% on CapEx
        
        profit_before_tax = annual_net_operating_income - avg_annual_interest - annual_depreciation
        tax_estimate = max(0.0, profit_before_tax * 0.05) # rural presumptive/micro tax rate
        net_annual_profit = profit_before_tax - tax_estimate
        
        # Debt Service Coverage Ratio (DSCR) = Net Operating Income / Annual Debt Service
        dscr = round(annual_net_operating_income / annual_debt_service, 2) if annual_debt_service > 0 else 9.99
        
        # Break-Even Point (BEP) in Revenue & %
        contribution_margin_ratio = (selling_price - unit_cost) / selling_price if selling_price > 0 else 0.35
        fixed_costs_total = annual_fixed_overhead + avg_annual_interest
        bep_revenue_inr = round(fixed_costs_total / contribution_margin_ratio, 2) if contribution_margin_ratio > 0 else 0
        bep_utilization_pct = round((bep_revenue_inr / annual_revenue) * 100, 1) if annual_revenue > 0 else 0
        
        # Payback period (Months)
        monthly_cash_generation = (net_annual_profit + annual_depreciation) / 12.0
        payback_months = round(self.project_cost / monthly_cash_generation, 1) if monthly_cash_generation > 0 else 99.0
        
        # 3/7-Year Projection Table
        projection_years = self.scheme_info["tenure_years"]
        multi_year_data = []
        for y in range(1, projection_years + 1):
            growth_mult = (1.0 + 0.06) ** (y - 1) # 6% annual inflation/scale growth
            rev_y = annual_revenue * growth_mult
            cogs_y = annual_cogs * growth_mult
            gp_y = rev_y - cogs_y
            overhead_y = annual_fixed_overhead * ((1.04) ** (y - 1))
            ebitda_y = gp_y - overhead_y
            
            # Debt service (year 1 factors in moratorium)
            if y == 1:
                active_months_y1 = 12 - self.scheme_info["moratorium_months"]
                debt_y = repayment["monthly_emi_post_moratorium"] * active_months_y1
            else:
                debt_y = annual_debt_service
                
            net_cashflow_y = ebitda_y - debt_y
            
            multi_year_data.append({
                "Year": f"Year {y}",
                "Gross_Revenue_INR": round(rev_y, 2),
                "Operating_Costs_INR": round(cogs_y + overhead_y, 2),
                "Net_Operating_Income_INR": round(ebitda_y, 2),
                "Debt_Repayment_INR": round(debt_y, 2),
                "Net_Retained_Cash_Flow_INR": round(net_cashflow_y, 2),
                "DSCR": round(ebitda_y / debt_y, 2) if debt_y > 0 else 9.99
            })

        return {
            "annual_revenue_inr": round(annual_revenue, 2),
            "annual_operating_costs_inr": round(annual_cogs + annual_fixed_overhead, 2),
            "annual_net_operating_income_inr": round(annual_net_operating_income, 2),
            "annual_debt_service_inr": round(annual_debt_service, 2),
            "net_annual_profit_inr": round(net_annual_profit, 2),
            "net_profit_margin_pct": round((net_annual_profit / annual_revenue) * 100, 1) if annual_revenue > 0 else 0,
            "dscr": dscr,
            "dscr_verdict": "Robust & Highly Bankable (DSCR > 2.0x)" if dscr >= 2.0 else ("Bankable (DSCR 1.4x - 2.0x)" if dscr >= 1.4 else "Marginal; Needs Cost Optimization"),
            "bep_revenue_inr": bep_revenue_inr,
            "bep_utilization_pct": bep_utilization_pct,
            "payback_period_months": payback_months,
            "multi_year_projection_df": pd.DataFrame(multi_year_data)
        }

    def run_stress_test(self, revenue_shock_pct: float = 0.0, cost_inflation_pct: float = 0.0, dry_spell_months: int = 0) -> Dict[str, Any]:
        """
        Interactive What-If Scenario Stress Testing:
        Simulates drop in revenue, increase in input costs, and seasonal lean months.
        """
        baseline = self.compute_viability_metrics()
        
        base_rev = baseline["annual_revenue_inr"]
        base_cost = baseline["annual_operating_costs_inr"]
        debt_service = baseline["annual_debt_service_inr"]
        
        # Apply shocks
        stressed_revenue = base_rev * (1.0 - (revenue_shock_pct / 100.0))
        if dry_spell_months > 0:
            # During dry spell months, revenue drops by 60%
            monthly_rev = stressed_revenue / 12.0
            stressed_revenue -= (monthly_rev * 0.60 * dry_spell_months)
            
        stressed_cost = base_cost * (1.0 + (cost_inflation_pct / 100.0))
        stressed_ebitda = max(0.0, stressed_revenue - stressed_cost)
        stressed_dscr = round(stressed_ebitda / debt_service, 2) if debt_service > 0 else 0.0
        stressed_net_cash_flow = stressed_ebitda - debt_service
        
        if stressed_dscr >= 1.5:
            resilience = "🟢 High Resilience: Enterprise easily services debt even under severe market shocks."
        elif stressed_dscr >= 1.1:
            resilience = "🟡 Moderate Resilience: Business remains solvent; avoid unnecessary CapEx."
        else:
            resilience = "🔴 High Vulnerability: Cash flow deficit under this scenario. Requires 3-month working capital reserve or emergency line of credit."
            
        return {
            "revenue_shock_pct": revenue_shock_pct,
            "cost_inflation_pct": cost_inflation_pct,
            "dry_spell_months": dry_spell_months,
            "baseline_revenue": base_rev,
            "stressed_revenue": round(stressed_revenue, 2),
            "baseline_ebitda": baseline["annual_net_operating_income_inr"],
            "stressed_ebitda": round(stressed_ebitda, 2),
            "baseline_dscr": baseline["dscr"],
            "stressed_dscr": stressed_dscr,
            "stressed_net_cash_flow": round(stressed_net_cash_flow, 2),
            "resilience_verdict": resilience
        }

    def generate_complete_financial_report(self) -> Dict[str, Any]:
        """Consolidates complete financial blueprint."""
        return {
            "capital_structure": {
                "available_margin_inr": self.available_margin,
                "total_project_cost_inr": self.project_cost,
                "eligible_loan_inr": self.loan_amount,
                "promoter_margin_pct": 10.0,
                "concessional_loan_pct": 90.0
            },
            "scheme_details": self.scheme_info,
            "capex_opex": self.compute_capex_opex_allocation(),
            "repayment": self.calculate_repayment_schedules(),
            "viability": self.compute_viability_metrics()
        }
