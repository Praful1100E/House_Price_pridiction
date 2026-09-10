"""
Marketplace UI Module: Full Buy and Sell Real Estate Experience.
Features AI Deal Radar, property catalog with high-res galleries, Buy Now / Offer / Tour booking workflows,
and Sell Property wizard with instant AI Price Recommendations.
"""

from datetime import datetime
import uuid
import pandas as pd
import streamlit as st

from src.data_manager import (
    add_marketplace_property,
    delete_marketplace_property,
    delete_property_inquiry,
    get_marketplace_properties,
    get_marketplace_property_by_id,
    get_property_inquiries,
    submit_property_inquiry,
    update_property_status,
)
from src.ml_engine import (
    HP_MARKET_DATA,
    format_currency,
    predict_single_property,
)
from src.ui_theme import (
    render_deal_badge,
    render_metric_card,
    render_transaction_receipt,
)

# Preset Curated Luxury Architecture Photos for Sellers
CURATED_PHOTOS = {
    "Modern Glass Villa": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
    "Alpine Hill Chalet": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
    "Nordic Contemporary": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
    "Luxury Skyline Penthouse": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
    "Texas Modern Farmhouse": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80",
    "Himalayan Pine Retreat": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=1200&q=80",
    "Lakefront Forest Lodge": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80",
    "Colonial Teak Estate": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80",
}


def compute_ai_fair_value(pipe, data_info, prop: dict) -> float:
    """Calculates the AI estimated fair market value for a given marketplace property."""
    if pipe is None or data_info is None:
        return float(prop.get("price", 0))

    try:
        is_hp = prop.get("currency") == "INR" or any(
            d.lower() in prop.get("location", "").lower()
            for d in HP_MARKET_DATA["districts"]
        )

        if is_hp:
            # Find best matching district
            matched_district = "Shimla"
            for d in HP_MARKET_DATA["districts"]:
                if d.lower() in prop.get("location", "").lower() or d.lower() in prop.get("city_district", "").lower():
                    matched_district = d
                    break

            view_type = "Snow Mountain View" if "mountain" in prop.get("amenities", "").lower() else "Valley View"
            res = predict_single_property(
                pipeline=pipe,
                data_info=data_info,
                input_features={
                    "GrLivArea": prop.get("area_sqft", 2000),
                    "OverallQual": prop.get("condition_rating", 8),
                    "YearBuilt": prop.get("year_built", 2021),
                    "FullBath": int(prop.get("bathrooms", 2)),
                    "TotRmsAbvGrd": int(prop.get("bedrooms", 3)) + 2,
                    "GarageCars": int(prop.get("garage_cars", 2)),
                    "TotalBsmtSF": prop.get("area_sqft", 2000) * 0.35,
                },
                is_regional_hp=True,
                district=matched_district,
                view_type=view_type,
            )
            return float(res["predicted_price"])
        else:
            res = predict_single_property(
                pipeline=pipe,
                data_info=data_info,
                input_features={
                    "GrLivArea": prop.get("area_sqft", 2500),
                    "OverallQual": prop.get("condition_rating", 8),
                    "YearBuilt": prop.get("year_built", 2021),
                    "FullBath": int(prop.get("bathrooms", 2)),
                    "TotRmsAbvGrd": int(prop.get("bedrooms", 3)) + 2,
                    "GarageCars": int(prop.get("garage_cars", 2)),
                    "TotalBsmtSF": prop.get("area_sqft", 2500) * 0.4,
                    "Neighborhood": "CollgCr",
                },
                is_regional_hp=False,
            )
            return float(res["predicted_price"])
    except Exception:
        return float(prop.get("price", 0))


# ====================================================
# TAB: BUY HOUSES (MARKETPLACE)
# ====================================================

