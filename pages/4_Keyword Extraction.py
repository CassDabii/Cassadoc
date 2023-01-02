import streamlit as st
import pyrebase
import streamlit as st
import spacy
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest



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

    def extract_named_entities(text):
        nlp = spacy.load("en_core_web_md")
        doc = nlp(text)
        ent_html = displacy.render(doc, style='ent', jupyter=False)
        st.markdown(ent_html, unsafe_allow_html=True)

    def show_sentiment(text):
        nlp = spacy.load("en_core_web_md")
        nlp.add_pipe(SpacyTextBlob, name='spacytextblob')
        doc = nlp(text)
        doc._.blob.polarity                           
        doc._.blob.subjectivity                        
        doc._.blob.sentiment_assessments.assessments   
        doc._.blob.ngrams()
       
        st.write('Polarity:', round(doc._.sentiment.polarity, 2))
        st.write('Subjectivity:', round(doc._.sentiment.subjectivity, 2)) 


    def show_summary(text,summary_length):

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        len(list(doc.sents))
        keyword = []
        stopwords = list(STOP_WORDS)
        pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
        for token in doc:
            if(token.text in stopwords or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                keyword.append(token.text)
        freq_word = Counter(keyword)
        print(freq_word.most_common(5))
        type(freq_word)#
        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():  
            freq_word[word] = (freq_word[word]/max_freq)
        freq_word.most_common(5)

        sent_strength={}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent]+=freq_word[word.text]
                    else:
                        sent_strength[sent]=freq_word[word.text]

        # Use the value from the slider to determine the number of sentences in the summary
        summarized_sentences = nlargest(summary_length, sent_strength, key=sent_strength.get)

        final_sentences = [ w.text for w in summarized_sentences ]
        summary = ' '.join(final_sentences)
        st.info(summary)
    
    def extract_keywords(text):
        return

    def main():
        with st.spinner("Loading page due to NLP model..."):
            option = st.radio("Select an option:", ("Named Entity Recognition", "Sentiment Analysis", "Text Summarization", "Keyword Extraction"), horizontal= True)
            # Get user input
            text = st.text_area("Enter text or upload a file (PDF or TXT)")
            file = st.file_uploader("Or select a file (PDF or TXT)", type=["doc", "docx", "pdf", "txt"])

            # Process the text with spaCy

            if file is not None:
                text = file.getvalue()
                if not file.name.endswith('.txt'):
                    file.name += '.txt'
                    text = text.decode("utf-8")

            # Show options

            if option == 'Text Summarization':
                with st.sidebar:
                    summary_length = st.slider("Choose the summary length:", min_value=1, max_value=10, value=3)

            # Add a submit button
            if st.button("Submit"):
                
                # Perform selected option
                if option == "Named Entity Recognition":
                    extract_named_entities(text)
                elif option == "Sentiment Analysis":
                    show_sentiment(text)
                elif option == "Text Summarization":
                    show_summary(text,summary_length)
                elif option == "Keyword Extraction":
                    extract_keywords(text)
if __name__ == "__main__":
        main()


else:
    st.error("Login Required to use this page")


