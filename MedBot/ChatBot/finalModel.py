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

dirname = os.path.dirname(__file__)

train_data = pd.read_csv(os.path.join(dirname, './dataSet/Training.csv'))
X = train_data.iloc[:, :-2]
y = train_data.iloc[:, -2]

labelEnc = LabelEncoder()
labelEnc.fit(y)
y = labelEnc.transform(y)

X = np.array(X)
y = np.array(y)


class Center(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.mean_ = X.mean()
        return self

    def transform(self, X):
        X_transformed = X - X.mean()
        return X_transformed


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

