# Here, you can find some helper files that were refactor out of the notebook to clean it up.
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import requests
import re
from bs4 import BeautifulSoup
from sklearn.metrics import mean_absolute_percentage_error

def load_data(filepath):
    data = pd.read_csv(filepath, sep= ';', encoding='utf-16')
    data.rename(columns={' Mittauspiste Sijainti Päivä Suuntakoodi Ajoneuvoluokka': 'TMS', 'Unnamed: 1': 'Location', "Unnamed: 2": 'Date', "Unnamed: 3":'Direction', "Unnamed: 4":'Type'}, inplace=True)
    data.columns = data.columns.str.replace(' KLO_', '')
    data.Date = pd.to_datetime(data.Date)
    for column in data.columns[5:]:
        data[column] = data[column].replace(' ', 0)
        data[column] = pd.to_numeric(data[column])
    return data

def get_file_paths(url, params={}, years = r'(.*2020[0-9]{4}.*|.*2021[0-9]{4}.*)'):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href')]
    r = re.compile(years)
    filenames = []
    
    folders =  list(filter(r.search, parent))
    for folder in folders:
        response = requests.get(folder, params=params)
        if response.ok:
            response_text = response.text
        else:
            return response.raise_for_status()
        soup = BeautifulSoup(response_text, 'html.parser')
        parent = [url + node.get('href') for node in soup.find_all('a')]
        station = ".*117.*Munkkiniemi.*"
        r = re.compile(station)
        file =  list(filter(r.match, parent))
        # Each folder has two instances of the same file. We only need to have one of them to reduce number of duplicates 
        if file:
            filenames.append(str(folder + file[0].split("/")[-1]))
    return filenames

def plotCoefficients(model, input_features):
    """
        Plots sorted coefficient values of the model
    """
    importances = model.feature_importances_
    forest_importances = pd.Series(importances, index=input_features).sort_values(ascending=True)
    std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)

    fig, ax = plt.subplots(figsize=(10,6))
    forest_importances.plot.barh(xerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()

def plotModelResults(model, X_train, X_test, y_test, size, cv, plot_intervals=False, plot_anomalies=False):
    """
        Plots modelled vs fact values, prediction intervals and anomalies
    
    """
    
    prediction = model.predict(X_test[-size:])
    
    plt.figure(figsize=(15, 7))
    plt.plot(prediction, "g", label="prediction", linewidth=2.0)
    plt.plot(y_test[-size:], label="actual", linewidth=2.0)
    
    if plot_intervals:
        mae = cv.mean() * (-1)
        deviation = cv.std()
        
        scale = 1.96
        lower = prediction - (mae + scale * deviation)
        upper = prediction + (mae + scale * deviation)

        plt.plot(lower, "r--", label="upper bound / lower bound", alpha=0.5)
        plt.plot(upper, "r--", alpha=0.5)
        
        if plot_anomalies:
            anomalies = np.array([np.NaN]*len(y_test))
            anomalies[y_test<lower] = y_test[y_test<lower]
            anomalies[y_test>upper] = y_test[y_test>upper]
            plt.plot(anomalies, "o", markersize=10, label = "Anomalies")
    
    error = mean_absolute_percentage_error(prediction, y_test[-size:])
    plt.title("Mean absolute percentage error {0:.2f}%".format(error))
    plt.legend(loc="best")
    plt.tight_layout()
    plt.grid(True);