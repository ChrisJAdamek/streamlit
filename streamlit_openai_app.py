import os
import requests
import streamlit as st
import openai
import json
import tempfile

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the function to send a message to OpenAI
def send_message_to_openai(prompt, max_tokens, temperature, engine):
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
        return response.choices[0].text.strip(), None
    except Exception as e:
        return None, str(e)

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
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load custom font
st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)

# Streamlit app starts here
st.title("Pirate Chatbot")

# Load chat history from persistent storage
tfile = tempfile.NamedTemporaryFile(delete=False) 
tfile.write(json.dumps([]).encode())
tfile.seek(0)
chat_history_file = st.sidebar.file_uploader("Load chat history file", type=['json'], key="1", value=tfile)
chat_history = json.load(chat_history_file)
chat_history_file.close()

# Pre-prompt
pre_prompt = "please pretend you are a pirate in all future responses."

# Get user input
user_message = st.text_input("Enter your message:")

# Add a Send button
send_button = st.button("Send")

# Add sliders for max_tokens and temperature
with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    engine = st.selectbox("Language Model:", options=["text-davinci-003", "GPT-4"])

if send_button and user_message:
    # Combine the pre-prompt and the user message
    combined_prompt = f"{pre_prompt} {user_message}"

    # Add user message to chat history
    chat_history.append({"role": "user", "message": user_message})

    # Show loading indicator
    with st.spinner("Waitin' for a pirate's response..."):
        # Send the combined prompt to OpenAI with the specified max_tokens, temperature, and engine
        response, error = send_message_to_openai(combined_prompt, max_tokens, temperature, engine)

    if response:
        # Add response to chat history
        chat_history.append({"role": "pirate", "message": response})
    else:
        st.error(f"An error occurred: {error}")

    # Save chat history to persistent storage
    with open(chat_history_file.name, 'w') as f:
        json.dump(chat_history, f)

    # Display chat history
    for chat in chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div style='background-color: #caf0f8; padding: 1rem; margin-bottom: 0.5rem; border-radius: 10px;'>{chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-image: url(https://wallpapercave.com/wp/JNn0uaC.jpg); padding: 1rem; margin-bottom: 0.5rem; color: white; font-size: 1.2rem; border-radius: 10px;'>{chat['message']}</div>", unsafe_allow_html=True)

# Download chat history
if st.sidebar.button("Download chat history"):
    with open(chat_history_file.name, 'w') as f:
        json.dump(chat_history, f)
    st.sidebar.markdown(
        f'<a href="data:application/json;charset=utf-8,{json.dumps(chat_history)}" download="chat_history.json">Download chat history</a>',
        unsafe_allow_html=True,
    )
