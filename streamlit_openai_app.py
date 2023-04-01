import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

def send_message_to_openai(prompt, max_tokens, temperature, engine):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}'
    }

    try:
        if engine == "gpt-3.5-turbo":
            data = {
                'model': engine,
                'messages': [{"role": "system", "content": pre_prompt}, {"role": "user", "content": user_message}],
                'max_tokens': max_tokens,
                'n': 1,
                'temperature': temperature,
            }
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
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
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"Error details: {e.response.text}")
        return ""

    return response.choices[0].text.strip()

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
    .user-bubble {
        background-color: #34C759;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 1rem;
        max-width: 75%;
        color: white;
    }
    .pirate-bubble {
        background-color: #0A84FF;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 1rem;
        max-width: 75%;
        color: white;
    }
    textarea {
        resize: vertical;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)

st.markdown("<h1 tabindex='0'>Pirate Chatbot</h1>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

pre_prompt = "You are a scholar of logical reasoning.  You specialize in propositional logic. Your job is to critically analyze the thesis statement submitted by students and provide advice on the logical validity and soundness of the thesis. Let's take this step by step as follows:

1. Print: "Please submit your thesis statement for review".
2. When the student submits a thesis statement, print: "Validity and Soundness of Thesis Statement"
3. List of all propositions contained in the thesis statement (noting whether each is a premise or a conclusion).
4. List any unstated assumptions underlying the argument. 
5. For each premise and unstated assumption, print a heading "[the premise/assumption statements]" and then:
	- List the key concepts that are necessary to understand the ]premise/assumption] (including technical terms, subject background, and any relevant academic theories).
	- Print: "This [premise/assumption] is sound because [insert a list of two or more true statements that each prove or infer the truth of the premise/assumption]".
	- Print: "This [premise/assumption] may be unsound because [insert a list of two or more true statement that each disprove or undermine the truth of the premise/assumption]".
	- Print: "This [premise/assumption] can be tested by [insert list of two or more empirical methods for testing the truth of the premise/assumption]""

user_message = st.text_area("Enter your message:", key="user_input")

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
        st.markdown(f"<div class='user-bubble' tabindex='0'>{chat['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='pirate-bubble' tabindex='0'>{chat['message']}</div>", unsafe_allow_html=True)

