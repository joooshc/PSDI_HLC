import pandas as pd
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def dfToDict(df):
    """ 
    Function that converts a DataFrame to a dictionary.
    df: DataFrame
    
    Returns a dictionary with the column name as the key and the values as the value."""
    dfDict = {}
    columns = list(df.columns) #Selecting columns
    for col in columns: #Iterating through columns
        values = df[col].values
        if len(values) == 0:
            dfDict[col] = np.nan
        else:
            dfDict[col] =  values #Adding to dictionary
    return dfDict