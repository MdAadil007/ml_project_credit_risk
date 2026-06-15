import streamlit as st
from prediction_helper import predict

st.set_page_config(
    page_title="Credit Risk Modelling",
    page_icon="💳",
    layout="wide"
)

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 0px;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }
        .result-box {
            padding: 18px;
            border-radius: 16px;
            background: #f8f9fb;
            border: 1px solid #e6e8ef;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">CREDIT RISK MODELLING</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Predict whether a customer is likely to default on a loan</div>',
    unsafe_allow_html=True
)

with st.form("credit_form"):
    st.subheader("Enter Customer Details")

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=18, max_value=100, value=28, step=1)
    with c2:
        income = st.number_input("Income", min_value=0.0, value=1200000.0, step=1000.0)
    with c3:
        loan_amount = st.number_input("Loan Amount", min_value=0.0, value=2560000.0, step=1000.0)

    c4, c5, c6 = st.columns(3)
    with c4:
        loan_tenure_months = st.number_input("Loan Tenure (months)", min_value=1, value=36, step=1)
    with c5:
        avg_dpd_per_deliquency = st.number_input("Avg DPD", min_value=0.0, value=20.0, step=1.0)
    with c6:
        deliquency_ratio = st.number_input("Delinquency Ratio", min_value=0.0, value=30.0, step=1.0)

    c7, c8, c9 = st.columns(3)
    with c7:
        credit_utilization_per_income = st.number_input("Credit Utilization Ratio", min_value=0.0, value=30.0, step=1.0)
    with c8:
        num_open_accounts = st.number_input("Open Loan Accounts", min_value=0, value=2, step=1)
    with c9:
        residence_type = st.selectbox("Residence Type", ["Owned", "Rented"])

    c10, c11, c12 = st.columns(3)
    with c10:
        loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Personal"])
    with c11:
        loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
    with c12:
        st.write("")
        st.write("")

    submit = st.form_submit_button("Calculate Risk")

if submit:
    if income <= 0:
        st.error("Income must be greater than 0.")
    else:
        probability, credit_score, rating, loan_to_income = predict(
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

        st.markdown("### Prediction Result")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Default Probability", f"{probability:.2%}")
        r2.metric("Credit Score", f"{credit_score}")
        r3.metric("Rating", rating)
        r4.metric("Loan to Income", f"{loan_to_income:.2f}")

        st.progress(min(max(probability, 0.0), 1.0))

        if probability >= 0.5:
            st.error("High Risk Customer")
        else:
            st.success("Low Risk Customer")

        st.markdown("### Input Used by the Model")
        st.write(f"Loan to Income = {loan_to_income:.4f}")
else:
    st.info("Fill the form and click **Calculate Risk**.")