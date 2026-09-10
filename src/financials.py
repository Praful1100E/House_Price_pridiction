"""
Financial and Mortgage Planning Module for Real Estate Investments.
Calculates monthly EMI, loan amortization schedules, rental yields, and cashflow.
"""

from typing import Dict, Tuple
import altair as alt
import numpy as np
import pandas as pd


def calculate_mortgage_emi(
    property_price: float,
    down_payment_pct: float = 20.0,
    interest_rate_annual: float = 8.5,
    loan_term_years: int = 20,
) -> Dict[str, float]:
    """Calculates monthly EMI, total interest, and loan summary."""
    down_payment = property_price * (down_payment_pct / 100.0)
    principal = property_price - down_payment

    if principal <= 0:
        return {
            "monthly_emi": 0.0,
            "principal": 0.0,
            "down_payment": property_price,
            "total_interest": 0.0,
            "total_payment": property_price,
        }

    monthly_rate = (interest_rate_annual / 100.0) / 12.0
    num_months = loan_term_years * 12

    if monthly_rate > 0:
        emi = (
            principal
            * monthly_rate
            * ((1 + monthly_rate) ** num_months)
            / (((1 + monthly_rate) ** num_months) - 1)
        )
    else:
        emi = principal / num_months

    total_payment = emi * num_months
    total_interest = total_payment - principal

    return {
        "monthly_emi": float(emi),
        "principal": float(principal),
        "down_payment": float(down_payment),
        "total_interest": float(total_interest),
        "total_payment": float(total_payment),
    }


def generate_amortization_schedule(
    principal: float, interest_rate_annual: float = 8.5, loan_term_years: int = 20
) -> pd.DataFrame:
    """Generates annual amortization breakdown."""
    if principal <= 0:
        return pd.DataFrame()

    monthly_rate = (interest_rate_annual / 100.0) / 12.0
    num_months = loan_term_years * 12
    if monthly_rate > 0:
        emi = (
            principal
            * monthly_rate
            * ((1 + monthly_rate) ** num_months)
            / (((1 + monthly_rate) ** num_months) - 1)
        )
    else:
        emi = principal / num_months

    records = []
    balance = principal

    for year in range(1, loan_term_years + 1):
        year_interest = 0.0
        year_principal = 0.0

        for _ in range(12):
            if balance <= 0:
                break
            interest = balance * monthly_rate
            principal_part = emi - interest
            if principal_part > balance:
                principal_part = balance
                balance = 0
            else:
                balance -= principal_part

            year_interest += interest
            year_principal += principal_part

        records.append(
            {
                "Year": year,
                "Principal Paid": round(year_principal, 2),
                "Interest Paid": round(year_interest, 2),
                "Ending Balance": round(balance, 2),
            }
        )

    return pd.DataFrame(records)


def plot_amortization_chart(df_amort: pd.DataFrame) -> alt.Chart:
    """Plots interactive Principal vs Interest over the loan lifetime."""
    if df_amort.empty:
        return None

    df_melt = df_amort.melt(
        id_vars=["Year"],
        value_vars=["Principal Paid", "Interest Paid"],
        var_name="Component",
        value_name="Amount",
    )

    chart = (
        alt.Chart(df_melt)
        .mark_bar(opacity=0.85)
        .encode(
            x=alt.X("Year:O", title="Loan Year"),
            y=alt.Y("Amount:Q", title="Annual Payment Breakdown"),
            color=alt.Color(
                "Component:N",
                scale=alt.Scale(
                    domain=["Principal Paid", "Interest Paid"],
                    range=["#10b981", "#f59e0b"],
                ),
            ),
            tooltip=[
                alt.Tooltip("Year:O"),
                alt.Tooltip("Component:N"),
                alt.Tooltip("Amount:Q", format=",.0f"),
            ],
        )
        .properties(height=300)
        .interactive()
    )
    return chart


def calculate_investment_yield(
    property_price: float,
    monthly_rent: float,
    annual_expenses: float = 0.0,
) -> Dict[str, float]:
    """Computes Gross and Net rental yield metrics."""
    annual_rent = monthly_rent * 12.0
    if property_price <= 0:
        return {"gross_yield": 0.0, "net_yield": 0.0, "annual_net_income": 0.0}

    gross_yield = (annual_rent / property_price) * 100.0
    net_income = annual_rent - annual_expenses
    net_yield = (net_income / property_price) * 100.0

    return {
        "gross_yield": round(gross_yield, 2),
        "net_yield": round(net_yield, 2),
        "annual_gross_rent": round(annual_rent, 2),
        "annual_net_income": round(net_income, 2),
    }
