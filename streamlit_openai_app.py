import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the function to send a message to OpenAI
def send_message_to_openai(prompt, max_tokens, temperature):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return ""

    return response.choices[0].text.strip()

# Custom CSS for the app
custom_css = """
<style>
    body {
        background-color: #f7f7f7;
    }
    .stApp {
        padding: 2rem;
    }
    h1 {
        font-family: 'Pirata One', cursive;
        font-size: 3rem;
    }
    .user-message {
        background-color: #caf0f8;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
    }
    .pirate-message {
        background-color: #d35400;
        color: white;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
    }
    .message-icon {
        width: 24px;
        height: 24px;
        margin-right: 1rem;
        border-radius: 50%;
        object-fit: cover;
    }
    .message-text {
        flex: 1;
    }
    .message-timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-left: 1rem;
    }
    .message-bubble {
        max-width: 80%;
        margin-left: auto;
    }
    .user-message .message-icon {
        background-image: url(https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/bear_russian_animal_avatar-256.png);
    }
    .pirate-message .message-icon {
        background-image: url(https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/pirate_animal_avatar_pirate_bear-256.png);
    }
    .pirate-message .message-bubble {
        background-color: #fcf3cf;
    }
    .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load custom font
st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)

# Streamlit app starts here
st.title("Pirate Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

pre_prompt = "please pretend you are a pirate in all future responses."

user_message = st.text_input("Enter your message:")

with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0)

if st.button("Send"):
    if user_message:
        combined_prompt = f"{pre_prompt} {user_message}"
        st.session_state.chat_history.append({"role": "user", "message": user_message})

        with st.spinner("Waitin' for a pirate's response..."):
            response = send_message_to_openai(combined_prompt, max_tokens, temperature)

        if response:
            st.session_state.chat_history.append({"role": "pirate", "message": response})

for chat in st.session_state.chat_history:
    message_icon_url = ""
    if chat["role"] == "user":
        message_icon_url = "https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/bear_russian_animal_avatar-256.png"
    else:
        message_icon_url = "https://cdn4.iconfinder.com/data/icons/avatars-xmas-giveaway/128/pirate_animal_avatar_pirate_bear-256.png"
        
    st.markdown(f"""
        <div class="message-container {chat['role']}-message">
            <img class="message-icon" src="{message_icon_url}" alt="{chat['role']} icon">
            <div class="message-bubble">
                <div class="message-text">{chat['message']}</div>
                <div class="message-timestamp">{st.session_state['timestamp']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state['timestamp'] = "" # reset timestamp for the next message

    # Add timestamp to the latest message
    if chat == st.session_state.chat_history[-1]:
        st.session_state['timestamp'] = st.experimental_get_single_slot_value() or st.session_state['timestamp']
        st.session_state['timestamp'] = st.slider("Set timestamp (in seconds)", min_value=0, max_value=60, value=0, step=1) * 1000
        st.experimental_set_single_slot(key="timestamp", value=st.session_state['timestamp'])

