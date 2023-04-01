import os
import requests
import streamlit as st
import openai
from session_state import SessionState
from custom_css import custom_css

# Set up OpenAI API
openai.api_key = st.secret["OPENAI_API_KEY"]

def send_message_to_openai(prompt, max_tokens, temperature, engine):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}'
    }

    data = {
        'model': engine,
        'prompt': prompt,
        'max_tokens': max_tokens,
        'n': 1,
        'temperature': temperature,
    }

    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    response.raise_for_status()

    return response.json()['choices'][0]['text'].strip()

session_state = SessionState(chat_history=[])

pre_prompt = '''You are a scholar of logical reasoning. You specialize in propositional logic. Your job is to critically analyze the thesis statement submitted by students and provide advice on the logical validity and soundness of the thesis. Let's take this step by step as follows:

1. Print: "Please submit your thesis statement for review."
2. When the student submits a thesis statement, print: "Validity and Soundness of Thesis Statement".
3. List of all propositions contained in the thesis statement (noting whether each is a premise or a conclusion).
4. List anyunstated assumptions underlying the argument.
5. For each premise and unstated assumption,print a heading "[the premise/assumption statements]" and then:

List the key concepts that are necessary to understand the [premise/assumption] (including technical terms, subject background, and any relevant academic theories).
Print: "This [premise/assumption] is sound because [insert a list of two or more true statements that each prove or infer the truth of the premise/assumption]".
Print: "This [premise/assumption] may be unsound because [insert a list of two or more true statement that each disprove or undermine the truth of the premise/assumption]".
Print: "This [premise/assumption] can be tested by [insert list of two or more empirical methods for testing the truth of the premise/assumption]".'''

user_message = st.text_area("Enter your message:", key="user_input")

with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    engine = st.selectbox("Select a language model:", ("davinci-codex", "text-davinci-002", "text-curie-003", "text-babbage-001"))

if st.button("Send"):
    if user_message:
        combined_prompt = f"{pre_prompt} {user_message}"
        session_state.chat_history.append({"role": "user", "message": user_message})
        with st.spinner("Waitin' for a pirate's response..."):
            try:
                response = send_message_to_openai(combined_prompt, max_tokens, temperature, engine)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                response = ""

        if response:
            session_state.chat_history.append({"role": "pirate", "message": response})

chat_container = st.container()
for chat in session_state.chat_history:
    with chat_container:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-bubble">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="pirate-bubble">{chat["message"]}</div>', unsafe_allow_html=True)

