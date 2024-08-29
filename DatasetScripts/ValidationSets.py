import pandas as pd
import numpy as np

def getValidationSet(df, split, randomState):
    """
    Splits the DataFrame into a Validation Set and a Train Set based on the InChI column.
    The split is based on the quantile of the random number assigned to each InChI.

    Parameters
    ----------
    df : DataFrame
        DataFrame to split
    split : float
        Proportion of the DataFrame to be assigned to the Validation Set
    randomState : int
        Random seed to use for reproducibility

    Returns
    -------
    validationSet : DataFrame
        DataFrame containing the Validation Set
    trainSet : DataFrame
        DataFrame containing the Train Set
    """

    # Checking input values
    if randomState != None:
        np.random.seed(randomState)

    if split < 0 or split > 1:
        print("Error: Split value must be between 0 and 1")
        return None, None
    
    # Main Code
    grouped = df.groupby("InChI") #Grouping by InChI
    groupedDict = {}
    for name, grouped in grouped: #Iterating through the groups and assigning each inchi a random number
        groupedDict[name] = [grouped, np.random.randint(0, 20000)]

    sortOrder = sorted(groupedDict, key=lambda x: groupedDict[x][1]) #Sorting by the random number
    length = len(sortOrder) #Getting the length of the sorted InChIs

    quantileIndex = [int(length * quantile) for quantile in [0, split, length]] #Getting the quantile index fractions
    inchiByQuantile = [sortOrder[quantileIndex[i]:quantileIndex[i+1]] for i in range(len(quantileIndex)-1)] #Getting the indexes of the InChIs to split at

    validationSet = pd.concat([groupedDict[inchi][0] for inchi in inchiByQuantile[0]]) #Creating the Validation Set
    trainSet = pd.concat([groupedDict[inchi][0] for inchi in inchiByQuantile[1]]) #Creating the Train Set

    if validationSet.shape[0] + trainSet.shape[0] != df.shape[0]: #Checking if the split was done correctly
        print("Error: Validation Set and Train Set do not add up to the original DataFrame")
        print("Validation Set Shape:", validationSet.shape)
        print("Train Set Shape:", trainSet.shape)
        print("Original DataFrame Shape:", df.shape)
        return None, None
    
    return validationSet, trainSet

if __name__ == "__main__":
    version = "0.7.0"
    indatasets = ["hasLogH", "hasLogS"]
    outdatasets = ["logHenry", "logS"]
    split = 0.15

    for i in range(len(indatasets)):
        dataset = indatasets[i]

        df = pd.read_csv(f"Data/Datasets/{version}-{dataset}.csv", low_memory=False)
        validationSet, trainSet = getValidationSet(df, split, randomState=None)

        dataset = outdatasets[i]
        validationSet.to_csv(f"Data/Datasets/TrainTest/{version}-{dataset}-ValidationSet.csv", index=False)
        trainSet.to_csv(f"Data/Datasets/TrainTest/{version}-{dataset}-TrainSet.csv", index=False)

        print(dataset, df.shape)
        print("Train Set Shape:", trainSet.shape)
        print("Validation Set Shape:", validationSet.shape)
        print("\n")
