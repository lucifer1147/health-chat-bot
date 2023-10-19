import json
import os

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

related_symptoms_descriptions = {
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

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, './jsons/related_symptoms.json'), 'w', encoding='utf-8') as rs:
    json.dump(related_symptoms, rs)
with open(os.path.join(dirname, './jsons/related_symptoms_names.json'), 'w', encoding='utf-8') as rsn:
    json.dump(related_symptoms_names, rsn)
with open(os.path.join(dirname, './jsons/related_symptoms_descriptions.json'), 'w', encoding='utf-8') as rsd:
    json.dump(related_symptoms_descriptions, rsd)
