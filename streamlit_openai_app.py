import os
import requests
import streamlit as st
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_pre_prompt():
    return '''You are a scholar of logical reasoning. You specialize in propositional logic. Your job is to critically analyze the thesis statement submitted by students and provide advice on the logical validity and soundness of the thesis. Let's take this step by step as follows:

1. Print: "Please submit your thesis statement for review."
2. When the student submits a thesis statement, print: "Validity and Soundness of Thesis Statement".
3. List of all propositions contained in the thesis statement (noting whether each is a premise or a conclusion).
4. List anyunstated assumptions underlying the argument.
5. For each premise and unstated assumption,print a heading "[the premise/assumption statements]" and then:

List the key concepts that are necessary to understand the [premise/assumption] (including technical terms, subject background, and any relevant academic theories).
Print: "This [premise/assumption] is sound because [insert a list of two or more true statements that each prove or infer the truth of the premise/assumption]".
Print: "This [premise/assumption] may be unsound because [insert a list of two or more true statement that each disprove or undermine the truth of the premise/assumption]".
Print: "This [premise/assumption] can be tested by [insert list of two or more empirical methods for testing the truth of the premise/assumption]".'''

@st.cache_data(show_spinner=False)
def send_message_to_openai(prompt, user_message, max_tokens, temperature, engine):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}'
    }

    data = {
        'model': engine,
        'messages': [{"role": "system", "content": get_pre_prompt()}, {"role": "user", "content": user_message}],
        'max_tokens': max_tokens,
        'n': 1,
        'temperature': temperature,
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"Error details: {e.response.text}")
        return ""

st.set_page_config(page_title="Thesis Review", layout="wide")


def update_session_state_user_input():
    st.session_state.user_input = st.text_area("Enter your message:", value=st.session_state.user_input, key="user_input")

def main():
    with st.form(key='message_form'):
        user_message = st.text_area("Enter your message:", value=st.session_state.user_input, key="user_input")
        submit_button = st.form_submit_button("Send")
        st.markdown("""<style>
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
            }
        </style>""", unsafe_allow_html=True)

    cols = st.columns(2)
    chat_container = cols[0].container()
    with chat_container:
        st.write('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.write(f'<div class="message"><span>{chat["message"]}</span></div>', unsafe_allow_html=True)
            else:
                st.write(f'<div class="message"><span>{chat["message"]}</span></div>', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

    control_container = cols[1].container()
    with control_container:
        with st.expander("Advanced Settings", expanded=False):
            max_tokens = st.slider("Max tokens:", min_value=10, max_value=1000, value=100, step=10)
            temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
            engine = st.selectbox(
                "Select a language model:",
                (
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-4-32k",
                ),
            )

    return user_message, submit_button, max_tokens, temperature, engine

if __name__ == "__main__":
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    user_message, submit_button, max_tokens, temperature, engine = main()

if submit_button:
    if user_message:
        st.session_state.chat_history.append({"role": "user", "message": user_message})
        combined_prompt = f"{get_pre_prompt()} {user_message}"
        with st.spinner("Waitin' for a pirate's response..."):
            try:
                response = send_message_to_openai(combined_prompt, user_message, max_tokens, temperature, engine)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                response = ""

        if response:
            st.session_state.chat_history.append({"role": "pirate", "message": response})

            # Clear the user message input by directly setting the value of the text area widget to an empty string
            user_message = ""
            st.experimental_rerun()
