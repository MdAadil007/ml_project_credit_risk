import streamlit as st
import plotly.graph_objects as go
from prediction_helper import predict

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Credit Risk Modelling",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Custom Theme / CSS
# -----------------------------
st.markdown(
    """
    <style>
        /* App background */
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }

        /* Main container */
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        /* Hero */
        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #334155 100%);
            border-radius: 28px;
            padding: 34px 30px;
            color: white;
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.22);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 22px;
        }

        .hero h1 {
            margin: 0;
            font-size: 44px;
            font-weight: 900;
            letter-spacing: 0.5px;
            line-height: 1.05;
        }

        .hero p {
            margin: 10px 0 0 0;
            font-size: 18px;
            color: rgba(255,255,255,0.82);
        }

        .hero-badges {
            margin-top: 18px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .badge {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.14);
            font-size: 13px;
            font-weight: 600;
        }

        /* Section cards */
        .section-card {
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 24px;
            padding: 22px 22px 16px 22px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(10px);
        }

        .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
        }

        .section-subtitle {
            color: #64748b;
            margin-bottom: 18px;
            font-size: 14px;
        }

        /* Metric cards */
        .metric-card {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            padding: 16px 16px 14px 16px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
            min-height: 110px;
        }

        .metric-label {
            color: #64748b;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #0f172a;
            font-size: 30px;
            font-weight: 900;
            line-height: 1.1;
        }

        .metric-note {
            margin-top: 6px;
            color: #475569;
            font-size: 13px;
        }

        /* Risk banner */
        .risk-banner {
            border-radius: 22px;
            padding: 18px 20px;
            color: white;
            font-weight: 800;
            font-size: 18px;
            margin-top: 10px;
        }

        .risk-low {
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
        }

        .risk-medium {
            background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
        }

        .risk-high {
            background: linear-gradient(135deg, #b91c1c 0%, #ef4444 100%);
        }

        .hint-box {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 18px;
            padding: 14px 16px;
            color: #1e3a8a;
            font-size: 14px;
            margin-top: 10px;
        }

        /* Make inputs nicer */
        div[data-baseweb="input"], div[data-baseweb="select"] {
            border-radius: 14px !important;
        }

        /* Buttons */
        .stButton > button {
            width: 100%;
            border: none;
            border-radius: 14px;
            padding: 0.8rem 1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            color: white;
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(37, 99, 235, 0.3);
        }

        .footer-note {
            text-align: center;
            color: #64748b;
            margin-top: 18px;
            font-size: 13px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helper functions
# -----------------------------
def risk_label(probability: float) -> tuple[str, str, str]:
    """Return label, human-readable note, and CSS class for the risk band."""
    if probability >= 0.75:
        return "High Risk", "Careful review recommended.", "risk-high"
    elif probability >= 0.40:
        return "Medium Risk", "Proceed with caution.", "risk-medium"
    else:
        return "Low Risk", "Looks relatively safe.", "risk-low"


def gauge_chart(probability: float):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 42}},
            delta={"reference": 50, "increasing": {"color": "#ef4444"}, "decreasing": {"color": "#22c55e"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": "#2563eb"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#e2e8f0",
                "steps": [
                    {"range": [0, 35], "color": "#dcfce7"},
                    {"range": [35, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#fee2e2"},
                ],
                "threshold": {
                    "line": {"color": "#0f172a", "width": 4},
                    "thickness": 0.75,
                    "value": probability * 100,
                },
            },
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0f172a"),
    )
    return fig


def metric_card(label: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


# -----------------------------
# Hero Section
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>💳 Credit Risk Intelligence System</h1>
        <p>Predict whether a customer is likely to default on a loan with a clean, modern, business-friendly dashboard.</p>
        <div class="hero-badges">
            <span class="badge">Fast prediction</span>
            <span class="badge">Explainable output</span>
            <span class="badge">Fintech-style UI</span>
            <span class="badge">Portfolio ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Optional top KPIs
# -----------------------------
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Model Accuracy", "92%", "Replace with your real test score")
    with c2:
        metric_card("ROC AUC", "0.95", "Replace with your real AUC")
    with c3:
        metric_card("Recall", "88%", "Important for default detection")
    with c4:
        metric_card("Features Used", "12", "After preprocessing")

st.write("")

# -----------------------------
# Main Layout
# -----------------------------
left, right = st.columns([1.3, 1], gap="large")

with left:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_header(
        "Enter Customer Details",
        "Group related inputs carefully to make the form easier to scan.",
    )

    with st.form("credit_form"):
        # Customer profile
        st.markdown("### 👤 Customer Profile")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", min_value=18, max_value=70, value=28, step=1)
        with c2:
            income = st.number_input("Income", min_value=1.0, value=1200000.0, step=10000.0, format="%.2f")
        with c3:
            residence_type = st.selectbox("Residence Type", ["Owned", "Rented"])

        st.markdown("### 🏦 Loan Details")
        c4, c5, c6 = st.columns(3)
        with c4:
            loan_amount = st.number_input("Loan Amount", min_value=0.0, value=2560000.0, step=10000.0, format="%.2f")
        with c5:
            loan_tenure_months = st.number_input(
                "Loan Tenure (Months)", min_value=6, max_value=59, value=36, step=1
            )
        with c6:
            loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Personal"])

        st.markdown("### 📊 Credit Behaviour")
        c7, c8, c9 = st.columns(3)
        with c7:
            credit_utilization_ratio = st.number_input(
                "Credit Utilization Ratio",
                min_value=0.0,
                value=30.0,
                step=0.5,
                format="%.2f",
            )
        with c8:
            avg_dpd_per_deliquency = st.number_input(
                "Avg DPD Per Delinquency",
                min_value=0.0,
                max_value=100.0,
                value=8.0,
                step=0.5,
                format="%.2f",
            )
        with c9:
            deliquency_ratio = st.number_input(
                "Delinquency Ratio (%)",
                min_value=0.0,
                max_value=100.0,
                value=40.0,
                step=0.5,
                format="%.2f",
            )

        c10, c11, c12 = st.columns(3)
        with c10:
            number_of_open_accounts = st.number_input(
                "Open Loan Accounts", min_value=1, max_value=20, value=2, step=1
            )
        with c11:
            loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])
        with c12:
            loan_to_income_preview = loan_amount / income if income > 0 else 0
            st.number_input(
                "Loan To Income Ratio",
                value=float(loan_to_income_preview),
                disabled=True,
                format="%.2f",
            )

        submitted = st.form_submit_button("Calculate Risk")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    section_header(
        "Prediction Dashboard",
        "Results will appear here after you click the button.",
    )

    if submitted:
        probability, credit_score, rating, loan_to_income = predict(
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
        )

        label, note, risk_css = risk_label(probability)

        st.markdown(
            f"""
            <div class="risk-banner {risk_css}">
                {label} — {note}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(gauge_chart(probability), use_container_width=True)

        r1, r2 = st.columns(2)
        with r1:
            metric_card("Default Probability", f"{probability:.2%}", "Higher means more likely to default")
        with r2:
            metric_card("Credit Score", str(credit_score), f"Rating: {rating}")

        r3, r4 = st.columns(2)
        with r3:
            metric_card("Loan To Income", f"{loan_to_income:.2f}", "Lower is usually safer")
        with r4:
            metric_card("Decision", "Review" if probability >= 0.5 else "Approve", "Basic rule-based output")

        st.markdown(
            f"""
            <div class="hint-box">
                <strong>Interpretation:</strong> The model sees this customer as <strong>{label.lower()}</strong>.
                Use this score alongside business rules, bureau checks, and manual review.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Recommendation")
        if probability >= 0.75:
            st.error("⚠️ High risk customer. Manual review strongly recommended.")
        elif probability >= 0.40:
            st.warning("🟠 Medium risk customer. Review additional documents and repayment capacity.")
        else:
            st.success("✅ Low risk customer. Looks relatively safe based on the model output.")

        with st.expander("Model insights"):
            st.write("Use this section for feature importance, SHAP plots, or a short model summary.")
            st.write("Suggested items:")
            st.write("• Top 5 contributing features")
            st.write("• SHAP waterfall plot")
            st.write("• Training metrics and data summary")
    else:
        st.info("Fill in the form and click **Calculate Risk** to see the dashboard output.")
        st.markdown(
            """
            <div class="hint-box">
                Tip: To make this even better, add a SHAP feature-importance section and a small loan approval policy box.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer-note'>Built with Streamlit • Clean UI • Fintech-style dashboard</div>",
    unsafe_allow_html=True,
)
