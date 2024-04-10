import streamlit as st
import random
import json
import pickle
import numpy as np
import nltk
import keras
# from gpt4all import GPT4All
from nltk.stem import WordNetLemmatizer 
from tensorflow.keras.models import load_model
nltk.download()
lemmatizer = WordNetLemmatizer()

# gpt = GPT4All(model_name="wizardlm-13b-v1.2.Q4_0.gguf")
# Creating the Session
if "messages" not in st.session_state:
    st.session_state.messages=[]

st.set_page_config(page_title="Chat-express",layout='wide',page_icon="./Videos/logo.png")

# Load intents
intents = json.loads(open('insten2.json').read())

# Load pre-trained model and other necessary files
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("chars.pkl",'rb'))
model = load_model('chatbot_model_ecom.h5')

def clean_up_sentence(sent):
    sentence = nltk.word_tokenize(sent)
    sentence = [lemmatizer.lemmatize(w).lower() for w in sentence]
    return sentence    

def bag_of_words(sent):
    sentence_words = clean_up_sentence(sent)
    bag=[0]*len(words)
    for w in sentence_words:
        for i , word in enumerate(words):
            if(word == w):
                bag[i]=1
    return np.array(bag)

def predict_classes(sent):
    bow = bag_of_words(sent)
    res=model.predict([np.array([bow])])[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x:x[1],reverse=True)

    return_list = []

    for r in results:
        return_list.append({'intent': classes[r[0]],'prob': str(r[1])})

    return return_list

def get_response(intent_list,intent_json):
    tag = intent_list[0]['intent']
    list_of_intents=intent_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result = random.choice(i['responses'])
            print(result)
            break
    return result


st.title("Chat Express")

st.text("Go! Bot is Activated")

for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get('content'))

msg = st.chat_input("Enter message:")

if msg:
    st.session_state.messages.append({'role':'user','content':msg})
    with st.chat_message("user"):
        st.write(msg)
    ints = predict_classes(str(msg))
    res = get_response(ints, intents) 

    # rugp = gpt.generate(prompt=str(msg),temp=0.5)

    # st.session_state.messages.append({'role':'assistant', 'content':res+'\n\n'+rugp})
    st.session_state.messages.append({'role':'assistant', 'content':res})
    with st.chat_message("assistant"):
        # st.write(res+"----"+rugp)
        st.write(res)
else:
    with st.chat_message("assistant"):
        st.write("How may i help You")





