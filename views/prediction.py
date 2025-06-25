import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import google.generativeai as genai
import database

if "authenticated" in st.session_state and st.session_state.authenticated:
# --- Load and preprocess dataset ---
    df = pd.read_csv("health_disease_dataset.csv", encoding="latin1")
    df['Sex'] = LabelEncoder().fit_transform(df['Sex'])
    df['Disease'] = df['Disease'].apply(lambda x: [d.strip() for d in x.split(',')])

    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(df['Disease'])
    X = df.drop(columns=['Disease'])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- Train the model ---
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    model = MultiOutputClassifier(rf)
    model.fit(X_scaled, y)
    st.markdown("<div class='headline'>What's Your Health Story?</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    feature_names = X.columns.tolist()
    input_data = []

    # Background image + general style
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');

        .stApp {{
            background: linear-gradient(to top, #002d6c, #002a69);
            font-size: 20px;
        }}

        .headline {{
            font-size: 90px;
            font-weight: bold;
            font-family: 'Special Gothic Expanded One', sans-serif;
            margin: 0;
        }}

        .subheadline {{
            font-size: 35px;
            font-family: 'Roboto Condensed', sans-serif;
            color: white;
            margin-bottom: 30px;
        }} 

        .custom-label {{
            font-size: 25px;
            color: white;
            font-style: "Roboto Condensed", sans-serif;
            font-style: italic;
            margin-bottom: 1rem;
        }}

    </style>
""", unsafe_allow_html=True)

        
# First, split features
    with col1:
        st.markdown('<h2 class="subheadline">Just provide your vital stats — we’ll do the rest and predict potential risks.</h2>', unsafe_allow_html=True)
        st.markdown("<div class='custom-label'>This app provides health predictions based on entered values. It is not a substitute for professional medical advice. Always consult a healthcare provider for a diagnosis.</div>", unsafe_allow_html=True)

        # --- Sliders and other inputs (VERTICALLY stacked) ---
        for feature in feature_names:
            if feature == "Age":
                val = st.slider("What's your age?", 0, 100, 30)
                input_data.append(val)

            elif feature in ["Systolic", "Diastolic", "HeartRate", "Glucose", "SpO2", "RespiratoryRate","Daily Steps"]:
                if feature == "HeartRate":
                    val = st.slider("Set Your Heart Rate (Beats/Min) - Measured Using a Pulse Sensor/Fitness Band", 0, 300, 80)
                elif feature == "Glucose":
                    val = st.slider("Set Your Glucose Level (mg/dL) - Measured Using a Glucometer", 0, 300, 90)
                elif feature == "SpO2":
                    val = st.slider("Enter Your SpO2 Level (%) - Using a Pulse Oximeter", 0, 100, 95)
                elif feature == "RespiratoryRate":
                    val = st.slider("Set Your Respiratory Rate (Breaths/Min) - Measured Using a Smartwatch or Fitness Tracker", 0, 50, 18)
                elif feature == "Systolic":
                    val = st.slider("Enter Your Systolic Blood Pressure (mmHg) - Measured Using a Blood Pressure Monitor", 30, 200, 120)
                elif feature == "Diastolic":
                    val = st.slider("Enter Your Diastolic Blood Pressure (mmHg) - Measured Using a Blood Pressure Monitor", 30, 120, 80)
                elif feature == "Daily Steps":
                    val = st.number_input("How many steps do you take daily?", min_value=0, max_value=50000, step=100, value=5000)
                input_data.append(val)
            
            elif feature not in ["Sex", "Smoking", "Alcohol", "FamilyHistory", "Medication"]:
                val = st.number_input(feature, step=0.1, value=1.0)
                input_data.append(val)

    with col2:
        img = Image.open("imgs/6.png")
        new_width = 1200   # Increase width
        new_height = 2000   # Increase height

        # Resize the image
        img = img.resize((new_width, new_height))

        # Show the image
        st.image(img, use_container_width=False) 

        # --- Binary Features 0 or 1 ---
        for feature in feature_names:
            if feature == "Sex":
                sex = st.selectbox("Gender", ["Male", "Female"])
                input_data.append(1 if sex == "Male" else 0)

            elif feature in ["Smoking", "Alcohol", "FamilyHistory", "Medication"]:
                if feature == "Smoking":
                    binary = st.selectbox("Do you smoke? (0 = No, 1 = Yes)", [0, 1])
                elif feature == "Alcohol":
                    binary = st.selectbox("Do you consume alcohol? (0 = No, 1 = Yes)", [0, 1])
                elif feature == "FamilyHistory":
                    binary = st.selectbox("Any family history of diseases? (0 = No, 1 = Yes)", [0, 1])
                elif feature == "Medication":
                    binary = st.selectbox("Are you currently on any medication? (0 = No, 1 = Yes)", [0, 1])
                input_data.append(binary)

    # --- Predict button ---
    if st.button("Make Prediction"):
        try:
            # Ensure input_data matches feature names used in training
            input_df = pd.DataFrame([input_data], columns=feature_names)
            input_df

            # Transform input data with the scaler
            input_scaled = scaler.transform(input_df)

            # Make prediction
            prediction = model.predict(input_scaled)
            predicted_labels = mlb.inverse_transform(prediction)[0]

            if predicted_labels:
                st.success("The system has identified the following possible condition(s): " + ", ".join(predicted_labels))
                
                database.save_prediction(
                email=st.session_state.user_email,
                input_data=input_data,
                predicted_diseases=predicted_labels
            )
                # Gemini Enhanced Explanation
                try:
                    with st.spinner("Analyzing..."):
                        genai.configure(api_key="AIzaSyAhQM6icwPc-Wlx4xdIr4Xp9ndolCCIqEM")  # replace with your API key
                        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
                        prompt = f"The system has identified the following possible condition(s): {', '.join(predicted_labels)}. I have a dataset containing the following features: Age, Systolic, Diastolic, HeartRate, RespiratoryRate, Glucose, SpO2, Sex, Smoking, Alcohol, FamilyHistory, Medication, Height(m), Weight(kg), BMI, BodyTemp, SleepHours, StepsPerDay, Hydration(L), WaistCircumference. Based on these inputs, the system has identified the following possible condition(s): [List the conditions identified by the system].Please explain the possible causes of each condition, the other symptoms associated with it, and suggest solutions to address or manage the condition. If the condition is related to lifestyle factors, provide recommendations for improvement in diet, exercise, and habits."
                        gemini_response = gemini_model.generate_content(prompt)
                        st.markdown("")
                        st.write(gemini_response.text)
                except Exception as e:
                    st.warning("⚠️ Gemini API error. Check your key or connection.")
                    st.text(str(e))
            else:
                st.info("No signs of any disease detected. You appear to be in good health.")

        except Exception as e:
            st.error("Something went wrong with the prediction.")
            st.text(str(e))

else:
    st.warning("You're Almost There – Just Log In.")