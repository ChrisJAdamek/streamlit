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

# Streamlit app starts here
st.title("Pirate Chatbot")

# Pre-prompt
pre_prompt = "please pretend you are a pirate in all future responses."

# Get user input
user_message = st.text_input("Enter your message:")

# Add sliders for max_tokens and temperature
max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)

if user_message:
    # Combine the pre-prompt and the user message
    combined_prompt = f"{pre_prompt} {user_message}"

    # Send the combined prompt to OpenAI with the specified max_tokens and temperature
    response = send_message_to_openai(combined_prompt, max_tokens, temperature)

    # Display the response
    st.write(response)
