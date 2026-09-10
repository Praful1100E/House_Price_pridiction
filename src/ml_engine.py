"""
Machine Learning Engine for House Price Prediction.
Provides end-to-end preprocessing, multi-model training (Random Forest, Gradient Boosting,
Ridge, Lasso, Linear Regression), evaluation metrics, feature importance extraction,
batch inference, and regional valuation multipliers.
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DEFAULT_MODEL_FILE = MODELS_DIR / "house_price_model.joblib"
DEFAULT_META_FILE = MODELS_DIR / "data_info.json"

# Regional market multipliers for Himachal Pradesh & Hill stations
HP_MARKET_DATA = {
    "districts": [
        "Shimla",
        "Manali",
        "Kasauli",
        "Dharamshala",
        "Kullu",
        "Solan",
        "Mandi",
        "Kangra",
    ],
    "district_multipliers": {
        "Kasauli": 1.28,
        "Manali": 1.25,
        "Shimla": 1.20,
        "Solan": 1.12,
        "Kullu": 1.10,
        "Dharamshala": 1.08,
        "Kangra": 1.05,
        "Mandi": 0.98,
    },
    "view_multipliers": {
        "Valley View": 1.18,
        "Snow Mountain View": 1.22,
        "Forest View": 1.10,
        "City/Road View": 1.00,
        "Standard": 0.95,
    },
    "inr_rate_factor": 83.0,  # USD to INR conversion rate
}


def build_pipeline(
    numeric_features: List[str],
    categorical_features: List[str],
    model_instance: Any,
) -> Pipeline:
    """Builds a Scikit-Learn Pipeline with numeric/categorical preprocessing."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model_instance)])


def get_available_models(random_state: int = 42) -> Dict[str, Any]:
    """Returns a dictionary of supported regression models."""
    return {
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=120, max_depth=16, random_state=random_state, n_jobs=-1
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=120,
            learning_rate=0.08,
            max_depth=5,
            random_state=random_state,
        ),
        "Ridge Regression": Ridge(alpha=10.0, random_state=random_state),
        "Lasso Regression": Lasso(
            alpha=15.0, max_iter=2000, random_state=random_state
        ),
        "Linear Regression": LinearRegression(),
    }


