from pathlib import Path

import joblib
import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "deliquency_ratio",
    "loan_to_income",
    "avg_dpd_per_deliquency",
    "loan_tenure_months",
    "credit_utilization_per_income",
    "age",
    "number_of_open_accounts",
    "loan_purpose_Education",
    "loan_purpose_Home",
    "loan_purpose_Personal",
    "residence_type_Owned",
    "residence_type_Rented",
    "loan_type_Unsecured",
]


def load_model_data():
    current_dir = Path(__file__).resolve().parent
    model_path = current_dir.parent / "Artifacts" / "model_data.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    model_data = joblib.load(model_path)

    if not isinstance(model_data, dict):
        return {"model": model_data, "scaler": None, "features": FEATURE_COLUMNS}

    model = (
        model_data.get("model")
        or model_data.get("classifier")
        or model_data.get("clf")
        or model_data.get("best_model")
        or model_data.get("pipeline")
    )

    scaler = (
        model_data.get("scaler")
        or model_data.get("standard_scaler")
        or model_data.get("preprocessor")
    )

    features = (
        model_data.get("features")
        or model_data.get("feature_names")
        or model_data.get("columns")
        or FEATURE_COLUMNS
    )

    cols_to_scale = (
        model_data.get("cols_to_scale")
        or model_data.get("columns_to_scale")
        or model_data.get("numeric_columns")
        or []
    )

    if model is None:
        raise KeyError(
            "Could not find model inside model_data.joblib. "
            "Open your notebook and check the dictionary keys. "
            "Expected one of: model, classifier, clf, best_model, pipeline."
        )

    return {
        "model": model,
        "scaler": scaler,
        "features": list(features),
        "cols_to_scale": list(cols_to_scale),
    }


MODEL_DATA = load_model_data()


def prepare_input(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_deliquency,
    deliquency_ratio,
    credit_utilization_ratio,
    number_of_open_accounts,
    residence_type,
    loan_purpose,
    loan_type,
):
    loan_to_income = loan_amount / income if income > 0 else 0

    input_data = {
        "deliquency_ratio": deliquency_ratio,
        "loan_to_income": loan_to_income,
        "avg_dpd_per_deliquency": avg_dpd_per_deliquency,
        "loan_tenure_months": loan_tenure_months,
        "credit_utilization_per_income": credit_utilization_ratio,
        "age": age,
        "number_of_open_accounts": number_of_open_accounts,
        "loan_purpose_Education": 1 if loan_purpose == "Education" else 0,
        "loan_purpose_Home": 1 if loan_purpose == "Home" else 0,
        "loan_purpose_Personal": 1 if loan_purpose == "Personal" else 0,
        "residence_type_Owned": 1 if residence_type == "Owned" else 0,
        "residence_type_Rented": 1 if residence_type == "Rented" else 0,
        "loan_type_Unsecured": 1 if loan_type == "Unsecured" else 0,
    }

    df = pd.DataFrame([input_data])

    for column in FEATURE_COLUMNS:
        if column not in df.columns:
            df[column] = 0

    return df[FEATURE_COLUMNS]


def predict_credit_risk(input_df):
    model = MODEL_DATA["model"]
    scaler = MODEL_DATA.get("scaler")

    prediction_df = input_df.copy()

    if scaler is not None:
        scaler_features = getattr(scaler, "feature_names_in_", FEATURE_COLUMNS)
        scaler_features = list(scaler_features)
        prediction_df = prediction_df[scaler_features]
        prediction_df = pd.DataFrame(
            scaler.transform(prediction_df),
            columns=scaler_features,
            index=input_df.index,
        )

    if hasattr(model, "predict_proba"):
        default_probability = model.predict_proba(prediction_df)[0][1]
    else:
        prediction = model.predict(prediction_df)[0]
        default_probability = float(prediction)

    default_probability = float(np.clip(default_probability, 0, 1))

    credit_score = int(300 + (1 - default_probability) * 600)

    if credit_score >= 750:
        rating = "Excellent"
    elif credit_score >= 650:
        rating = "Good"
    elif credit_score >= 550:
        rating = "Average"
    elif credit_score >= 450:
        rating = "Poor"
    else:
        rating = "Very Poor"

    return default_probability, credit_score, rating
