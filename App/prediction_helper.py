import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "Artifacts" / "model_data.joblib"

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
scaler = model_data["scaler"]
features = list(model_data["features"])


def prepare_input(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_deliquency,
    deliquency_ratio,
    credit_utilization_per_income,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type
):
    loan_to_income = loan_amount / income if income > 0 else 0.0

    input_data = {
        "deliquency_ratio": deliquency_ratio,
        "loan_to_income": loan_to_income,
        "avg_dpd_per_deliquency": avg_dpd_per_deliquency,
        "loan_tenure_months": loan_tenure_months,
        "credit_utilization_per_income": credit_utilization_per_income,
        "age": age,
        "number_of_open_accounts": num_open_accounts,
        "loan_purpose_Education": 1 if loan_purpose == "Education" else 0,
        "loan_purpose_Home": 1 if loan_purpose == "Home" else 0,
        "loan_purpose_Personal": 1 if loan_purpose == "Personal" else 0,
        "residence_type_Owned": 1 if residence_type == "Owned" else 0,
        "residence_type_Rented": 1 if residence_type == "Rented" else 0,
        "loan_type_Unsecured": 1 if loan_type == "Unsecured" else 0,
    }

    df = pd.DataFrame([input_data])

    # Make sure the columns are in exactly the same order as training
    df = df.reindex(columns=features, fill_value=0)

    # Scale the full 13-feature input, because the model was trained on that
    df[features] = scaler.transform(df[features])

    return df, loan_to_income


def predict(
    age,
    income,
    loan_amount,
    loan_tenure_months,
    avg_dpd_per_deliquency,
    deliquency_ratio,
    credit_utilization_per_income,
    num_open_accounts,
    residence_type,
    loan_purpose,
    loan_type
):
    input_df, loan_to_income = prepare_input(
        age,
        income,
        loan_amount,
        loan_tenure_months,
        avg_dpd_per_deliquency,
        deliquency_ratio,
        credit_utilization_per_income,
        num_open_accounts,
        residence_type,
        loan_purpose,
        loan_type
    )

    probability = float(model.predict_proba(input_df)[0][1])

    credit_score = int(round(300 + (1 - probability) * 600))
    credit_score = max(300, min(900, credit_score))

    if credit_score < 500:
        rating = "Poor"
    elif credit_score < 650:
        rating = "Average"
    elif credit_score < 750:
        rating = "Good"
    else:
        rating = "Excellent"

    return probability, credit_score, rating, loan_to_income