import streamlit as st

st.set_page_config(layout="wide")

# --- Apply custom CSS for dark navy-blue sidebar styling ---
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
    <style>
        html, body {
            font-size: 18px;
            font-family: 'Poppins', sans-serif !important;
        }

        /* Hide scrollbar for sidebar */
        [data-testid="stSidebar"] ::-webkit-scrollbar {
            display: none;
        }

        [data-testid="stSidebar"] {
            background-color: #0A192F;
            color: #ffffff;
            font-family: 'Poppins', sans-serif !important;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }

        /* Sidebar button style */
        section[data-testid="stSidebar"] button {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 90px;
            border-radius: 8px;
            background: linear-gradient(135deg, #112240, #233554);
            color: #ffffff;
            border: none;
            font-size: 20px !important;
            font-family: 'Poppins', sans-serif !important;
            box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            margin: 6px 0;
            cursor: pointer;
            padding: 0 16px;
        }

        /* Hover effect */
        .stButton > button:hover {
            background: linear-gradient(135deg, #233554, #112240);
            box-shadow: 0px 8px 24px rgba(100, 255, 218, 0.2);
            transform: translateY(-2px);
        }

        /* Focus effect */
        .stButton > button:focus {
            background-color: #64FFDA !important;
            color: #ffffff !important;
            outline: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar logo
st.sidebar.image("imgs/logo2.png", use_container_width=True)

# Navigation options
pages = {
    "HOME": "views/home.py",
    "USER LOGIN": "views/login.py",
    "REPORT ANALYSIS": "views/upload.py",
    "PREDICTION": "views/prediction.py",
    "CHAT SUPPORT": "views/chatbot.py",
    "DASHBOARD": "views/dashboard.py"
}

# Initialize session state for selected page
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "views/home.py"  # Default page

# Sidebar navigation using buttons
for page_name, script in pages.items():
    if st.sidebar.button(page_name, use_container_width=True):
        st.session_state.selected_page = script  # Store selection in session state

# Run the selected page
exec(open(st.session_state.selected_page, encoding='utf-8').read())
