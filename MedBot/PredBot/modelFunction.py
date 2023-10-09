import sys
import time
start = time.time()
if '--time=1' in sys.argv:
    print("Loading modelFunction.py...", end="\t")

import os
import joblib
import pickle
import numpy
import pandas

dirname = os.path.dirname(__file__)

def load_model(association: str):

    global model, label_enc, diseases

    pipeline_name = f'final_pipeline_{association}.joblib'
    labelEnc_name = f'labelEnc_{association}.joblib'

    try:
        with open(os.path.join(dirname, f'Model/{pipeline_name}'), 'rb') as fl:
            model = joblib.load(fl)
        with open(os.path.join(dirname, f'Model/{labelEnc_name}'), 'rb') as fl:
            label_enc = joblib.load(fl)

    except FileNotFoundError:
        from .finalModel import fitModel, modelDump
        final_pipeline, labelEnc = fitModel(os.path.join(dirname, './dataSet/Training.csv'))
        modelDump(association, final_pipeline, labelEnc)


    with open(os.path.join(dirname, 'pickles/disease_list.pkl'), 'rb') as fl:
        diseases = pickle.load(fl)
        diseases = numpy.array(diseases).reshape(1, -1)

    return model, label_enc, diseases


def pred_with_model(input_features, model, labelEnc, diseases):
    prediction = model.predict_proba(input_features)
    output_results = 5-len(numpy.argwhere(input_features == 1))
    output_results = output_results if output_results>0 else 1

    prediction = numpy.array(pandas.DataFrame(numpy.c_[diseases.reshape(-1, 1), prediction.reshape(-1, 1)]).sort_values(by=1, ascending=False))[:output_results, 0]
    return list(prediction)


end = time.time()
if '--time=1' in sys.argv:
    print(f"Loaded modelFunction.py in {round(end-start)/10}s")
