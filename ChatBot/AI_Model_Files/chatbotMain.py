import time
start = time.time()

import os
import random
import json
import pickle
import numpy as np
import sys

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

from .similarityGetter import get_similarity
from .modelFunction import pred_with_model
from .getAsked import get_asked
from .wikipediaFuncs import get_content
from .symptomInput import get_feature_input

end = time.time()

if '--no-time' not in sys.argv:
    print(f"Total time taken: {round(end-start)/10}s")

dirname = os.path.dirname(__file__)

lematizer = WordNetLemmatizer()
intents = json.loads(open(os.path.join(dirname, "jsons/intents.json")).read())

words = pickle.load(open(os.path.join(dirname, 'pickles/words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join(dirname, 'pickles/classes.pkl'), 'rb'))

disease_list = pickle.load(open(os.path.join(dirname, 'pickles/disease_list.pkl'), 'rb'))
symptoms_list = pickle.load(open(os.path.join(dirname, 'pickles/symptom_names.pkl'), 'rb'))

model = load_model(os.path.join(dirname, 'Model/chatbot_model.h5'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]

    ERROR_THRESHOLD = 0.25

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result, tag


diseases_asked_memory = []

def get_output(inp: str):
    if inp.lower() not in ['quit', 'q']:
        intents_li = predict_class(inp.lower())
        response, tag = get_response(intents_li, intents)

        if tag == "tell_about_disease":
            response = ""
            diseases, cats = get_asked(inp)

            if len(diseases_asked_memory) > 3:
                diseases_asked_memory.pop(1)

            if diseases[0] in ['it', 'their', 'its']:
                diseases = diseases_asked_memory[-1]
            else:
                diseases_asked_memory.append(diseases)

            for disease in diseases:
                response += str(disease).capitalize() + ":\n"
                for cat in cats:
                    response += ". ".join(get_content(disease, cat)) + "\n\n"

        if tag == "predict_disease":
            features = get_feature_input()
            predictions = pred_with_model(features)

            if len(predictions) == 1:
                response = f"\nYou most likely suffer from {predictions[0]}"
            elif len(predictions) == 2:
                response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
            else:
                response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[1:-1]} or {predictions[-1]}"

        return response

