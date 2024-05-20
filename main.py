import streamlit as st
from utils import *

hide_sidebar()

st.title("Welcome to the uesr study! Please enter your participant ID")
participant_id = st.text_input("**Participant ID:**")

if st.button("Submit"):
    if len(participant_id) > 0:
        st.session_state['id'] = participant_id
        st.switch_page("pages/questions.py")