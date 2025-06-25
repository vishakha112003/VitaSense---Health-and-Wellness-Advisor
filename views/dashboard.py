import streamlit as st
import database
import ast
import base64
import pandas as pd
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("imgs/2.jpg")

def calculate_health_score(inputs):
    """
    inputs: dictionary with keys like 'BMI', 'SleepHours', 'StepsPerDay', 'Hydration(L)'
    returns: health score out of 100
    """
    score = 0

    # BMI (Healthy range: 18.5 - 24.9)
    bmi = inputs.get('BMI')
    if bmi:
        if 18.5 <= bmi <= 24.9:
            score += 25
        elif 17 <= bmi <= 27:
            score += 15
        else:
            score += 5

    # Sleep Hours (Ideal 7-9 hours)
    sleep = inputs.get('Sleep Hours')
    if sleep:
        if 7 <= sleep <= 9:
            score += 25
        elif 6 <= sleep <= 10:
            score += 15
        else:
            score += 5

    # Steps per Day (Ideal 8000-10000)
    steps = inputs.get('Daily Steps')
    if steps:
        if 8000 <= steps <= 10000:
            score += 25
        elif 5000 <= steps <= 12000:
            score += 15
        else:
            score += 5

    # Hydration (Ideal 2-3 Liters)
    hydration = inputs.get('Daily Water Intake(L)')
    if hydration:
        if 2 <= hydration <= 3:
            score += 25
        elif 1.5 <= hydration <= 4:
            score += 15
        else:
            score += 5

    return score

