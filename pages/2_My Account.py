import streamlit as st
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyA3WPDfbN3X1CnuP1CtFv03dIM-ziN0_pA",
    "authDomain": "cassadoc-8ed54.firebaseapp.com",
    "databaseURL": "https://cassadoc-8ed54-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "cassadoc-8ed54",
    "storageBucket": "cassadoc-8ed54.appspot.com",
    "messagingSenderId": "81127139191",
    "appId": "1:81127139191:web:c1d12aae17717660dd6372",
    "measurementId": "G-0Y8CJPJCGN"
    };

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

st.set_page_config(page_title="CassaDoc", page_icon=":page_with_curl:", layout="wide",initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
})

if st.session_state['loggedIn'] == True: 
    st.title("Account Profile")
    

else:
    st.error("Login Required to use this page")
