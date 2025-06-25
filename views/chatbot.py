import streamlit as st
import cohere
import base64
import time

# Set up Cohere API key
COHERE_API_KEY = "aH4cYU8eyVoMx3wN56yjZUf8ClJZQiK2o4gEJtkE"  # Replace with your actual API key

# Initialize Cohere Client
co = cohere.Client(COHERE_API_KEY)

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("imgs/bot.png")

# Function to get response from Cohere model
def get_cohere_response(user_input):
    response = co.chat(
    model="command-r-plus",
    message=user_input
    )
    return response.text.strip()

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
                font-size: 50px;
                font-family: 'Cal Sans', sans-serif;
                color: white;
                }}

        .subheadline {{
                font-size: 30px;
                font-family: 'Roboto Condensed', sans-serif;
            }}

        /* Custom styles for message layout */
        .message {{
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }}

        .user-message {{
            background-color: #0d1547;
            text-align: right;
            color: white;
        }}

        .assistant-message {{
            background-color: #08596f;
            text-align: left;
            color: white;
            margin-top: 65px;
        }}

        </style>

        <div id="bgimg"></div>
        """,
        unsafe_allow_html=True
    )

def main():
    st.markdown("<div class='headline'>VitaSense: The Chatbot That Cares for Your Health.</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheadline'>From symptoms to suggestions — just start the conversation.</div>", unsafe_allow_html=True)
    
    # Welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Hello and welcome! I'm VitaSense, your personal health assistant, here to help you make smarter, healthier decisions. Whether you have questions about your well-being, need personalized advice, or want to track your health goals, I'm here to guide you every step of the way. How can I assist you today on your path to better health?"})
    
    # Display chat history with columns
    for message in st.session_state.messages:
        col1, col2 = st.columns([2, 2])  # Column layout: col1 for assistant, col2 for user
        with col1:
            if message["role"] == "assistant":
                st.markdown(f'<div class="message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        with col2:
            if message["role"] == "user":
                st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # User input
    user_input = st.chat_input("How are you feeling?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message in the second column (right)
        col1, col2 = st.columns([2, 2])
        with col2:
            st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)
        
        # Display assistant's response in the first column (left)
        with col1:
            with st.spinner("Typing..."):
                time.sleep(1)  # Simulate typing delay
                response = get_cohere_response(user_input)
                st.markdown(f'<div class="message assistant-message">{response}</div>', unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
