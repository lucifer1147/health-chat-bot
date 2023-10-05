import pandas as pd
import pickle as pkl

train_data = pd.read_csv('dataSet/Training.csv')
X = train_data.iloc[:, :-2]
y = train_data.iloc[:, -2]

disease_list = []

for item in list(y.values):
    if item not in disease_list:
        disease_list.append(item)

with open('pickles/disease_list.pkl', 'wb') as fl:
    pkl.dump(disease_list, fl)

with open('pickles/symptom_names.pkl', 'wb') as fl:
    pkl.dump(X.columns, fl)
