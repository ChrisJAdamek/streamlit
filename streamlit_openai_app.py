import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the function to send a message to OpenAI
def send_message_to_openai(prompt, max_tokens, temperature, engine):
    try:
        if engine == "gpt-3.5-turbo":
            response = openai.ChatCompletion.create(
                engine=engine,
                messages=[{"role": "system", "content": pre_prompt}, {"role": "user", "content": user_message}],
                max_tokens=max_tokens,
                n=1,
                temperature=temperature,
            )
            return response.choices[0].message['content'].strip()
        else:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
            return response.choices[0].text.strip()
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
    .accessible-text {
        color: #4a4a4a;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load custom font
st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)

# Streamlit app starts here
st.markdown("<h1 tabindex='0'>Pirate Chatbot</h1>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

pre_prompt = "please pretend you are a pirate in all future responses."

user_message = st.text_input("Enter your message:", key="user_input")

with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    engine = st.selectbox("Select a language model:", ("gpt-4-32k", "gpt-3.5-turbo", "text-davinci-003", "code-davinci-002"))

if st.button("Send"):
    if user_message:
        combined_prompt = f"{pre_prompt} {user_message}"
        st.session_state.chat_history.append({"role": "user", "message": user_message})

        with st.spinner("Waitin' for a pirate's response..."):
            response = send_message_to_openai(combined_prompt, max_tokens, temperature, engine)

        if response:
            st.session_state.chat_history.append({"role": "pirate", "message": response})

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div style='background-color: #caf0f8; padding: 1rem; margin-bottom: 0.5rem; border-radius: 10px;' tabindex='0'>{chat['message']}</div>", unsafe_allow_html=True)
else:
st.markdown(f"<div style='background-image: url(https://wallpapercave.com/wp/JNn0uaC.jpg); padding: 1rem; margin-bottom: 0.5rem; color: white; font-size: 1.2rem; border-radius: 10px;' tabindex='0' role='img' aria-label='Pirate response'><div class='accessible-text'>{chat['message']}</div></div>", unsafe_allow_html=True)
