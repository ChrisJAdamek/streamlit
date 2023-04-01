

import os
import requests
import streamlit as st
import openai
from streamlit.hashing import _CodeHasher
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def send_completion(prompt, max_tokens, temperature, engine):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0].text.strip()

def send_chat(prompt, max_tokens, temperature, engine):
    data = {
        'model': engine,
        'prompt': prompt,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'stop': "\n",
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}'
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    return response.json()['choices'][0]['text'].strip()

engine_options = {
    "gpt-4-32k": "GPT-4 32k",
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "text-davinci-003": "Davinci Text",
    "code-davinci-002": "Davinci Codex",
}

st.set_page_config(page_title="Pirate Chatbot", page_icon=":ship:", layout="wide")

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
        color: #4a4a4
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

session_id = CodeHasher().to_bytes(st.session_id)[:8]
chat_history_key = f"chat_history{session_id.hex()}"

if chat_history_key not in st.session_state:
    st.session_state[chat_history_key] = []

pre_prompt = '''You are a scholar of logical reasoning. You specialize in propositional logic. Your job is to critically analyze the thesis statement submitted by students and provide advice on the logical validity and soundness of the thesis. Let's take this step by step as follows:
1. Print: "Please submit your thesis statement for review."
2. When the student submits a thesis statement, print: "Validity and Soundness of Thesis Statement".
3. List of all propositions contained in the thesis statement (noting whether each is a premise or a conclusion).
4. List any unstated assumptions underlying the argument.
5. For each premise and unstated assumption, print a heading "[the premise/assumption statements]" and then:
   * List the key concepts that are necessary to understand the [premise/assumption] (including technical terms, subject background, and any relevant academic theories).
   * Print: "This [premise/assumption] is sound because [insert a list of two or more true statements that each prove or infer the truth of the premise/assumption]".
   * Print: "This [premise/assumption] may be unsound because [insert a list of two or more true statement that each disprove or undermine the truth of the premise/assumption]".
   * Print: "This [premise/assumption] can be tested by [insert list of two or more empirical methods for testing the truth of the premise/assumption]".'''

user_message = st.text_area("Enter your message:", key="user_input")

with st.expander("Advanced Settings", expanded=False):
    max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    engine = st.selectbox("Select a language model:", list(engine_options.values()), index=list(engine_options.keys()).index("gpt-3.5-turbo"))

if st.button("Send"):
    if user_message:
        chat_history = st.session_state[chat_history_key]
        combined_prompt = f"{pre_prompt} {user_message}"
        chat_history.append({"role": "user", "message": user_message})
        with st.spinner("Waitin' for a pirate's response..."):
            if engine == "code-davinci-002":
                response = send_chat(combined_prompt, max_tokens, temperature, engine)
            else:
                response = send_completion(combined_prompt, max_tokens, temperature, engine)
        if response:
            chat_history.append({"role": "pirate", "message": response})

        st.session_state[chat_history_key] = chat_history

chat_history = st.session_state[chat_history_key]

if len(chat_history) > 0:
    with st.container():
        for chat in chat_history:
            if chat["role"] == "user":
                st.write(f"User: {chat['message']}")
            else:
                st.write(f"Pirate: {chat['message']}")
