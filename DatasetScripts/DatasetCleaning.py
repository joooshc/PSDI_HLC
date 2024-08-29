import pandas as pd
import numpy as np
from scipy import stats
from tqdm import tqdm
import warnings

def combineDuplicateValues(cols, df, tList):
    """ 
    Combines duplicate values in the dataset.
        
    Inputs:
    cols: list, the columns to combine
    df: pd.DataFrame, the dataset
    tList: list, the list of temperatures
    
    Outputs:
    clean: pd.DataFrame, the cleaned dataset
    """

    clean = pd.DataFrame()
    for temp in tList: #Iterating through the temperatures
        subdf = df[df["Temperature"] == temp] #Extracting the subset

        subDict = {"Temperature": temp} #Creating the dictionary
        subDict.update(getPoints(cols, subdf)) #Getting datapoints

        subTemp = pd.DataFrame(subDict, index=[0]) #Creating the dataframe
        clean = pd.concat([clean, subTemp]) #Concatenating the dataframes
    return clean

def getPoints(cols, subdf):
    """ 
    Gets the points for the dataset.
    
    Inputs:
    cols: list, the columns to get the points for
    subdf: pd.DataFrame, the subset
    
    Outputs:
    subDict: dict, the dictionary of points
    """

    subDict = {}
    for col in cols: #Iterating through the columns
        colVals = subdf[col].values.astype(float) #Extracting the values that are not NaN
        colVals = colVals[~np.isnan(colVals)]
        
        if len(colVals) == 0: #If there are no values, fill with NaN
            subDict[col] = np.nan
        elif len(colVals) > 2: #If there are more than 2 values, remove outliers
            oLen = len(colVals) #Getting the length of the original values
            z = np.abs(stats.zscore(colVals))
            newColVals = colVals[(z < 3)]
            nLen = len(newColVals) #Getting the length of the new values

            if nLen == 0: #If there are no new values, use mean of original values
                subDict[col] = np.mean(colVals)
            else:
                if nLen < 100:
                    subDict[col] = np.mean(newColVals) #Otherwise, use the mean of the new values

                    if oLen != nLen: #If there are outliers, print the number of outliers removed
                        print(f"\n Removed {oLen - nLen} outliers, retained {nLen} values for {col}")
                else:
                    subDict[col] = np.nan
                    print("Too many values for", col)
                    print(subdf)
                    subdf.to_csv("Data/Processed/0.2.7-HL_WrongIdentifiers.csv", index=False)
        else:
            subDict[col] = np.mean(colVals) #If there are less than 2 values, use the mean

    return subDict

def getLabels(cols, df):
    """ 
    Gets the labels for the dataset.
    
    Inputs:
    cols: list, the columns to get the labels for
    df: pd.DataFrame, the dataset
    
    Outputs:
    retDict: dict, the dictionary of labels
    """
    retDict = {}
    for col in cols: #Iterating through the columns
        colVals = df[col].values.astype(str).tolist() #Extracting the values and removing duplicates
        colVals = np.unique(colVals)
        colVals = [x for x in colVals if x != "nan"] #Removing NaN values

        try: #Trying to get the first value
            retVal = colVals[0].strip()
            if len(colVals) > 1:
                if "source" in col.lower():
                    colVals = [x.replace(",", "") for x in colVals]
                    retVal = ", ".join(colVals)
                else:
                    retVal = colVals[0]
            else:
                retVal = colVals[0].strip()
        except: #If no values are present, insert NaN
            retVal = np.nan

        retDict[col] = retVal
    return retDict

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    df = pd.read_csv("Data/Combined/0.5.0-Master.csv", low_memory=False)

    # pointsToCheck = ["MeltingPoint/C", "BoilingPoint/C", "nIsomers"] #Initialising lists
    pointsToCheck = ["nIsomers"]
    colsToCombine = ["logS", "HenryConstant"]
    # labelList = ["Compound", "SMILES", "InChI", "Melting/BoilingPoint-dataSource", "logS-dataSource", "HenryConstant-dataSource", "MeltingPoint-dataSource"]
    labelList = ["Compound", "SMILES", "InChI", "logS-dataSource", "HenryConstant-dataSource"]
    inchiList = df["InChI"].values.tolist()
    inchiList = np.unique(inchiList)

    temps = df["Temperature"].values.tolist()
    cleanTemps = []
    for t in temps: #Cleaning the temperatures to remove things with letters, etc
        try:
            cleanTemps.append(float(t))
        except:
            cleanTemps.append(np.nan)

    df["Temperature"] = cleanTemps

    cleanedDF = pd.DataFrame()

    for inchi in tqdm(inchiList): #Iterating through the InChI values
        subdf = df[df["InChI"] == inchi] #Extracting the subset

        tempList = subdf["Temperature"].values.tolist() # Only works when there is a temperature in the column
        tempList = np.unique(tempList)

        subFeatures = combineDuplicateValues(colsToCombine, subdf, tempList) #Combining duplicate values

        subLabels = getLabels(labelList, subdf) #Getting the labels
        subPoints = getPoints(pointsToCheck, subdf) #Getting the points
        subLabels.update(subPoints) #Updating the labels

        keys = subLabels.keys() #Inserting the labels
        for key in reversed(keys): #Iterating through reversed keys (to put columns in preferred order)
            subFeatures.insert(0, key, subLabels[key]) #Inserting the labels
        cleanedDF = pd.concat([cleanedDF, subFeatures]) #Concatenating the dataframes

    cleanedDF.reset_index(drop=True, inplace=True)

    newInChI = cleanedDF["InChI"].values.tolist()
    print(len(set(newInChI) - set(inchiList)))
    cleanedDF.to_csv("Data/Combined/0.5.0-CleanedMaster.csv", index=False)