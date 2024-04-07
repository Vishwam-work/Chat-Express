import random
import json
import pickle
import numpy as np
import nltk
import keras
import streamlit as st

from nltk.stem import WordNetLemmatizer 

# to load the model
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('insten.json').read())

# use the word classes models

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("chars.pkl",'rb'))

model = load_model('chatbot_model.h5')


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

# predict fun

def predict_classes(sent):
    bow = bag_of_words(sent)
    res=model.predict([np.array([bow])])[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x:x[1],reverse=True)
    # sort the prob by the reverse order 

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
            break
    return result

print("Go! Bot is Activated")

while True:
    msg = input("Enter -> ")
    if msg=='bye':
        break
    ints = predict_classes(msg)
    res = get_response(ints,intents)
    print('CHAT-EXPRESS:',res)