import streamlit as st
import pickle
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# import nltk
# nltk.download('punkt')

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    stp = stopwords.words('english')
    for i in text:
        if i not in stp and i not in string.punctuation:
            y.append(i)   

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

############Banned Keywords#######################
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def check_banned(input_sms, banned_keywords):
    banned_keywords = banned_keywords.lower()
    banned_keywords = nltk.word_tokenize(banned_keywords)
    input_sms = input_sms.lower()
    input_sms = nltk.word_tokenize(input_sms)
    # bn_key =
    
    ls = []
    for i in banned_keywords:
        if i not in string.punctuation:
            ls.append(i)
    if len(ls) == 0: return False
    # st.header(ls)
    for i in input_sms:
        if i in ls:
            return True
    return False

banned_keywords = st.text_input("Banned Keywords", "")


#######################################

############Allowed Keywords#######################


def check_allowed(input_sms, allowed_keywords):
    allowed_keywords = allowed_keywords.lower()
    allowed_keywords = nltk.word_tokenize(allowed_keywords)
    input_sms = input_sms.lower()
    input_sms = nltk.word_tokenize(input_sms)
    # bn_key =
    
    ls = []
    for i in allowed_keywords:
        if i not in string.punctuation:
            ls.append(i)
    if len(ls) == 0: return True
    # st.header(ls)
    for i in input_sms:
        if i in ls:
            return False
    return True

allowed_keywords = st.text_input("Allowed Keywords", "")


#######################################

if st.button('Predict'):

    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # st.header("Spam")
    # print(transformed_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    
    ##Extra check
    if result == 0: 
        result = check_banned(input_sms, banned_keywords)

    if result == 1:
        result = check_allowed(input_sms, allowed_keywords)

    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
