import pandas as pd
import warnings
import numpy as np
warnings.filterwarnings("ignore")
from tqdm import tqdm
import datetime as dt

def unlog(x): #Undo log scaling on Henry's Constant
    return np.exp(x)

def retrievePredictions(target):
    """ 
    Retrieve predictions from the LightGBM model results folder.
    Note: Change path as required!
    
    Parameters:
    target (str): The target variable to retrieve predictions for.
    
    Returns:
    df (pd.DataFrame): The predictions for the target variable.
    """

    df = pd.read_csv(f"Results/{target}/Prediction/LGBM/0.1.0_MRobust-2024-08-13_11.11.21_UnknownPreds.csv")

    df = df.rename(columns = {"yUnk" : target}) #Rename the prediction column to the target variable
    if target == "logHenry": #Edge case for Henry's Constant
        df["HenryConstant"] = unlog(df[target].values)
        df[f"HenryConstant-dataSource"] = "LightGBM"
    else:
        df[f"{target}-dataSource"] = "LightGBM" #Add a column to indicate the source of the prediction
    return df

def prepPredictions(masterdf, df, target):
    """ 
    Prepare the predictions for merging with the master dataset. Removes duplicates and InChI's that are already in the master dataset.
    
    Parameters:
    masterdf (pd.DataFrame): The master dataset.
    df (pd.DataFrame): The predictions for the target variable.
    target (str): The target variable to retrieve predictions for.
    
    Returns:
    df (pd.DataFrame): The cleaned predictions for the target variable.
    """

    print(target, "predictions shape:", df.shape)
    hasTarget = masterdf.dropna(subset=[target], how="all") #Getting list of inchi that already have a true value for the target variable
    hasTarget = hasTarget["InChI"].values.tolist()

    predInChI = df["InChI"].values.tolist() #Getting list of InChI's in the predictions
    intersect = list(set(hasTarget) & set(predInChI)) #Finding the InChI's that are in both the master dataset and the predictions
    print(len(intersect), "InChI's found in both datasets")

    for inchi in intersect: #Dropping the InChI's that are in both datasets
        df = df.drop(df[df["InChI"] == inchi].index)
    print("Dropped", len(intersect), "InChI's from predictions")

    predInChI = df["InChI"].values.tolist() #Getting list of InChI's in the predictions after dropping intersecting InChI's
    print(len(list(set(predInChI) - set(masterInChI))), "InChI's not found in master dataset") #Finding InChI's that are in the predictions but not in the master dataset. This should be 0!

    print(target, "predictions shape:", df.shape, "\n\n")
    return df

def addData(df, pred, target):
    """
    Add the predictions to the master dataset.

    Parameters:
    df (pd.DataFrame): The master dataset.
    pred (pd.DataFrame): The predictions for the target variable.
    target (str): The target variable to retrieve predictions for.

    Returns:
    df (pd.DataFrame): The master dataset with the predictions added.
    """

    errors = []
    print("Initial Stats:", target, df.shape)
    print(df.isna().sum(), "\n\n")

    inchiList = np.unique(pred["InChI"].values.tolist()) #Getting list of InChI's in the predictions
    for inchi in tqdm(inchiList):
        subpred = pred[pred["InChI"] == inchi] #Subsetting the predictions for the current InChI
        subdata = df[df["InChI"] == inchi]

        if subdata.shape[0] != subpred.shape[0]: #Checking number of datapoints for predictions and master dataset
            print("Error: Different number of rows for", inchi)
            errors.append(inchi)
        else:
            subdata[target] = subpred[target].values #Adding the predictions to the master dataset
            subdata[f"{target}-dataSource"] = subpred[f"{target}-dataSource"].values
            df.loc[df["InChI"] == inchi] = subdata

    print("Final Stats:",target , df.shape)
    print(df.isna().sum(), "\n\n")
    return df

def sanitizeTarget(df, target):
    """
    Sanitize the target variable by converting it to a float and replacing infinite values with NaN.

    Parameters:
    df (pd.DataFrame): The master dataset with the predictions added.
    target (str): The target variable to retrieve predictions for.

    Returns:
    df (pd.DataFrame): The master dataset with the sanitized target variable.
    """

    targVals = df[target].values.tolist()
    cleanVals = []
    for val in targVals: #Converting target variable to float
        try:
            cleanVals.append(float(val))
        except:
            cleanVals.append(np.nan)

    cleanVals = pd.Series(cleanVals) #Removing infinite values
    cleanVals = cleanVals.replace([np.inf, -np.inf], np.nan)

    df[target] = cleanVals
    return df

def removeUnneededCols(df, toDelete):
    """
    Remove columns that are not needed in the dataset.

    Parameters:
    df (pd.DataFrame): The master dataset with the predictions added.
    toDelete (list): The list of columns to delete.

    Returns:
    df (pd.DataFrame): The master dataset with the columns deleted.
    """

    cols = df.columns.tolist()

    for col in cols:
        for delete in toDelete:
            if delete in col:
                try:
                    df.drop(col, axis=1, inplace=True)
                    print("Deleted", col)
                except:
                    pass
    return df

if __name__ == "__main__":
    og = pd.read_csv("Data/Combined/LargeFiles/0.3.3-CleanedMaster.csv")
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

    toDelete = ["Melting", "Boiling"]
    targets = ["logS", "HenryConstant"]
    fileTargets = ["logS", "logHenry"] #File names

    og = removeUnneededCols(og, toDelete)

    df = og.copy()
    df.dropna(subset=targets, inplace=True, how = "all") #Dropping rows where both targets are missing
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    masterInChI = df["InChI"].values.tolist() #Getting list of InChI's in the master dataset

    for i in range(len(targets)):
        preds = retrievePredictions(fileTargets[i])
        preds = prepPredictions(df, preds, targets[i])

        df = addData(df, preds, targets[i])
        df = sanitizeTarget(df, targets[i])
    
    df.to_csv(f"Results/Datasets/{timestamp}-AugmentedLogHlogS.csv", index=False)