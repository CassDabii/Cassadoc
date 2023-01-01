import streamlit as st
import pyrebase
import streamlit as st
import spacy
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob




firebaseConfig = {
  'apiKey': "AIzaSyA3WPDfbN3X1CnuP1CtFv03dIM-ziN0_pA",
  'authDomain': "cassadoc-8ed54.firebaseapp.com",
  'databaseURL': "https://cassadoc-8ed54-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "cassadoc-8ed54",
  'storageBucket': "cassadoc-8ed54.appspot.com",
  'messagingSenderId': "81127139191",
  'appId': "1:81127139191:web:c1d12aae17717660dd6372",
  'measurementId': "G-0Y8CJPJCGN"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

MAX_FILE_SIZE = 4096 * 4096 


if st.session_state['loggedIn'] == True:

    
    nlp = spacy.load("en_core_web_md")

    def extract_named_entities(text):
        doc = nlp(text)
        ent_html = displacy.render(doc, style='ent', jupyter=False)
        st.markdown(ent_html, unsafe_allow_html=True)

    def show_sentiment(text):
        nlp.add_pipe(SpacyTextBlob, name='spacytextblob')
        doc = nlp(text)
        doc._.blob.polarity                           
        doc._.blob.subjectivity                        
        doc._.blob.sentiment_assessments.assessments   
        doc._.blob.ngrams()
       
        st.write('Polarity:', round(doc._.sentiment.polarity, 2))
        st.write('Subjectivity:', round(doc._.sentiment.subjectivity, 2)) 

    def show_summary(text):
        return
    
    def extract_keywords(text):
        return

    def main():
        # Get user input
        text = st.text_area("Enter text or upload a file (PDF or TXT)")
        file = st.file_uploader("Or select a file (PDF or TXT)", type=["doc", "docx", "pdf", "txt"])

        # Process the text with spaCy
        if file is not None:
            text = file.getvalue()
            text = text.decode("utf-8")

        # Show options
        option = st.radio("Select an option:", ("Named Entity Recognition", "Sentiment Analysis", "Text Summarization", "Keyword Extraction"))
        
        # Add a submit button
        if st.button("Submit"):

          # Perform selected option
          if option == "Named Entity Recognition":
              extract_named_entities(text)
          elif option == "Sentiment Analysis":
              show_sentiment(text)
          elif option == "Text Summarization":
              show_summary(text)
          elif option == "Keyword Extraction":
              extract_keywords(text)
    if __name__ == "__main__":
        main()


      
else:
    st.error("Login Required to use this page")


