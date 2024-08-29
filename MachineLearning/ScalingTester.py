import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score
from MyFuncs.plotters import dualPlot
import datetime as dt
import warnings
from tqdm import trange
from MyFuncs.checkDirs import checkPath
import os
import lightgbm as lgb

def testModel(X, Y, meta, inchi, model):
    """
    Tests the model using GroupShuffleSplit.

    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    inchi: list, the InChI keys
    model: model, the model to be tested

    Outputs:
    yPredList: list, the predicted data
    yTestList: list, the target data
    """

    mseList = []; r2List = [] #Lists to store the MSE and R2 values
    yPredList = []; yTestList = []

    gss = GroupShuffleSplit(n_splits = 5, train_size = 0.8, random_state = 42) # GroupShuffleSplit to ensure no data leakage, 5 splits
    for train_index, test_index in gss.split(X, Y, groups = inchi): # Looping through the splits
        xTrain, xTest = X[train_index], X[test_index]
        yTrain, yTest = Y[train_index], Y[test_index]

        model.fit(xTrain, yTrain) # Fitting the model
        Y_pred = model.predict(xTest)

        yPredList.extend(Y_pred); yTestList.extend(yTest) # Appending the predictions and test values to the lists
        mseList.append(mean_squared_error(yTest, Y_pred))
        r2List.append(r2_score(yTest, Y_pred))
    
    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta["filepath"]}.csv", index=False) # Saving the metrics to a csv file

    dualPlot(yTestList, yPredList, meta) # Plotting the data (MSE hist + yhat v ytrue scatter plot)

    return yPredList, yTestList

def lgbmModel():
    model = lgb.LGBMRegressor(n_estimators = 100, verbose = -1)
    return model

def updateMetadata(meta, model, variant, dataset):
    """
    Updates the metadata dictionary.

    Inputs:
    meta: dict, the metadata
    model: str, the model
    variant: str, the variant
    dataset: str, the dataset

    Outputs:
    meta: dict, the updated metadata
    """

    meta["model"] = model
    meta["variant"] = variant
    meta["dataset"] = dataset
    meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/{targ}/{meta["variant"]}-{meta["timestamp"]}"
    return meta

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}
    vers = "0.2.1"

    dataPath = "Data/Datasets/BPMP_Scaling" #Change this to the path you want to check for large files.
    datasets = list(os.listdir(dataPath))
    datasets = [d for d in datasets if d.startswith(vers)]

    targets = ["MeltingPoint_C"]
    errors = []

    for targ in targets:
        meta["version"] = f"{vers}_{targ}"
        scoreByDataset = {} #Dictionary to store the scores by Dataset
        tdset = trange(len(datasets), desc = "Datasets") #Setting up tqdm
        for i in tdset: #Iterating through the datasets
            tdset.set_description(f"Datasets: {datasets[i]}")
            dset = datasets[i]

            meta = updateMetadata(meta, "LGBM", dset.replace(".csv", ""), "MPBP_Scaling") #Updating the metadata
            checkPath(f"Results/{meta['dataset']}/{meta['model']}/{targ}") #Checking the path exists, if not, creating folder(s)

            df = pd.read_csv(f"{dataPath}/{dset}") #Reading in the dataset

            inchi = df["InChI"].values.tolist() #Selecting data
            X = df.iloc[:, 8:].values
            Y = df[targ]

            model = lgbmModel() #Setting up the model
            try:
                yHat, Y = testModel(X, Y, meta, inchi, model) #Testing the model

                scoreByDataset[f"{targ}_{dset}"] = {"Scaling" : dset, "MSE" : mean_squared_error(Y, yHat), "R2" : r2_score(Y, yHat)} #Storing the scores
            except:
                print(f"Error with {dset}")
                errors.append(f"{dset} - {targ}")
                continue

        df = pd.DataFrame(scoreByDataset).T
        df.columns = ["Target", "MSE", "R2"]
        df.to_csv(f"Results/MPBP_Scaling/{meta["model"]}/{targ}/{meta['version']}_ScoreByScaler-{meta['timestamp']}.csv", index=False) #Saving the scores to a csv file

    if len(errors) > 0:
        with open(f"Results/MPBP_Scaling/{meta["timestamp"]}-Errors.txt", "w") as f:
            for error in errors:
                f.write(f"{error}\n")
print("Completed")