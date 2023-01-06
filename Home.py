import pyrebase
import streamlit as st
import re

st.set_page_config(page_title="CassaDoc", page_icon=":page_with_curl:", layout="wide",initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
})

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

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()

def mainpage():    
    with mainSection:
        st.subheader("What is CassDoc and how does it work?")
        st.write("CassDoc is a web application that allows users to easily create technical specifications for their products or projects. It provides a user-friendly interface for users to enter relevant information, such as project name, description, and tech stack. The app then generates a professional PDF document containing this information, which users can download or view as needed.")
        st.write("In addition to creating technical specifications, CassDoc also offers a keyword extraction function. This function allows users to extract key words from input text or uploaded PDFs, making it easier to identify and focus on the most important aspects of a project or product.")
        st.write("To use CassDoc, users will need to create an account and log in to the app. They can then access all of the app's features and view a list of all the technical specs they have created. If needed, users can also reset their password through the app.")
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Features Prospectus")
            st.write("##")
            st.write("● Technical specification creation: Users can create new technical specifications by entering relevant data into various fields. They can save their progress and return to the specification later if needed.")
            st.write("● PDF generation: Once a technical specification is complete, users can generate a professional PDF document containing the specification information. The PDF includes a header with the product name and other relevant information.")
            st.write("● View specification list: Users will be able to view a list of all the technical specs they have created. They will be able to click on each specification to view it in more detail or download it as a PDF.")
            st.write("● Edit and delete specifications: Users will be able to edit and delete their technical specifications if needed. They will be able to make changes to the specification data and save the changes, or delete the specification entirely.")
            st.write("● Regular updates: The app will receive regular updates to add new features, improve performance, and fix any bugs that are discovered.")
            st.write("---")
        with right_column:
            st.header("Why this app was made?")
            st.write("This app was made to provide a simple and efficient way for users to create professional-quality technical specifications. By streamlining the specification creation process, " +
             "users can save time and effort and focus on other important tasks. The app's keyword extraction function can also be a useful tool for extracting key words and concepts from text and PDF documents.")

def login_form():
    with loginSection:
        # Get the form selected by the user
        form = st.selectbox("Choose an option: ", ["Login", "Create account", "Reset password"])

        if form == "Login":
                # Get email and password from the user
                email = st.text_input("Email")
                password = st.text_input("Password", type='password')

                # Try to sign in with email and password
                if st.button("Login"):
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                    except Exception as e:
                        # Display error message
                        st.error(str(e))
                    else:
                        # Sign-in successful
                        st.success("Sign-in successful")
                        # Update session state
                        st.session_state['loggedIn'] = True

        elif form == "Create account":
            # Get email, password, and password confirmation from the user
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')
            password_confirm = st.text_input("Confirm password", type='password')

            if st.button("Create Account"):
                # Check if passwords match
                if password != password_confirm:
                    st.error("Passwords do not match")
                    return

                # Check if email is valid
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    st.error("Invalid email")
                    return

                # Check if password meets criteria (8 characters, 1 capital letter, 1 special character)
                if not (any(c.isupper() for c in password) and any(c.isdigit() for c in password) and len(password) >= 8):
                    st.error("Password must be at least 8 characters long and contain at least 1 capital letter and 1 special character")
                    return

                # Try to create a new account with email and password
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                except Exception as e:
                    if "EMAIL_EXISTS" in str(e):
                        st.error("A user with this email already exists")
                    else:
                        st.error(e)
                else:
                    # Check if account was created
                    try:
                        account_info = auth.get_account_info(user['idToken'])
                    except Exception as e:
                        st.error("Account not created: {}".format(e))
                    else:
                        st.success("Account created for {}".format(email))


        elif form == "Reset password":
            # Get email from the user
            email = st.text_input("Email")
            if st.button("Reset password"):
                

                # Try to reset the password for the given email
                try:
                    auth.send_password_reset_email(email)
                except Exception as e:
                    # Display error message
                    st.error(str(e))
                else:
                    # Password reset email sent successfully
                    st.success("Password reset email sent")


# Create a function to handle logging out
def logout():
    st.session_state['loggedIn'] = False
    st.success("Logged Out")

def show_logout_button():
    with st.sidebar:
        st.button ("Log Out", key="logout", on_click=logout)

with headerSection:
    st.title("CassaDoc")
    #first run will have nothing in session_state
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        login_form()
    else:
        if st.session_state['loggedIn']:
            show_logout_button()
            mainpage()
        else:
            login_form()
