import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app
st.title("Streamlit OpenAI App")
st.write("This app connects to the OpenAI API to generate text based on user input.")

user_input = st.text_input("Enter some text to get a response from OpenAI:")

max_tokens_options = [50, 100, 150, 200]
max_tokens = st.radio("Select max tokens:", max_tokens_options)

temperature = st.slider("Select temperature:", min_value=0.0, max_value=1.0, value=0.8, step=0.1)

if user_input:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
        st.write(response.choices[0].text.strip())
    except Exception as e:
        st.write("Error:", str(e))
