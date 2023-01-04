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
from textblob import TextBlob
from collections import defaultdict




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

nlp = spacy.load("en_core_web_md")

if st.session_state['loggedIn'] == True:

    def extract_named_entities(text):
        
        doc = nlp(text)
        ent_html = displacy.render(doc, style='ent', jupyter=False)
        st.markdown(ent_html, unsafe_allow_html=True)

    def show_sentiment(text):
        # Calculate the sentiment of the text using TextBlob
        sentiment = TextBlob(text).sentiment

        # Return the polarity and subjectivity as a tuple
        return sentiment.polarity, sentiment.subjectivity

    def show_summary(text,summary_length):
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
    
    def extract_keywords(text, num_keywords):
    # Tokenize the text and create a set of stopwords
        doc = nlp(text)
        stopwords = set(nlp.Defaults.stop_words)

        # Initialize a defaultdict with a default factory function that returns 0
        freq_dist = defaultdict(lambda: 0)

        # Iterate through the tokens (words and punctuation) in the document
        for token in doc:
            # If the token is a stopword or punctuation, skip it
            if token.text in stopwords or token.is_punct:
                continue
            # If the token has a noun or verb part-of-speech, increment its frequency in the frequency distribution
            if token.pos_ in ['NOUN', 'VERB']:
                freq_dist[token.text] += 1

        # Sort the frequency distribution by frequency in descending order
        sorted_freq_dist = sorted(freq_dist.items(), key=lambda item: item[1], reverse=True)

        # Return the top num_keywords keywords
        return sorted_freq_dist[:num_keywords]

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
            if option == "Keyword Extraction":
                with st.sidebar:
                    num_keywords = st.slider("Number of top keywords:", 1, 20, 5)

            # Add a submit button
            if st.button("Submit"):
                
                # Perform selected option
                if option == "Named Entity Recognition":
                    extract_named_entities(text)
                elif option == "Sentiment Analysis":
                    show_sentiment(text)
                    polarity, subjectivity = show_sentiment(text)
                    # Display the sentiment values
                    st.write("Polarity:", polarity)
                    st.write("Subjectivity:", subjectivity)
                    # Add some text to explain what the values mean in more detail
                    st.success("Polarity is a value from -1 (most negative) to 1 (most positive) that indicates the sentiment of the text. A polarity of -1 means that the text has a negative sentiment,"
                    + " a polarity of 0 means that the text is neutral or factual, and a polarity of 1 means that the text has a positive sentiment. Subjectivity is a value from 0 (completely objective) "
                    + "to 1 (completely subjective) that indicates the amount of personal opinion in the text. A subjectivity of 0 means that the text is completely objective and based on facts," + 
                    "a subjectivity of 0.5 means that the text is balanced between facts and opinions, and a subjectivity of 1 means that the text is completely subjective and based on personal opinions.")
                elif option == "Text Summarization":
                    show_summary(text,summary_length)
                elif option == "Keyword Extraction":
                    keywords = extract_keywords(text, num_keywords)
                    # Output the keywords and their occurrences vertically
                    for keyword, freq in keywords:
                        st.info(f"{keyword}: {freq}")
if __name__ == "__main__":
        main()


else:
    st.error("Login Required to use this page")
