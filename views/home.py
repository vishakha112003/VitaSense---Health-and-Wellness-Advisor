import streamlit as st
import base64

# Function to encode video to base64
def get_base64_video(video_file):
    with open(video_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return encoded

# Path to your local video file
video_path = "background2.mp4"

# Convert video to base64
video_base64 = get_base64_video(video_path)

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("imgs/logo2.png")

# Embed base64 video into HTML with a rounded rectangle overlay
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');

    .stApp {{
        background: transparent;
    }}

    video#bgvid {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
    }}

    .overlay-box {{
        position: relative;
        z-index: 1;
        margin: 5% auto;
        width: 100%;
        height: 80vh;
        padding: 50px;
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 30px;
        border: 1px solid white;
        color: white;
    }}

    .highlight {{
        color: #01224d;
    }}

    .headline {{
        font-size: 85px;
        font-weight: bold;
        font-family: 'Special Gothic Expanded One', sans-serif;
        margin: 0;
    }}

    .subheadline {{
        font-size: 30px;
        font-family: 'Roboto Condensed', sans-serif;
        margin-top: 20px;
    }}

    .about-section {{
        position: absolute;
        bottom: 80px;
        left: 50px;
        width: 40%;
        font-family: 'Roboto Condensed', sans-serif;
        font-size: 18px;
    }}

    .about-heading {{
        font-size: 35px;
        font-weight: bold;
        margin-bottom: 10px;
    }}

    .carousel {{
        position: relative;
        height: 80px;
        overflow: hidden;
    }}

    .carousel p {{
        position: absolute;
        width: 100%;
        opacity: 0;
        animation: fade 20s infinite;
        margin: 0;
    }}

    .carousel p:nth-child(1) {{ animation-delay: 0s; }}
    .carousel p:nth-child(2) {{ animation-delay: 4s; }}
    .carousel p:nth-child(3) {{ animation-delay: 8s; }}
    .carousel p:nth-child(4) {{ animation-delay: 12s; }}
    .carousel p:nth-child(5) {{ animation-delay: 16s; }}

    @keyframes fade {{
        0% {{ opacity: 0; }}
        5% {{ opacity: 1; }}
        20% {{ opacity: 1; }}
        25% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}

    .experience-box {{
        position: absolute;
        bottom: 40px;
        right: 40px;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        font-family: 'Roboto Condensed', sans-serif;
        z-index: 2;
    }}

    .experience-box .top {{
        display: flex;
        flex-direction: row;
        align-items: flex-end;
        gap: 10px;
        margin-bottom: 10px;
    }}

    .experience-box .label {{
        font-size: 24px;
        font-weight: bold;
        color: white;
        line-height: 1.2;
        text-align: right;
    }}

    .experience-box .years {{
        font-size: 80px;
        font-weight: bold;
        color: #01224d;
        font-family: 'Special Gothic Expanded One', sans-serif;
        line-height: 1;
    }}

    .experience-box .count {{
        background-color: #01224d;
        color: white;
        padding: 10px 25px;
        border-radius: 20px;
        font-size: 40px;
        font-weight: bold;
        font-family: 'Special Gothic Expanded One', sans-serif;
        display: inline-block;
    }}

    </style>

    <video autoplay muted loop id="bgvid">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>

    <div class="overlay-box">
        <div class="experience-box">
            <div class="top">
                <div class="label">Boost Your<br> Health</div>
                <div class="years">100%</div>
            </div>
            <div class="count">WELLNESS 10x</div>
        </div>
        <div class="headline">MAKE SENSE OF YOUR HEALTH WITH <span class="highlight">VITASENSE</span>.</div>
        <div class="subheadline">
            Unlock the power of your health. Predict potential risks, keep an eye on your vitals and take charge of your well-being like never before. It’s time to live smarter, healthier, and in control.
        </div>
        <div class="about-section">
            <img src="data:image/png;base64,{logo_base64}" style="width: 120px; margin-bottom: 15px;" />
            <div class="about-heading">ABOUT US</div>
            <div class="carousel">
                <p>Easily upload your lab reports and let VitaSense analyze them to help you understand what's going on inside your body in simple, clear terms. Get actionable insights from your reports to take control of your health.</p>
                <p>Create your personal account to securely store health records and track your health journey over time with clear, easy-to-read trends. Enjoy peace of mind knowing your data is safe and easily accessible whenever you need it.</p>
                <p>Enter basic health readings like blood pressure, heart rate, BMI etc. and get early predictions about potential health risks. With regular updates, stay informed and make timely decisions to safeguard your health.</p>
                <p>Have questions about your health? Just ask our intelligent chatbot anytime for instant, reliable answers. No more scrolling through dozens of articles — get quick help, right when you need it.</p>
                <p>Stay on top of your health with visual dashboard that shows how your vitals and health metrics change over time. Easily spot trends and track improvements to keep yourself motivated and on the right path.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
