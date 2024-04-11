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
import sqlite3
import re

conn = sqlite3.connect('data.db')
c = conn.cursor()   


lemmatizer = WordNetLemmatizer()

# gpt = GPT4All(model_name="wizardlm-13b-v1.2.Q4_0.gguf")
# Creating the Session
if "messages" not in st.session_state:
    st.session_state.messages=[]

st.set_page_config(page_title="Chat-express",layout='wide',page_icon="./Videos/logo.png")

# Load intents
intents = json.loads(open('insten2.json').read())
# intents = json.loads(open('insten.json').read())

# Load pre-trained model and other necessary files
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("chars.pkl",'rb'))
model = load_model('chatbot_model_ecom.h5')


def extract_order_id(message):
    pattern = r'\b[A-Z0-9]{8}\b'

    match = re.search(pattern, message, re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        return None
def retrieve_order(order_id):
    c.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    return c.fetchone()

iphone_13_info = c.fetchall()
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

def get_response(intent_list,intent_json,msg):
    tag = intent_list[0]['intent']
    list_of_intents=intent_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result = random.choice(i['responses'])
            if tag == 'order_tracking':
                orderid = extract_order_id(msg)
                order_info = retrieve_order(orderid)
                print("order id -----",orderid)
                print("order info -----",order_info)
                if order_info:
                    # If order information is found, include it in the response
                    result += f"\n\nYour order with ID {orderid} will be delivereed at {order_info[2]}."
                elif orderid == None:
                    result += "\n\nSorry, please provide me order ID."
                else:
                    result += "\n\nSorry, I couldn't find any information for that order ID."
            
                    
            break
    return result


st.header("Chat Express 🤖",divider='rainbow')
multi = '''Hi there! 👋 I'm your personal shopping assistant, here to make your e-commerce experience smoother and more enjoyable.'''

st.markdown(multi)
st.markdown('- **:blue[Product Information]:** "What are the specifications of the iPhone 13?')
st.markdown('- **:blue[Order Status]:** Where is my order #123456?')
st.markdown('- **:blue[Returns and Exchanges]:** How can I return an item?')
st.markdown('- **:blue[Promotions and Discounts]:** Are there any ongoing sales?')
st.markdown('- **:blue[Payment Assistance]:** Can I pay with PayPal?')

for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get('content'))

msg = st.chat_input("Enter message:")

if msg:
    st.session_state.messages.append({'role':'user','content':msg})
    with st.chat_message("user"):
        st.write(msg)
    ints = predict_classes(str(msg))
    res = get_response(ints, intents,msg) 

    # rugp = gpt.generate(prompt=str(msg),temp=0.5)s

    # st.session_state.messages.append({'role':'assistant', 'content':res+'\n\n'+rugp})
    st.session_state.messages.append({'role':'assistant', 'content':res})
    with st.chat_message("assistant"):
        # st.write(res+"----"+rugp)
        st.write(res)
else:
    with st.chat_message("assistant"):
        st.write("How may i help You")





