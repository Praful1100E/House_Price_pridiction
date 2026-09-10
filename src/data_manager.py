"""
Data Manager Module for House Price Prediction Platform.
Handles data loading, caching, dataset audits, and SQLite database persistence
for prediction history and custom property inventory.
"""

from datetime import datetime
import json
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "real_estate.db"


def ensure_directories():
    """Ensures required data and database directories exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)


def get_data_filepath(filename: str = "train.csv") -> Path:
    """Finds a dataset file across data/, projects/, or root."""
    search_paths = [
        DATA_DIR / filename,
        BASE_DIR / "projects" / filename,
        BASE_DIR / filename,
    ]
    for p in search_paths:
        if p.exists():
            return p
    return DATA_DIR / filename


@st.cache_data(show_spinner="Loading dataset...")
def load_dataset(filename: str = "train.csv") -> pd.DataFrame:
    """Loads a CSV dataset with error handling and caching."""
    path = get_data_filepath(filename)
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error reading dataset at {path}: {e}")
        return None


def get_dataset_summary(df: pd.DataFrame, target_col: str = "SalePrice") -> dict:
    """Generates comprehensive summary metrics for the dataset."""
    if df is None or df.empty:
        return {}

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    total_missing = int(df.isnull().sum().sum())
    missing_cells_pct = (total_missing / (df.shape[0] * df.shape[1])) * 100

    target_stats = {}
    if target_col in df.columns and pd.api.types.is_numeric_dtype(df[target_col]):
        target_stats = {
            "mean": float(df[target_col].mean()),
            "median": float(df[target_col].median()),
            "min": float(df[target_col].min()),
            "max": float(df[target_col].max()),
            "std": float(df[target_col].std()),
        }

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "num_features": len(num_cols),
        "cat_features": len(cat_cols),
        "total_missing": total_missing,
        "missing_pct": round(missing_cells_pct, 2),
        "target_stats": target_stats,
    }


def get_missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a breakdown of missing values per column."""
    if df is None:
        return pd.DataFrame()
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df)) * 100
    res = pd.DataFrame(
        {
            "Column": df.columns,
            "Missing Count": missing_count.values,
            "Percentage (%)": missing_pct.round(2).values,
            "Data Type": df.dtypes.astype(str).values,
        }
    )
    return res[res["Missing Count"] > 0].sort_values(
        by="Missing Count", ascending=False
    ).reset_index(drop=True)


# ==========================================
# SQLite Database Management
# ==========================================


