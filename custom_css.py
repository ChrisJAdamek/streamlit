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

st.markdown("<link href='https://fonts.googleapis.com/css?family=Pirata+One' rel='stylesheet'>", unsafe_allow_html=True
