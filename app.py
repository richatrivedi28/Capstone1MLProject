import streamlit as st
import pandas as pd
import pickle

# Load the trained XGBoost model
model_path = 'churn_xgb_optimal.pkl'
with open(model_path, 'rb') as f:
    xg_model = pickle.load(f)

# Function to create sample customer
# Model expects these features (matching `churn_xgb_optimal.pkl`):
# ['Dependents','tenure','OnlineSecurity','TechSupport','PaperlessBilling','MonthlyCharges','TotalCharges','InternetService_1','Contract_0','Contract_1','PaymentMethod_1','PaymentMethod_2']

def create_sample_customer(Dependents, tenure, OnlineSecurity, TechSupport, PaperlessBilling, MonthlyCharges, TotalCharges, InternetService, Contract, PaymentMethod):
    # Updated mappings to include 'No internet service' and remove 'PaymentMethod'
    # Create the feature values expected by the XGBoost model
    # Dependents: 1/0
    # tenure: int months
    # OnlineSecurity, TechSupport, PaperlessBilling: 1/0
    # MonthlyCharges, TotalCharges: numeric
    # InternetService_1: 1 if 'Fiber optic' else 0
    # Contract_0: 1 if 'One year' else 0
    # Contract_1: 1 if 'Two year' else 0
    # PaymentMethod_1: 1 if 'Mailed check' else 0
    # PaymentMethod_2: 1 if 'Electronic check' else 0

    internet_fiber = 1 if InternetService == 'Fiber optic' else 0
    contract_0 = 1 if Contract == 'One year' else 0
    contract_1 = 1 if Contract == 'Two year' else 0
    payment_1 = 1 if PaymentMethod == 'Mailed check' else 0
    payment_2 = 1 if PaymentMethod == 'Electronic check' else 0

    sample_data = [
        1 if Dependents else 0,
        int(tenure),
        1 if OnlineSecurity else 0,
        1 if TechSupport else 0,
        1 if PaperlessBilling else 0,
        float(MonthlyCharges),
        float(TotalCharges),
        internet_fiber,
        contract_0,
        contract_1,
        payment_1,
        payment_2,
    ]
    return sample_data

# Sample usage:
sample_customer = create_sample_customer(
    Dependents=0,
    tenure=10,
    OnlineSecurity=False,
    TechSupport=True,
    PaperlessBilling=True,
    MonthlyCharges=70,
    TotalCharges=700,
    InternetService='Fiber optic',
    Contract='Month-to-month',
    PaymentMethod='Electronic check'
)

# Convert to DataFrame using the model's expected column order
model_cols = ['Dependents','tenure','OnlineSecurity','TechSupport','PaperlessBilling','MonthlyCharges','TotalCharges','InternetService_1','Contract_0','Contract_1','PaymentMethod_1','PaymentMethod_2']
sample_customer_df = pd.DataFrame([sample_customer], columns=model_cols)

# Quick local check (optional): predict on the sample
try:
    churn_prediction = xg_model.predict(sample_customer_df)
    prediction_text = "will churn" if int(churn_prediction[0]) == 1 else "will not churn"
    print(f"The customer {prediction_text}.")
except Exception:
    # If model prediction fails here, we'll handle it in the Streamlit button
    churn_prediction = None

# Function to generate insights
def generate_insights(customer_features):
    insights = []
    # Example conditions for insights
    if customer_features[9] == 0:  # Assuming 1 is 'Fiber optic'
        insights.append("The customer may value cost-effective options over high-speed internet like fiber optic.")
    if customer_features[0] == 0:  # Assuming 0 is 'Month-to-month'
        insights.append("The customer prefers flexibility with month-to-month contracts rather than long-term commitments.")
    if customer_features[8] == 0:  # Assuming this is 'OnlineBackup'
        insights.append("The customer might not prioritize data security solutions like Online Backup services.")
    if customer_features[11] == 0:  # No Device Protection
        insights.append("The customer may not see device protection as a necessary value addition to their plan.")
    if customer_features[5] == 0:  # No Tech Support
        insights.append("The customer may rely on self-resolution methods instead of Tech Support services.")
    if customer_features[2] <= 12:  # Less than 1 year
        insights.append("The customer is relatively new and may still be exploring the service's value proposition.")
    if customer_features[1] > 75:  # High Monthly Charges
        insights.append("The customer incurs high monthly charges, which might impact their satisfaction level.")    
    
    return insights if insights else ["Customer Was Retained Amazing!!!!!"]

# Generate insights if the customer is predicted to churn
if churn_prediction[0] == 1:
    insights = generate_insights(sample_customer)
    print("Insights From Churned Customer:")
    for insights in insights:
        print(f"- {insights}")

# Streamlit UI
st.title("📡Telecom Customer Churn Prediction")

# Apply light-peach background to the Streamlit app
st.markdown(
    """
    <style>
    /* Page background and base text */
    .stApp, .reportview-container, .main {
        background-color: #FFDAB9;
        color: #333333;
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    /* Center the main content and add a soft card appearance */
    .main .block-container {
        background: rgba(255, 255, 255, 0.7);
        padding: 24px 28px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    /* Buttons */
    .stButton>button {
        background-color: #FFB6A0;
        color: #333333;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #ffa089;
    }

    /* Input controls: slightly rounded and subtle border */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
        padding: 8px !important;
    }

    /* Headings */
    .css-1d391kg h1, .stMarkdown h1 {
        color: #6b2b14;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Collect user inputs matching the model's expected features
Dependents = st.checkbox('Dependents')
tenure = st.number_input('Tenure (months)', min_value=0, value=12)
OnlineSecurity = st.checkbox('Online Security')
TechSupport = st.checkbox('Tech Support')
PaperlessBilling = st.checkbox('Paperless Billing')
MonthlyCharges = st.number_input('Monthly Charges', min_value=0.0, value=70.0)
TotalCharges = st.number_input('Total Charges', min_value=0.0, value=MonthlyCharges * tenure)
InternetService = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
Contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
PaymentMethod = st.selectbox('Payment Method', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

if st.button('Predict Churn'):
    row = create_sample_customer(
        Dependents=Dependents,
        tenure=tenure,
        OnlineSecurity=OnlineSecurity,
        TechSupport=TechSupport,
        PaperlessBilling=PaperlessBilling,
        MonthlyCharges=MonthlyCharges,
        TotalCharges=TotalCharges,
        InternetService=InternetService,
        Contract=Contract,
        PaymentMethod=PaymentMethod,
    )

    df = pd.DataFrame([row], columns=model_cols)

    try:
        pred = int(xg_model.predict(df)[0])
        prob = xg_model.predict_proba(df)[0][pred]
        prob_pct = round(float(prob) * 100, 2)
        if pred == 1:
            st.warning(f" ⚠️Prediction: Customer will churn — Confidence {prob_pct}%")
        else:
            st.success(f" ✅ 📌 Prediction: Customer will NOT churn — Confidence {prob_pct}%")

        if pred == 1:
            insights = generate_insights(row)
            st.write("**Actionable Insights to Reduce Churn Risk:**")
            for it in insights:
                st.write(f"- {it}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
