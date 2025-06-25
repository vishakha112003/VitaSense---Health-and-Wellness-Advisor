import streamlit as st
from database import create_tables, add_user, authenticate_user

create_tables()

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# Custom styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');
    
    .stApp {
        background: linear-gradient(to bottom, #000428, #004e92);
        color: white;
    }

    /* Remove top spacing */
    section.main > div {
        padding-top: 0rem !important;
    }

    /* Remove shadow/extra container spacing */
    [data-testid="stSidebar"], .block-container {
        box-shadow: none !important;
    }

    .form-container {
        display: flex;
        flex-direction: column;
        justify-content: center;  /* Changed from flex-start to center */
        align-items: center;
        padding-top: 10vh;  /* Adjusted padding for better vertical alignment */
        min-height: 20vh;  /* Adjusted height for better centering */
    }

    .form-title {
        font-size: 50px;
        font-style: "Roboto Condensed", sans-serif;
        font-weight: bold;
        text-align: center;
       
    }

    .form-subtitle {
        font-size: 25px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        font-style: "Roboto Condensed", sans-serif;
        font-style: italic;
    }

    .custom-label {
        font-size: 30px;
        color: white;
        font-style: "Roboto Condensed", sans-serif;
        font-style: italic;
        margin-bottom: 1rem;
    }
        
    .left-image-container img {
    max-height: 300px;  /* Increase height to your desired size */
    width: 100%;
    object-fit: contain;
    margin-left: -50px;  /* Move image more to the left */
    margin-top: -40px;   /* Move image upwards */
    }

    .left-image-container {
        padding: 0 !important;
        margin: 0  !important;
    }
    
    input:focus {
        border: 2px solid #1e90ff !important;
        outline: none !important;
        box-shadow: 0 0 8px #1e90ff;
        transition: 0.2s ease-in-out;
    }
               
    </style>
""", unsafe_allow_html=True)

def main():
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown('<div class="left-image-container">', unsafe_allow_html=True)
        st.image("imgs/login2.png", use_container_width = True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        # Ensure clean layout
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)

        if st.session_state.authenticated:
            show_home()
        elif st.session_state.show_signup:
            signup()
        else:
            login()

        st.markdown("</div></div>", unsafe_allow_html=True)

def login():
    st.markdown("<div class='form-title'>Good to See You Again!</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-subtitle'>Login to continue your journey.</div>", unsafe_allow_html=True)
    
    email = st.text_input("Email Address", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Sign in"):
        if authenticate_user(email, password):
            st.success(f"Welcome {email}!")
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Invalid credentials!")

    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
        st.rerun()

def signup():
    st.markdown("<div class='form-title'>Join the Journey!</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-subtitle'>Create your account in seconds.</div>", unsafe_allow_html=True)

    email = st.text_input("Email Address", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign up"):
        if add_user(email, password):
            st.success("Account created successfully! Please log in.")
            st.session_state.show_signup = False
            st.rerun()
        else:
            st.error("Email already exists. Please log in.")

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

def show_home():
    st.markdown(
    f"""
    <div class="custom-label">
        Welcome to <strong>VitaSense</strong>, {st.session_state.user_email}!<br>
        Your personalized health journey starts here.<br>
        Stay proactive. Stay healthy. Let’s take the next step towards better wellness together.
    </div>
    """,
    unsafe_allow_html=True
)
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.rerun()

if __name__ == "__main__":
    main()
