"""
Geographic & Rural Micro-Enterprise Knowledge Base.
Contains curated datasets of Indian States, Districts, rural demographic profiles,
Agro-climatic indicators, Mandi/Haat connectivity, and 12+ Rural Micro-Enterprise Archetypes.
"""

from typing import Dict, List, Any

# Curated State and District Catalog with Agro-Climatic & Demographic Attributes
GEO_DATA: Dict[str, Dict[str, Any]] = {
    "Uttar Pradesh": {
        "districts": {
            "Varanasi": {"region": "Eastern UP", "purchasing_power": 1.15, "rural_pop_density": 850, "haat_freq_weekly": 4, "mandi_dist_km": 8, "top_crops": ["Paddy", "Wheat", "Vegetables", "Mustard"], "livestock_density": "High"},
            "Gorakhpur": {"region": "Eastern UP", "purchasing_power": 1.05, "rural_pop_density": 780, "haat_freq_weekly": 3, "mandi_dist_km": 12, "top_crops": ["Sugarcane", "Paddy", "Wheat"], "livestock_density": "High"},
            "Lucknow": {"region": "Central UP", "purchasing_power": 1.25, "rural_pop_density": 720, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Mango", "Vegetables", "Wheat"], "livestock_density": "Moderate"},
            "Jhansi": {"region": "Bundelkhand", "purchasing_power": 0.90, "rural_pop_density": 450, "haat_freq_weekly": 2, "mandi_dist_km": 15, "top_crops": ["Pulses", "Oilseeds", "Millets"], "livestock_density": "High (Goat/Cattle)"},
            "Bareilly": {"region": "Rohilkhand", "purchasing_power": 1.10, "rural_pop_density": 690, "haat_freq_weekly": 3, "mandi_dist_km": 10, "top_crops": ["Sugarcane", "Rice", "Wheat"], "livestock_density": "High"},
            "Prayagraj": {"region": "Eastern UP", "purchasing_power": 1.12, "rural_pop_density": 740, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Guava", "Wheat", "Paddy"], "livestock_density": "High"}
        },
        "blocks": ["Sadar / Central", "Chiraigaon", "Kashi Vidyapeeth", "Pindra", "Baragaon", "Araziline", "Sewapuri", "Badagaon"]
    },
    "Bihar": {
        "districts": {
            "Muzaffarpur": {"region": "North Bihar", "purchasing_power": 0.95, "rural_pop_density": 920, "haat_freq_weekly": 4, "mandi_dist_km": 7, "top_crops": ["Litchi", "Maize", "Paddy", "Vegetables"], "livestock_density": "High"},
            "Patna": {"region": "Central Bihar", "purchasing_power": 1.20, "rural_pop_density": 850, "haat_freq_weekly": 5, "mandi_dist_km": 5, "top_crops": ["Vegetables", "Paddy", "Wheat"], "livestock_density": "Moderate"},
            "Gaya": {"region": "Magadh", "purchasing_power": 0.90, "rural_pop_density": 680, "haat_freq_weekly": 3, "mandi_dist_km": 11, "top_crops": ["Paddy", "Lentils", "Sesame"], "livestock_density": "High"},
            "Darbhanga": {"region": "Mithilanchal", "purchasing_power": 0.92, "rural_pop_density": 880, "haat_freq_weekly": 3, "mandi_dist_km": 10, "top_crops": ["Makhana (Foxnut)", "Fish", "Paddy"], "livestock_density": "High"},
            "Bhagalpur": {"region": "Anga", "purchasing_power": 1.00, "rural_pop_density": 760, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Silk/Textiles", "Mango", "Maize"], "livestock_density": "Moderate"}
        },
        "blocks": ["Kanti", "Motipur", "Musahari", "Bochahan", "Sakra", "Kurhani", "Minapur", "Gaighat"]
    },
    "Madhya Pradesh": {
        "districts": {
            "Indore": {"region": "Malwa", "purchasing_power": 1.30, "rural_pop_density": 520, "haat_freq_weekly": 4, "mandi_dist_km": 5, "top_crops": ["Soybean", "Wheat", "Potato", "Garlic"], "livestock_density": "Moderate"},
            "Jabalpur": {"region": "Mahakoshal", "purchasing_power": 1.08, "rural_pop_density": 480, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Wheat", "Gram", "Peas"], "livestock_density": "High"},
            "Ujjain": {"region": "Malwa", "purchasing_power": 1.15, "rural_pop_density": 490, "haat_freq_weekly": 3, "mandi_dist_km": 7, "top_crops": ["Soybean", "Wheat", "Onion"], "livestock_density": "Moderate"},
            "Rewa": {"region": "Vindhya", "purchasing_power": 0.88, "rural_pop_density": 410, "haat_freq_weekly": 2, "mandi_dist_km": 14, "top_crops": ["Paddy", "Wheat", "Mustard"], "livestock_density": "High"},
            "Chhindwara": {"region": "Satpura", "purchasing_power": 0.95, "rural_pop_density": 360, "haat_freq_weekly": 2, "mandi_dist_km": 12, "top_crops": ["Maize", "Cotton", "Oranges"], "livestock_density": "Moderate"}
        },
        "blocks": ["Sanwer", "Depalpur", "Mhow", "Hatod", "Patan", "Sihora", "Kundam", "Panagar"]
    },
    "Maharashtra": {
        "districts": {
            "Pune": {"region": "Western Maharashtra", "purchasing_power": 1.35, "rural_pop_density": 580, "haat_freq_weekly": 5, "mandi_dist_km": 6, "top_crops": ["Sugarcane", "Vegetables", "Dairy", "Flowers"], "livestock_density": "Very High"},
            "Nashik": {"region": "Khandesh / North", "purchasing_power": 1.25, "rural_pop_density": 540, "haat_freq_weekly": 4, "mandi_dist_km": 7, "top_crops": ["Grapes", "Onion", "Tomatoes", "Dairy"], "livestock_density": "High"},
            "Kolhapur": {"region": "Western Maharashtra", "purchasing_power": 1.30, "rural_pop_density": 610, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Sugarcane", "Jaggery", "Dairy", "Spices"], "livestock_density": "Very High"},
            "Nagpur": {"region": "Vidarbha", "purchasing_power": 1.18, "rural_pop_density": 470, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Oranges", "Cotton", "Soybean"], "livestock_density": "Moderate"},
            "Solapur": {"region": "Solapur / Marathwada", "purchasing_power": 1.05, "rural_pop_density": 440, "haat_freq_weekly": 3, "mandi_dist_km": 10, "top_crops": ["Pomegranate", "Jowar", "Textiles"], "livestock_density": "High (Goat/Dairy)"},
            "Nanded": {"region": "Marathwada", "purchasing_power": 0.96, "rural_pop_density": 430, "haat_freq_weekly": 2, "mandi_dist_km": 11, "top_crops": ["Cotton", "Soybean", "Turmeric"], "livestock_density": "Moderate"}
        },
        "blocks": ["Haveli", "Baramati", "Shirur", "Junnar", "Khed", "Ambegaon", "Indapur", "Daund"]
    },
    "Rajasthan": {
        "districts": {
            "Jaipur": {"region": "Dhundhar", "purchasing_power": 1.25, "rural_pop_density": 510, "haat_freq_weekly": 4, "mandi_dist_km": 7, "top_crops": ["Mustard", "Wheat", "Vegetables", "Handicrafts"], "livestock_density": "High"},
            "Jodhpur": {"region": "Marwar", "purchasing_power": 1.10, "rural_pop_density": 320, "haat_freq_weekly": 3, "mandi_dist_km": 12, "top_crops": ["Millets (Bajra)", "Guar Gum", "Spices", "Handicrafts"], "livestock_density": "Very High (Camel/Goat/Sheep)"},
            "Udaipur": {"region": "Mewar", "purchasing_power": 1.08, "rural_pop_density": 390, "haat_freq_weekly": 3, "mandi_dist_km": 10, "top_crops": ["Maize", "Wheat", "Minerals", "Handicrafts"], "livestock_density": "High"},
            "Alwar": {"region": "Mewat / NCR", "purchasing_power": 1.15, "rural_pop_density": 530, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Mustard", "Dairy / Khoya", "Wheat"], "livestock_density": "Very High (Buffalo/Cow)"},
            "Kota": {"region": "Hadoti", "purchasing_power": 1.12, "rural_pop_density": 420, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Soybean", "Paddy", "Garlic", "Coriander"], "livestock_density": "Moderate"}
        },
        "blocks": ["Sanganer", "Amber", "Chaksu", "Bassie", "Jamwa Ramgarh", "Phagi", "Kotputli", "Shahpura"]
    },
    "West Bengal": {
        "districts": {
            "Burdwan (Purba Bardhaman)": {"region": "Rarh", "purchasing_power": 1.15, "rural_pop_density": 790, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Paddy (Rice Bowl)", "Potatoes", "Mustard", "Dairy"], "livestock_density": "High"},
            "Nadia": {"region": "Presidency", "purchasing_power": 1.08, "rural_pop_density": 830, "haat_freq_weekly": 4, "mandi_dist_km": 7, "top_crops": ["Jute", "Handloom / Tant", "Vegetables", "Flowers"], "livestock_density": "High"},
            "Murshidabad": {"region": "Central Bengal", "purchasing_power": 0.95, "rural_pop_density": 890, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Silk / Sericulture", "Jute", "Mango", "Mustard"], "livestock_density": "High"},
            "Hooghly": {"region": "Lower Gangetic", "purchasing_power": 1.18, "rural_pop_density": 860, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Potatoes", "Jute", "Vegetables", "Fish"], "livestock_density": "Moderate"}
        },
        "blocks": ["Burdwan-I", "Burdwan-II", "Memari-I", "Kalna-I", "Katwa-I", "Bhatar", "Galsi-I", "Ausgram-I"]
    },
    "Tamil Nadu": {
        "districts": {
            "Coimbatore": {"region": "Kongu Nadu", "purchasing_power": 1.40, "rural_pop_density": 620, "haat_freq_weekly": 5, "mandi_dist_km": 5, "top_crops": ["Coconut", "Poultry", "Textiles / Weaving", "Vegetables"], "livestock_density": "Very High"},
            "Madurai": {"region": "Pandya Nadu", "purchasing_power": 1.18, "rural_pop_density": 590, "haat_freq_weekly": 4, "mandi_dist_km": 7, "top_crops": ["Paddy", "Jasmine / Flowers", "Pulses", "Dairy"], "livestock_density": "High"},
            "Thanjavur": {"region": "Cauvery Delta", "purchasing_power": 1.12, "rural_pop_density": 670, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Paddy", "Coconut", "Banana", "Handicrafts"], "livestock_density": "High"},
            "Salem": {"region": "Kongu Nadu", "purchasing_power": 1.20, "rural_pop_density": 600, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Tapioca / Sago", "Mango", "Silk Handloom", "Poultry"], "livestock_density": "Very High"}
        },
        "blocks": ["Pollachi North", "Pollachi South", "Sulur", "Thondamuthur", "Annur", "Karamadai", "Madukkarai"]
    },
    "Telangana / Andhra Pradesh": {
        "districts": {
            "Warangal": {"region": "Telangana Central", "purchasing_power": 1.10, "rural_pop_density": 460, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Chilli", "Cotton", "Paddy", "Turmeric"], "livestock_density": "High"},
            "Guntur": {"region": "Coastal Andhra", "purchasing_power": 1.22, "rural_pop_density": 640, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Chilli", "Tobacco", "Cotton", "Aqua/Fish"], "livestock_density": "Moderate"},
            "Karimnagar": {"region": "North Telangana", "purchasing_power": 1.12, "rural_pop_density": 490, "haat_freq_weekly": 3, "mandi_dist_km": 7, "top_crops": ["Paddy", "Cotton", "Dairy", "Poultry"], "livestock_density": "High"},
            "East Godavari": {"region": "Delta", "purchasing_power": 1.25, "rural_pop_density": 710, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Paddy", "Coconut", "Aquaculture", "Banana"], "livestock_density": "Moderate"}
        },
        "blocks": ["Hanamkonda", "Wardhannapet", "Geesugonda", "Atmakur", "Dharmasagar", "Parkal", "Narsampet"]
    },
    "Gujarat": {
        "districts": {
            "Anand": {"region": "Charotar / Milk Capital", "purchasing_power": 1.35, "rural_pop_density": 680, "haat_freq_weekly": 4, "mandi_dist_km": 5, "top_crops": ["Dairy (Amul hub)", "Tobacco", "Banana", "Vegetables"], "livestock_density": "Extremely High"},
            "Rajkot": {"region": "Saurashtra", "purchasing_power": 1.28, "rural_pop_density": 510, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Groundnut / Oil", "Cotton", "Cumin", "Diesel Engines/Tools"], "livestock_density": "Moderate"},
            "Mehsana": {"region": "North Gujarat", "purchasing_power": 1.26, "rural_pop_density": 560, "haat_freq_weekly": 3, "mandi_dist_km": 7, "top_crops": ["Dairy (Dudhsagar)", "Castor", "Fennel / Spices"], "livestock_density": "Very High"},
            "Surat Rural": {"region": "South Gujarat", "purchasing_power": 1.38, "rural_pop_density": 640, "haat_freq_weekly": 5, "mandi_dist_km": 5, "top_crops": ["Sugarcane", "Textiles / Weaving", "Paddy", "Vegetables"], "livestock_density": "Moderate"}
        },
        "blocks": ["Anand", "Borsad", "Petlad", "Khambhat", "Umreth", "Tarapur", "Sojitra", "Anklav"]
    },
    "Punjab / Haryana": {
        "districts": {
            "Ludhiana": {"region": "Central Malwa", "purchasing_power": 1.42, "rural_pop_density": 650, "haat_freq_weekly": 4, "mandi_dist_km": 4, "top_crops": ["Wheat", "Paddy", "Hosiery/Garments", "Dairy"], "livestock_density": "Very High"},
            "Amritsar": {"region": "Majha", "purchasing_power": 1.30, "rural_pop_density": 620, "haat_freq_weekly": 4, "mandi_dist_km": 5, "top_crops": ["Wheat", "Basmati Rice", "Dairy", "Food Processing"], "livestock_density": "High"},
            "Karnal": {"region": "NCR / GT Road", "purchasing_power": 1.36, "rural_pop_density": 590, "haat_freq_weekly": 4, "mandi_dist_km": 5, "top_crops": ["Basmati Rice", "Wheat", "Dairy (NDRI hub)", "Vegetables"], "livestock_density": "Very High"}
        },
        "blocks": ["Ludhiana-1", "Ludhiana-2", "Samrala", "Khanna", "Jagraon", "Raikot", "Doraha"]
    },
    "Odisha": {
        "districts": {
            "Cuttack": {"region": "Coastal Odisha", "purchasing_power": 1.05, "rural_pop_density": 660, "haat_freq_weekly": 3, "mandi_dist_km": 7, "top_crops": ["Paddy", "Vegetables", "Silver Filigree / Handicrafts", "Dairy"], "livestock_density": "High"},
            "Ganjam": {"region": "South Coastal", "purchasing_power": 0.98, "rural_pop_density": 580, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Paddy", "Cashew", "Fisheries", "Handloom"], "livestock_density": "High"},
            "Sambalpur": {"region": "Western Odisha", "purchasing_power": 1.02, "rural_pop_density": 420, "haat_freq_weekly": 2, "mandi_dist_km": 11, "top_crops": ["Paddy", "Sambalpuri Handloom", "Forest Produce"], "livestock_density": "Moderate"}
        },
        "blocks": ["Baranga", "Salepur", "Nischintakoili", "Mahanga", "Tangi-Choudwar", "Banki", "Athagarh"]
    },
    "Karnataka": {
        "districts": {
            "Mysuru": {"region": "South Karnataka", "purchasing_power": 1.25, "rural_pop_density": 560, "haat_freq_weekly": 4, "mandi_dist_km": 6, "top_crops": ["Silk / Sericulture", "Paddy", "Sugarcane", "Handicrafts"], "livestock_density": "High"},
            "Belagavi": {"region": "North Karnataka", "purchasing_power": 1.18, "rural_pop_density": 520, "haat_freq_weekly": 3, "mandi_dist_km": 8, "top_crops": ["Sugarcane", "Vegetables", "Dairy", "Poultry"], "livestock_density": "Very High"},
            "Shivamogga": {"region": "Malnad", "purchasing_power": 1.15, "rural_pop_density": 440, "haat_freq_weekly": 3, "mandi_dist_km": 9, "top_crops": ["Arecanut", "Paddy", "Spices", "Dairy"], "livestock_density": "Moderate"}
        },
        "blocks": ["Mysuru", "Hunsur", "Nanjangud", "T. Narasipura", "K.R. Nagar", "Piriyapatna", "H.D. Kote"]
    }
}

# 12 Detailed Rural Micro-Enterprise Archetypes
BUSINESS_CATALOG: Dict[str, Dict[str, Any]] = {
    "Dairy Farming & Value-Added Milk Products": {
        "category_id": "dairy",
        "icon": "🐄",
        "description": "Establishment of mini dairy unit (crossbred cows/buffaloes), milk chilling, and value addition into Paneer, Curd, Ghee, and Khoya.",
        "capex_items": [
            {"item": "High-Yielding Milking Animals (Cow/Murrah Buffalo)", "pct": 48},
            {"item": "Cattle Shed Construction with Pucca Flooring & Drainage", "pct": 22},
            {"item": "Milking Machine & Stainless Steel Milk Cans (30-40L)", "pct": 10},
            {"item": "Chaff Cutter, Fodder Chopper & Solar Water Pump", "pct": 10},
            {"item": "Paneer Press, Cream Separator & Deep Freezer (Cold Storage)", "pct": 10}
        ],
        "opex_items": [
            {"item": "Green/Dry Fodder & Cattle Feed Concentrate", "pct": 55},
            {"item": "Veterinary Care, Deworming, Vaccination & Breeding / AI", "pct": 12},
            {"item": "Electricity, Water, Transportation to Collection Center", "pct": 15},
            {"item": "Sanitation, Packaging Pouches / Glass Bottles, Misc Labour", "pct": 18}
        ],
        "unit_economics": {
            "base_unit": "Litre of Milk / Kg of Ghee-Paneer",
            "cost_per_unit_liquid": 34.0,     # ₹ cost to produce 1L milk
            "selling_price_liquid": 54.0,     # ₹ selling price per 1L raw milk
            "value_add_cost_paneer_kg": 240.0,# ₹ cost to produce 1kg paneer
            "selling_price_paneer_kg": 380.0, # ₹ selling price 1kg paneer
            "value_add_margin_pct": 36.8,     # higher profit on value addition
            "daily_output_litres_per_animal": 12.0
        },
        "market_channels": ["Local Village Households (B2C)", "Village Dairy Cooperative / Milk Union", "Local Tea Stalls & Sweet Shops (Halwais)", "Weekly Haat / Town Market"],
        "threats": ["Fodder and grain price inflation", "Seasonal milk production drop in summer (flush vs lean period)", "Risk of Bovine diseases (FMD / Lumpy Skin)", "Lack of reliable cold-chain or power cuts"],
        "mitigation": ["Tie-up with local Dairy Cooperative / SCA animal insurance", "Silage preparation during green fodder surplus", "Routine vaccination through Veterinary Dispensary", "Dual solar-powered chilling battery setup"],
        "niche_opportunities": ["Desi Cow A2 Ghee & Vedic Butter in nearby town market", "Fresh Paneer & Khoya supply to local Halwais during wedding seasons", "Organic Vermicompost slurry packaged from cattle dung"],
        "saturation_baseline_per_block": 18  # avg typical units per block
    },
    "Poultry & Broiler / Layer Farming": {
        "category_id": "poultry",
        "icon": "🐔",
        "description": "Commercial broiler rearing (6-7 batches/year) or indigenous Kadaknath/Desi egg production unit with scientific bio-security.",
        "capex_items": [
            {"item": "Ventilated Poultry Shed with Brooder Setup", "pct": 42},
            {"item": "Automatic Drinkers, Feeders & Fogger System", "pct": 20},
            {"item": "Day-Old Chicks (DOC) Initial Batch Procuring", "pct": 18},
            {"item": "Backup Generator / Inverter & Temperature Regulators", "pct": 12},
            {"item": "Disinfection Spray Equipment & Weighing Scale", "pct": 8}
        ],
        "opex_items": [
            {"item": "Poultry Feed (Starter, Grower, Finisher Mash)", "pct": 68},
            {"item": "Vaccines (Ranikhet, Gumboro), Antibiotics & Supplements", "pct": 10},
            {"item": "Bedding Material (Paddy Husk/Sawdust), Heating & Power", "pct": 12},
            {"item": "Culling, Crates & Transport to Wholesale Buyer", "pct": 10}
        ],
        "unit_economics": {
            "base_unit": "Kg Live Weight / Dozen Eggs",
            "cost_per_unit_liquid": 82.0,     # ₹ cost per kg live broiler
            "selling_price_liquid": 120.0,    # ₹ selling price per kg
            "value_add_cost_paneer_kg": 6.0,  # ₹ Desi Egg cost
            "selling_price_paneer_kg": 12.0,  # ₹ Desi Egg selling price
            "value_add_margin_pct": 31.6,
            "daily_output_litres_per_animal": 1.0
        },
        "market_channels": ["Local Dhaba & Meat Retailers", "Weekly Rural Haat Live Bird Stalls", "Town Wholesale Chicken Aggregators", "Direct Household Sales"],
        "threats": ["Avian Influenza (Bird Flu) outbreak rumors", "Extreme summer mortality due to heat stress", "Feed price volatility (Maize & Soymeal)", "Sudden wholesale farm-gate price fluctuations"],
        "mitigation": ["Contract farming buy-back agreement or staggered batches", "Foggers, wet curtains, and anti-stress electrolytes in summer", "Strict farm bio-security and SCA poultry livestock insurance", "Local direct retail integration to capture wholesale spread"],
        "niche_opportunities": ["Desi country bird (Aseel / Kadaknath) fetching 2x premium in nearby cities", "Ready-to-cook dressed frozen chicken for local rural weddings/caterers", "Poultry manure sold to neighboring horticulture farms"],
        "saturation_baseline_per_block": 14
    },
    "Agro-Processing, Flour / Oil Mill & Spice Grinding": {
        "category_id": "agro_mill",
        "icon": "🌾",
        "description": "Multi-crop processing unit: Flour Atta Chakki, Mustard/Groundnut Cold-Pressed Oil Expeller, and Masala Spice Pulverizer.",
        "capex_items": [
            {"item": "Commercial Heavy-Duty Atta Chakki (Flour Mill Machine)", "pct": 28},
            {"item": "Cold-Press Oil Expeller (Mustard / Sesame / Groundnut)", "pct": 32},
            {"item": "Spice Pulverizer & Vibratory Grader / Cleaner", "pct": 18},
            {"item": "Commercial 3-Phase Electric Connection & Panel / Motor", "pct": 14},
            {"item": "Nitrogen / Vacuum Pouch Sealing Machine & Digital Scales", "pct": 8}
        ],
        "opex_items": [
            {"item": "Raw Grains, Mustard Seeds, Dry Chillies, Turmeric", "pct": 65},
            {"item": "Electricity Charges, Diesel Generator Backup", "pct": 15},
            {"item": "Printed Pouches, Gunny Bags, Tin Cans / Bottles", "pct": 12},
            {"item": "Screen Replacement, Oil Machine Lubricants & Maintenance", "pct": 8}
        ],
        "unit_economics": {
            "base_unit": "Kg Flour / Litre Pure Oil / 100g Spice Pouch",
            "cost_per_unit_liquid": 26.0,     # ₹ Wheat flour processing + grain cost/kg
            "selling_price_liquid": 38.0,     # ₹ Retail pure atta/kg
            "value_add_cost_paneer_kg": 110.0,# ₹ 1L Cold-pressed mustard oil cost
            "selling_price_paneer_kg": 175.0, # ₹ 1L Mustard oil selling price
            "value_add_margin_pct": 37.1,
            "daily_output_litres_per_animal": 200.0
        },
        "market_channels": ["Village Custom Grinding Services (Job Work)", "Direct Retail Branded Flour/Oil Pouches", "Rural Kirana Stores & Sweet Makers", "FPO / SHG Collective Consignment"],
        "threats": ["Frequent 3-phase rural power outages", "Grain post-harvest pest infestation / dampness", "Competition from big industrial packaged brands", "Fluctuating raw seed prices during off-season"],
        "mitigation": ["Solar hybrid inverter or dual motor generator setup", "Moisture-proof hermetic grain storage silos with neem tablets", "Focus on local 100% purity freshness guarantee (zero adulteration)", "Pre-booking seasonal harvest grain directly from farmer networks"],
        "niche_opportunities": ["Unadulterated Cold-Pressed Mustard & Sesame Oil with transparent glass bottling", "Stone-ground (Chakki) whole-wheat multi-grain atta with bran intact", "Locally roasted and ground Sattu / Haldi powder packages"],
        "saturation_baseline_per_block": 12
    },
    "Rural Retail, Kirana & Departmental Supply Hub": {
        "category_id": "retail_kirana",
        "icon": "🛒",
        "description": "Modern rural mini-supermarket & wholesale distribution point for FMCG, daily staples, agricultural inputs, and household goods.",
        "capex_items": [
            {"item": "Modular Steel Slotted Angle Racks & Display Gondolas", "pct": 30},
            {"item": "POS Billing Counter, Barcode Scanner, Computer & Inverter", "pct": 25},
            {"item": "Commercial Refrigerator & Beverage Showcase Cooler", "pct": 20},
            {"item": "Shop Renovation, Shutter, LED Lighting & Signage Board", "pct": 15},
            {"item": "CCTV Security Camera Setup with 4G SIM router", "pct": 10}
        ],
        "opex_items": [
            {"item": "Fast-Moving Inventory (Grains, Pulses, Oils, FMCG, Soap)", "pct": 75},
            {"item": "Shop Rent, Municipal / Panchayat Cess", "pct": 10},
            {"item": "Electricity, Generator fuel, Logistics / Tempo Trips", "pct": 8},
            {"item": "Loss / Shrinkage Buffer, Carry bags, Promotional flyers", "pct": 7}
        ],
        "unit_economics": {
            "base_unit": "Average Customer Basket (₹500 Transaction)",
            "cost_per_unit_liquid": 415.0,    # ₹ wholesale cost of goods
            "selling_price_liquid": 500.0,    # ₹ retail invoice
            "value_add_cost_paneer_kg": 750.0,# ₹ bulk agri-input pack cost
            "selling_price_paneer_kg": 950.0, # ₹ bulk selling price
            "value_add_margin_pct": 21.0,
            "daily_output_litres_per_animal": 60.0
        },
        "market_channels": ["Main Village Chowk / Panchayat Ghar Walk-in", "Adjacent Hamlets & Farm Homesteads", "Wholesale supply to smaller tea shops / roadside vendors", "Home Delivery for senior citizens & bulk event orders"],
        "threats": ["Over-extension of informal credit (Udhaar khata)", "Inventory expiry on slow-moving branded cosmetic goods", "Price discounting from district town wholesale markets", "Working capital blockage during harvest sowing seasons"],
        "mitigation": ["Digital UPI-first payment incentive (2% instant cash discount) & strict 15-day credit caps", "Algorithmic re-ordering focused only on top-40 high-velocity SKUs", "Direct distributor tie-ups to capture FMCG margins", "Seasonal inventory adjustment (more seeds/fertilisers in Kharif/Rabi)"],
        "niche_opportunities": ["Combo Festival Baskets (Diwali / Chhath / Eid grocery packs)", "Adding Micro-ATM & Aadhaar Enabled Payment (AePS) cash withdrawal counter", "Direct aggregation of locally made papads, ghee, and pickles on top shelf"],
        "saturation_baseline_per_block": 25
    },
    "Handloom, Garment Manufacturing & Custom Tailoring": {
        "category_id": "textiles",
        "icon": "🧵",
        "description": "Apparel micro-unit: High-speed sewing machines, embroidery, school uniform production, and traditional handloom weaving.",
        "capex_items": [
            {"item": "Industrial Motorized Sewing Machines (Juki/Singer) x 4", "pct": 35},
            {"item": "Overlock (Interlock) Machine & Button-Hole Attachment", "pct": 20},
            {"item": "Fabric Cutting Table, Steam Press Ironing Station", "pct": 18},
            {"item": "Embroidery / Handloom Loom Frame Setup", "pct": 17},
            {"item": "Workshop Furniture, Thread Racks & Mannequins", "pct": 10}
        ],
        "opex_items": [
            {"item": "Fabric Rolls (Cotton, Polyester, Rayon, School Uniform Khadi)", "pct": 58},
            {"item": "Threads, Zippers, Buttons, Lace, Interfacing Canvas", "pct": 15},
            {"item": "Electricity, Ironing power, Needle replacements", "pct": 12},
            {"item": "Packaging plastic covers, Hangers, Delivery bags", "pct": 15}
        ],
        "unit_economics": {
            "base_unit": "Stitched Garment / School Uniform Set",
            "cost_per_unit_liquid": 220.0,    # ₹ material + thread + power cost
            "selling_price_liquid": 480.0,    # ₹ stitching charge + dress sale
            "value_add_cost_paneer_kg": 450.0,# ₹ Designer Suit / Saree embroidery cost
            "selling_price_paneer_kg": 1100.0,# ₹ Selling price
            "value_add_margin_pct": 54.1,
            "daily_output_litres_per_animal": 8.0
        },
        "market_channels": ["Local Village Ladies & Festive Orders", "Rural School Uniform Annual Supply Contracts", "Weekly Haat Stalls for Ready-Made Kurtas/Pajamas", "B2B Supply to District Town Garment Showrooms"],
        "threats": ["Rapid fashion trend changes and fabric wastage", "Seasonal peaks (Weddings/Eid/Diwali) followed by dry months", "Power cuts halting motorized machines", "Shortage of skilled stitching labor in village"],
        "mitigation": ["Pre-booking institutional school uniform contracts during off-season", "Solar DC powered industrial sewing machines", "Conducting free 15-day skill workshops for local SHG women to create labor pool", "Standardized readymade sizing patterns (S, M, L, XL)"],
        "niche_opportunities": ["Annual Uniform Supplier to 4-5 local Gram Panchayat schools", "Bridal trousseau custom fitting and Zari/Aari hand embroidery", "Low-cost cotton cloth bags replacing banned plastic bags in Mandi"],
        "saturation_baseline_per_block": 10
    },
    "Food Processing, Pickles, Papad & Spices": {
        "category_id": "food_processing",
        "icon": "🥒",
        "description": "Value-addition micro-enterprise: Traditional mango/chilli pickles, sun-dried papad, turmeric powder, and dried fruit/vegetable processing.",
        "capex_items": [
            {"item": "Commercial Vegetable/Fruit Dicer, Washer & Pulping Unit", "pct": 30},
            {"item": "Stainless Steel Mixing Vats, Solar Dryers & Trays", "pct": 28},
            {"item": "Continuous Band Pouch Sealer & Bottle Capper", "pct": 20},
            {"item": "Digital Refractometer, pH Meter & Weighing Scale", "pct": 10},
            {"item": "FSSAI Compliance Setup (Storage Racks, Netting, Utensils)", "pct": 12}
        ],
        "opex_items": [
            {"item": "Seasonal Fresh Fruits/Vegetables (Mango, Amla, Chilli, Lemons)", "pct": 50},
            {"item": "Mustard Oil, Spices, Salt, Preservatives & Ingredients", "pct": 22},
            {"item": "Glass Jars, Food-Grade Pouches, Labels & Corrugated Boxes", "pct": 18},
            {"item": "FSSAI Testing, Panchayat Licensing, Transport", "pct": 10}
        ],
        "unit_economics": {
            "base_unit": "500g Pickle Jar / 250g Papad Pack",
            "cost_per_unit_liquid": 45.0,     # ₹ cost of raw ingredients + jar
            "selling_price_liquid": 95.0,     # ₹ retail selling price
            "value_add_cost_paneer_kg": 60.0, # ₹ Organic Amla Candy / Murabba pack cost
            "selling_price_paneer_kg": 150.0, # ₹ Premium price
            "value_add_margin_pct": 52.6,
            "daily_output_litres_per_animal": 50.0
        },
        "market_channels": ["District Town Grocery Stores & Supermarkets", "Direct Sales at Government / MoSJE Saras Melas & Exhibitions", "Rural Dhabas, Canteens & Highway Eateries", "E-commerce via ONDC / Tribal Cooperative / SHG portals"],
        "threats": ["Raw material crop failure due to unseasonal rain", "Food spoilage/fungus if oil level or salt ratio is inaccurate", "Stringent FSSAI quality inspections", "Competition from large commercial FMCG pickle brands"],
        "mitigation": ["MoSJE / KVIC food safety standard training & batch date stamping", "Strict standard recipe formulation book with exact oil/brine ratios", "Direct seasonal farm procurement when mango/amla prices crash", "Leveraging 'Ghar ka Swaad' (Home-made authentic rural recipe) branding"],
        "niche_opportunities": ["Traditional Amla Murabba & Garlic-Chilli Chutney without synthetic preservatives", "Gluten-free Ragi / Moong Dal high-protein papads for health-conscious town buyers", "Export-grade seasonal organic mango pickle with GI-tag storytelling"],
        "saturation_baseline_per_block": 8
    },
    "Solar Service Kiosk, Battery & Rural Tech Hub": {
        "category_id": "solar_tech",
        "icon": "☀️",
        "description": "Rural clean energy & digital services kiosk: Solar panel installation & maintenance, EV battery charging, and CSC digital citizen services.",
        "capex_items": [
            {"item": "5kW Rooftop Solar PV System with Lithium Battery Bank", "pct": 45},
            {"item": "Fast EV / E-Rickshaw Battery Charger & Testing Bench", "pct": 22},
            {"item": "Multi-Function Laser Printer, Scanner, Lamination & PC", "pct": 18},
            {"item": "Solar Installation Toolkit (Crimper, Multimeter, Inverter tester)", "pct": 10},
            {"item": "Kiosk Interior, Counter & Signage", "pct": 5}
        ],
        "opex_items": [
            {"item": "Replacement Solar Connectors, Cables, Distilled Water", "pct": 35},
            {"item": "Broadband Internet / 5G Router Subscription", "pct": 20},
            {"item": "Printing Paper, Ink Cartridges, Thermal Rolls, Lamination Sheets", "pct": 25},
            {"item": "Travel / Bike Fuel for on-site farm solar pump servicing", "pct": 20}
        ],
        "unit_economics": {
            "base_unit": "Solar Service Call / E-Rickshaw Full Charge / Digital Docs",
            "cost_per_unit_liquid": 60.0,     # ₹ electricity + consumables cost
            "selling_price_liquid": 180.0,    # ₹ service price
            "value_add_cost_paneer_kg": 1200.0,# ₹ Solar Home Lighting installation cost
            "selling_price_paneer_kg": 2800.0,# ₹ Installation service charge
            "value_add_margin_pct": 57.1,
            "daily_output_litres_per_animal": 25.0
        },
        "market_channels": ["Farmers with PM-KUSUM Solar Irrigation Pumps", "Rural E-Rickshaw and 2-Wheeler Drivers", "Gram Panchayat Citizens needing Aadhaar/Certificates/Govt Form submission", "Villagers looking for home solar backup during power outages"],
        "threats": ["Rapid hardware price deflation", "Frequent local internet fiber cut", "Seasonal monsoon drop in solar generation", "High battery replacement cost"],
        "mitigation": ["Lithium Ferrophosphate (LiFePO4) 5-year warranty batteries", "Dual SIM fallback router (Jio + Airtel)", "Annual maintenance contract (AMC) model with 50+ local farmers", "Partnership with PM-KUSUM approved vendor for authorized repair"],
        "niche_opportunities": ["PM-KUSUM Solar Pump cleaning and inverter maintenance AMC", "Night-time emergency DC charging for rural electric loaders / tempo", "Farmer soil-health card testing and drone spraying liaison desk"],
        "saturation_baseline_per_block": 5
    },
    "Metal Fabrication, Carpentry & Farm Implement Repair": {
        "category_id": "fabrication",
        "icon": "⚒️",
        "description": "Engineering workshop: Welding, fabrication of tractor trolleys, seed drills, iron grills, gates, shutters, and wooden farm implements.",
        "capex_items": [
            {"item": "Inverter Arc & MIG Welding Machines (Heavy-Duty)", "pct": 32},
            {"item": "High-Speed Metal Cut-Off Saw, Angle Grinder & Bench Drill", "pct": 25},
            {"item": "Wood Planner, Circular Saw & Lathe Turning Machine", "pct": 20},
            {"item": "3-Phase High Voltage Stabilizer & Heavy Wiring", "pct": 13},
            {"item": "Safety Gear, Gas Torch & Heavy-Duty Vices / Worktables", "pct": 10}
        ],
        "opex_items": [
            {"item": "Mild Steel Pipes, Angles, Sheets, Iron Channels", "pct": 62},
            {"item": "Welding Electrodes, Cutting Discs, Oxygen/Acetylene gas", "pct": 15},
            {"item": "Electricity bill (Industrial 3-phase tariff)", "pct": 13},
            {"item": "Anti-Rust Primer, Enamel Paints, Thinner & Brushes", "pct": 10}
        ],
        "unit_economics": {
            "base_unit": "Fabricated Iron Gate / Tractor Trolley Side / Window Grill (per Sq Ft)",
            "cost_per_unit_liquid": 140.0,    # ₹ per sq ft steel + weld cost
            "selling_price_liquid": 230.0,    # ₹ per sq ft finished price
            "value_add_cost_paneer_kg": 3200.0,# ₹ Farm implement overhaul cost
            "selling_price_paneer_kg": 6500.0,# ₹ Repair and reinforcement charge
            "value_add_margin_pct": 39.1,
            "daily_output_litres_per_animal": 30.0
        },
        "market_channels": ["Farmers building new houses / tubewells", "Tractor & Thresher Owners needing urgent harvest repairs", "Gram Panchayat civil contractors (School desks, railings)", "Commercial shops needing rolling shutters and iron gates"],
        "threats": ["Spike in raw iron/steel prices in wholesale mandi", "Occupational safety hazards (Eye arc injuries, metal sparks)", "High competition from established district workshops", "Power fluctuations burning transformer coils"],
        "mitigation": ["Advance 50% cash deposit from client before buying raw steel", "Strict use of auto-darkening welding helmets and ISI safety gear", "Fast turnaround (2-hour express repair) during peak harvest season", "Servo voltage stabilizer installation"],
        "niche_opportunities": ["Lightweight galvanized iron cages for goat and poultry farms", "Customized solar panel mounting structures for rooftop/field installations", "Tractor-mounted bund makers and ditchers for precision farming"],
        "saturation_baseline_per_block": 9
    },
    "Cold Chain, Micro-Storage & Rural Logistics/Transport": {
        "category_id": "cold_chain_logistics",
        "icon": "🚛",
        "description": "5-10 MT Micro Solar Cold Room & 3-Wheeler Electric Refrigerated Van for reducing post-harvest vegetable and milk spoilage.",
        "capex_items": [
            {"item": "Prefabricated Thermal Insulated Chamber (5 MT PUF Panels)", "pct": 40},
            {"item": "Solar-Powered Hermetic Chilling Unit with Thermal Storage", "pct": 28},
            {"item": "Electric Cargo Loader / 3-Wheeler Delivery Van", "pct": 20},
            {"item": "Crates, Pallets, Humidity Controllers & Digital Loggers", "pct": 8},
            {"item": "Weighing Platform & Sanitizing Wash Basins", "pct": 4}
        ],
        "opex_items": [
            {"item": "Electricity / Solar Battery Maintenance & Grid Backup", "pct": 30},
            {"item": "Vehicle Charging, Tyre Maintenance & Insurance", "pct": 30},
            {"item": "Cleaning Disinfectants, Fungicide Rinses, Pallet repairs", "pct": 20},
            {"item": "Driver / Operator Allowance, Mandi Toll & Loading labor", "pct": 20}
        ],
        "unit_economics": {
            "base_unit": "Storage (per Crate per Day) / Transport Trip (₹/km)",
            "cost_per_unit_liquid": 8.0,      # ₹ cost per crate/day storage
            "selling_price_liquid": 22.0,     # ₹ storage fee charged to farmer
            "value_add_cost_paneer_kg": 450.0,# ₹ per round trip direct to APMC
            "selling_price_paneer_kg": 1100.0,# ₹ Mandi delivery fee
            "value_add_margin_pct": 63.6,
            "daily_output_litres_per_animal": 80.0
        },
        "market_channels": ["Horticulture Farmers (Tomato, Green Chilli, Capsicum, Strawberry)", "Local Dairy Cooperatives for evening milk hold-over", "Flower Cultivators (Marigold, Jasmine, Rose) for market auctions", "District Town Supermarkets & Hotels needing daily fresh delivery"],
        "threats": ["Refrigerant leakage or compressor breakdown", "Farmers reluctant to pay daily rental unless price surge happens", "Seasonal crop gaps with empty cold room", "Battery degradation in solar cold room"],
        "mitigation": ["Multi-commodity temperature calibration (can switch from potato to milk to flowers)", "Profit-sharing storage model (take 20% of extra price farmer gets later)", "Tie-up with local FPOs (Farmer Producer Organizations) for guaranteed capacity", "AMC with certified thermal engineering technician"],
        "niche_opportunities": ["Evening milk holding for small farmers to eliminate distress night sales", "Marigold and Jasmine flower cold preservation before festival morning pujas", "Direct farm-to-door fresh vegetable subscription crates to town colonies"],
        "saturation_baseline_per_block": 4
    },
    "Mushroom Cultivation & Organic Bio-Fertilizer (Vermicompost)": {
        "category_id": "mushroom_biofertilizer",
        "icon": "🍄",
        "description": "High-density indoor Oyster/Button mushroom shed paired with cattle dung vermicomposting beds and organic liquid vermiwash.",
        "capex_items": [
            {"item": "Insulated Cropping Room with Bamboo Racks & Fogging Misters", "pct": 38},
            {"item": "Substrate Pasteurization Boiler / Autoclave Drum", "pct": 22},
            {"item": "HDPE Vermicompost Beds (12ft x 4ft x 2ft) x 10 units", "pct": 20},
            {"item": "Australian Earthworms (Eisenia Fetida) 25 kg Colony", "pct": 10},
            {"item": "Dehydrator for Dried Mushrooms & Pouch Vacuum Sealer", "pct": 10}
        ],
        "opex_items": [
            {"item": "Paddy Straw / Wheat Straw & Certified Mushroom Spawn", "pct": 45},
            {"item": "Raw Cow Dung, Agricultural Biomass & Fallen Leaves", "pct": 25},
            {"item": "Perforated PP Grow Bags, Rubber Bands, Disinfectants (Formalin/Bavistin)", "pct": 15},
            {"item": "Water, Electricity, Packaging gunny sacks & HDPE Bags", "pct": 15}
        ],
        "unit_economics": {
            "base_unit": "Kg Fresh Oyster Mushroom / 50kg Bag Vermicompost",
            "cost_per_unit_liquid": 42.0,     # ₹ cost per kg mushroom harvested
            "selling_price_liquid": 110.0,    # ₹ fresh mushroom farm-gate price
            "value_add_cost_paneer_kg": 180.0,# ₹ 50kg Vermicompost bag cost
            "selling_price_paneer_kg": 450.0, # ₹ Organic nursery & farm sale price
            "value_add_margin_pct": 61.8,
            "daily_output_litres_per_animal": 25.0
        },
        "market_channels": ["Local Dhabas, Restaurants & Town Pizza / Burger joints", "Weekly Vegetable Mandis & Direct Household Walk-in", "Organic Farming Growers & Polyhouse Nurseries (Vermicompost)", "Ayurvedic & Health Food Buyers (Dehydrated Mushroom Powder)"],
        "threats": ["Green mold / Trichoderma fungal contamination in substrate", "High summer ambient temperatures exceeding 32°C for Button mushrooms", "Short 48-hour shelf-life of fresh mushrooms without refrigeration", "Quality degradation of earthworms due to extreme heat or ant attack"],
        "mitigation": ["Shift to warm-weather Milky Mushrooms (Calocybe indica) during summer", "Strict substrate steam sterilization protocol with temperature monitoring", "Small solar dehydrator to immediately convert unsold stock into dried mushroom slices", "Neem cake border around vermicompost beds to prevent red ant infestation"],
        "niche_opportunities": ["Dehydrated Oyster Mushroom Powder packaged as protein supplement", "Liquid Vermiwash bottled in 1-Litre sprayers for terrace gardeners", "Ready-to-grow DIY mushroom fruiting bags sold to school students/hobbyists"],
        "saturation_baseline_per_block": 6
    },
    "Rural Beauty, Wellness & Personal Grooming Studio": {
        "category_id": "beauty_wellness",
        "icon": "💇‍♀️",
        "description": "Professional women's salon, bridal makeup studio, skincare, and herbal organic cosmetic center in rural market hubs.",
        "capex_items": [
            {"item": "Hydraulic Salon Chairs, Hair Washing Station & Mirrors", "pct": 32},
            {"item": "Professional Facial Steamer, High-Frequency & Hair Dryers", "pct": 24},
            {"item": "Bridal Makeup Vanity Kit, Ring Lights & Airbrush Gun", "pct": 20},
            {"item": "Salon Interior, Air Conditioner / Inverter, Partitioning", "pct": 16},
            {"item": "Herbal Product Display Counter & Towel Sterilizer", "pct": 8}
        ],
        "opex_items": [
            {"item": "Branded Cosmetic Creams, Hair Colors, Bleach & Wax", "pct": 52},
            {"item": "Disposable Sheets, Cotton, Aprons, Cleansers & Sponges", "pct": 18},
            {"item": "Electricity, Inverter power, Air conditioning", "pct": 16},
            {"item": "Promotional bridal photo albums, social media boosts", "pct": 14}
        ],
        "unit_economics": {
            "base_unit": "Standard Grooming Service / Bridal Full Package",
            "cost_per_unit_liquid": 65.0,     # ₹ facial/wax consumables cost
            "selling_price_liquid": 280.0,    # ₹ basic package charge
            "value_add_cost_paneer_kg": 1100.0,# ₹ Premium Bridal Makeup kit cost
            "selling_price_paneer_kg": 5500.0,# ₹ Bridal Package charge
            "value_add_margin_pct": 76.8,
            "daily_output_litres_per_animal": 12.0
        },
        "market_channels": ["Village Women & College Girls", "Wedding Season Bridal Packages (Sagan, Mehndi, Reception)", "Festival Makeovers (Karva Chauth, Teej, Eid, Diwali, Durga Puja)", "Home-Visit Service for VIP wedding parties in nearby villages"],
        "threats": ["Seasonal business swings with extreme peaks in wedding months and dips in monsoon", "Skin allergy reactions from spurious duplicate cosmetics", "Power outages disabling hair styling appliances", "Intense price bargaining by customers"],
        "mitigation": ["Launch off-season herbal skincare & haircare package discounts", "Strict use of 100% genuine sealed branded products with allergy patch tests", "Solar inverter connection for continuous lighting and hair tools", "Transparent printed rate-card displayed proudly at reception"],
        "niche_opportunities": ["Complete Bridal Destination Package covering Bride + 5 Family Members", "Organic homemade Ubtan & Haldi herbal skincare packs for sale", "Certified 30-day beautician training courses for local village girls"],
        "saturation_baseline_per_block": 11
    },
    "Handicrafts, Clay Pottery & Terracotta Art": {
        "category_id": "handicrafts",
        "icon": "🏺",
        "description": "Artisan enterprise: Motorized potter's wheel, smokeless kiln, terracotta tableware, festival diyas, and eco-friendly home decor.",
        "capex_items": [
            {"item": "Motorized Electric Potter's Wheel with Speed Regulator x 2", "pct": 30},
            {"item": "Smokeless Brick Kiln / Electric Pottery Furnace", "pct": 35},
            {"item": "Clay Pug Mill (Clay Mixer & De-airing machine)", "pct": 18},
            {"item": "Display Shelves, Drying Racks & Packing Workstation", "pct": 10},
            {"item": "Glazing Equipment, Brushes & Mold Sets", "pct": 7}
        ],
        "opex_items": [
            {"item": "Specialized Riverbed Clay, Terracotta Sand, Organic Glazes", "pct": 45},
            {"item": "Kiln Fuel (Biomass Briquettes / Wood / Electricity)", "pct": 25},
            {"item": "Shock-Proof Bubble Wrap, Shredded Paper, Carton Boxes", "pct": 20},
            {"item": "Transport to Urban Handicraft Emporiums & Melas", "pct": 10}
        ],
        "unit_economics": {
            "base_unit": "Terracotta Cooking Handi / Set of 50 Diwali Diyas",
            "cost_per_unit_liquid": 35.0,     # ₹ clay + firing + labor cost
            "selling_price_liquid": 110.0,    # ₹ retail artisan selling price
            "value_add_cost_paneer_kg": 180.0,# ₹ Glazed Terracotta Designer Vase cost
            "selling_price_paneer_kg": 650.0, # ₹ Urban decor boutique selling price
            "value_add_margin_pct": 68.2,
            "daily_output_litres_per_animal": 40.0
        },
        "market_channels": ["Diwali & Festive Pop-up Haats", "Urban Home Decor Boutiques & Nursery Planter Retailers", "Direct Tourists & Cultural Resorts", "MoSJE / TRIFED / Dastkar National Exhibitions"],
        "threats": ["High product transit breakage rate if poorly packed", "Rainy season halting open-air clay drying", "Competition from cheap plastic & cheap ceramic imports", "Physical fatigue from manual clay processing"],
        "mitigation": ["Motorized pug mill to eliminate manual leg-kneading of clay", "Puffed air-cushion corrugated boxing for zero-breakage transport", "Emphasizing lead-free, food-grade laboratory certified cooking pots", "Pre-season bulk diya production starting 4 months before Diwali"],
        "niche_opportunities": ["Lead-Free Microwave-Safe Terracotta Curd Pots and Tea Kulhads for cafes", "Terracotta Water Bottles with cork caps for eco-conscious city consumers", "Customized architectural terracotta jalis and garden wall tiles"],
        "saturation_baseline_per_block": 7
    }
}
