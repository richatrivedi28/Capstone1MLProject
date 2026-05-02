import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ===================== PAGE CONFIG & STYLING =====================
st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Color Scheme
PRIMARY_COLOR = "#1F77B4"        # Professional Blue
SECONDARY_COLOR = "#2CA02C"      # Professional Green (Retained)
DANGER_COLOR = "#D62728"         # Professional Red (Churn)
NEUTRAL_COLOR = "#7F7F7F"        # Gray
LIGHT_BG = "#F8F9FA"             # Light background
CARD_BG = "#FFFFFF"              # Card background
TEXT_PRIMARY = "#1A1A1A"         # Dark text
TEXT_SECONDARY = "#666666"       # Gray text

# Custom CSS for professional styling
st.markdown("""
    <style>
        :root {
            --primary-color: #1F77B4;
            --secondary-color: #2CA02C;
            --danger-color: #D62728;
        }
        
        body {
            background: linear-gradient(135deg, #0F1A2E 0%, #1a2a4e 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #0F1A2E 0%, #1a2a4e 100%);
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0F1A2E 0%, #1a2a4e 100%);
        }
        
        [data-testid="stHeader"] {
            background-color: transparent;
        }
        
        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1F77B4;
        }
        
        .risk-high {
            border-left-color: #D62728 !important;
        }
        
        .risk-low {
            border-left-color: #2CA02C !important;
        }
        
        h1 {
            color: #FFD700;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        h2 {
            color: #FFD700;
            font-weight: 600;
            margin-top: 20px;
        }
        
        .section-header {
            color: #FFD700;
            font-weight: 600;
            padding: 15px;
            background-color: #1a2a4e;
            border-radius: 5px;
            margin: 20px 0 15px 0;
        }
        
        .prediction-card {
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
        }
        
        .prediction-churn {
            background: linear-gradient(135deg, #FF6B6B, #D62728);
            color: white;
        }
        
        .prediction-retain {
            background: linear-gradient(135deg, #51CF66, #2CA02C);
            color: white;
        }
        
        .stMetric {
            background-color: #FFD700; /* Golden */
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #1F77B4;
        }
        
        /* Streamlit title styling */
        [class*="st-emotion-cache"] h1 {
            color: #FFD700 !important;
        }
        
        /* Checkbox and label styling - White */
        [data-testid="stCheckbox"] label {
            color: #FFFFFF !important;
            font-weight: 500;
        }
        
        [data-testid="stCheckbox"] span {
            color: #FFFFFF !important;
        }

        /* Radio labels - White */
        [data-testid="stRadio"] label {
            color: #FFFFFF !important;
            font-weight: 500;
        }
        [data-testid="stRadio"] span {
            color: #FFFFFF !important;
        }
        
        /* Input labels styling - White */
        label {
            color: #FFFFFF !important;
        }
        
        /* Selectbox labels - White */
        [data-testid="stSelectbox"] label {
            color: #FFFFFF !important;
        }
        
        /* Slider labels - White */
        [data-testid="stSlider"] label {
            color: #FFFFFF !important;
        }
        
        /* Number input labels - White */
        [data-testid="stNumberInput"] label {
            color: #FFFFFF !important;
        }
        
        /* Target all text and span elements for white color - EXCEPT selectbox */
        p:not([data-testid*="stSelectbox"]), 
        span:not([data-testid*="stSelectbox"]),
        div:not([data-testid*="stSelectbox"]),
        label:not([data-testid*="stSelectbox"]) {
            color: #FFFFFF !important;
        }
        
        /* Markdown text - White */
        [data-testid="stMarkdown"] {
            color: #FFFFFF !important;
        }
        
        [data-testid="stMarkdown"] * {
            color: #FFFFFF !important;
        }
        
        /* Checkbox wrapper text */
        [data-testid="stCheckbox"] {
            color: #FFFFFF !important;
        }
        
        [data-testid="stCheckbox"] * {
            color: #FFFFFF !important;
        }
        
        /* Selectbox options/values - Black */
        [data-testid="stSelectbox"] div, 
        [data-testid="stSelectbox"] button,
        [data-testid="stSelectbox"] span {
            color: #000000 !important;
        }
        
        /* Dropdown menu items - Black */
        [role="option"] {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }
        
        [role="listbox"] {
            color: #000000 !important;
        }
        
        /* Selectbox button text */
        [data-testid="stSelectbox"] button span {
            color: #000000 !important;
        }
        
        [data-testid="stSelectbox"] button p {
            color: #000000 !important;
        }
        
        /* Selectbox dropdown items */
        [data-testid="stSelectbox"] [role="option"] {
            color: #000000 !important;
        }
        
        /* All selectbox text */
        .st-emotion-cache-1e0h6sb, 
        .st-emotion-cache-1eoqy1a,
        [class*="st-emotion-cache"] [data-testid="stSelectbox"] span {
            color: #000000 !important;
        }
        
        /* Metric values - Black */
        [data-testid="metric-container"] {
            color: #000000 !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        
        [data-testid="stMetricValue"] * {
            color: #000000 !important;
        }
        
        /* Metric label - Black */
        [data-testid="stMetricLabel"] {
            color: #000000 !important;
        }
        
        /* Force all selectbox-related text to BLACK */
        [data-testid="stSelectbox"] {
            color: #000000 !important;
        }
        
        [data-testid="stSelectbox"] * {
            color: #000000 !important;
            background-color: white !important;
        }
        
        [data-testid="stSelectbox"] p,
        [data-testid="stSelectbox"] span,
        [data-testid="stSelectbox"] div {
            color: #000000 !important;
        }
        
        /* Force metrics to BLACK */
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] span {
            color: #000000 !important;
        }
        
        [data-testid="stMetricValue"] p,
        [data-testid="stMetricValue"] span {
            color: #000000 !important;
        }

        /* Aggressive overrides for dropdown menus (BaseWeb / Portal) */
        .baseweb-menu, .baseweb-list, .baseweb-list-item, .baseweb-dropdown, .menu {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        div[role="listbox"] {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        div[role="option"] {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        div[role="option"] *,
        div[role="listbox"] * {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        /* Aria attributes used by some menus */
        [aria-selected="true"], [aria-selected="false"] {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }

        /* Final catch-all for any element inside a dropdown overlay */
        [data-testid="stAppViewContainer"] div[style*="position: fixed"] * {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== LOAD MODEL =====================
@st.cache_resource
def load_model():
    with open('churn_xgb_optimal.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

# ===================== HELPER FUNCTIONS =====================
def create_customer_features(dependents, tenure, online_security, tech_support, 
                            paperless_billing, monthly_charges, total_charges, 
                            internet_service, contract, payment_method):
    """Convert UI inputs to model features"""
    internet_fiber = 1 if internet_service == 'Fiber optic' else 0
    contract_0 = 1 if contract == 'One year' else 0
    contract_1 = 1 if contract == 'Two year' else 0
    payment_1 = 1 if payment_method == 'Mailed check' else 0
    payment_2 = 1 if payment_method == 'Electronic check' else 0
    
    return [
        1 if dependents else 0,
        int(tenure),
        1 if online_security else 0,
        1 if tech_support else 0,
        1 if paperless_billing else 0,
        float(monthly_charges),
        float(total_charges),
        internet_fiber,
        contract_0,
        contract_1,
        payment_1,
        payment_2,
    ]

def generate_insights(features, churn_prob):
    """Generate actionable insights based on customer features"""
    dependents, tenure, online_security, tech_support, paperless_billing, \
        monthly_charges, total_charges, internet_fiber, contract_0, contract_1, \
        payment_1, payment_2 = features
    
    insights = []
    
    # Tenure-based insights
    if tenure < 6:
        insights.append({
            "type": "warning",
            "title": "New Customer",
            "description": "Customer is relatively new. Focus on onboarding and value demonstration."
        })
    elif tenure > 48:
        insights.append({
            "type": "success",
            "title": "Long-term Loyalty",
            "description": "Customer has been with you for 4+ years. Maintain strong relationship."
        })
    
    # Service adoption insights
    services_adopted = online_security + tech_support + paperless_billing
    if services_adopted == 0:
        insights.append({
            "type": "warning",
            "title": "Low Service Adoption",
            "description": "Customer hasn't adopted additional services. Consider cross-selling opportunities."
        })
    elif services_adopted == 3:
        insights.append({
            "type": "success",
            "title": "High Engagement",
            "description": "Customer is utilizing multiple services. Strong product affinity."
        })
    
    # Contract insights
    if contract_0 == 0 and contract_1 == 0:
        insights.append({
            "type": "warning",
            "title": "Month-to-Month Contract",
            "description": "Customer is on flexible contract. Higher churn risk. Consider incentives for longer commitment."
        })
    else:
        insights.append({
            "type": "success",
            "title": "Long-term Commitment",
            "description": "Customer is on annual contract. Lower churn probability."
        })
    
    # Charge insights
    if monthly_charges > 100:
        insights.append({
            "type": "warning",
            "title": "High Monthly Spend",
            "description": "Customer has high charges. Monitor satisfaction levels closely."
        })
    elif total_charges < 100 and tenure > 1:
        insights.append({
            "type": "info",
            "title": "Low Revenue Customer",
            "description": "Opportunity to upgrade customer to higher-value plans."
        })
    
    # Payment method insights
    if payment_2 == 1:
        insights.append({
            "type": "info",
            "title": "Electronic Check Payment",
            "description": "Customer uses electronic checks. Consider offering automatic payment incentives."
        })
    
    return insights

def get_risk_color(prob):
    """Return color based on churn probability"""
    if prob > 0.7:
        return DANGER_COLOR
    elif prob > 0.4:
        return "#FF9500"
    else:
        return SECONDARY_COLOR

def create_probability_gauge(prob):
    """Create a gauge chart for churn probability"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prob * 100,
        title={'text': "Churn Risk %"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': get_risk_color(prob)},
            'steps': [
                {'range': [0, 33], 'color': "#E8F5E9"},
                {'range': [33, 66], 'color': "#FFF3E0"},
                {'range': [66, 100], 'color': "#FFEBEE"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#F3F4F6",
        plot_bgcolor="#F3F4F6",
        font={'size': 12, 'family': 'Arial'}
    )
    return fig

# ===================== MAIN APP =====================

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊Telco Customer Churn Prediction")
    st.markdown("*Predict customer churn risk and generate actionable insights*")

with col2:
    st.write("")
    st.write("")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

st.markdown("---")

# Create two main columns
input_col, result_col = st.columns([1, 1], gap="large")

# ===================== INPUT SECTION =====================
with input_col:
    st.markdown('<div class="section-header">👤 Customer Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        dependents = st.checkbox("Has Dependents", value=False)
        online_security = st.checkbox("Online Security Service", value=False)
        paperless_billing = st.checkbox("Paperless Billing", value=False)
        
    with col2:
        tech_support = st.checkbox("Tech Support Service", value=False)
        st.write("")  # spacing
        st.write("")  # spacing
    
    st.markdown('<div class="section-header">💰 Service Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    # Legacy input toggle for old browsers (IE) - uses radio buttons instead of selectboxes
    legacy_input = st.checkbox("Legacy input mode (use radio buttons for dropdowns)", value=True, help="Enable for older browsers like Internet Explorer")

    with col1:
        tenure = st.slider(
            "Tenure (Months)",
            min_value=0,
            max_value=72,
            value=12,
            help="How long has the customer been with us?"
        )
        monthly_charges = st.number_input(
            "Monthly Charges ($)",
            min_value=0.0,
            max_value=200.0,
            value=70.0,
            step=0.5,
            help="Monthly subscription cost"
        )
    
    with col2:
        total_charges = st.number_input(
            "Total Charges ($)",
            min_value=0.0,
            max_value=10000.0,
            value=700.0,
            step=10.0,
            help="Total amount paid to date"
        )
        # Dropdown / Radio for Internet Service
        if legacy_input:
            internet_service = st.radio(
                "Internet Service",
                ["DSL", "Fiber optic", "No internet service"],
                index=0,
                help="Type of internet service"
            )
        else:
            internet_service = st.selectbox(
                "Internet Service",
                ["DSL", "Fiber optic", "No internet service"],
                help="Type of internet service"
            )
    
    st.markdown('<div class="section-header">📋 Contract & Payment</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if legacy_input:
            contract = st.radio(
                "Contract Type",
                ["Month-to-month", "One year", "Two year"],
                index=0,
                help="Customer contract length"
            )
        else:
            contract = st.selectbox(
                "Contract Type",
                ["Month-to-month", "One year", "Two year"],
                help="Customer contract length"
            )
    
    with col2:
        if legacy_input:
            payment_method = st.radio(
                "Payment Method",
                ["Bank transfer", "Credit card", "Mailed check", "Electronic check"],
                index=0,
                help="How customer pays their bill"
            )
        else:
            payment_method = st.selectbox(
                "Payment Method",
                ["Bank transfer", "Credit card", "Mailed check", "Electronic check"],
                help="How customer pays their bill"
            )
    
    # Predict button
    predict_button = st.button(
        "🔮 Predict Churn Risk",
        key="predict",
        use_container_width=True,
        type="primary"
    )

# ===================== PREDICTION SECTION =====================
with result_col:
    if predict_button:
        # Create features and predict
        features = create_customer_features(
            dependents, tenure, online_security, tech_support,
            paperless_billing, monthly_charges, total_charges,
            internet_service, contract, payment_method
        )
        
        # Extract feature values for later use
        # features order: [Dependents, tenure, OnlineSecurity, TechSupport, PaperlessBilling, 
        #                  MonthlyCharges, TotalCharges, internet_fiber, contract_0, contract_1, 
        #                  payment_1, payment_2]
        contract_0 = features[8]
        contract_1 = features[9]
        online_security_val = features[2]
        tech_support_val = features[3]
        paperless_billing_val = features[4]
        
        # Prepare dataframe
        cols = ['Dependents', 'tenure', 'OnlineSecurity', 'TechSupport', 
                'PaperlessBilling', 'MonthlyCharges', 'TotalCharges', 
                'InternetService_1', 'Contract_0', 'Contract_1', 
                'PaymentMethod_1', 'PaymentMethod_2']
        df = pd.DataFrame([features], columns=cols)
        
        # Get prediction and probability
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0]
        churn_prob = probability[1]  # Probability of churn class (1)
        
        # Display prediction result
        st.markdown('<div class="section-header">🎯 Prediction Result</div>', unsafe_allow_html=True)
        
        if prediction == 1:
            st.markdown(
                f'<div class="prediction-card prediction-churn">'
                f'⚠️ HIGH CHURN RISK<br>'
                f'<span style="font-size: 36px; font-weight: 700;">{churn_prob*100:.1f}%</span><br>'
                f'This customer is likely to churn'
                f'</div>',
                unsafe_allow_html=True
            )
            risk_level = "🔴 High Risk"
            risk_color = DANGER_COLOR
        else:
            st.markdown(
                f'<div class="prediction-card prediction-retain">'
                f'✅ LOW CHURN RISK<br>'
                f'<span style="font-size: 36px; font-weight: 700;">{(1-churn_prob)*100:.1f}%</span><br>'
                f'This customer is likely to stay'
                f'</div>',
                unsafe_allow_html=True
            )
            risk_level = "🟢 Low Risk"
            risk_color = SECONDARY_COLOR
        
        # Probability Gauge
        st.markdown('<div class="section-header">📈 Risk Gauge</div>', unsafe_allow_html=True)
        fig = create_probability_gauge(churn_prob)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key Metrics
        st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            st.metric(
                "Churn Probability",
                f"{churn_prob*100:.1f}%",
                delta=f"{abs(churn_prob - 0.5)*100:.1f}% from 50%"
            )
        
        with metric_cols[1]:
            st.metric(
                "Customer Tenure",
                f"{tenure} months",
                delta=f"{tenure//12} years"
            )
        
        with metric_cols[2]:
            st.metric(
                "Total Revenue",
                f"${total_charges:.2f}",
                delta=f"${monthly_charges*12:.2f}/year"
            )

# ===================== INSIGHTS & RECOMMENDATIONS SECTION =====================
if predict_button:
    st.markdown("---")
    st.markdown('<div class="section-header">💡 Insights & Recommendations</div>', unsafe_allow_html=True)
    
    insights = generate_insights(features, churn_prob)
    
    # Display insights in organized layout
    for insight in insights:
        if insight['type'] == 'success':
            col = st.columns([0.5, 9.5])[1]
            col.success(f"**✅ {insight['title']}**  \n{insight['description']}")
        elif insight['type'] == 'warning':
            col = st.columns([0.5, 9.5])[1]
            col.warning(f"**⚠️ {insight['title']}**  \n{insight['description']}")
        else:
            col = st.columns([0.5, 9.5])[1]
            col.info(f"**ℹ️ {insight['title']}**  \n{insight['description']}")
    
    # Actionable recommendations
    st.markdown('<div class="section-header">🎯 Recommended Actions</div>', unsafe_allow_html=True)
    
    recommendations = []
    
    if churn_prob > 0.7:
        recommendations.append("🚨 **Immediate Retention**: Contact customer urgently with retention offer")
        if contract_0 == 0 and contract_1 == 0:
            recommendations.append("💼 **Lock-in Strategy**: Offer incentive for upgrading to annual contract")
        if (online_security_val + tech_support_val + paperless_billing_val) < 2:
            recommendations.append("📦 **Bundle Offer**: Propose value-add services at discounted rate")
    elif churn_prob > 0.4:
        recommendations.append("⚠️ **Proactive Engagement**: Schedule satisfaction check-in call")
        recommendations.append("🎁 **Loyalty Program**: Offer exclusive perks or loyalty rewards")
    else:
        recommendations.append("✅ **Maintain Relationship**: Continue standard customer care")
        recommendations.append("📈 **Upsell Opportunity**: Consider premium service offerings")
    
    for idx, rec in enumerate(recommendations, 1):
        st.write(f"{idx}. {rec}")

# ===================== FOOTER =====================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("🔐 This prediction is based on XGBoost ML model trained on historical customer data")
