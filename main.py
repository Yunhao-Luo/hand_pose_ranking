import streamlit as st
from utils import *

hide_sidebar()

st.title("Welcome to the uesr study! Please enter your participant ID")
id = get_user_id()
participant_id = st.text_input("**Participant ID:**", value=id)
submit_css = """
    <style>
    /* Styles for the button */
    .stButton>button {
        padding: 5rem 10rem;
    }

    /* Styles for the button text */
    .stButton>button span {
        font-size: 24px; /* Change the font size here */
    }
    </style>
    """
st.write(submit_css, unsafe_allow_html=True)
if st.button(label=r"$\textsf{\huge Submit}$"):
    if len(participant_id) > 0:
        st.session_state['id'] = participant_id
        st.switch_page("pages/questions.py")