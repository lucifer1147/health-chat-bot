import json
import pickle
import numpy as np
import random
import os

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

dirname = os.path.dirname(__file__)

def train():
    lemmatizer = WordNetLemmatizer()

    intents = json.loads(open(os.path.join(dirname, "jsons/intents.json")).read())

    words = []
    classes = []
    documents = []
    ignore_letters = ["?", "!", ",", "."]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent["tag"]))

            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))

    pickle.dump(words, open(os.path.join(dirname, 'pickles/words.pkl'), 'wb'))
    pickle.dump(classes, open(os.path.join(dirname, 'pickles/classes.pkl'), 'wb'))

    train = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        train.append([bag, output_row])


    random.shuffle(train)
    train = np.array(train, dtype='object')

    X = list(train[:, 0])
    y = list(train[:, 1])

    # print(X)
    # print(y)

    model = Sequential()
    model.add(Dense(128, input_shape=(len(X[0]), ), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(y[0], ), activation='softmax'))

    sgd = SGD(learning_rate=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(X), np.array(y), epochs=200, batch_size=5, verbose=1)
    model.save(os.path.join(dirname, 'Model/chatbot_model.h5'), hist)
    print('\nDone')
