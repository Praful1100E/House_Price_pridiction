"""
Detailed Project Report (DPR) Generator.
Generates institutional-grade, Bank-Ready and MoSJE / SCA compliant DPRs in HTML format
with printable layouts, tables, financial schedules, and official application badges.
"""

from typing import Dict, Any
import datetime

class DPRGenerator:
    """Generates official Bank-Ready Detailed Project Reports."""

    def __init__(self, feasibility_report: Dict[str, Any], financial_report: Dict[str, Any], lang: str = "en"):
        self.f_rep = feasibility_report
        self.fin_rep = financial_report
        self.lang = lang
        self.date_str = datetime.datetime.now().strftime("%d %B, %Y")

    def generate_html_dpr(self) -> str:
        """Generates comprehensive bank-ready HTML DPR document."""
        loc = self.f_rep["location_summary"]
        reach = self.f_rep["market_reach"]
        swot = self.f_rep["swot_analysis"]
        pricing = self.f_rep["unit_pricing_economics"]
        threats = self.f_rep["threats_mitigation"]
        
        cap = self.fin_rep["capital_structure"]
        scheme = self.fin_rep["scheme_details"]
        capex_opex = self.fin_rep["capex_opex"]
        repay = self.fin_rep["repayment"]
        viab = self.fin_rep["viability"]
        proj_df = viab["multi_year_projection_df"]

        # Build capex table rows
        capex_rows = "".join([
            f"<tr><td>{item['item']}</td><td>{item['percentage_of_capex']}%</td><td style='text-align:right;'>₹{item['allocated_amount_inr']:,.2f}</td></tr>"
            for item in capex_opex["capex_breakdown"]
        ])
        
        # Build opex table rows
        opex_rows = "".join([
            f"<tr><td>{item['item']}</td><td>{item['percentage_of_opex']}%</td><td style='text-align:right;'>₹{item['allocated_amount_inr']:,.2f}</td></tr>"
            for item in capex_opex["opex_breakdown"]
        ])

        # Build multi-year table rows
        proj_rows = ""
        for _, row in proj_df.iterrows():
            proj_rows += f"""
            <tr>
                <td><b>{row['Year']}</b></td>
                <td style='text-align:right;'>₹{row['Gross_Revenue_INR']:,.0f}</td>
                <td style='text-align:right;'>₹{row['Operating_Costs_INR']:,.0f}</td>
                <td style='text-align:right;'>₹{row['Net_Operating_Income_INR']:,.0f}</td>
                <td style='text-align:right;'>₹{row['Debt_Repayment_INR']:,.0f}</td>
                <td style='text-align:right; font-weight:bold; color:#1b5e20;'>₹{row['Net_Retained_Cash_Flow_INR']:,.0f}</td>
                <td style='text-align:center;'><b>{row['DSCR']}x</b></td>
            </tr>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bank-Ready Detailed Project Report (DPR) — {loc['business_name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 30px;
            background-color: #f8f9fa;
            color: #212529;
            line-height: 1.6;
        }}
        .dpr-container {{
            max-width: 950px;
            margin: auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-top: 8px solid #1b5e20;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .emblem-title {{
            font-size: 13px;
            font-weight: 700;
            color: #555;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}
        .ministry-title {{
            font-size: 20px;
            font-weight: 800;
            color: #1b5e20;
            margin: 5px 0;
        }}
        .sub-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        .report-title {{
            font-size: 24px;
            font-weight: 800;
            color: #0d47a1;
            margin-top: 15px;
            background: #e3f2fd;
            padding: 10px;
            border-radius: 6px;
            display: inline-block;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            background: #f1f8e9;
            padding: 18px;
            border-radius: 6px;
            border-left: 4px solid #43a047;
            margin-bottom: 25px;
        }}
        .meta-item {{
            font-size: 14px;
        }}
        .meta-item b {{
            color: #2e7d32;
        }}
        h2 {{
            font-size: 18px;
            color: #1b5e20;
            border-bottom: 2px solid #c8e6c9;
            padding-bottom: 6px;
            margin-top: 30px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0 25px 0;
            font-size: 14px;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #f5f5f5;
            color: #333;
            padding: 10px;
            text-align: left;
        }}
        td {{
            padding: 9px 10px;
        }}
        .metric-cards {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .card {{
            background: #f9fbe7;
            border: 1px solid #dce775;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .card-val {{
            font-size: 20px;
            font-weight: bold;
            color: #33691e;
            margin-top: 5px;
        }}
        .card-lbl {{
            font-size: 12px;
            color: #555;
            text-transform: uppercase;
        }}
        .swot-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }}
        .swot-box {{
            padding: 15px;
            border-radius: 6px;
            font-size: 13px;
        }}
        .swot-s {{ background: #e8f5e9; border: 1px solid #a5d6a7; }}
        .swot-w {{ background: #fff3e0; border: 1px solid #ffcc80; }}
        .swot-o {{ background: #e1f5fe; border: 1px solid #81d4fa; }}
        .swot-t {{ background: #ffebee; border: 1px solid #ef9a9a; }}
        .swot-box h4 {{
            margin-top: 0;
            font-size: 14px;
            font-weight: 700;
        }}
        .signature-section {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px dashed #ccc;
            display: flex;
            justify-content: space-between;
        }}
        .sig-box {{
            width: 40%;
            text-align: center;
            border-top: 1px solid #333;
            padding-top: 8px;
            margin-top: 50px;
            font-size: 13px;
            font-weight: 600;
        }}
        @media print {{
            body {{
                background: none;
                padding: 0;
            }}
            .dpr-container {{
                box-shadow: none;
                padding: 15px;
                border: none;
            }}
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>

<div class="dpr-container">
    <div class="header">
        <div class="emblem-title">Government of India • Ministry of Social Justice and Empowerment</div>
        <div class="ministry-title">Department of Social Justice & Empowerment (MoSJE)</div>
        <div class="sub-title">State Channelizing Agencies (SCAs) Concessional Credit Assistance Program</div>
        <div class="report-title">DETAILED PROJECT REPORT (DPR) & FEASIBILITY STUDY</div>
        <div style="font-size: 12px; color: #777; margin-top: 8px;">Date of Appraisal: {self.date_str} | Ref ID: MoSJE/DPR/2026/{cap['total_project_cost_inr']:.0f}</div>
    </div>

    <div class="meta-grid">
        <div class="meta-item"><b>Proposed Enterprise:</b> {loc['business_name']}</div>
        <div class="meta-item"><b>Location:</b> {loc['block']}, {loc['district']}, {loc['state']}</div>
        <div class="meta-item"><b>Auto-Selected Scheme:</b> {scheme['scheme_name']}</div>
        <div class="meta-item"><b>Interest Rate:</b> {scheme['interest_rate_pct']}% p.a. (Concessional)</div>
        <div class="meta-item"><b>Total Project Cost:</b> ₹{cap['total_project_cost_inr']:,.2f}</div>
        <div class="meta-item"><b>Promoter Contribution (10%):</b> ₹{cap['available_margin_inr']:,.2f}</div>
        <div class="meta-item"><b>SCA Concessional Loan (90%):</b> ₹{cap['eligible_loan_inr']:,.2f}</div>
        <div class="meta-item"><b>Moratorium Grace Period:</b> {scheme['moratorium_months']} Months (Tenure: {scheme['tenure_years']} Years)</div>
    </div>

    <h2>1. Executive Summary & Scheme Allocation</h2>
    <p>
        The applicant proposes to establish a <b>{loc['business_name']}</b> unit in <b>{loc['block']}, {loc['district']} ({loc['state']})</b>.
        Under MoSJE / SCA lending guidelines, the promoter contributes 10% margin money (<b>₹{cap['available_margin_inr']:,.2f}</b>), qualifying for a 90% concessional credit facility of <b>₹{cap['eligible_loan_inr']:,.2f}</b> under the <b>{scheme['scheme_name']}</b> at a subsidized rate of <b>{scheme['interest_rate_pct']}% p.a.</b>
        A statutory grace period of <b>{scheme['moratorium_months']} months</b> has been incorporated prior to active debt amortization to ensure stabilization of production and positive operational cash flow.
    </p>

    <div class="metric-cards">
        <div class="card">
            <div class="card-lbl">Project Cost</div>
            <div class="card-val">₹{cap['total_project_cost_inr']/100000:,.2f} L</div>
        </div>
        <div class="card">
            <div class="card-lbl">Post-Moratorium EMI</div>
            <div class="card-val">₹{repay['monthly_emi_post_moratorium']:,.0f}</div>
        </div>
        <div class="card">
            <div class="card-lbl">Quarterly SCA Dues</div>
            <div class="card-val">₹{repay['quarterly_installment_post_moratorium']:,.0f}</div>
        </div>
        <div class="card">
            <div class="card-lbl">DSCR Viability</div>
            <div class="card-val">{viab['dscr']}x</div>
        </div>
    </div>

    <h2>2. Hyper-Local Market Feasibility & Catchment Area</h2>
    <table>
        <tr>
            <th>Parameter</th>
            <th>5 km Radius (Immediate)</th>
            <th>10 km Radius (Catchment)</th>
        </tr>
        <tr>
            <td>Reachable Rural Population</td>
            <td><b>{reach['radius_5km']['population']:,}</b> persons</td>
            <td><b>{reach['radius_10km']['population']:,}</b> persons</td>
        </tr>
        <tr>
            <td>Target Rural Households</td>
            <td><b>{reach['radius_5km']['households']:,}</b> households</td>
            <td><b>{reach['radius_10km']['households']:,}</b> households</td>
        </tr>
        <tr>
            <td>Monthly Addressable Consumer Spend</td>
            <td>₹{reach['radius_5km']['monthly_addressable_spend_inr']:,.2f}</td>
            <td>₹{reach['radius_10km']['monthly_addressable_spend_inr']:,.2f}</td>
        </tr>
        <tr>
            <td>Weekly Rural Haat Frequency</td>
            <td colspan="2">{reach['haat_frequency_weekly']} Market Days / Week across Gram Panchayats</td>
        </tr>
        <tr>
            <td>Distance to APMC Mandi / Town Hub</td>
            <td colspan="2">{reach['mandi_distance_km']} km via All-Weather Pucca Road</td>
        </tr>
    </table>

    <h2>3. Capital Expenditure (CapEx) Breakdown — 70% Fixed Assets</h2>
    <table>
        <tr>
            <th>Asset / Machinery Description</th>
            <th>CapEx Share (%)</th>
            <th style="text-align:right;">Estimated Outlay (₹)</th>
        </tr>
        {capex_rows}
        <tr style="background:#e8f5e9; font-weight:bold;">
            <td>Total Fixed Capital (CapEx)</td>
            <td>70.0%</td>
            <td style="text-align:right;">₹{capex_opex['capex_total_inr']:,.2f}</td>
        </tr>
    </table>

    <h2>4. Working Capital & Operating Expenditure (OpEx) — 30% Buffer</h2>
    <table>
        <tr>
            <th>Operational Expense / Raw Material Category</th>
            <th>OpEx Share (%)</th>
            <th style="text-align:right;">Allocated Working Capital (₹)</th>
        </tr>
        {opex_rows}
        <tr style="background:#e8f5e9; font-weight:bold;">
            <td>Total Working Capital (OpEx)</td>
            <td>30.0%</td>
            <td style="text-align:right;">₹{capex_opex['opex_total_inr']:,.2f}</td>
        </tr>
    </table>

    <h2>5. Multi-Year Financial Projections & Debt Servicing ({scheme['tenure_years']}-Year Horizon)</h2>
    <table>
        <tr>
            <th>Financial Year</th>
            <th style="text-align:right;">Gross Revenue</th>
            <th style="text-align:right;">Operating Costs</th>
            <th style="text-align:right;">EBITDA</th>
            <th style="text-align:right;">Debt Service</th>
            <th style="text-align:right;">Retained Cash Flow</th>
            <th style="text-align:center;">DSCR</th>
        </tr>
        {proj_rows}
    </table>

    <h2>6. Key Financial Viability Metrics & Break-Even Analysis</h2>
    <table>
        <tr>
            <td><b>Annual Net Operating Income (EBITDA)</b></td>
            <td>₹{viab['annual_net_operating_income_inr']:,.2f}</td>
            <td><b>Net Profit Margin</b></td>
            <td>{viab['net_profit_margin_pct']}%</td>
        </tr>
        <tr>
            <td><b>Debt Service Coverage Ratio (DSCR)</b></td>
            <td><b>{viab['dscr']}x</b> ({viab['dscr_verdict']})</td>
            <td><b>Break-Even Revenue (BEP)</b></td>
            <td>₹{viab['bep_revenue_inr']:,.2f} ({viab['bep_utilization_pct']}% Capacity)</td>
        </tr>
        <tr>
            <td><b>Estimated Payback Period</b></td>
            <td>{viab['payback_period_months']} Months</td>
            <td><b>Unit Gross Margin</b></td>
            <td>{pricing['gross_margin_pct']}% (₹{pricing['profit_per_unit_inr']}/unit)</td>
        </tr>
    </table>

    <h2>7. Strategic SWOT Matrix</h2>
    <div class="swot-grid">
        <div class="swot-box swot-s">
            <h4>🟢 STRENGTHS</h4>
            <ul>
                {"".join([f"<li>{s}</li>" for s in swot['strengths']])}
            </ul>
        </div>
        <div class="swot-box swot-w">
            <h4>🟡 WEAKNESSES</h4>
            <ul>
                {"".join([f"<li>{w}</li>" for w in swot['weaknesses']])}
            </ul>
        </div>
        <div class="swot-box swot-o">
            <h4>🔵 OPPORTUNITIES</h4>
            <ul>
                {"".join([f"<li>{o}</li>" for o in swot['opportunities']])}
            </ul>
        </div>
        <div class="swot-box swot-t">
            <h4>🔴 THREATS & MITIGATIONS</h4>
            <ul>
                {"".join([f"<li><b>{t['threat']}</b>: {t['mitigation']}</li>" for t in threats])}
            </ul>
        </div>
    </div>

    <h2>8. Statutory Enclosures & Verification Checklist</h2>
    <p>The applicant confirms possession and attachment of the following original / attested verification records:</p>
    <table>
        <tr>
            <th>#</th>
            <th>Required Enclosure</th>
            <th>Status / Document Type</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Applicant Identity & Permanent Address Verification</td>
            <td>Aadhaar Card / Voter ID / Resident Certificate</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Category / Caste Certificate (for MoSJE Corp Beneficiary)</td>
            <td>Competent Authority Certificate (SC / OBC / Safai Karamchari)</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Enterprise Premises & Land / Tenancy Agreement</td>
            <td>Panchayat NOC / Registered Lease / 7/12 / Khatauni</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Proforma Invoices & Machinery Quotations</td>
            <td>2 Proforma Invoices from Authorized Machinery Vendors</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Banking Record & 10% Margin Proof</td>
            <td>Bank Passbook / FDR Showing ₹{cap['available_margin_inr']:,.2f} Margin</td>
        </tr>
    </table>

    <div class="signature-section">
        <div class="sig-box">
            Applicant Signature & Thumb Impression<br>
            (Beneficiary / Promoter)
        </div>
        <div class="sig-box">
            Appraisal Officer & Branch Seal<br>
            State Channelizing Agency (SCA) / Bank
        </div>
    </div>
</div>

</body>
</html>
"""
        return html_content
