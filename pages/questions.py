import streamlit as st
from PIL import Image
from utils import *
from constant import *

if 'current_q' not in st.session_state:
    round, question = get_current_q()
    round = int(round)
    question = int(question)
    st.session_state['current_q'] = question
    st.session_state['round'] = round
if 'pairs' not in st.session_state:
    st.session_state['pairs'] = PAIRS
if 'stage' not in st.session_state:
    st.session_state['stage'] = 0
if 'res' not in st.session_state:
    st.session_state['res'] = []

if (st.session_state['current_q'] % 5) == 0 and st.session_state['stage'] == 0:
    local_file = st.session_state['id'] + '.csv'
    save_ans_to_file(st.session_state['res'], local_file)
    upload_file_to_dropbox(local_file, '/results/' + local_file)
    update_current_q()
    st.session_state['res'] = []

pair_num = st.session_state['current_q'] + 1
st.write(f"### Pair {pair_num}")

img = st.session_state['pairs'][st.session_state['current_q']]
img1 = 'poses/' + img[0] + '.png'
img2 = 'poses/' + img[1] + '.png'

if st.session_state['stage'] == 0:
    st.write('No. 1')
    st.image(img1)
elif st.session_state['stage'] == 1:
    st.write('No. 2')
    st.image(img2)
elif st.session_state['stage'] == 2:
    html_reminder = """
    <div style='background-color: #ff6347; color: #f0f2f6; padding: 10px;'>
        <strong>Please select only one option.</strong> If both are selected, No.1 will be recorded.
    </div>
    """
    st.markdown(html_reminder, unsafe_allow_html=True)
    st.write("### Which pose requires more effort?")
    col1, col2 = st.columns(2)
    col1.write('No. 1')
    col1.image(img1)
    col2.write('No. 2')
    col2.image(img2)


if st.session_state['stage'] >= 2:
    st.write()
    # select = st.radio(label=r"$\textsf{\Large Which hand pose requires more effort?:}$", options=["No.1", "No.2"], index=None)
    check_css = """
    <style>
    [data-baseweb="checkbox"] [data-testid="stWidgetLabel"] p {
        /* Styles for the label text for checkbox */
        font-size: 3.5rem;
        width: 600px;
        margin-top: 1rem;
    }

    [data-baseweb="checkbox"] div {
        /* Styles for the slider container */
        height: 3rem;
        width: 4rem;
    }
    [data-baseweb="checkbox"] div div {
        /* Styles for the slider circle */
        height: 2.8rem;
        width: 2.8rem;
    }
    [data-testid="stCheckbox"] label span {
        /* Styles the checkbox */
        height: 4rem;
        width: 4rem;
    }
    </style>
    """
    st.write(check_css, unsafe_allow_html=True)
    First = col1.checkbox("First Pose")
    Second = col2.checkbox("Second Pose")
    confirm_css = """
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
    st.write(confirm_css, unsafe_allow_html=True)
    if st.button('Confirm'):
        if First == False and Second == False:
            st.write(":red[Please make a selection.]")
        else:
            ans = ""
            if First: ans = "No.1"
            else: ans = "No.2"
            current_q = str(st.session_state['current_q'] + 1)
            st.session_state['res'].append([current_q + '_' + str(img[0]) + str(img[1]), ans])
            st.session_state['stage'] = 0
            st.session_state['current_q'] += 1
            st.rerun()
else:
    next_css = """
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
    st.write(next_css, unsafe_allow_html=True)
    if st.button('Next'):
        st.session_state['stage'] += 1
        st.rerun()
