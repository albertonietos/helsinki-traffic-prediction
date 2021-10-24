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