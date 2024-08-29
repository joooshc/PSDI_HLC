import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score
from MyFuncs.plotters import dualPlot
import datetime as dt
import warnings
from tqdm import trange
from MyFuncs.checkDirs import checkPath

from Models.AdaboostModel import Ada
from Models.KernelRidge import KRR
from Models.KNearestNeighbours import KNN
from Models.LightGBM_Models import lgbmModel, randomForest
from Models.SVR import svrModel

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

    gss = GroupShuffleSplit(n_splits = 5, train_size = 0.8) # GroupShuffleSplit to ensure no data leakage, 5 splits
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

def getModels(modelClass):
    """ 
    Returns a list of models from the model class.
    
    Inputs:
    modelClass: class, the model class
    
    Outputs:
    modelDict: dict, the models
    """

    modelFuncsList = [method for method in dir(modelClass) if callable(
    getattr(modelClass, method)) and not method.startswith("__")] #Getting list of functions in class

    modelDict = {}
    for method in modelFuncsList: #Iterating through functions and appending to list
        modelClass.method = getattr(modelClass, method)
        modelDict[method] = modelClass.method()

    if len(list(modelDict.keys())) < 3:
        print("Error: Not all models have been defined")
    
    return modelDict

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
    meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/{meta["version"]}_{meta["variant"]}-{meta["timestamp"]}"
    return meta

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"version" : "0.7.0", #Setting up metadata
            "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}
    
    datasets = {"logHenry" : "MRobust", #Datasets to iterate through
                "logS" : "MRobust"}
                # "logHlogS" : "MRobust",
                # "logSlogH" : "MRobust"}
    
    algorithms = {"AdaBoost" : Ada,
                  "KernelRidgeRegression" : KRR,
                  "KNN" : KNN,
                  "LGBM" : lgbmModel,
                  "RandomForest" : randomForest}#,
                  #"SVR" : svrModel} #Algorithms to iterate through

    tdset = trange(len(datasets), desc = "Datasets") #Setting up tqdm
    for i in tdset: #Iterating through the datasets
        tdset.set_description(f"Datasets: {list(datasets.keys())[i]}")
        dset = list(datasets.keys())[i]

        scoreByAlgorithm = {} #Dictionary to store the scores by algorithm

        talg = trange(len(algorithms), desc = "Algorithms") #Setting up tqdm
        for j in talg: #Iterating through the models
            talg.set_description(f"Algorithms: {list(algorithms.keys())[j]}. Dataset: {dset}")
            alg = list(algorithms.keys())[j]

            meta = updateMetadata(meta, alg, datasets[dset], dset)
            checkPath(f"Results/{meta['dataset']}/{meta['model']}") #Checking the path exists, if not, creating folder(s)
            modelDict = getModels(algorithms[alg])

            df = pd.read_csv(f"Data/Datasets/ScaledTrainTest/{meta['version']}-{meta['dataset']}-{meta["variant"]}-TrainSet.csv") #Reading in the dataset
            inchi = df["InChI"].values.tolist() #Selecting data
            X = df.iloc[:, 6:].values
            Y = df.iloc[:, 0].values

            # try:
            yHat, Y = testModel(X, Y, meta, inchi, modelDict[dset]) #Testing the model

            scoreByAlgorithm[f"{alg}_{dset}"] = {"Algorithm" : alg, "MSE" : mean_squared_error(Y, yHat), "R2" : r2_score(Y, yHat)} #Storing the scores
            # except:
            #     print(f"Error: missing algorithm for {alg} and {dset}")
    
        df = pd.DataFrame(scoreByAlgorithm).T
        df.columns = ["Algorithm", "MSE", "R2"]
        df.to_csv(f"Results/{dset}/{dset}-ScoreByAlgorithm-{meta['timestamp']}.csv", index=False) #Saving the scores to a csv file
    print("Completed")