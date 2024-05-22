import streamlit as st
import dropbox
import random
import csv

def hide_sidebar(set_wide=False):
    if set_wide:
        st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    else:
        st.set_page_config(initial_sidebar_state="collapsed")
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

def get_name(i):
    if i <= 17:
        return "B" + str(i)
    else:
        return "C" + str(i-17)

def get_current_q():
    download_file_from_dropbox('/info/current_q.csv', './current_q.csv')
    with open('./current_q.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            round = row['round']
            question = row['current_q']
            return round, question

def generate_pairs(items):
    pairs = []
    for i in range(1, items+1):
        for j in range(i+1, items+1):
            pairs.append([get_name(i), get_name(j)])

    for i in pairs:
        random.shuffle(i)
    random.shuffle(pairs)

    return pairs

def save_ans_to_file(ans, filename):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for i in ans:
            writer.writerow(i)

def update_current_q():
    update = [['round', 'current_q'],
              [st.session_state['round'], st.session_state['current_q']]]
    with open('./current_q.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(update)
    upload_file_to_dropbox('./current_q.csv', '/info/current_q.csv')

def upload_file_to_dropbox(file_path, dropbox_path):
    app_key = st.secrets["dropbox"]["app_key"]
    app_secret = st.secrets["dropbox"]["app_secret"]
    refresh_token = st.secrets["dropbox"]["refresh_token"]
    try:
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret
        )
        
        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    except Exception as e:
        print("Error during file upload:", e)

def download_file_from_dropbox(dropbox_path, local_path):
    app_key = st.secrets["dropbox"]["app_key"]
    app_secret = st.secrets["dropbox"]["app_secret"]
    refresh_token = st.secrets["dropbox"]["refresh_token"]
    try:
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret
        )
        
        with open(local_path, "wb") as f:
            metadata, response = dbx.files_download(dropbox_path)
            f.write(response.content)
            print("File downloaded:", metadata.path_display)
    except Exception as e:
        print("Error during file download:", e)


if __name__ == '__main__':
    # upload_file_to_dropbox('./current_q.csv', '/info/current_q.csv')
    # download_file_from_dropbox('/info/current_q.csv', './current_q.csv')
    # pass
    pairs = generate_pairs(40)
    print(len(pairs))
