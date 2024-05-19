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
    save_ans_to_file(st.session_state['res'], FILENAME)
    upload_file_to_dropbox(FILENAME, '/results/' + FILENAME)
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
    col1, col2 = st.columns(2)
    col1.write('No. 1')
    col1.image(img1)
    col2.write('No. 2')
    col2.image(img2)


if st.session_state['stage'] >= 2:
    st.write()
    select = st.radio(label=r"$\textsf{\Large Which hand pose requires more effort?:}$", options=["No.1", "No.2"], index=None)
    if st.button('Confirm'):
        if select == None:
            st.write(":red[Please make a selection.]")
        else:
            current_q = str(st.session_state['current_q'] + 1)
            st.session_state['res'].append([current_q + '_' + str(img[0]) + str(img[1]), select])
            st.session_state['stage'] = 0
            st.session_state['current_q'] += 1
            st.rerun()
else:
    if st.button('Next'):
        st.session_state['stage'] += 1
        st.rerun()