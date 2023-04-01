import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the function to send a message to OpenAI
def send_message_to_openai(prompt, max_tokens, temperature):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )

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
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load custom font
st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)

# Streamlit app starts here
st.title("Pirate Chatbot")

# Pre-prompt
pre_prompt = "please pretend you are a pirate in all future responses."

# Get user input
user_message = st.text_input("Enter your message:")

# Add sliders for max_tokens and temperature
with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)

if user_message:
    # Combine the pre-prompt and the user message
    combined_prompt = f"{pre_prompt} {user_message}"

    # Send the combined prompt to OpenAI with the specified max_tokens and temperature
    response = send_message_to_openai(combined_prompt, max_tokens, temperature)

    # Display the response in a container with a pirate-themed background
    st.markdown(f"<div style='background-image: url(https://wallpapercave.com/wp/JNn0uaC.jpg); padding: 2rem; color: white; font-size: 1.2rem; border-radius: 10px;'>{response}</div>", unsafe_allow_html=True)
