import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from src.data_manager import (
    load_dataset,
    init_db,
    save_prediction_log,
    get_prediction_history,
    add_custom_property,
    get_custom_properties,
)
from src.ml_engine import (
    train_single_model,
    benchmark_all_models,
    predict_single_property,
    run_batch_inference,
    extract_feature_importances,
)
from src.analytics import (
    plot_feature_correlations,
    plot_feature_importance_chart,
    plot_missing_values,
    plot_price_by_neighborhood,
    plot_price_distribution,
    plot_price_vs_area,
)
from src.financials import (
    calculate_mortgage_emi,
    generate_amortization_schedule,
    calculate_investment_yield,
)
from src.data_manager import (
    get_marketplace_properties,
    get_marketplace_property_by_id,
    add_marketplace_property,
    update_property_status,
    delete_marketplace_property,
    submit_property_inquiry,
    get_property_inquiries,
    delete_property_inquiry,
)
from src.marketplace_ui import compute_ai_fair_value


def test_full_pipeline():
    print("1. Initializing DB...")
    init_db()

    print("2. Loading Dataset...")
    df = load_dataset("train.csv")
    assert df is not None and not df.empty, "Dataset load failed"
    print(f"   Loaded dataset with shape: {df.shape}")

    print("3. Testing ML Training...")
    pipe, metrics, info = train_single_model(df, target_col="SalePrice", model_name="Random Forest Regressor")
    assert pipe is not None, "Model pipeline training failed"
    print(f"   Trained RF model: R2={metrics['R2_Score']:.3f}, MAE=${metrics['MAE']:,.0f}")

    print("4. Testing Prediction (USD Standard)...")
    pred_usd = predict_single_property(
        pipe,
        info,
        {"GrLivArea": 1800, "OverallQual": 7, "YearBuilt": 2015, "FullBath": 2, "TotRmsAbvGrd": 6, "GarageCars": 2, "TotalBsmtSF": 1000},
        is_regional_hp=False,
    )
    print(f"   Standard Pred: {pred_usd['formatted_price']}, Range: {pred_usd['formatted_range']}")

    print("5. Testing Prediction (INR Himachal Pradesh)...")
    pred_inr = predict_single_property(
        pipe,
        info,
        {"GrLivArea": 2000, "OverallQual": 8, "YearBuilt": 2018, "FullBath": 2, "TotRmsAbvGrd": 5, "GarageCars": 1, "TotalBsmtSF": 800},
        is_regional_hp=True,
        district="Shimla",
        view_type="Snow Mountain View",
    )
    print(f"   Regional HP Pred: {pred_inr['formatted_price']}, Range: {pred_inr['formatted_range']}")

    print("6. Testing Database Logging...")
    saved = save_prediction_log(
        "Regional HP",
        "Shimla (Snow Mountain View)",
        2000,
        3,
        2,
        8,
        2018,
        "Random Forest",
        pred_inr["predicted_price"],
        "INR",
        pred_inr["low_bound"],
        pred_inr["high_bound"],
        "Test Villa",
    )
    assert saved, "Save prediction log failed"
    history = get_prediction_history(5)
    assert len(history) > 0, "History retrieval failed"
    print(f"   History entries count: {len(history)}")

    print("7. Testing Custom Properties DB...")
    prop_saved = add_custom_property("Shimla Pine Cottage", "Shimla, HP", 1600, 3, 2, 8500000, "INR", "For Sale", "Scenic view")
    assert prop_saved, "Add custom property failed"
    props = get_custom_properties()
    assert len(props) > 0, "Custom properties retrieval failed"
    print(f"   Custom properties count: {len(props)}")

    print("8. Testing Batch Inference on test.csv...")
    test_df = load_dataset("test.csv")
    if test_df is not None:
        batch_res = run_batch_inference(pipe, info, test_df.head(10))
        assert "Predicted_Price_USD" in batch_res.columns, "Batch inference failed"
        print(f"   Batch predicted 10 rows: Avg USD = ${batch_res['Predicted_Price_USD'].mean():,.0f}")

    print("9. Testing Analytics Charts...")
    c_dist = plot_price_distribution(df, "SalePrice")
    c_scatter = plot_price_vs_area(df, "SalePrice")
    c_neigh = plot_price_by_neighborhood(df, "SalePrice")
    c_corr = plot_feature_correlations(df, "SalePrice")
    c_miss = plot_missing_values(df)
    imp_df = extract_feature_importances(pipe, info, top_n=10)
    c_imp = plot_feature_importance_chart(imp_df)
    assert c_dist is not None and c_scatter is not None, "Altair charts generation failed"
    assert c_imp is not None, "Feature importance chart generation failed"
    # Validate Altair spec schema conversion without error
    _ = c_imp.to_dict()

    print("10. Testing Financials...")
    emi = calculate_mortgage_emi(350000, down_payment_pct=20, interest_rate_annual=7.5, loan_term_years=20)
    amort = generate_amortization_schedule(emi["principal"], 7.5, 20)
    yield_res = calculate_investment_yield(350000, 2000, 3500)
    print(f"   Monthly EMI: ${emi['monthly_emi']:,.0f}, Gross Yield: {yield_res['gross_yield']}%")

    print("11. Testing Marketplace Properties Seeding & Filters...")
    market_props = get_marketplace_properties()
    assert len(market_props) >= 10, f"Expected at least 10 seeded properties, found {len(market_props)}"
    print(f"   Marketplace properties loaded: {len(market_props)} listings")

    # Filter test
    usd_props = get_marketplace_properties(currency_filter="USD")
    inr_props = get_marketplace_properties(currency_filter="INR")
    assert len(usd_props) > 0 and len(inr_props) > 0, "Currency filters failed"
    print(f"   USD listings: {len(usd_props)}, INR listings: {len(inr_props)}")

    print("12. Testing Sell House (Add Listing)...")
    added_prop = add_marketplace_property(
        title="Modern Hillside Sanctuary",
        property_type="Luxury Villa",
        location="Manali, HP, India",
        city_district="Manali",
        price=21000000.0,
        currency="INR",
        area_sqft=3200.0,
        bedrooms=4,
        bathrooms=4.0,
        garage_cars=2,
        year_built=2023,
        condition_rating=9,
        amenities="Mountain View, Heated Floors, Private Garden",
        seller_name="Himachal Realty Co.",
        seller_contact="sales@himachalrealty.com",
    )
    assert added_prop, "Add marketplace property failed"
    searched = get_marketplace_properties(search_query="Modern Hillside Sanctuary")
    assert len(searched) > 0, "Failed to retrieve newly added listing"
    new_prop_id = int(searched.iloc[0]["id"])
    print(f"   Listing created successfully with ID: {new_prop_id}")

    print("13. Testing Buy Now / Purchase Order Submission...")
    inquiry_saved = submit_property_inquiry(
        property_id=new_prop_id,
        property_title="Modern Hillside Sanctuary",
        buyer_name="Rajesh Kumar",
        buyer_email="rajesh.kumar@example.com",
        buyer_phone="+91 9876543210",
        offer_amount=21000000.0,
        inquiry_type="Buy Now / Purchase Order",
        notes="Wire Escrow Transfer Selected",
    )
    assert inquiry_saved, "Buy inquiry failed"
    inquiries = get_property_inquiries(property_id=new_prop_id)
    assert len(inquiries) > 0, "Failed to retrieve inquiry"
    print(f"   Buy transaction logged: #{inquiries.iloc[0]['id']} ({inquiries.iloc[0]['inquiry_type']})")

    # Verify status changed to 'Under Offer'
    updated_prop = get_marketplace_property_by_id(new_prop_id)
    assert updated_prop["status"] == "Under Offer", "Property status not updated to Under Offer"
    print(f"   Property status transitioned to: {updated_prop['status']}")

    print("14. Testing AI Price Recommender for Marketplace...")
    sample_prop = {
        "currency": "INR",
        "location": "Shimla",
        "city_district": "Shimla",
        "area_sqft": 2500,
        "bedrooms": 3,
        "bathrooms": 3,
        "garage_cars": 2,
        "year_built": 2022,
        "condition_rating": 8,
        "amenities": "Snow Mountain View",
    }
    ai_val = compute_ai_fair_value(pipe, info, sample_prop)
    assert ai_val > 0, "AI Fair value computation failed"
    print(f"   AI Recommended Price: ₹{ai_val:,.0f}")

    print("15. Testing Property & Inquiry Cleanup...")
    del_inq = delete_property_inquiry(int(inquiries.iloc[0]["id"]))
    del_prop = delete_marketplace_property(new_prop_id)
    assert del_inq and del_prop, "Deletion cleanup failed"
    print("   Cleaned up test listing & inquiry.")

    print("\n🎉 ALL TESTS (INCLUDING BUY/SELL MARKETPLACE) PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_full_pipeline()

