import pandas as pd
import numpy as np
from workalendar.europe import Finland

def preprocess_input(date, time, direction):
    time = str(time) + ':00:00'
    time = ' ' + time
    
    timestamp = pd.to_datetime(date + time, infer_datetime_format=True)

    direction = direction
    hour = timestamp.hour
    holiday = Finland().is_working_day(timestamp)
    year = timestamp.year
    month = timestamp.month
    week = timestamp.week
    weekday = timestamp.weekday()
    day = timestamp.day
    is_weekend = 1 if weekday in [5, 6] else 0

    return np.array([direction, hour, holiday, year, month, week, weekday, day, is_weekend]).reshape(-1, 1).T