import random
import json
import pickle
import numpy as np
import nltk
import keras

# work working works worked ---- work
from nltk.stem import WordNetLemmatizer


from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
# from tensorflow.keras.optimizers import SGD
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('insten2.json').read())
# print(intents)

words=[]
classes=[]
documents=[]
ignore_words = ['?',"!",".",","]
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the pattern
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))

        if(intent['tag'] not in classes):
            classes.append(intent['tag'])

# print("Documents",documents)
# print("Words",words)

words=[lemmatizer.lemmatize(word) for word in words if word not in ignore_words]

# eliminate duplicate
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('chars.pkl','wb'))

# training the ChatBot

training =[]
output_empt = [0]*len(classes)

for doc in documents:
    bag = []
    word_pattern = doc[0]
    word_pattern=[lemmatizer.lemmatize(w.lower()) for w in word_pattern]
    for w in words:
        if w in word_pattern:
            bag.append(1)
        else:
            bag.append(0)
    output_row = list(output_empt)
    output_row[classes.index(doc[1])]=1
    training.append([bag,output_row])

random.shuffle(training)
training = np.array(training,dtype=object)
# print(training)
train_x = list(training[:,0])
train_y = list(training[:,1])

# build Neural network 
model = Sequential()
model.add(Dense(126,input_shape=(len(train_x[0]),),activation='relu'))
# prevent overfitting
model.add(Dropout(0.5))

model.add(Dense(64,activation='relu'))
model.add(Dropout(0.3))

model.add(Dense(len(train_y[0]),activation='softmax'))
# compile and train

# sgd=SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5,verbose=1)
# model.save("chatbot_model.model")
model.save("chatbot_model_ecom.h5")
print('Model saved')