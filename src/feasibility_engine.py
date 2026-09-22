"""
Module 1: Hyper-Local Business Feasibility Engine.
Generates comprehensive 6-part localized strategy:
1. Market Reach (5–10 km radius)
2. Opportunity & High-Value Gap Analysis
3. Dynamic SWOT Matrix
4. Local Threats Identification & Actionable Mitigations
5. Competitor Density & Saturation Index
6. Product Market Value, Unit Economics & Pricing Strategy
"""

import math
from typing import Dict, Any, List
from src.geo_database import GEO_DATA, BUSINESS_CATALOG

class FeasibilityEngine:
    """Hyper-Local Feasibility & Market Strategy Engine."""

    def __init__(self, state: str, district: str, block: str, business_name: str, margin_capital: float):
        self.state = state
        self.district = district
        self.block = block
        self.business_name = business_name
        self.margin_capital = float(margin_capital)
        self.project_cost = self.margin_capital * 10.0  # 10% margin rule
        
        # Resolve geo attributes
        self.state_data = GEO_DATA.get(state, list(GEO_DATA.values())[0])
        self.dist_data = self.state_data.get("districts", {}).get(district, {
            "region": "Rural Heartland",
            "purchasing_power": 1.0,
            "rural_pop_density": 600,
            "haat_freq_weekly": 3,
            "mandi_dist_km": 8,
            "top_crops": ["Paddy", "Wheat", "Vegetables"],
            "livestock_density": "Moderate"
        })
        
        # Resolve business catalog archetype
        self.biz_data = BUSINESS_CATALOG.get(business_name, list(BUSINESS_CATALOG.values())[0])

    def calculate_market_reach(self) -> Dict[str, Any]:
        """
        Estimates the immediate consumer base within 5km and 10km radius
        and identifies primary distribution channels.
        """
        density = self.dist_data.get("rural_pop_density", 600)  # people per sq km
        ppi = self.dist_data.get("purchasing_power", 1.0)
        
        # 5 km radius area = pi * 5^2 ~ 78.5 sq km
        # 10 km radius area = pi * 10^2 ~ 314.15 sq km
        area_5km = math.pi * (5 ** 2)
        area_10km = math.pi * (10 ** 2)
        
        # Rural population factor (accounting for uninhabited farmland 60% occupancy)
        pop_5km = int(area_5km * density * 0.45)
        pop_10km = int(area_10km * density * 0.45)
        
        households_5km = int(pop_5km / 5.2)  # avg Indian rural household size 5.2
        households_10km = int(pop_10km / 5.2)
        
        # Estimated monthly addressable consumer spend (₹)
        base_monthly_basket_per_hh = 8500 * ppi
        addressable_market_5km_monthly = int(households_5km * (base_monthly_basket_per_hh * 0.12)) # 12% relevant share
        addressable_market_10km_monthly = int(households_10km * (base_monthly_basket_per_hh * 0.12))
        
        channels = [
            {"channel": "Village B2C Direct (Doorstep & Walk-in)", "share_pct": 35, "description": "Immediate local villagers & neighboring hamlets within 3km"},
            {"channel": "Weekly Rural Haats (पेठ / हाट)", "share_pct": 30, "description": f"Targeting {self.dist_data.get('haat_freq_weekly', 3)} weekly haats in the block"},
            {"channel": "B2B Supply to Panchayat / Roadside Dhaba / Stores", "share_pct": 20, "description": "Local tea stalls, kirana shops, sweet makers & institutions"},
            {"channel": f"Sub-District Mandi / Tier-3 Town ({self.dist_data.get('mandi_dist_km', 8)} km)", "share_pct": 15, "description": "Bulk aggregation & premium customer sales"}
        ]
        
        return {
            "radius_5km": {
                "population": pop_5km,
                "households": households_5km,
                "monthly_addressable_spend_inr": addressable_market_5km_monthly
            },
            "radius_10km": {
                "population": pop_10km,
                "households": households_10km,
                "monthly_addressable_spend_inr": addressable_market_10km_monthly
            },
            "haat_frequency_weekly": self.dist_data.get("haat_freq_weekly", 3),
            "mandi_distance_km": self.dist_data.get("mandi_dist_km", 8),
            "distribution_channels": channels
        }

    def analyze_opportunities(self) -> Dict[str, Any]:
        """
        Highlights unserved or underserved niches and value-addition gaps.
        """
        niches = self.biz_data.get("niche_opportunities", [])
        ue = self.biz_data.get("unit_economics", {})
        
        raw_price = ue.get("selling_price_liquid", 50.0)
        value_add_price = ue.get("selling_price_paneer_kg", 150.0)
        margin_boost = ue.get("value_add_margin_pct", 35.0)
        
        seasonal_factors = [
            {"season": "Post-Harvest (Nov–Feb / Apr–May)", "demand_multiplier": 1.45, "driver": "Farmer cash liquidity, weddings, and local festival fairs"},
            {"season": "Festive Peaks (Diwali / Eid / Chhath / Pongal)", "demand_multiplier": 1.65, "driver": "Surge in household consumption, gifts, and temple rituals"},
            {"season": "Monsoon / Sowing (Jul–Aug)", "demand_multiplier": 0.85, "driver": "Farm labor occupied in fields; focus shifted to essential inputs"}
        ]
        
        value_addition_gap = {
            "standard_product": f"Commodity Sale (Raw unit @ ₹{raw_price:,.1f})",
            "value_added_product": f"Value-Added / Packaged Output (Unit @ ₹{value_add_price:,.1f})",
            "profit_margin_gain": f"+{margin_boost:.1f}% higher gross margin",
            "action_recommendation": f"Dedicate at least 35% of production capacity to value-added lines for higher margin resilience."
        }
        
        return {
            "niche_opportunities": niches,
            "value_addition_gap": value_addition_gap,
            "seasonal_demand_trends": seasonal_factors,
            "agro_climate_alignment": f"High synergy with {self.district}'s key commodities ({', '.join(self.dist_data.get('top_crops', ['Crops']))}) and {self.dist_data.get('livestock_density', 'Moderate')} livestock base."
        }

    def generate_swot_analysis(self) -> Dict[str, List[str]]:
        """
        Generates dynamic SWOT matrix tailored to the micro-enterprise scale and geography.
        """
        scale_badge = "Micro Scale (< ₹1.4L)" if self.project_cost <= 140000 else "Term Loan Scale (₹1.4L - ₹50L)"
        
        strengths = [
            f"Low capital barrier with concessional MoSJE loan funding (90% debt backed at low interest).",
            f"Direct local sourcing of raw materials in {self.district} avoiding middleman commission.",
            f"Close hyper-local community trust and personalized customer service in {self.block}.",
            f"Low fixed operational overheads compared to urban enterprises."
        ]
        
        weaknesses = [
            f"Limited initial working capital reserve for aggressive inventory stockpiling.",
            f"Reliance on unorganized informal village credit ('Udhaar') requiring tight collection discipline.",
            f"Lack of mechanized automated packaging or storage in initial Phase 1.",
            f"Susceptibility to seasonal income cycles in the agricultural block."
        ]
        
        opportunities = [
            f"Capture unmet demand across {self.calculate_market_reach()['radius_5km']['households']:,} households within 5 km radius.",
            f"Form supply tie-ups with local SHGs (Self Help Groups) and Village Dairy Cooperatives / FPOs.",
            f"Leverage government MoSJE / Saras Mela stalls and state exhibitions for high-margin festive sales.",
            f"Expand into adjacent blocks as brand familiarity grows."
        ]
        
        threats = [
            f"Seasonal input price volatility (raw seeds, feed, electricity tariffs).",
            f"Weather risks / severe monsoon dampening transport to weekly haats.",
            f"Intrusion of mass industrial FMCG brands offering heavy retailer credit.",
            f"Unscheduled 3-phase rural power tripping during processing hours."
        ]
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats,
            "scale_context": scale_badge
        }

    def identify_threats_and_mitigation(self) -> List[Dict[str, str]]:
        """
        Pinpoints localized risks with actionable rural mitigation strategies.
        """
        threat_list = self.biz_data.get("threats", [])
        mitigation_list = self.biz_data.get("mitigation", [])
        
        results = []
        for i in range(len(threat_list)):
            t_text = threat_list[i]
            m_text = mitigation_list[i] if i < len(mitigation_list) else "Maintain 20% liquid cash buffer and diversify customer base."
            results.append({
                "threat": t_text,
                "mitigation": m_text,
                "risk_level": "High" if i == 0 else ("Medium" if i == 1 else "Moderate")
            })
        return results

    def map_competitors_and_saturation(self) -> Dict[str, Any]:
        """
        Estimates density of similar businesses in the block, saturation index, and spatial buffer.
        """
        baseline_units = self.biz_data.get("saturation_baseline_per_block", 12)
        ppi = self.dist_data.get("purchasing_power", 1.0)
        
        # Estimated active similar micro-units in block
        estimated_competitors = int(baseline_units * (0.85 + (ppi * 0.2)))
        
        # Saturation categorization
        if estimated_competitors < 8:
            sat_status = "Low Saturation (High Growth Potential)"
            sat_score = 30
            rec_distance_km = "1.0 – 1.5 km"
            advice = "Untapped rural pocket. Early-mover advantage to capture loyalty."
        elif estimated_competitors <= 18:
            sat_status = "Moderate Saturation (Viable with Differentiation)"
            sat_score = 55
            rec_distance_km = "2.0 – 3.0 km"
            advice = "Viable market. Differentiate on 100% purity, doorstep delivery, and prompt service."
        else:
            sat_status = "High Saturation (Requires Niche Focus)"
            sat_score = 80
            rec_distance_km = "3.5 – 5.0 km"
            advice = "Competitive sector. Focus on premium value-addition or underserved adjacent hamlets."

        return {
            "estimated_competitors_in_block": estimated_competitors,
            "saturation_status": sat_status,
            "saturation_score_pct": sat_score,
            "recommended_spatial_buffer_km": rec_distance_km,
            "differentiation_strategy": advice
        }

    def calculate_pricing_and_unit_economics(self) -> Dict[str, Any]:
        """
        Suggests optimal pricing and unit economics based on regional purchasing power.
        """
        ue = self.biz_data.get("unit_economics", {})
        ppi = self.dist_data.get("purchasing_power", 1.0)
        
        base_cost = ue.get("cost_per_unit_liquid", 40.0)
        base_sell = ue.get("selling_price_liquid", 65.0)
        
        # Calibrate selling price with local PPI
        calibrated_selling_price = round(base_sell * (0.90 + (0.10 * ppi)), 1)
        calibrated_cost = round(base_cost, 1)
        unit_profit = round(calibrated_selling_price - calibrated_cost, 1)
        unit_margin_pct = round((unit_profit / calibrated_selling_price) * 100, 1) if calibrated_selling_price > 0 else 0
        
        # Daily and monthly capacity based on project cost scale
        scale_multiplier = max(1.0, math.sqrt(self.project_cost / 100000.0))
        daily_units = int(ue.get("daily_output_litres_per_animal", 15.0) * scale_multiplier)
        monthly_units = daily_units * 26  # 26 working days
        
        monthly_revenue = int(monthly_units * calibrated_selling_price)
        monthly_cogs = int(monthly_units * calibrated_cost)
        monthly_gross_profit = monthly_revenue - monthly_cogs
        
        # Fixed monthly overheads (electricity, rent/maintenance, misc)
        monthly_fixed_overhead = int(self.project_cost * 0.015) + 3000
        monthly_net_operating_income = monthly_gross_profit - monthly_fixed_overhead
        
        # Break-even calculation (Units needed to cover fixed overheads)
        break_even_units_monthly = int(monthly_fixed_overhead / unit_profit) if unit_profit > 0 else 0
        break_even_days = round(break_even_units_monthly / daily_units, 1) if daily_units > 0 else 0
        
        return {
            "unit_name": ue.get("base_unit", "Standard Unit"),
            "cost_per_unit_inr": calibrated_cost,
            "recommended_selling_price_inr": calibrated_selling_price,
            "profit_per_unit_inr": unit_profit,
            "gross_margin_pct": unit_margin_pct,
            "daily_production_capacity": daily_units,
            "monthly_production_units": monthly_units,
            "monthly_revenue_inr": monthly_revenue,
            "monthly_cogs_inr": monthly_cogs,
            "monthly_fixed_overhead_inr": monthly_fixed_overhead,
            "monthly_net_operating_income_inr": monthly_net_operating_income,
            "break_even_units_monthly": break_even_units_monthly,
            "break_even_operating_days_per_month": break_even_days
        }

    def compute_overall_feasibility_score(self) -> Dict[str, Any]:
        """
        Computes composite Feasibility Index (0-100 score).
        """
        reach = self.calculate_market_reach()
        comp = self.map_competitors_and_saturation()
        pricing = self.calculate_pricing_and_unit_economics()
        
        # Score components
        demand_score = min(25, int((reach["radius_5km"]["population"] / 15000) * 25))
        financial_score = min(30, int((pricing["gross_margin_pct"] / 40.0) * 30))
        competition_score = max(5, min(20, int(20 - (comp["saturation_score_pct"] * 0.15))))
        operational_score = 22  # baseline strong rural availability
        
        total_score = min(98, demand_score + financial_score + competition_score + operational_score)
        
        if total_score >= 80:
            rating = "Highly Feasible (Green Flag)"
            summary = "Excellent market potential with strong margin resilience and healthy rural demand."
        elif total_score >= 60:
            rating = "Feasible with Strategic Focus (Yellow-Green)"
            summary = "Viable enterprise; ensure disciplined inventory management and value-addition."
        else:
            rating = "Requires Budget / Location Fine-Tuning"
            summary = "Moderate viability; explore adjacent high-demand clusters or expand product range."

        return {
            "total_score": total_score,
            "rating": rating,
            "summary": summary,
            "breakdown": {
                "Market Demand & Catchment": f"{demand_score}/25",
                "Financial Margins & Unit Profit": f"{financial_score}/30",
                "Competition & Saturation Index": f"{competition_score}/20",
                "Operational & Supply Resilience": f"{operational_score}/25"
            }
        }

    def generate_complete_feasibility_report(self) -> Dict[str, Any]:
        """Generates all 6 modules of Feasibility report."""
        return {
            "location_summary": {
                "state": self.state,
                "district": self.district,
                "block": self.block,
                "region": self.dist_data.get("region", "Rural"),
                "purchasing_power_index": self.dist_data.get("purchasing_power", 1.0),
                "business_name": self.business_name,
                "icon": self.biz_data.get("icon", "🌱")
            },
            "market_reach": self.calculate_market_reach(),
            "opportunity_analysis": self.analyze_opportunities(),
            "swot_analysis": self.generate_swot_analysis(),
            "threats_mitigation": self.identify_threats_and_mitigation(),
            "competitor_mapping": self.map_competitors_and_saturation(),
            "unit_pricing_economics": self.calculate_pricing_and_unit_economics(),
            "feasibility_scorecard": self.compute_overall_feasibility_score()
        }
