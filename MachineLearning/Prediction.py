import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from MyFuncs.plotters import dualPlot
import datetime as dt
import warnings
from tqdm import trange
from MyFuncs.checkDirs import checkPath
import json

from Models.KernelRidge import KRR
from Models.LightGBM_Models import lgbmModel, randomForest

def testModel(dataPath, meta, model):
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
    yValList: list, the target data
    """
    xTrain, yTrain = getData(dataPath, "Train", meta["dataset"]) #Getting the training data
    xVal, yVal = getData(dataPath, "Validation", meta["dataset"]) #Getting the validation data
    xPredict, yPredict = getData(dataPath, "Prediction", meta["dataset"]) #Getting the prediction data
    abc, InChI = getData(dataPath, "Prediction", "InChI") #Getting the InChI keys

    mseList = []; r2List = [] #Lists to store the MSE and R2 values

    model.fit(xTrain, yTrain) # Fitting the model
    yPred = model.predict(xVal)
    yUnk = model.predict(xPredict)

    mseList.append(mean_squared_error(yVal, yPred))
    r2List.append(r2_score(yVal, yPred))
    
    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta["filepath"]}_Metrics.csv", index=False) # Saving the metrics to a csv file
    pd.DataFrame({"yVal": yVal, "yPred": yPred}).to_csv(f"{meta["filepath"]}_ValidationPreds.csv", index=False) # Saving the data to a csv file
    pd.DataFrame({"InChI" : InChI, "yUnk": yUnk}).to_csv(f"{meta["filepath"]}_UnknownPreds.csv", index=False) # Saving the data to a csv file

    dualPlot(yVal, yPred, meta) # Plotting the data (MSE hist + yhat v ytrue scatter plot)

    return yPred, yVal

def getData(dataPath, dsettype, target):
    data = pd.read_csv(f"{dataPath}-{dsettype}Set.csv")
    X = data.iloc[:, 7:].values
    # Y = data[target].values
    Y = data.iloc[:, 0].values
    return X, Y

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
    meta["filepath"] = f"Results/{meta['dataset']}/Prediction/{meta['model']}/{meta["version"]}_{meta["variant"]}-{meta["timestamp"]}"
    return meta

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"version" : "0.2.2", #Setting up metadata
            "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}
    
    with open("MachineLearning/TrainingInfo.json") as f: #Reading in the training info
        data = json.load(f)
    f.close()

    datasets = list(data.keys()) #Getting the datasets
    algFuncs = {
        "KRR" : KRR,
        "RandomForest" : randomForest,
        "LGBM" : lgbmModel
    }

    tdset = trange(len(datasets), desc = "Datasets") #Setting up tqdm
    for i in tdset: #Iterating through the datasets
        tdset.set_description(f"Datasets: {datasets[i]}")
        dset = datasets[i]
        algorithms = data[dset]["algorithms"]

        scoreByAlgorithm = {} #Dictionary to store the scores by algorithm

        talg = trange(len(algorithms), desc = "Algorithms") #Setting up tqdm
        for j in talg: #Iterating through the models
            talg.set_description(f"Algorithms: {algorithms[j]}. Dataset: {dset}")
            alg = algorithms[j]

            meta = updateMetadata(meta, alg, data[dset]["scaling"], dset)
            checkPath(f"Results/{meta['dataset']}/Prediction/{meta['model']}") #Checking the path exists, if not, creating folder(s)
            modelDict = getModels(algFuncs[alg])

            dataPath = (f"Data/Datasets/PredictionDatasets/{meta['version']}-{meta['dataset']}-{meta["variant"]}") #Reading in the dataset

            model = modelDict[dset]
            yHat, Y = testModel(dataPath, meta, model) #Testing the model
    
    print("Completed")