
import streamlit as st
import pdfplumber
import pytesseract
import google.generativeai as genai
import base64
from PIL import Image
import os
import html

# Set up Google Gemini API
genai.configure(api_key="")  # <-- Replace if needed

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("imgs/4.png")

def get_base64_video(video_file):
    with open(video_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return encoded

# Path to your local video file
video_path = "background1 .mp4"

# Convert video to base64
video_base64 = get_base64_video(video_path)

# Function to extract text from images
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to analyze text using Google Gemini
def analyze_with_gemini(report_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Objective: Based on the uploaded lab report and detected health conditions, generate a highly structured, comprehensive health improvement plan.\n\n"
        f"Required Structure and Order:\n"
        f"1. Proactive Health Analysis:\n"
        f"- Analyze the lab report in detail and predict any possible underlying or emerging health conditions or risks the user might develop, even if not explicitly mentioned (e.g., prediabetes, anemia, metabolic syndrome, thyroid dysfunction, early cardiovascular risk).\n"
        f"- Clearly explain the basis of each prediction in simple, understandable terms.\n"
        f"2. Specialist Consultations:\n"
        f"- Based on the current findings and the proactive risk analysis, recommend which specialists (e.g., endocrinologist, cardiologist, nephrologist) the user should consult for further evaluation, confirmation, or management.\n"
        f"- Briefly mention why each specialist visit is suggested.\n"
        f"3. Supplements Recommendation:\n"
        f"- Recommend specific supplements tailored to address detected deficiencies or health conditions (e.g., Vitamin D3, Iron, B12, Omega-3).\n"
        f"- Clearly state:\n"
        f"  a) Name of supplement\n"
        f"  b) Dosage (e.g., 1000 IU per day)\n"
        f"  c) Timing (e.g., after breakfast)\n"
        f"  d) Suggested duration (e.g., 3 months or as per doctor's advice)\n"
        f"4. 7-Day Indian Diet Plan (Tabular Format):\n"
        f"- Create a detailed, practical 7-day meal plan (breakfast, lunch, evening snack, dinner) clearly presented in a table.\n"
        f"- Meals must:\n"
        f"  a) Be regionally Indian, easy to prepare, and seasonal\n"
        f"  b) Use only healthy, whole, unprocessed foods\n"
        f"  c) Include portion sizes (e.g., 2 small rotis, 1 bowl dal)\n"
        f"  d) Specify options for both vegetarians and non-vegetarians wherever appropriate\n"
        f"  e) Maintain balanced macronutrients (carbs, proteins, fats) and fiber\n"
        f"5. Foods to Avoid:\n"
        f"- Clearly list foods, ingredients, and preparation styles that must be avoided to support healing and avoid worsening of detected or predicted conditions.\n"
        f"- Categorize if needed (e.g., High Sugar, High Fat, Processed Foods).\n"
        f"6. Physical Activity Plan:\n"
        f"- Suggest a practical exercise routine based on the user's health profile.\n"
        f"- Specify:\n"
        f"  a) Type of activities (e.g., brisk walking, yoga, strength training)\n"
        f"  b) Frequency (e.g., 5 times per week)\n"
        f"  c) Duration (e.g., 30–45 minutes per session)\n"
        f"- Mention precautions if any (e.g., for joint pain or heart risks).\n"
        f"7. Lifestyle Recommendations:\n"
        f"- Suggest daily habit improvements like:\n"
        f"  a) Sleep hygiene\n"
        f"  b) Stress management techniques (e.g., meditation, breathing exercises)\n"
        f"  c) Mindful eating practices\n"
        f"  d) Hydration habits\n"
        f"- Keep suggestions practical, clear, and immediately actionable.\n\n"
        f"Important Instructions:\n"
        f"- Each section must be clearly defined separately and NOT merged.\n"
        f"- The output must be clean, professional, easy to read, and directly actionable.\n"
        f"- Avoid unnecessary filler; focus on making recommendations practical and user-friendly.\n\n"
        f"Given this lab report data, generate the requested health improvement plan:\n\n{report_text}"
    )

    return response.text

# --- Streamlit App ---
if "authenticated" in st.session_state and st.session_state.authenticated:

    # Background image + general style
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cal+Sans&display=swap');
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
            filter: brightness(50%);
        }}

        .headline {{
            font-size: 70px;
            font-family: 'Cal Sans', sans-serif;
            color: white;
            margin-bottom: 20px;
        }}

        .subheadline {{
            font-size: 35px;
            font-family: 'Roboto Condensed', sans-serif;
            color: white;
            margin-bottom: 30px;
        }}

        .white-box {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 30px;
            height: 100%;
            color: #000;
            font-family: 'Roboto Condensed', sans-serif;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        }}
        </style>

        <div id="bgimg"></div>
        """,
        unsafe_allow_html=True
    )

    # Overlay and Columns
    with st.container():
        st.markdown("<div class='headline'>Upload,  Analyze,  Understand — Your Health Decoded.</div>", unsafe_allow_html=True)
        st.markdown("<div class='subheadline'>Upload your medical reports, get clear predictions, personalized recommendations, and take control of your health journey — all in minutes.</div>", unsafe_allow_html=True)
        st.markdown(
        f"""
        <div style="width: 100%; max-width: 1700px; height: 450px; margin: 0 auto; overflow: hidden; border-radius: 10px; margin-bottom: 50px;">
            <video width="100%" height="auto" autoplay muted loop playsinline style="display: block;">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
                "Upload your lab report (PDF/Image)", 
                type=["pdf", "png", "jpg", "jpeg"], 
                key="fileUploader"
            )
            
    if uploaded_file:
        file_type = uploaded_file.type
        extracted_text = ""

        if file_type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = extract_text_from_image(uploaded_file)

        st.subheader("Extracted Text from Report")
        st.text_area("Lab Report Data", extracted_text, height=200)
        x = st.button("Analyze")

        if x:
            with st.spinner("Analyzing..."):
                result = analyze_with_gemini(extracted_text)
            st.subheader("Analysis Results")

            with st.container():
                st.markdown(
                    """
                    <style>
                    .navy-box {
                        background-color: #0A192F;
                        padding: 20px;
                        border-radius: 10px;
                        color: white;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Now safely render result inside a div with class
                st.markdown(
                    f'<div class="navy-box">{result}</div>',
                    unsafe_allow_html=True
                )

else:
    st.warning("You're Almost There – Just Log In.")
           
