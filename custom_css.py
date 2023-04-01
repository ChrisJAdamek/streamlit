import streamlit as st

custom_css = """
<style>
  body {
    background-color: #000000;
    font-family: 'Courier New', monospace;
  }

  .stApp {
    padding: 2rem;
  }

  .chat-container {
    background-color: #000000;
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    overflow-y: scroll;
    height: 500px;
  }

  .message {
    color: #00ff00;
    white-space: nowrap;
    overflow: hidden;
  }

  .message span {
    display: inline-block;
    animation: typing 2s steps(30, end) forwards;
  }

  @keyframes typing {
    0% {
      width: 0;
    }
    100% {
      width: 100%;
    }
  }
</style>

"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True)