def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection to the application database."""
    ensure_directories()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes SQLite database tables for prediction logs and property inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Prediction History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            property_mode TEXT NOT NULL,
            location TEXT,
            area_sqft REAL,
            bedrooms INTEGER,
            bathrooms REAL,
            overall_qual INTEGER,
            year_built INTEGER,
            model_used TEXT,
            predicted_price REAL,
            low_bound REAL,
            high_bound REAL,
            currency TEXT DEFAULT 'USD',
            notes TEXT
        )
    """)

    # 2. Custom Properties Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            area_sqft REAL NOT NULL,
            bedrooms INTEGER,
            bathrooms REAL,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            listing_type TEXT DEFAULT 'For Sale',
            date_added TEXT NOT NULL,
            notes TEXT
        )
    """)

    # 3. Marketplace Properties Table (Buy & Sell)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            property_type TEXT NOT NULL,
            location TEXT NOT NULL,
            city_district TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            area_sqft REAL NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms REAL NOT NULL,
            garage_cars INTEGER DEFAULT 1,
            year_built INTEGER DEFAULT 2020,
            condition_rating INTEGER DEFAULT 8,
            image_url TEXT,
            amenities TEXT,
            seller_name TEXT DEFAULT 'Property Owner',
            seller_contact TEXT DEFAULT 'contact@realestate-ai.com',
            status TEXT DEFAULT 'Available',
            date_listed TEXT NOT NULL,
            featured INTEGER DEFAULT 0,
            description TEXT
        )
    """)

    # 4. Property Inquiries & Purchase Offers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS property_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER NOT NULL,
            property_title TEXT NOT NULL,
            buyer_name TEXT NOT NULL,
            buyer_email TEXT NOT NULL,
            buyer_phone TEXT,
            offer_amount REAL NOT NULL,
            inquiry_type TEXT NOT NULL,
            tour_date TEXT,
            status TEXT DEFAULT 'Pending',
            timestamp TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (property_id) REFERENCES marketplace_properties(id)
        )
    """)

    conn.commit()
    conn.close()

    # Seed marketplace catalog if currently empty
    seed_marketplace_properties_if_empty()


# ==========================================
# Marketplace Properties & Seeding
# ==========================================

DEFAULT_MARKETPLACE_HOUSES = [
    {
        "title": "The Glass Horizon Modern Villa",
        "property_type": "Luxury Villa",
        "location": "Beverly Hills, CA",
        "city_district": "Beverly Hills",
        "price": 3850000.0,
        "currency": "USD",
        "area_sqft": 4800.0,
        "bedrooms": 5,
        "bathrooms": 5.5,
        "garage_cars": 3,
        "year_built": 2022,
        "condition_rating": 10,
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Infinity Pool, Smart Home Automation, Wine Cellar, Panoramic Ocean & City View, Solar Power, Chef's Kitchen",
        "seller_name": "Alexander Sterling",
        "seller_contact": "alex.sterling@prestigerealty.com",
        "status": "Available",
        "featured": 1,
        "description": "An architectural tour-de-force featuring soaring 14-foot ceilings, floor-to-ceiling motorized glass panels, zero-edge heated infinity pool, and seamless indoor-outdoor California living.",
    },
    {
        "title": "Himalayan Cedar Wood Haven",
        "property_type": "Hill Station Chalet",
        "location": "Mashobra / Shimla, HP, India",
        "city_district": "Shimla",
        "price": 28500000.0,
        "currency": "INR",
        "area_sqft": 3200.0,
        "bedrooms": 4,
        "bathrooms": 4.0,
        "garage_cars": 2,
        "year_built": 2021,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Snow-Capped Mountain View, Fireplace in all suites, Pine Forest Trail, Heated Wood Flooring, Solar Inverter, Organic Apple Orchard",
        "seller_name": "Vikramaditya Rana",
        "seller_contact": "vikram.rana@himalayanestates.in",
        "status": "Available",
        "featured": 1,
        "description": "Nestled in dense deodar forests with uninterrupted views of the Pir Panjal mountain range. Handcrafted with seasoned cedar wood, stone hearths, and modern radiant floor heating.",
    },
    {
        "title": "Nordic Light Contemporary Residence",
        "property_type": "Single Family Home",
        "location": "Bellevue, Seattle, WA",
        "city_district": "Bellevue",
        "price": 1450000.0,
        "currency": "USD",
        "area_sqft": 2950.0,
        "bedrooms": 4,
        "bathrooms": 3.5,
        "garage_cars": 2,
        "year_built": 2020,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "amenities": "EV Charger Ready, Private Japanese Garden, Quartz Waterfall Island, Dual Home Offices, Top Rated School District",
        "seller_name": "Sarah Jenkins",
        "seller_contact": "sarah.j@pacwestrealty.com",
        "status": "Available",
        "featured": 1,
        "description": "Minimalist Scandinavian aesthetics meet Pacific Northwest serenity. Features an open-concept great room, double-sided fireplace, and ultra-efficient heat pump HVAC system.",
    },
    {
        "title": "Manali Valley Pineview Estate",
        "property_type": "Luxury Cottage",
        "location": "Old Manali, HP, India",
        "city_district": "Manali",
        "price": 19500000.0,
        "currency": "INR",
        "area_sqft": 2600.0,
        "bedrooms": 3,
        "bathrooms": 3.0,
        "garage_cars": 2,
        "year_built": 2023,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Beas River Proximity, Rohtang Pass Views, Wooden Balconies, Dedicated Caretaker Quarters, High Speed Fiber",
        "seller_name": "Rohit & Meera Sharma",
        "seller_contact": "manali.pineview@outlook.com",
        "status": "Available",
        "featured": 0,
        "description": "Peaceful riverside haven near Old Manali with sweeping vistas of snow-capped peaks. Perfect as a high-yield boutique holiday homestay or private vacation home.",
    },
    {
        "title": "Skyline Penthouse with Private Terrace",
        "property_type": "Luxury Penthouse",
        "location": "Brickell, Miami, FL",
        "city_district": "Miami",
        "price": 2650000.0,
        "currency": "USD",
        "area_sqft": 3400.0,
        "bedrooms": 3,
        "bathrooms": 4.0,
        "garage_cars": 2,
        "year_built": 2023,
        "condition_rating": 10,
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Private Rooftop Jacuzzi, Biscayne Bay Views, 24/7 Concierge, Valet Parking, Private Elevator Access, Spa & Fitness Center",
        "seller_name": "Elena Rodriguez",
        "seller_contact": "elena.r@miamiluxuryliving.com",
        "status": "Available",
        "featured": 1,
        "description": "Dramatic double-height living areas framing glittering bay and skyline sunsets. Includes Italian designer cabinetry, motorized shades, and custom rooftop entertainment deck.",
    },
    {
        "title": "Solan Valley Green Orchard Villa",
        "property_type": "Villa",
        "location": "Kasauli Hills / Solan, HP, India",
        "city_district": "Solan",
        "price": 14500000.0,
        "currency": "INR",
        "area_sqft": 2400.0,
        "bedrooms": 3,
        "bathrooms": 3.0,
        "garage_cars": 2,
        "year_built": 2022,
        "condition_rating": 8,
        "image_url": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Terraced Organic Garden, Kasauli Sunset Views, Solar Water Heating, Gated Community, 24x7 Water Supply",
        "seller_name": "Captain K.S. Verma",
        "seller_contact": "ksverma.solan@gmail.com",
        "status": "Available",
        "featured": 0,
        "description": "Quiet hilltop location just 45 minutes from Chandigarh. Features spacious sunrooms, modular kitchen, and an expansive garden terrace overlooking misty valleys.",
    },
    {
        "title": "The Austin Hill Country Modern Farmhouse",
        "property_type": "Modern Farmhouse",
        "location": "Westlake Hills, Austin, TX",
        "city_district": "Austin",
        "price": 1875000.0,
        "currency": "USD",
        "area_sqft": 3650.0,
        "bedrooms": 4,
        "bathrooms": 4.5,
        "garage_cars": 3,
        "year_built": 2021,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Heated Saltwater Pool, Outdoor Kitchen & BBQ, Covered Veranda, 1-Acre Oak-Studded Lot, Metal Standing Seam Roof",
        "seller_name": "Travis & Chloe Miller",
        "seller_contact": "miller.atx@gmail.com",
        "status": "Available",
        "featured": 0,
        "description": "Quintessential Texas hill country luxury. White limestone exterior, board-and-batten finishes, wide-plank French white oak flooring, and custom built-ins throughout.",
    },
    {
        "title": "Dharamshala Dhauladhar View Residence",
        "property_type": "Hill Station Chalet",
        "location": "Dharamkot, Dharamshala, HP, India",
        "city_district": "Dharamshala",
        "price": 16500000.0,
        "currency": "INR",
        "area_sqft": 2100.0,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "garage_cars": 1,
        "year_built": 2022,
        "condition_rating": 8,
        "image_url": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Direct Dhauladhar Peak Panorama, Meditation Room, Tea Garden Access, Cedar Wood Ceilings, High Speed Fiber Internet",
        "seller_name": "Tenzin Norbu",
        "seller_contact": "tenzin.norbu@himalayanretreats.org",
        "status": "Available",
        "featured": 0,
        "description": "Inspiring sanctuary surrounded by pine and rhododendron woods. Panoramic views of snow-dusted Dhauladhar peaks, perfect for writers, artists, or wellness investors.",
    },
    {
        "title": "Emerald Lake Forest Cabin Retreat",
        "property_type": "Lakefront Cabin",
        "location": "Lake Tahoe, CA / NV",
        "city_district": "Lake Tahoe",
        "price": 2150000.0,
        "currency": "USD",
        "area_sqft": 3100.0,
        "bedrooms": 4,
        "bathrooms": 3.0,
        "garage_cars": 2,
        "year_built": 2019,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Private Boat Dock, Outdoor Hot Tub, Stone Hearth, Ski Equipment Locker, Vaulted Pine Ceilings",
        "seller_name": "David Thorne",
        "seller_contact": "dthorne@tahoerealty.com",
        "status": "Available",
        "featured": 0,
        "description": "Ultimate alpine haven just minutes from Heavenly ski slopes and crystal blue Lake Tahoe waters. Turnkey furnished with custom lodge-style craftsmanship.",
    },
    {
        "title": "Colonial Heritage Bungalow",
        "property_type": "Heritage Estate",
        "location": "Chail / Kufri, HP, India",
        "city_district": "Kullu",
        "price": 34000000.0,
        "currency": "INR",
        "area_sqft": 4200.0,
        "bedrooms": 5,
        "bathrooms": 5.0,
        "garage_cars": 3,
        "year_built": 2018,
        "condition_rating": 9,
        "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80",
        "amenities": "2-Acre Private Estate, Fireplaces in all rooms, Badminton Court, Gazebo, Staff Quarters, Heritage Brass Hardware",
        "seller_name": "Raja B.K. Singh Estate",
        "seller_contact": "heritage.estates.hp@gmail.com",
        "status": "Available",
        "featured": 1,
        "description": "Grand British colonial architecture blending antique British teak furniture with contemporary luxury. Features 360-degree Himalayan ridges, private drive, and manicured lawns.",
    },
    {
        "title": "Silicon Valley Eco-Smart Smart Home",
        "property_type": "Eco Smart Home",
        "location": "Palo Alto, CA",
        "city_district": "Palo Alto",
        "price": 3200000.0,
        "currency": "USD",
        "area_sqft": 3300.0,
        "bedrooms": 4,
        "bathrooms": 4.0,
        "garage_cars": 2,
        "year_built": 2024,
        "condition_rating": 10,
        "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Net-Zero Energy, Tesla Powerwall & Solar, AI Climate Control, Rainwater Harvesting, Home Theater",
        "seller_name": "Arjun & Priya Mehta",
        "seller_contact": "arjun.mehta@techfounders.io",
        "status": "Available",
        "featured": 1,
        "description": "State-of-the-art sustainable luxury in prime Silicon Valley. Powered 100% by solar and battery storage with automated voice and biometric controls.",
    },
    {
        "title": "Kullu Riverside Apple Estate",
        "property_type": "Orchard Estate",
        "location": "Naggar / Kullu Valley, HP, India",
        "city_district": "Kullu",
        "price": 22000000.0,
        "currency": "INR",
        "area_sqft": 3100.0,
        "bedrooms": 4,
        "bathrooms": 3.5,
        "garage_cars": 2,
        "year_built": 2020,
        "condition_rating": 8,
        "image_url": "https://images.unsplash.com/photo-1576941089067-2de3c901e126?auto=format&fit=crop&w=1200&q=80",
        "amenities": "Commercial Apple Orchard Yield, Beas River Trout Fishing, Wood-Fired Pizza Oven, Sun Deck, Spring Water Source",
        "seller_name": "Harish Thakur",
        "seller_contact": "kullu.appleorchards@gmail.com",
        "status": "Available",
        "featured": 0,
        "description": "Breathtaking orchard estate in historical Naggar. Yields high annual harvest income while serving as an idyllic mountain residence overlooking snowy peaks.",
    },
]


def seed_marketplace_properties_if_empty():
    """Seeds default realistic marketplace houses if the table is empty."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM marketplace_properties")
        row = cursor.fetchone()
        count = row["count"] if row else 0

        if count == 0:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for prop in DEFAULT_MARKETPLACE_HOUSES:
                cursor.execute(
                    """
                    INSERT INTO marketplace_properties (
                        title, property_type, location, city_district, price,
                        currency, area_sqft, bedrooms, bathrooms, garage_cars,
                        year_built, condition_rating, image_url, amenities,
                        seller_name, seller_contact, status, date_listed,
                        featured, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        prop["title"],
                        prop["property_type"],
                        prop["location"],
                        prop["city_district"],
                        prop["price"],
                        prop["currency"],
                        prop["area_sqft"],
                        prop["bedrooms"],
                        prop["bathrooms"],
                        prop.get("garage_cars", 2),
                        prop.get("year_built", 2022),
                        prop.get("condition_rating", 8),
                        prop["image_url"],
                        prop["amenities"],
                        prop["seller_name"],
                        prop["seller_contact"],
                        prop.get("status", "Available"),
                        now_str,
                        prop.get("featured", 0),
                        prop["description"],
                    ),
                )
            conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error seeding marketplace properties: {e}")


def get_marketplace_properties(
    search_query: str = "",
    currency_filter: str = "All",
    prop_type: str = "All",
    status_filter: str = "All",
    min_price: float = 0.0,
    max_price: float = 0.0,
    min_beds: int = 0,
    sort_by: str = "Featured / Newest",
) -> pd.DataFrame:
    """Fetches marketplace properties with dynamic multi-criteria filtering."""
    try:
        init_db()
        conn = get_db_connection()
        query = "SELECT * FROM marketplace_properties WHERE 1=1"
        params = []

        if currency_filter and currency_filter != "All":
            query += " AND currency = ?"
            params.append(currency_filter)

        if prop_type and prop_type != "All":
            query += " AND property_type = ?"
            params.append(prop_type)

        if status_filter and status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)

        if min_price > 0:
            query += " AND price >= ?"
            params.append(min_price)

        if max_price > 0:
            query += " AND price <= ?"
            params.append(max_price)

        if min_beds > 0:
            query += " AND bedrooms >= ?"
            params.append(min_beds)

        if search_query:
            query += " AND (title LIKE ? OR location LIKE ? OR city_district LIKE ? OR amenities LIKE ?)"
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])

        if sort_by == "Price: Low to High":
            query += " ORDER BY price ASC"
        elif sort_by == "Price: High to Low":
            query += " ORDER BY price DESC"
        elif sort_by == "Living Area: Large to Small":
            query += " ORDER BY area_sqft DESC"
        else:
            query += " ORDER BY featured DESC, id DESC"

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching marketplace properties: {e}")
        return pd.DataFrame()


def get_marketplace_property_by_id(property_id: int) -> dict:
    """Retrieves a single property record by ID."""
    try:
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM marketplace_properties WHERE id = ?", (property_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None
    except Exception as e:
        st.error(f"Error fetching property {property_id}: {e}")
        return None


def add_marketplace_property(
    title: str,
    property_type: str,
    location: str,
    city_district: str,
    price: float,
    currency: str,
    area_sqft: float,
    bedrooms: int,
    bathrooms: float,
    garage_cars: int = 1,
    year_built: int = 2022,
    condition_rating: int = 8,
    image_url: str = "",
    amenities: str = "",
    seller_name: str = "Property Owner",
    seller_contact: str = "",
    status: str = "Available",
    description: str = "",
    featured: int = 0,
) -> bool:
    """Adds a new house listing to the marketplace database."""
    try:
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not image_url:
            # High-res fallback luxury home image
            image_url = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80"

        cursor.execute(
            """
            INSERT INTO marketplace_properties (
                title, property_type, location, city_district, price,
                currency, area_sqft, bedrooms, bathrooms, garage_cars,
                year_built, condition_rating, image_url, amenities,
                seller_name, seller_contact, status, date_listed,
                featured, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                title,
                property_type,
                location,
                city_district,
                price,
                currency,
                area_sqft,
                bedrooms,
                bathrooms,
                garage_cars,
                year_built,
                condition_rating,
                image_url,
                amenities,
                seller_name,
                seller_contact,
                status,
                now_str,
                featured,
                description,
            ),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to list property in marketplace: {e}")
        return False


def update_property_status(property_id: int, new_status: str) -> bool:
    """Updates the availability status of a property (Available, Under Offer, Sold)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE marketplace_properties SET status = ? WHERE id = ?",
            (new_status, property_id),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error updating property status: {e}")
        return False


def delete_marketplace_property(property_id: int) -> bool:
    """Deletes a marketplace listing by ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM marketplace_properties WHERE id = ?", (property_id,))
        cursor.execute("DELETE FROM property_inquiries WHERE property_id = ?", (property_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ==========================================
# Inquiries, Offers & Purchase Transactions
# ==========================================

def submit_property_inquiry(
    property_id: int,
    property_title: str,
    buyer_name: str,
    buyer_email: str,
    buyer_phone: str,
    offer_amount: float,
    inquiry_type: str = "Make an Offer",
    tour_date: str = "",
    notes: str = "",
) -> bool:
    """Records a buyer purchase order, offer bid, or tour schedule."""
    try:
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status = "Confirmed" if inquiry_type == "Buy Now / Purchase Order" else "Pending"

        cursor.execute(
            """
            INSERT INTO property_inquiries (
                property_id, property_title, buyer_name, buyer_email,
                buyer_phone, offer_amount, inquiry_type, tour_date,
                status, timestamp, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                property_id,
                property_title,
                buyer_name,
                buyer_email,
                buyer_phone,
                offer_amount,
                inquiry_type,
                tour_date,
                status,
                now_str,
                notes,
            ),
        )

        # If Buy Now, automatically mark property as Under Offer
        if inquiry_type == "Buy Now / Purchase Order":
            cursor.execute(
                "UPDATE marketplace_properties SET status = 'Under Offer' WHERE id = ?",
                (property_id,),
            )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to submit inquiry/offer: {e}")
        return False


def get_property_inquiries(property_id: int = None) -> pd.DataFrame:
    """Retrieves all inquiries, bids, and purchase orders."""
    try:
        init_db()
        conn = get_db_connection()
        if property_id is not None:
            query = "SELECT * FROM property_inquiries WHERE property_id = ? ORDER BY id DESC"
            df = pd.read_sql_query(query, conn, params=[property_id])
        else:
            query = "SELECT * FROM property_inquiries ORDER BY id DESC"
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching inquiries: {e}")
        return pd.DataFrame()


def delete_property_inquiry(inquiry_id: int) -> bool:
    """Deletes an inquiry record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM property_inquiries WHERE id = ?", (inquiry_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ==========================================
# Legacy Custom Properties Helper
# ==========================================

def save_prediction_log(
    property_mode: str,
    location: str,
    area_sqft: float,
    bedrooms: int,
    bathrooms: float,
    overall_qual: int,
    year_built: int,
    model_used: str,
    predicted_price: float,
    currency: str = "USD",
    low_bound: float = 0.0,
    high_bound: float = 0.0,
    notes: str = "",
) -> bool:
    """Logs a new property valuation record into SQLite."""
    try:
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO prediction_history (
                timestamp, property_mode, location, area_sqft, bedrooms,
                bathrooms, overall_qual, year_built, model_used,
                predicted_price, low_bound, high_bound, currency, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                now_str,
                property_mode,
                location,
                area_sqft,
                bedrooms,
                bathrooms,
                overall_qual,
                year_built,
                model_used,
                predicted_price,
                low_bound,
                high_bound,
                currency,
                notes,
            ),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to log prediction to database: {e}")
        return False


def get_prediction_history(limit: int = 100) -> pd.DataFrame:
    """Retrieves past prediction logs as a DataFrame."""
    try:
        init_db()
        conn = get_db_connection()
        query = f"SELECT * FROM prediction_history ORDER BY id DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching prediction history: {e}")
        return pd.DataFrame()


def delete_prediction_log(record_id: int) -> bool:
    """Deletes a specific prediction log record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def clear_all_prediction_history() -> bool:
    """Clears all prediction logs."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history")
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def add_custom_property(
    title: str,
    location: str,
    area_sqft: float,
    bedrooms: int,
    bathrooms: float,
    price: float,
    currency: str = "USD",
    listing_type: str = "For Sale",
    notes: str = "",
) -> bool:
    """Adds a custom property listing to the database."""
    try:
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO custom_properties (
                title, location, area_sqft, bedrooms, bathrooms,
                price, currency, listing_type, date_added, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                title,
                location,
                area_sqft,
                bedrooms,
                bathrooms,
                price,
                currency,
                listing_type,
                now_str,
                notes,
            ),
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to add custom property: {e}")
        return False


def get_custom_properties() -> pd.DataFrame:
    """Fetches custom real estate inventory."""
    try:
        init_db()
        conn = get_db_connection()
        query = "SELECT * FROM custom_properties ORDER BY id DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching custom properties: {e}")
        return pd.DataFrame()


def delete_custom_property(property_id: int) -> bool:
    """Deletes a custom property record by ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM custom_properties WHERE id = ?", (property_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
