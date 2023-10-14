import sys
import time

start = time.time()
if '--time=1' in sys.argv:
    print("Loading symptomInput.py...", end="\t")

import os
import pickle
import numpy as np

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'pickles/symptoms.pkl'), 'rb') as fl:
    symptoms_li = pickle.load(fl)

related_symptoms = {
    '': [],
    'skin': ['ithcing', 'skin rash', 'nodal skin eruption', 'swollen blood vessels', 'drying and tingling lips',
             'slurred speech', 'dyschromic patches', 'pus filled pimples', 'blackheads', 'skin peeling', 'blisters'],
    'uncategorised': ['continuous sneezing', 'vommiting', 'cough', 'high fever', 'breathlessness', 'shivering',
                      'dehydration', 'sweating', 'nausea', 'mild fever', 'fluid overload', 'ulcers on tongue',
                      'abnormal menstruation', 'fluid overload'],
    'uncategorisedV2': ['phlegm', 'mucoid sputum', 'rusty sputum', 'blood in sputum'],
    'body': ['shivering', 'chills', 'weight gain', 'weight loss', 'headache', 'yellowish skin', 'back pain', 'cramps',
             'bruising', 'weakness of one body side', 'internal itching', 'red spots over body'],
    'nails': ['small dents in nails', 'brittle nails', 'inflamatory nails'],
    'movement': ['loss of balance', 'unstediness', 'spinning movements', 'altered sensorium', 'painful walking',
                 'skurrying'],
    'muscles/joints': ['joint pain', 'muscle wasting', 'fatigue', 'muscle weakness', 'swelling joints', 'muscle pain'],
    'abdomen': ['stomach pain', 'acidity', 'indigestion', 'acute liver failure', 'abdominal pain',
                'swelling of stomach', 'chest pain', 'fast heart rate', 'obesity', 'belly pain', 'stomach bleeding',
                'distention of abdomen'],
    'eyes': ['sunken eyes', 'pain behind the eyes', 'yellowing of eyes', 'blurred and distorted vision',
             'redness of eyes', 'puffy face and eyes', 'watering from eyes', 'visual disturbances'],
    'limbs': ['swollen extremeties', 'cold hands and feets', 'weakness in limbs', 'knee pain', 'movement stiffness',
              'swollen legs', 'prominent veins on calf'],
    'facese': ['constipation', 'diarrhea', 'pain during bowel movements', 'pain in anal region', 'bloody stool',
               'irritation in anus', 'hip joint pain', 'passage of gasses'],
    'urine': ['burning micturition', 'spotting urination', 'dark urine', 'yellow urine', 'bladder discomfort',
              'foul smell of urine', 'continuous fell of urine', 'polyuria'],
    'behavioral': ['anxiety', 'mood swings', 'restlessness', 'lethargy', 'loss of appetite', 'malaise', 'dizziness',
                   'excessive hunger', 'depression', 'irritability', 'increased appetite', 'lack of concentration'],
    'throat': ['patches in throat', 'swelled lymph nodes', 'throat irritation', 'neck pain', 'enlarged thyroid',
               'stiff neck'],
    'history': ['irregular sugar levels', 'family history', 'receiving blood transfusion',
                'receiving unsterile injections', 'history of alcohol consumption'],
    'nose': ['sinus pressure', 'runny nose', 'congestion', 'loss of smell', 'red sore around nose']
}

related_symptoms_names = {
    '': [],
    'skin': ['ithcing', 'skin rash', 'nodal skin eruption', 'swollen blood vessels', 'drying and tingling lips',
             'slurred speech', 'dyschromic patches', 'pus filled pimples', 'blackheads', 'skin peeling', 'blisters'],
    'uncategorised': ['continuous sneezing', 'vommiting', 'cough', 'high fever', 'breathlessness', 'shivering',
                      'dehydration', 'sweating', 'nausea', 'mild fever', 'fluid overload', 'ulcers on tongue',
                      'abnormal menstruation', 'fluid overload'],
    'uncategorisedV2': ['phlegm', 'mucoid sputum', 'rusty sputum', 'blood in sputum'],
    'body': ['shivering', 'chills', 'weight gain', 'weight loss', 'headache', 'yellowish skin', 'back pain', 'cramps',
             'bruising', 'weakness of one body side', 'internal itching', 'red spots over body'],
    'nails': ['small dents in nails', 'brittle nails', 'inflamatory nails'],
    'movement': ['loss of balance', 'unstediness', 'spinning movements', 'altered sensorium', 'painful walking',
                 'skurrying'],
    'muscles/joints': ['joint pain', 'muscle wasting', 'fatigue', 'muscle weakness', 'swelling joints', 'muscle pain'],
    'abdomen': ['stomach pain', 'acidity', 'indigestion', 'acute liver failure', 'abdominal pain',
                'swelling of stomach', 'chest pain', 'fast heart rate', 'obesity', 'belly pain', 'stomach bleeding',
                'distention of abdomen'],
    'eyes': ['sunken eyes', 'pain behind the eyes', 'yellowing of eyes', 'blurred and distorted vision',
             'redness of eyes', 'puffy face and eyes', 'watering from eyes', 'visual disturbances'],
    'limbs': ['swollen extremeties', 'cold hands and feets', 'weakness in limbs', 'knee pain', 'movement stiffness',
              'swollen legs', 'prominent veins on calf'],
    'facese': ['constipation', 'diarrhea', 'pain during bowel movements', 'pain in anal region', 'bloody stool',
               'irritation in anus', 'hip joint pain', 'passage of gasses'],
    'urine': ['burning micturition', 'spotting urination', 'dark urine', 'yellow urine', 'bladder discomfort',
              'foul smell of urine', 'continuous fell of urine', 'polyuria'],
    'behavioral': ['anxiety', 'mood swings', 'restlessness', 'lethargy', 'loss of appetite', 'malaise', 'dizziness',
                   'excessive hunger', 'depression', 'irritability', 'increased appetite', 'lack of concentration'],
    'throat': ['patches in throat', 'swelled lymph nodes', 'throat irritation', 'neck pain', 'enlarged thyroid',
               'stiff neck'],
    'history': ['irregular sugar levels', 'family history', 'receiving blood transfusion',
                'receiving unsterile injections', 'history of alcohol consumption'],
    'nose': ['sinus pressure', 'runny nose', 'congestion', 'loss of smell', 'red sore around nose']
}

i = 1
msg = []

for li in related_symptoms.values():
    response = ""
    for idx, symptom in enumerate(li):
        response += str(f"{idx + 1}: {symptom}" + "\t")
    msg.append(response)

inp = []


def get_feature_input(inp_=None, done=False):
    global i, inp

    try:
        response = msg[i]
    except IndexError:
        i += 1
        response = ""

    if inp_ is not None:
        try:
            inp.append(list(int(item.strip()) for item in str(inp_).split(",")))
        except ValueError:
            inp.append([])
    else:
        inp.append([])

    i += 1
    return response, i


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