def train_single_model(
    df: pd.DataFrame,
    target_col: str = "SalePrice",
    model_name: str = "Random Forest Regressor",
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[Optional[Pipeline], Dict[str, float], Dict[str, Any]]:
    """Trains a specific model and evaluates performance metrics."""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")

    y = df[target_col]
    X = df.drop(columns=[target_col])
    if "Id" in X.columns:
        X = X.drop(columns=["Id"])

    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    models = get_available_models(random_state)
    model_instance = models.get(model_name, models["Random Forest Regressor"])

    pipeline = build_pipeline(num_cols, cat_cols, model_instance)
    pipeline.fit(X_train, y_train)

    # Predictions
    test_preds = pipeline.predict(X_test)
    train_preds = pipeline.predict(X_train)

    metrics = {
        "R2_Score": float(r2_score(y_test, test_preds)),
        "Train_R2": float(r2_score(y_train, train_preds)),
        "MAE": float(mean_absolute_error(y_test, test_preds)),
        "RMSE": float(np.sqrt(mean_squared_error(y_test, test_preds))),
        "MAPE": float(mean_absolute_percentage_error(y_test, test_preds) * 100),
    }

    data_info = {
        "features": X.columns.tolist(),
        "num_feats": num_cols,
        "cat_feats": cat_cols,
        "target_col": target_col,
        "model_name": model_name,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rmse": metrics["RMSE"],
    }

    return pipeline, metrics, data_info


def benchmark_all_models(
    df: pd.DataFrame,
    target_col: str = "SalePrice",
    test_size: float = 0.2,
    random_state: int = 42,
) -> pd.DataFrame:
    """Trains all available models and returns a performance benchmark table."""
    results = []
    models = get_available_models(random_state)

    for name in models.keys():
        try:
            _, metrics, _ = train_single_model(
                df,
                target_col=target_col,
                model_name=name,
                test_size=test_size,
                random_state=random_state,
            )
            results.append(
                {
                    "Model": name,
                    "R² (Test)": round(metrics["R2_Score"], 4),
                    "R² (Train)": round(metrics["Train_R2"], 4),
                    "MAE ($)": f"${metrics['MAE']:,.0f}",
                    "RMSE ($)": f"${metrics['RMSE']:,.0f}",
                    "MAPE (%)": f"{metrics['MAPE']:.2f}%",
                    "_r2_raw": metrics["R2_Score"],
                }
            )
        except Exception as e:
            results.append({"Model": name, "Error": str(e), "_r2_raw": -999})

    res_df = pd.DataFrame(results)
    if "_r2_raw" in res_df.columns:
        res_df = res_df.sort_values(by="_r2_raw", ascending=False).drop(
            columns=["_r2_raw"]
        )
    return res_df


def extract_feature_importances(
    pipeline: Pipeline, data_info: Dict[str, Any], top_n: int = 15
) -> pd.DataFrame:
    """Extracts and formats top feature importances or coefficients."""
    if not pipeline or not data_info:
        return pd.DataFrame()

    try:
        model = pipeline.named_steps["model"]
        preprocessor = pipeline.named_steps["preprocessor"]

        cat_transformer = preprocessor.named_transformers_["cat"]
        ohe = cat_transformer.named_steps["onehot"]
        ohe_cols = ohe.get_feature_names_out(data_info["cat_feats"]).tolist()

        all_feature_names = data_info["num_feats"] + ohe_cols

        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            df_imp = pd.DataFrame(
                {"Feature": all_feature_names, "Importance": importances}
            )
            return (
                df_imp.sort_values(by="Importance", ascending=False)
                .head(top_n)
                .reset_index(drop=True)
            )

        elif hasattr(model, "coef_"):
            coefs = np.abs(model.coef_)
            df_imp = pd.DataFrame(
                {"Feature": all_feature_names, "Importance": coefs}
            )
            return (
                df_imp.sort_values(by="Importance", ascending=False)
                .head(top_n)
                .reset_index(drop=True)
            )
    except Exception:
        pass
    return pd.DataFrame()


def predict_single_property(
    pipeline: Pipeline,
    data_info: Dict[str, Any],
    input_features: Dict[str, Any],
    is_regional_hp: bool = False,
    district: str = "Shimla",
    view_type: str = "Standard",
) -> Dict[str, Any]:
    """Generates property valuation with confidence intervals and regional multipliers."""
    model_features = data_info["features"]
    row_dict = {feat: None for feat in model_features}

    # Populate mapped user inputs
    for k, v in input_features.items():
        if k in row_dict:
            row_dict[k] = v

    # Fill unprovided columns with defaults
    for feat in model_features:
        if row_dict[feat] is None:
            if feat in data_info.get("num_feats", []):
                row_dict[feat] = 0
            else:
                row_dict[feat] = "None"

    df_input = pd.DataFrame([row_dict])
    base_pred = float(pipeline.predict(df_input)[0])

    # Error margin calculation (approx 8-10% or from RMSE)
    error_pct = 0.08
    low_base = base_pred * (1 - error_pct)
    high_base = base_pred * (1 + error_pct)

    if is_regional_hp:
        dist_mult = HP_MARKET_DATA["district_multipliers"].get(district, 1.0)
        view_mult = HP_MARKET_DATA["view_multipliers"].get(view_type, 1.0)
        total_mult = dist_mult * view_mult

        # Scaled to INR
        inr_factor = HP_MARKET_DATA["inr_rate_factor"] * 0.7  # Calibrated for Indian hill stations
        inr_val = base_pred * total_mult * inr_factor
        inr_low = low_base * total_mult * inr_factor
        inr_high = high_base * total_mult * inr_factor

        return {
            "currency": "INR",
            "predicted_price": inr_val,
            "low_bound": inr_low,
            "high_bound": inr_high,
            "base_usd": base_pred,
            "district_multiplier": dist_mult,
            "view_multiplier": view_mult,
            "formatted_price": format_currency(inr_val, "INR"),
            "formatted_range": f"{format_currency(inr_low, 'INR')} - {format_currency(inr_high, 'INR')}",
        }
    else:
        return {
            "currency": "USD",
            "predicted_price": base_pred,
            "low_bound": low_base,
            "high_bound": high_base,
            "formatted_price": format_currency(base_pred, "USD"),
            "formatted_range": f"{format_currency(low_base, 'USD')} - {format_currency(high_base, 'USD')}",
        }


def format_currency(value: float, currency: str = "USD") -> str:
    """Formats numeric values into intuitive currency strings (USD $ or INR ₹ Lakhs/Crores)."""
    if currency == "USD":
        return f"${value:,.0f}"
    else:
        # Indian Numbering System formatting (Lakhs & Crores)
        if value >= 10000000:
            cr = value / 10000000
            return f"₹ {cr:.2f} Cr"
        elif value >= 100000:
            lakh = value / 100000
            return f"₹ {lakh:.2f} Lakh"
        else:
            return f"₹ {value:,.0f}"


def run_batch_inference(
    pipeline: Pipeline, data_info: Dict[str, Any], batch_df: pd.DataFrame
) -> pd.DataFrame:
    """Runs batch predictions on uploaded dataframe and returns annotated DataFrame."""
    model_features = data_info["features"]
    df_aligned = pd.DataFrame(index=batch_df.index)

    for feat in model_features:
        if feat in batch_df.columns:
            df_aligned[feat] = batch_df[feat]
        else:
            if feat in data_info.get("num_feats", []):
                df_aligned[feat] = 0
            else:
                df_aligned[feat] = "None"

    predictions = pipeline.predict(df_aligned)
    result_df = batch_df.copy()
    result_df["Predicted_Price_USD"] = np.round(predictions, 2)
    result_df["Predicted_Price_INR"] = np.round(
        predictions * HP_MARKET_DATA["inr_rate_factor"], 2
    )
    result_df["Valuation_Low"] = np.round(predictions * 0.92, 2)
    result_df["Valuation_High"] = np.round(predictions * 1.08, 2)

    return result_df


def save_trained_pipeline(
    pipeline: Pipeline,
    data_info: Dict[str, Any],
    filepath: Path = DEFAULT_MODEL_FILE,
    meta_filepath: Path = DEFAULT_META_FILE,
) -> bool:
    """Serializes pipeline and metadata to disk."""
    try:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, filepath)
        with open(meta_filepath, "w") as f:
            json.dump(data_info, f, indent=2)
        return True
    except Exception:
        return False


def load_trained_pipeline(
    filepath: Path = DEFAULT_MODEL_FILE,
    meta_filepath: Path = DEFAULT_META_FILE,
) -> Tuple[Optional[Pipeline], Optional[Dict[str, Any]]]:
    """Loads serialized pipeline and metadata from disk."""
    if not filepath.exists() or not meta_filepath.exists():
        return None, None
    try:
        pipeline = joblib.load(filepath)
        with open(meta_filepath, "r") as f:
            data_info = json.load(f)
        return pipeline, data_info
    except Exception:
        return None, None
