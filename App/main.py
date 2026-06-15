import streamlit as st

from prediction_helper import prepare_input, predict_credit_risk


st.set_page_config(
    page_title="Credit Risk Modelling",
    page_icon=":credit_card:",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f8fb;
        color: #111827;
    }
    .block-container {
        max-width: 1180px;
        padding-top: 48px;
    }
    .main-title {
        color: #111827;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .subtitle {
        color: #667085;
        font-size: 16px;
        margin-bottom: 28px;
    }
    .result-box {
        padding: 18px 20px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        margin-top: 18px;
        box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
    }
    [data-testid="stForm"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
    }
    [data-testid="InputInstructions"] {
        display: none;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        color: #111827;
    }
    label,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #111827;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Lauki Finance: Credit Risk Modelling</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Enter applicant and loan details to estimate default probability, credit score, and risk rating.</div>',
    unsafe_allow_html=True,
)

with st.form("credit_risk_form"):
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=28, step=1)
    with row1_col2:
        income = st.number_input(
            "Income",
            min_value=1.0,
            value=1200000.0,
            step=10000.0,
        )
    with row1_col3:
        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0.0,
            value=2560000.0,
            step=10000.0,
        )

    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        deliquency_ratio = st.number_input(
            "Delinquency Ratio",
            min_value=0.0,
            max_value=100.0,
            value=30.0,
            step=1.0,
        )
    with row2_col2:
        loan_tenure_months = st.number_input(
            "Loan Tenure (months)",
            min_value=1,
            max_value=360,
            value=36,
            step=1,
        )
    with row2_col3:
        loan_to_income = loan_amount / income if income > 0 else 0
        st.text_input(
            "Loan to Income Ratio",
            value=f"{loan_to_income:.2f}",
            disabled=True,
        )

    row3_col1, row3_col2, row3_col3 = st.columns(3)

    with row3_col1:
        residence_type = st.selectbox(
            "Residence Type",
            ["Rented", "Owned", "Mortgage"],
        )
    with row3_col2:
        credit_utilization_ratio = st.number_input(
            "Credit Utilization Ratio",
            min_value=0.0,
            max_value=100.0,
            value=30.0,
            step=1.0,
        )
    with row3_col3:
        avg_dpd_per_deliquency = st.number_input(
            "Avg DPD",
            min_value=0.0,
            max_value=365.0,
            value=20.0,
            step=1.0,
        )

    row4_col1, row4_col2, row4_col3 = st.columns(3)

    with row4_col1:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Education", "Home", "Auto", "Personal"],
        )
    with row4_col2:
        number_of_open_accounts = st.number_input(
            "Open Loan Accounts",
            min_value=0,
            max_value=50,
            value=2,
            step=1,
        )
    with row4_col3:
        loan_type = st.selectbox(
            "Loan Type",
            ["Unsecured", "Secured"],
        )

    submitted = st.form_submit_button("Calculate Risk")

if submitted:
    input_df = prepare_input(
        age=age,
        income=income,
        loan_amount=loan_amount,
        loan_tenure_months=loan_tenure_months,
        avg_dpd_per_deliquency=avg_dpd_per_deliquency,
        deliquency_ratio=deliquency_ratio,
        credit_utilization_ratio=credit_utilization_ratio,
        number_of_open_accounts=number_of_open_accounts,
        residence_type=residence_type,
        loan_purpose=loan_purpose,
        loan_type=loan_type,
    )

    default_probability, credit_score, rating = predict_credit_risk(input_df)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.metric("Default Probability", f"{default_probability * 100:.2f}%")
    st.metric("Credit Score", credit_score)
    st.metric("Rating", rating)

    if default_probability >= 0.70:
        st.error("High risk applicant. Credit approval is not recommended.")
    elif default_probability >= 0.40:
        st.warning("Medium risk applicant. Manual review is recommended.")
    else:
        st.success("Low risk applicant. Credit approval can be considered.")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("View model input data"):
        st.dataframe(input_df, use_container_width=True)
