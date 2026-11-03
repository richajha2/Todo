import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Multi-Disease Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e03e3e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("# 🩺 Health Portal")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio(
    "Select Prediction Model",
    ["🏠 Home Overview", "❤️ Heart Disease Prediction", "🎗️ Breast Cancer Prediction", "🧠 Student Mental Health"]
)

st.sidebar.markdown("---")
st.sidebar.info("Powered by Scikit-Learn Random Forest Models & Streamlit.")

# ==========================================
# 1. HOME OVERVIEW PAGE
# ==========================================
if app_mode == "🏠 Home Overview":
    st.title("Welcome to the Multi-Disease Prediction System 🌟")
    st.write("An advanced clinical and wellness decision-support web application powered by Machine Learning.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ❤️ Heart Health\nAssess cardiovascular risks based on clinical parameters.")
    with col2:
        st.markdown("### 🎗️ Oncology Check\nEvaluate diagnostic tumor features for breast cancer classification.")
    with col3:
        st.markdown("### 🧠 Mental Wellbeing\nAnalyze student survey indicators to gauge mental health risk.")
    
    st.markdown("---")
    st.markdown("👉 **Choose a model from the left sidebar to start predicting.**")

# ==========================================
# 2. HEART DISEASE PREDICTION
# ==========================================
elif app_mode == "❤️ Heart Disease Prediction":
    st.title("❤️ Heart Disease Risk Assessment")
    st.write("Please provide the patient's clinical attributes below:")

    try:
        model = pickle.load(open('heart.model.pkl', 'rb'))
        scaler = pickle.load(open('heart.scaler.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model files (`heart.model.pkl` or `heart.scaler.pkl`) not found in directory!")
        model = None

    with st.form("heart_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age (Years)", 20, 100, 50)
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
        with col2:
            chol = st.number_input("Serum Cholesterol (mg/dl)", 100, 600, 240)
            thalach = st.number_input("Max Heart Rate Achieved", 60, 220, 150)
        with col3:
            oldpeak = st.number_input("ST Depression (Oldpeak)", 0.0, 10.0, 1.0)
            
        submit_heart = st.form_submit_button("Predict Heart Risk")
        
        if submit_heart and model is not None:
            try:
                # Create input array matching scaler features expected shape
                n_features = scaler.n_features_in_
                input_data = np.zeros((1, n_features))
                
                # Assign values to available slots (mapping primary features safely)
                input_data[0, 0] = age
                if n_features > 1: input_data[0, 1] = trestbps
                if n_features > 2: input_data[0, 2] = chol
                if n_features > 3: input_data[0, 3] = thalach
                if n_features > 4: input_data[0, 4] = oldpeak

                scaled_data = scaler.transform(input_data)
                prediction = model.predict(scaled_data)

                st.markdown("---")
                if prediction[0] == 1:
                    st.error("⚠️ **Result: High Risk of Heart Disease.** Please consult a cardiologist.")
                else:
                    st.success("✅ **Result: Low Risk of Heart Disease.** Keep up a healthy lifestyle!")
            except Exception as e:
                st.error(f"Prediction Error: {e}")

# ==========================================
# 3. BREAST CANCER PREDICTION
# ==========================================
elif app_mode == "🎗️ Breast Cancer Prediction":
    st.title("🎗️ Breast Cancer Diagnosis Classifier")
    st.write("Enter the cell nuclei characteristic metrics below:")

    try:
        model = pickle.load(open('breast.model.pkl', 'rb'))
        scaler = pickle.load(open('breast.scaler.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model files (`breast.model.pkl` or `breast.scaler.pkl`) not found in directory!")
        model = None

    with st.form("breast_form"):
        col1, col2 = st.columns(2)
        with col1:
            mean_radius = st.number_input("Mean Radius", 0.0, 30.0, 14.0)
            mean_texture = st.number_input("Mean Texture", 0.0, 40.0, 19.0)
            mean_perimeter = st.number_input("Mean Perimeter", 0.0, 200.0, 90.0)
        with col2:
            mean_area = st.number_input("Mean Area", 0.0, 2500.0, 650.0)
            mean_smoothness = st.number_input("Mean Smoothness", 0.0, 0.2, 0.1)

        submit_breast = st.form_submit_button("Predict Diagnosis")
        
        if submit_breast and model is not None:
            try:
                n_features = scaler.n_features_in_
                input_data = np.zeros((1, n_features))
                
                input_data[0, 0] = mean_radius
                if n_features > 1: input_data[0, 1] = mean_texture
                if n_features > 2: input_data[0, 2] = mean_perimeter
                if n_features > 3: input_data[0, 3] = mean_area
                if n_features > 4: input_data[0, 4] = mean_smoothness

                scaled_data = scaler.transform(input_data)
                prediction = model.predict(scaled_data)

                st.markdown("---")
                if prediction[0] == 1:
                    st.error("⚠️ **Result: Malignant (Cancerous) Tumor Detected.** Immediate medical evaluation recommended.")
                else:
                    st.success("✅ **Result: Benign (Non-Cancerous) Tumor.**")
            except Exception as e:
                st.error(f"Prediction Error: {e}")

# ==========================================
# 4. STUDENT MENTAL HEALTH PREDICTION
# ==========================================
elif app_mode == "🧠 Student Mental Health":
    st.title("🧠 Student Depression & Mental Health Evaluation")
    st.write("Fill in the academic and lifestyle indicators below:")

    try:
        model = pickle.load(open('mental.model.pkl', 'rb'))
        scaler = pickle.load(open('mental.scaler.pkl', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model files (`mental.model.pkl` or `mental.scaler.pkl`) not found in directory!")
        model = None

    with st.form("mental_form"):
        col1, col2 = st.columns(2)
        with col1:
            cgpa = st.number_input("CGPA / Academic Score", 0.0, 10.0, 7.5)
            age_student = st.number_input("Student Age", 15, 40, 20)
        with col2:
            study_satisfaction = st.slider("Study Satisfaction Level (1-5)", 1, 5, 3)
            financial_stress = st.slider("Financial Stress Level (1-5)", 1, 5, 2)

        submit_mental = st.form_submit_button("Evaluate Mental Health Risk")
        
        if submit_mental and model is not None:
            try:
                n_features = scaler.n_features_in_
                input_data = np.zeros((1, n_features))
                
                input_data[0, 0] = cgpa
                if n_features > 1: input_data[0, 1] = age_student
                if n_features > 2: input_data[0, 2] = study_satisfaction
                if n_features > 3: input_data[0, 3] = financial_stress

                scaled_data = scaler.transform(input_data)
                prediction = model.predict(scaled_data)

                st.markdown("---")
                if prediction[0] == 1:
                    st.warning("⚠️ **Result: High Risk of Depression / Mental Health Stress.** Consider counseling support.")
                else:
                    st.success("✅ **Result: Low Risk / Stable Mental Wellbeing.**")
            except Exception as e:
                st.error(f"Prediction Error: {e}")