def render_buy_marketplace(pipe, data_info, global_is_inr: bool = False):
    """Renders the comprehensive Buy Houses Marketplace."""
    st.markdown("### 🛒 Real Estate Marketplace — Buy Houses & Luxury Estates")
    st.caption(
        "Browse verified residential properties, compare asking prices against our AI Valuation Engine, and submit buy orders or schedule tours."
    )

    # Top Search and Filter Bar
    with st.container():
        f1, f2, f3, f4 = st.columns([2, 1, 1, 1])
        with f1:
            search_text = st.text_input("🔍 Search Properties (City, Title, Amenities...)", "", placeholder="e.g. Villa, Shimla, Miami, Pool...")
        with f2:
            curr_opt = st.selectbox("Currency Filter", ["All", "USD ($)", "INR (₹)"], index=0)
            curr_val = "USD" if "USD" in curr_opt else ("INR" if "INR" in curr_opt else "All")
        with f3:
            prop_type_filter = st.selectbox(
                "Property Type",
                [
                    "All",
                    "Luxury Villa",
                    "Hill Station Chalet",
                    "Single Family Home",
                    "Luxury Penthouse",
                    "Modern Farmhouse",
                    "Lakefront Cabin",
                    "Heritage Estate",
                    "Eco Smart Home",
                    "Orchard Estate",
                    "Villa",
                ],
            )
        with f4:
            status_filter = st.selectbox("Listing Status", ["All", "Available", "Under Offer", "Sold"], index=0)

    # Collapsible Advanced Filters
    with st.expander("⚙️ Advanced Price, Bedrooms & Sorting Filters", expanded=False):
        c_af1, c_af2, c_af3, c_af4 = st.columns(4)
        with c_af1:
            min_beds = st.selectbox("Minimum Bedrooms", [0, 1, 2, 3, 4, 5], index=0)
        with c_af2:
            min_pr = st.number_input("Min Price", min_value=0.0, value=0.0, step=50000.0)
        with c_af3:
            max_pr = st.number_input("Max Price (0 for no limit)", min_value=0.0, value=0.0, step=100000.0)
        with c_af4:
            sort_by = st.selectbox(
                "Sort Results",
                [
                    "Featured / Newest",
                    "Price: Low to High",
                    "Price: High to Low",
                    "Living Area: Large to Small",
                ],
            )

    # Fetch Properties from Database
    props_df = get_marketplace_properties(
        search_query=search_text,
        currency_filter=curr_val,
        prop_type=prop_type_filter,
        status_filter=status_filter,
        min_price=min_pr,
        max_price=max_pr,
        min_beds=min_beds,
        sort_by=sort_by,
    )

    # Quick Marketplace Stats Counter
    st.markdown("---")
    s1, s2, s3, s4 = st.columns(4)
    total_props = len(props_df)
    avail_props = len(props_df[props_df["status"] == "Available"]) if not props_df.empty else 0
    with s1:
        render_metric_card("Active Listings", f"{avail_props} Available", delta=f"{total_props} Total Matching", delta_type="pos")
    with s2:
        avg_usd = props_df[props_df["currency"] == "USD"]["price"].mean() if not props_df.empty and (props_df["currency"] == "USD").any() else 0
        render_metric_card("Avg USD Price", f"${avg_usd:,.0f}" if avg_usd > 0 else "N/A", delta="US Market")
    with s3:
        avg_inr = props_df[props_df["currency"] == "INR"]["price"].mean() if not props_df.empty and (props_df["currency"] == "INR").any() else 0
        render_metric_card("Avg INR Price", format_currency(avg_inr, "INR") if avg_inr > 0 else "N/A", delta="Indian Market")
    with s4:
        featured_cnt = len(props_df[props_df["featured"] == 1]) if not props_df.empty else 0
        render_metric_card("Featured Estates", f"{featured_cnt} Prime Homes", delta="Handpicked Luxury")

    st.markdown("---")

    if props_df.empty:
        st.info("No properties found matching your filter criteria. Try clearing search keywords or expanding price filters.")
        return

    # Render 2-Column Property Grid
    prop_records = props_df.to_dict(orient="records")
    for idx in range(0, len(prop_records), 2):
        col_left, col_right = st.columns(2)
        cols = [col_left, col_right]

        for c_idx, col in enumerate(cols):
            item_idx = idx + c_idx
            if item_idx >= len(prop_records):
                break

            prop = prop_records[item_idx]
            curr = prop["currency"]
            price_val = float(prop["price"])
            price_str = format_currency(price_val, curr)
            prop_id = prop["id"]
            status = prop.get("status", "Available")

            # Compute AI Fair Valuation & Deal Badge
            ai_fair_val = compute_ai_fair_value(pipe, data_info, prop)
            price_diff_pct = ((price_val - ai_fair_val) / ai_fair_val) * 100 if ai_fair_val > 0 else 0
            deal_badge_html = render_deal_badge(0.0, price_diff_pct)

            # Status Badge Class
            if status == "Available":
                status_badge = '<span class="badge badge-emerald">● Available</span>'
            elif status == "Under Offer":
                status_badge = '<span class="badge badge-amber">⏳ Under Offer</span>'
            else:
                status_badge = '<span class="badge badge-purple">🔒 Sold</span>'

            # Amenities chips HTML
            amenities_list = [a.strip() for a in str(prop.get("amenities", "")).split(",") if a.strip()]
            amenities_html = "".join([f'<span class="prop-amenity-chip">{a}</span>' for a in amenities_list[:4]])

            with col:
                # Property Card Container
                card_html = f"""
                <div class="prop-card-container">
                    <div class="prop-img-wrapper">
                        <img src="{prop.get('image_url', '')}" alt="{prop['title']}">
                        <div class="prop-badge-overlay">
                            {deal_badge_html}
                        </div>
                        <div class="prop-status-overlay">
                            {status_badge}
                        </div>
                    </div>
                    <div style="padding: 1.2rem; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 700; text-transform: uppercase;">
                                {prop['property_type']} • {prop['city_district']}
                            </div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 0.2rem 0;">
                                {prop['title']}
                            </div>
                            <div style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 0.6rem;">
                                📍 {prop['location']}
                            </div>
                            <div class="prop-price-tag">
                                {price_str}
                            </div>
                            <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 0.6rem;">
                                AI Estimated Fair Value: <strong style="color: #cbd5e1;">{format_currency(ai_fair_val, curr)}</strong>
                            </div>
                            <div class="prop-specs-row">
                                <span>🛏️ {int(prop['bedrooms'])} Beds</span>
                                <span>🚿 {prop['bathrooms']} Baths</span>
                                <span>📐 {prop['area_sqft']:,.0f} SqFt</span>
                                <span>🚗 {prop['garage_cars']} Car</span>
                            </div>
                            <div style="margin: 0.5rem 0;">
                                {amenities_html}
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # Action & Inspection Expander
                with st.expander(f"🔍 Inspect & Buy: {prop['title']}", expanded=False):
                    st.markdown(f"**About this Property:** {prop.get('description', '')}")
                    st.markdown(f"**Listed by:** {prop.get('seller_name', 'Owner')} ({prop.get('seller_contact', 'N/A')})")

                    tab_buy, tab_offer, tab_tour = st.tabs(["⚡ Buy Now", "🏷️ Make Offer", "📅 Schedule Tour"])

                    # 1. Buy Now Tab
                    with tab_buy:
                        if status == "Sold":
                            st.warning("This property has already been sold.")
                        else:
                            with st.form(f"buy_now_form_{prop_id}"):
                                st.markdown(f"#### 💳 Instant Purchase Order — {price_str}")
                                b1, b2 = st.columns(2)
                                with b1:
                                    buyer_name = st.text_input("Full Name", "John Doe", key=f"bn_name_{prop_id}")
                                    buyer_email = st.text_input("Email Address", "john@example.com", key=f"bn_email_{prop_id}")
                                with b2:
                                    buyer_phone = st.text_input("Phone Number", "+1 555-0199", key=f"bn_phone_{prop_id}")
                                    pay_method = st.selectbox("Payment Escrow Method", ["Wire Transfer / Escrow", "Bank Mortgage Pre-approval", "Cash Full Settlement", "Cryptocurrency (USDC/ETH)"], key=f"bn_pay_{prop_id}")

                                buy_submit = st.form_submit_button("🔒 Confirm Instant Purchase Order", use_container_width=True)

                            if buy_submit:
                                order_id = str(uuid.uuid4())[:8].upper()
                                saved = submit_property_inquiry(
                                    property_id=prop_id,
                                    property_title=prop["title"],
                                    buyer_name=buyer_name,
                                    buyer_email=buyer_email,
                                    buyer_phone=buyer_phone,
                                    offer_amount=price_val,
                                    inquiry_type="Buy Now / Purchase Order",
                                    notes=f"Payment Method: {pay_method}. Transaction ID: {order_id}",
                                )
                                if saved:
                                    st.success("🎉 Purchase order confirmed! Escrow process initiated.")
                                    render_transaction_receipt(
                                        order_id=order_id,
                                        property_title=prop["title"],
                                        buyer_name=buyer_name,
                                        buyer_email=buyer_email,
                                        amount_formatted=price_str,
                                        transaction_type="Instant Purchase Order (Escrow)",
                                    )
                                    st.rerun()

                    # 2. Make an Offer Tab
                    with tab_offer:
                        if status == "Sold":
                            st.warning("This property has already been sold.")
                        else:
                            with st.form(f"offer_form_{prop_id}"):
                                st.markdown("#### 🏷️ Submit Counter Offer / Bid")
                                o1, o2 = st.columns(2)
                                with o1:
                                    o_name = st.text_input("Your Name", "Jane Smith", key=f"of_name_{prop_id}")
                                    o_email = st.text_input("Email Address", "jane@example.com", key=f"of_email_{prop_id}")
                                with o2:
                                    o_phone = st.text_input("Phone Number", "+1 555-0288", key=f"of_phone_{prop_id}")
                                    o_amount = st.number_input("Your Offer Amount", min_value=1000.0, value=price_val * 0.95, step=10000.0, key=f"of_amt_{prop_id}")
                                o_notes = st.text_area("Contingencies / Terms (e.g. 30-day closing, inspection waiver)", key=f"of_notes_{prop_id}")

                                offer_submit = st.form_submit_button("🚀 Submit Offer to Seller", use_container_width=True)

                            if offer_submit:
                                saved = submit_property_inquiry(
                                    property_id=prop_id,
                                    property_title=prop["title"],
                                    buyer_name=o_name,
                                    buyer_email=o_email,
                                    buyer_phone=o_phone,
                                    offer_amount=o_amount,
                                    inquiry_type="Make an Offer",
                                    notes=o_notes,
                                )
                                if saved:
                                    st.success(f"Offer of {format_currency(o_amount, curr)} submitted to the seller!")
                                    st.rerun()

                    # 3. Schedule Tour Tab
                    with tab_tour:
                        with st.form(f"tour_form_{prop_id}"):
                            st.markdown("#### 📅 Schedule In-Person or Virtual Tour")
                            t1, t2 = st.columns(2)
                            with t1:
                                t_name = st.text_input("Your Name", "Alex Morgan", key=f"tr_name_{prop_id}")
                                t_email = st.text_input("Email Address", "alex@example.com", key=f"tr_email_{prop_id}")
                                t_type = st.selectbox("Tour Format", ["In-Person Guided Tour", "Live 3D Virtual Walkthrough", "Self-Guided Open House"], key=f"tr_type_{prop_id}")
                            with t2:
                                t_phone = st.text_input("Phone", "+1 555-0377", key=f"tr_phone_{prop_id}")
                                t_date = st.date_input("Preferred Date", min_value=datetime.today(), key=f"tr_date_{prop_id}")
                                t_time = st.selectbox("Time Slot", ["10:00 AM - 11:00 AM", "01:00 PM - 02:00 PM", "04:00 PM - 05:00 PM", "06:00 PM - 07:00 PM"], key=f"tr_time_{prop_id}")

                            tour_submit = st.form_submit_button("📅 Confirm Tour Appointment", use_container_width=True)

                        if tour_submit:
                            tour_str = f"{t_date} at {t_time} ({t_type})"
                            saved = submit_property_inquiry(
                                property_id=prop_id,
                                property_title=prop["title"],
                                buyer_name=t_name,
                                buyer_email=t_email,
                                buyer_phone=t_phone,
                                offer_amount=0.0,
                                inquiry_type="Schedule Tour",
                                tour_date=tour_str,
                                notes=f"Tour Format: {t_type}",
                            )
                            if saved:
                                st.success(f"Tour confirmed for {tour_str}!")
                                render_transaction_receipt(
                                    order_id=str(uuid.uuid4())[:8].upper(),
                                    property_title=prop["title"],
                                    buyer_name=t_name,
                                    buyer_email=t_email,
                                    amount_formatted="Free Booking",
                                    transaction_type=f"Tour Appointment ({t_type})",
                                    tour_date=tour_str,
                                )


# ====================================================
# TAB: SELL HOUSES (LIST PROPERTY WIZARD)
# ====================================================

def render_sell_property_form(pipe, data_info, global_is_inr: bool = False):
    """Renders the step-by-step Sell Property Studio with AI Price Recommender."""
    st.markdown("### 🏷️ List Your Property for Sale")
    st.caption(
        "Publish your residential real estate listing to our global marketplace. Use our integrated AI Price Suggester to benchmark fair market value before publishing."
    )

    sub_sell1, sub_sell2 = st.tabs(["➕ Publish New Listing", "📋 Manage My Listings & Offers"])

    # SUB-TAB 1: Publish New Listing
    with sub_sell1:
        st.markdown("#### 🏡 Property Specifications & Details")

        col1, col2, col3 = st.columns(3)
        with col1:
            title_in = st.text_input("Property Title", "Luxury Sunset Hillside Villa")
            ptype_in = st.selectbox(
                "Property Type",
                [
                    "Luxury Villa",
                    "Hill Station Chalet",
                    "Single Family Home",
                    "Luxury Penthouse",
                    "Modern Farmhouse",
                    "Lakefront Cabin",
                    "Heritage Estate",
                    "Eco Smart Home",
                    "Orchard Estate",
                    "Townhouse",
                    "Apartment",
                ],
            )
            curr_in = st.selectbox("Currency", ["USD", "INR"], index=1 if global_is_inr else 0)

        with col2:
            loc_in = st.text_input("Full Address / Location", "Shimla Hills, HP, India" if curr_in == "INR" else "Austin, TX, USA")
            city_in = st.text_input("City / District", "Shimla" if curr_in == "INR" else "Austin")
            sqft_in = st.number_input("Living Floor Area (Sq Ft)", 300, 25000, 2800, step=50)

        with col3:
            beds_in = st.slider("Bedrooms (BHK)", 1, 10, 4)
            baths_in = st.slider("Bathrooms", 1.0, 8.0, 3.5, step=0.5)
            cars_in = st.slider("Garage / Parking Spaces", 0, 6, 2)

        col4, col5 = st.columns(2)
        with col4:
            year_in = st.number_input("Year Built", 1880, datetime.now().year, 2022, step=1)
            cond_in = st.slider("Construction & Finish Quality (1-10)", 1, 10, 8)
        with col5:
            photo_choice = st.selectbox("Select Featured Image", list(CURATED_PHOTOS.keys()) + ["Custom Image URL"])
            if photo_choice == "Custom Image URL":
                img_url_in = st.text_input("Custom Image URL", CURATED_PHOTOS["Modern Glass Villa"])
            else:
                img_url_in = CURATED_PHOTOS[photo_choice]

            # Image Preview
            if img_url_in:
                st.image(img_url_in, caption="Listing Image Preview", use_container_width=True)

        st.markdown("#### 🌟 Amenities & Features")
        amenity_options = [
            "Swimming Pool",
            "Mountain View",
            "Smart Home Automation",
            "Solar Power / Net Zero",
            "EV Charger Ready",
            "Private Garden / Lawn",
            "Fireplace",
            "Wine Cellar",
            "Rooftop Terrace",
            "24/7 Gated Security",
            "Chef's Kitchen",
            "Home Theater",
        ]
        selected_amenities = st.multiselect(
            "Select Property Amenities",
            options=amenity_options,
            default=["Mountain View", "Private Garden / Lawn", "Smart Home Automation"] if curr_in == "INR" else ["Swimming Pool", "EV Charger Ready", "Smart Home Automation"],
        )

        st.markdown("---")
        st.markdown("#### 🤖 AI-Powered Price Estimator")
        st.caption("Let our trained machine learning pipeline analyze your property specifications to recommend an optimal asking price.")

        # AI Valuation Calculation on Demand
        if st.button("⚡ Calculate Recommended Price with AI"):
            prop_temp = {
                "currency": curr_in,
                "location": loc_in,
                "city_district": city_in,
                "area_sqft": sqft_in,
                "bedrooms": beds_in,
                "bathrooms": baths_in,
                "garage_cars": cars_in,
                "year_built": year_in,
                "condition_rating": cond_in,
                "amenities": ", ".join(selected_amenities),
            }
            suggested_val = compute_ai_fair_value(pipe, data_info, prop_temp)
            st.session_state["suggested_price"] = suggested_val
            st.success(f"🎯 AI Recommended Asking Price: {format_currency(suggested_val, curr_in)}")

        default_price_input = st.session_state.get(
            "suggested_price",
            18500000.0 if curr_in == "INR" else 850000.0,
        )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            asking_price = st.number_input(
                f"Your Final Asking Price ({curr_in})",
                min_value=1000.0,
                value=float(default_price_input),
                step=10000.0,
            )
        with col_p2:
            is_featured = st.checkbox("Feature this listing prominently on homepage (Top Spotlight)", value=True)

        st.markdown("#### 👤 Seller Details & Description")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            seller_name_in = st.text_input("Seller / Agency Name", "Prime Estate Partners")
            seller_contact_in = st.text_input("Seller Contact (Email or Phone)", "listings@primeestates.com")
        with col_s2:
            desc_in = st.text_area(
                "Property Description",
                "Spacious architecture boasting natural light, premium fittings, high rental potential, and serene surroundings.",
            )

        if st.button("🚀 Publish Property to Live Marketplace", use_container_width=True):
            if not title_in or not loc_in:
                st.error("Please provide property title and location.")
            else:
                saved = add_marketplace_property(
                    title=title_in,
                    property_type=ptype_in,
                    location=loc_in,
                    city_district=city_in,
                    price=float(asking_price),
                    currency=curr_in,
                    area_sqft=float(sqft_in),
                    bedrooms=int(beds_in),
                    bathrooms=float(baths_in),
                    garage_cars=int(cars_in),
                    year_built=int(year_in),
                    condition_rating=int(cond_in),
                    image_url=img_url_in,
                    amenities=", ".join(selected_amenities),
                    seller_name=seller_name_in,
                    seller_contact=seller_contact_in,
                    status="Available",
                    description=desc_in,
                    featured=1 if is_featured else 0,
                )
                if saved:
                    st.success(f"🎉 Congratulations! '{title_in}' has been published to the Marketplace!")
                    st.balloons()

    # SUB-TAB 2: Manage My Listings & Offers
    with sub_sell2:
        render_my_listings_and_offers()


def render_my_listings_and_offers():
    """Renders the seller dashboard to manage listings and inspect incoming buyer offers."""
    st.markdown("#### 📋 Active Marketplace Inventory")
    all_props = get_marketplace_properties()

    if not all_props.empty:
        display_df = all_props[["id", "title", "property_type", "location", "price", "currency", "bedrooms", "bathrooms", "status", "seller_name"]].copy()
        st.dataframe(display_df, use_container_width=True, height=260)

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            prop_id_action = st.number_input("Select Listing ID", min_value=1, step=1, key="prop_act_id")
        with col_m2:
            new_status = st.selectbox("Update Status", ["Available", "Under Offer", "Sold"], key="prop_stat_select")
            if st.button("Update Status"):
                if update_property_status(int(prop_id_action), new_status):
                    st.success(f"Listing #{prop_id_action} marked as {new_status}!")
                    st.rerun()
        with col_m3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Listing"):
                if delete_marketplace_property(int(prop_id_action)):
                    st.success(f"Listing #{prop_id_action} deleted!")
                    st.rerun()

    st.markdown("---")
    st.markdown("#### 📬 Incoming Buyer Offers, Purchase Orders & Tour Requests")
    inquiries_df = get_property_inquiries()

    if not inquiries_df.empty:
        st.dataframe(inquiries_df, use_container_width=True, height=280)

        col_inq1, col_inq2 = st.columns([1, 2])
        with col_inq1:
            inq_id_del = st.number_input("Inquiry ID to Remove", min_value=1, step=1, key="inq_id_key")
            if st.button("Delete Inquiry Record"):
                if delete_property_inquiry(int(inq_id_del)):
                    st.success(f"Inquiry #{inq_id_del} removed!")
                    st.rerun()
    else:
        st.info("No incoming buyer offers or tour bookings recorded yet.")