if "authenticated" in st.session_state and st.session_state.authenticated:

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');

        .stApp {{
            background: transparent;
        }}

        #bgimg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: url('data:image/jpeg;base64,{logo_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: brightness(30%);
        }}

        .headline {{
            font-size: 70px;
            font-family: 'Special Gothic Expanded One', sans-serif;
            color: white;
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

         <div id="bgimg"></div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='headline'> Track Your Progress: Your Health Metrics — Visualized for Better Insight.</div>", unsafe_allow_html=True)

    user_predictions = database.get_user_predictions(st.session_state.user_email)

    if user_predictions:
        all_inputs = []  # To collect all input values

        for idx, prediction in enumerate(user_predictions[::-1], start=1):
            inputs = prediction['input_data']
            diseases = prediction['predicted_diseases']
            timestamp = prediction['timestamp']
            inputs = ast.literal_eval(inputs)  # convert string to list or dict

            # Assuming inputs is a list
            if isinstance(inputs, list):
                all_inputs.append(inputs)
            elif isinstance(inputs, dict):
                all_inputs.append(list(inputs.values()))
            
            '''st.subheader(f"Entry #{idx}")
            st.write("Unput", inputs)
            st.write("**Predicted Diseases:**", diseases)
            st.markdown("---")'''

        # After collecting all inputs, create a combined chart
        if all_inputs:
            # Convert all_inputs into a DataFrame
            df = pd.DataFrame(all_inputs)

            # Feature names (adjust these according to your feature order!)
            feature_names = ['Age', 'Systolic', 'Diastolic', 'HeartRate', 'RespiratoryRate',
                             'Glucose', 'SpO2', 'Height(m)','Weight(kg)',  'BMI','Body Temperature(in F)','Sleep Hours',
                             'Daily Steps','Daily Water Intake(L)', 'Waist Circumference','Sex', 'Smoking', 'Alcohol', 'FamilyHistory', 'Medication']

            if len(feature_names) == df.shape[1]:
                df.columns = feature_names
            else:
                st.error("Mismatch between feature names and input dimensions.")
            
            st.markdown("<div class='custom-label'>Take a closer look at how your daily habits and health inputs—like sleep, hydration, activity, and more—are shaping your overall well-being. This trend analysis will give you a better understanding of what’s working for you and where you can improve. Keep going, your health journey is all about progress.</div>", unsafe_allow_html=True)
            avg_inputs = df.mean()

            # Calculate health score
            avg_inputs_dict = avg_inputs.to_dict()
            health_score = calculate_health_score(avg_inputs_dict)
            st.markdown(f"""
            <div style='
                padding: 15px; 
                font-size; 30px;
                font-family: "Roboto-Condensed", sans-serif;
            '>
                <div style='font-size: 40px; font-weight: 600;'>Here's your current health score! </div>
                <div style='font-size: 36px; font-weight: bold;'>{health_score} / 100</div>
            </div>
            """, unsafe_allow_html=True)

            if health_score >= 80:
                st.success(f"Your Health Score: {health_score} / 100 (Excellent!)")
            elif 60 <= health_score < 80:
                st.warning(f"Your Health Score: {health_score} / 100 (Moderate)")
            else:
                st.error(f"Your Health Score: {health_score} / 100 (Needs Improvement)")

            st.subheader("📊 Average Health Metrics Trend")

            #------Bar Chart------#
            # Calculate average values
            avg_inputs = df.mean()

            # Plot combined bar chart
            selected_features = ['Systolic', 'Diastolic', 'HeartRate', 'RespiratoryRate',
                             'Glucose', 'SpO2', 'BMI', 'Body Temperature(in F)', 'Sleep Hours', 'Daily Water Intake(L)', 'Waist Circumference']  # <-- modify as needed

            # Filter avg_inputs
            filtered_avg_inputs = avg_inputs[selected_features]

            # Prepare chart data
            chart_df = filtered_avg_inputs.reset_index()
            chart_df.columns = ['Feature', 'Average Value']

            # Plot
            fig = px.bar(chart_df, x='Feature', y='Average Value', text_auto='.2s', color='Feature')
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No inputs available to generate combined chart.")
        
       #---- Pie Chart ---- 
        all_diseases = []

        for prediction in user_predictions:
            diseases = prediction.get("predicted_diseases", [])

            # If the diseases are stored as a single string
            if isinstance(diseases, str):
                split_diseases = [d.strip() for d in diseases.split(",") if d.strip()]
                all_diseases.extend(split_diseases)

            # If diseases are stored as a list
            elif isinstance(diseases, list):
                for item in diseases:
                    if isinstance(item, str):
                        split_diseases = [d.strip() for d in item.split(",") if d.strip()]
                        all_diseases.extend(split_diseases)

        disease_counts = dict(Counter(all_diseases))

        if disease_counts:
            pie_fig = px.pie(
                names=list(disease_counts.keys()),
                values=list(disease_counts.values()),
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.subheader("📊 Frequency of Predicted Diseases")
            st.plotly_chart(pie_fig)
        else:
            st.info("No disease data available.")
                        
        records = []
        for p in user_predictions:
            input_data_raw = p.get("input_data", [])

            # Ensure input_data is a list
            if isinstance(input_data_raw, str):
                input_data = [x.strip() for x in input_data_raw.split(",")]
            else:
                input_data = list(input_data_raw)  # In case it's another iterable


            if len(input_data) >= 19:
                record = {
                    "timestamp": p.get("timestamp", None),
                    "BMI": input_data[9],
                    "Sleep Hours": input_data[11],
                    "Daily Water Intake(L)": input_data[13],
                }
                records.append(record)
            
        df = pd.DataFrame(records)
        print(df)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        # Line chart for metrics
        if not df.empty:
            st.subheader("Health Metrics Over Time")

            line_fig = px.line(
                df,
                x="timestamp",
                y=["BMI", "Sleep Hours", "Daily Water Intake(L)"],
                markers=True,
                title="Trends in Sleep, Hydration & BMI"
            )
            st.plotly_chart(line_fig)
        else:
            st.info("No valid health records found for trend visualization.")

        
        records = []
        for p in user_predictions:
            input_data_raw = p.get("input_data", [])

            # Ensure input_data is a list
            if isinstance(input_data_raw, str):
                input_data = [x.strip() for x in input_data_raw.split(",")]
            else:
                input_data = list(input_data_raw)  # In case it's another iterable


            if len(input_data) >= 19:
                record = {
                    "timestamp": p.get("timestamp", None),
                    "Daily Steps": input_data[12]}
                records.append(record)
            
        df = pd.DataFrame(records)
        print(df)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        # Line chart for metrics
        if not df.empty:
            st.subheader("Trends in Daily Steps")

            if not df.empty:
                area_fig = px.area(
                    df,
                    x="timestamp",
                    y="Daily Steps"
                )
                st.plotly_chart(area_fig)
        else:
            st.info("No valid health records found for trend visualization.")



else:
    st.warning("You're Almost There – Just Log In.")
