import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import LabelEncoder

import pandas as pd
import os
import joblib

dirname = os.path.dirname(__file__)

data_path_default = os.path.join(dirname, './dataSet/Training.csv')


class Center(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.mean_ = X.mean()
        return self

    def transform(self, X):
        X_transformed = X - X.mean()
        return X_transformed


def fitModel(data_path=data_path_default):
    global final_pipeline, labelEnc

    data = pd.read_csv(data_path)

    X = data.iloc[:, :-2]
    y = data.iloc[:, -2]

    labelEnc = LabelEncoder()
    labelEnc.fit(y)
    y = labelEnc.transform(y)

    X = np.array(X)
    y = np.array(y)

    votingClf = VotingClassifier(estimators=[
        ('SVC', SVC(probability=True)),
        ('DecisionTree', DecisionTreeClassifier(max_leaf_nodes=10)),
        ('LogisticRegressor', LogisticRegression()),
    ], voting='soft')

    final_pipeline = Pipeline([
        ('Center', Center()),
        ('kPCA', KernelPCA(n_components=60, kernel='rbf', gamma=0.05)),
        ('VotingClf', votingClf),
    ])

    final_pipeline.fit(X, y)
    return final_pipeline, labelEnc


def modelDump(association, final_pipeline, labelEnc):
    pipeline_name = f'final_pipeline_{association}.joblib'
    labelEnc_name = f'labelEnc_{association}.joblib'

    with open(os.path.join(dirname, f'Model/{pipeline_name}'), 'wb') as fl:
        joblib.dump(final_pipeline, fl)

    with open(os.path.join(dirname, f'Model/{labelEnc_name}'), 'wb') as fl:
        joblib.dump(labelEnc, fl)
