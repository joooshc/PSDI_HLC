import numpy as np
from scipy import stats
import pandas as pd

def dropLowDistinction(data, tol):
    dropped = []
    for col in data.columns:
        if len(data[col].unique()) < tol*data.shape[0]:
            data.drop(col, axis=1, inplace=True)
            dropped.append(col)
    return data, dropped

def dropNaN_cols(data, cols, tol):
    """ 
    Function that iterates though columns and deletes columns with more NaNs than the tolerance.
    
    Parameters:
    data: pandas DataFrame
    cols: list of strings
    tol: int
    
    Returns:
    data: pandas DataFrame
    dropped: list of strings
    """

    dropped = []

    for col in cols:
        numNaNs = data[col].isna().sum()
        if numNaNs > tol:
            data.drop(col, axis=1, inplace=True)
            dropped.append(col)
    return data, dropped

def removeOutliers(data, cols, tol):
    """ 
    Function that iterates though columns and deletes rows with more outliers than the tolerance.
    
    Parameters:
    data: pandas DataFrame
    cols: list of strings
    tol: int
    
    Returns:
    data: pandas DataFrame
    dropped: list of strings
    """

    values = data[cols].values.astype(float).tolist()
    z = np.abs(stats.zscore(values))

    data = data[(z < tol).all(axis=1)]
    return data

def prepForScaling(df, dset, toDrop):
    df.drop_duplicates(inplace=True)

    df = df[pd.to_numeric(df[dset], errors='coerce').notnull()] #Filters out non numeric values and replaces with NaN
    df.dropna(subset=[dset], inplace=True) 
    print(f"\n Variable: {dset}\n", df.shape)

    popped = df.pop(dset) #Moving target column
    df.insert(0, dset, popped)

    for d in toDrop:
        try:
            del df[d]
        except:
            pass
    
    tol = df.shape[0] * 0.01
    cols = df.iloc[:, 8:].columns #Filtering through rest of columns
    df, dropped = dropNaN_cols(df, cols, tol)

    df = df[df[dset] != -np.inf]
    df = df[df[dset] != np.inf]

    cols = df.iloc[:, 8:].columns
    for col in cols:
        df.dropna(subset=[col], inplace=True)

    print("After dropping NaNs:", df.shape)

    df = removeOutliers(df, [dset], 3)
    print("After dropping outliers:", df.shape)

    df.dropna(subset=[dset], inplace=True)
    print("After dropping NaNs again:", df.shape)

    return df