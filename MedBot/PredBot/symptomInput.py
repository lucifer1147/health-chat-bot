import json
import sys
import time
import os
import pickle
import numpy as np

start = time.time()
if '--time=1' in sys.argv:
    print("Loading symptomInput.py...", end="\t")


dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'pickles/symptoms.pkl'), 'rb') as fl:
    symptoms_li = pickle.load(fl)

with open(os.path.join(dirname, 'jsons/related_symptoms.json'), 'r') as fl:
    related_symptoms = json.load(fl)
with open(os.path.join(dirname, 'jsons/related_symptoms_names.json'), 'r') as fl:
    related_symptoms_names = json.load(fl)
with open(os.path.join(dirname, 'jsons/related_symptoms_descriptions.json'), 'r') as fl:
    related_symptoms_descriptions = json.load(fl)

i = 1
msg = []

for li in related_symptoms.values():
    response = ""
    for idx, symptom in enumerate(li):
        response += str(f"{idx + 1}: {symptom}" + "\t")
    msg.append(response)

inp = []


def get_features(feats: list = None):
    if feats is None:
        global i, inp
        i = 1
        symptoms = []
        for idx in range(len(related_symptoms.values())):
            cur_li = list(related_symptoms.values())[idx]
            cur_inp = inp[idx]

            try:
                for num in cur_inp:
                    symptoms.append(cur_li[num - 1])
            except IndexError as ve:
                print(cur_li, cur_inp, ve, len(inp), sep="\n")
    else:
        symptoms = feats

    feature_array = np.zeros(len(symptoms_li))
    for idx, item in enumerate(symptoms_li):
        if item in symptoms:
            feature_array[idx] = 1

    inp = []
    return feature_array.reshape(1, -1)


end = time.time()
if '--time=1' in sys.argv:
    print(f"Loaded symptomInput.py in {round(end - start) / 10}s")
