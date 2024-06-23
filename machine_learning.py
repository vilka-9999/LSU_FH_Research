import csv
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import random

from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


def compare_algorithms(data, data_name, lbl):
    
    # creating learning models
    rfc = RandomForestClassifier()
    knc = KNeighborsClassifier()
    svc = SVC()
    perc = Perceptron()
    gnb = GaussianNB()
    # creating an array of these models
    models = [rfc, knc, svc, perc, gnb]

    # get labels for supervised learning
    evidence = data[['Distance (miles)', 'Sprint Distance (m)', 'Power Plays', 'Energy (kcal)', 'Player Load', 'Top Speed (m/s)', 'Distance Per Min (m/min)']]
    label = data[f'{lbl}']
    # scale data
    sc = StandardScaler() 
    evidence = sc.fit_transform(evidence)

    # create df for saving and graph results, and create column with the type of the score
    df = {
        'score_name': ['accuracy', 'precision_macro', 'recall_macro']
    }
    df = pd.DataFrame(df)

    # loop through models to check results for every model
    for model in models:
        # check cross value for 3 fields
        accuracy = cross_val_score(model, evidence, label, cv=10)
        precision = cross_val_score(model, evidence, label, cv=10, scoring='precision_macro')
        recall = cross_val_score(model, evidence, label, cv=10, scoring='recall_macro')
        # mean results
        accuracy_mean = round(accuracy.mean() * 100, 2)
        precision_mean = round(precision.mean() * 100, 2)
        recall_mean = round(recall.mean() * 100, 2)
        # get model name
        model_name = type(model).__name__
        
        # print results
        print(f'Results for model {model_name}')
        print(f'Accuracy {accuracy}')
        print(f'Precision {precision}')
        print(f'Recall {recall}')
        # save results into df
        df[f'{model_name}'] = [accuracy_mean, precision_mean, recall_mean]
    
    # save df
    filename = f'{data_name}_{lbl}_predict.csv'
    if os.path.exists(f'Results/{filename}'):
        os.remove(f'Results/{filename}')
    df.to_csv(f'Results/{filename}', index=False)



def main():
    os.makedirs('Results', exist_ok=True)
    
    directory = 'data_cleaned/split_data/semesters'
    # loop through file in the directory
    for filename in os.listdir(directory):
        # get file and name
        file_path = os.path.join(directory, filename)
        data = pd.read_csv(f'{file_path}')
        data_name = filename[ : filename.index('.')]
        # compare algorithms
        compare_algorithms(data, data_name, 'Tags')

if __name__ == "__main__":
    main()