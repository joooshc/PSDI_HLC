import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from MyFuncs.plotters import dualPlot
import datetime as dt
import warnings
from tqdm import tqdm
from MyFuncs.checkDirs import checkPath
import time

from Models.GridSearchModels import *

def performGridSearch(X, Y, meta, gs):
    """
    Performs a GridSearch on the data.

    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    gs: GridSearchCV, the GridSearch model

    Outputs:
    yPredList: list, the predicted data
    yTestList: list, the target data
    """

    mseList = []; r2List = [] #Lists to store the MSE and R2 values
    yPredList = []; yTestList = []

    xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size = 0.2, random_state = 42) #Split the data with specified seed for reproducibility

    model = gs.fit(xTrain, yTrain) #Fit the model with grid search
    Y_pred = model.predict(xTest) #Predict the test data

    yPredList.extend(Y_pred); yTestList.extend(yTest) # Appending the predictions and test values to the lists
    mseList.append(mean_squared_error(yTest, Y_pred))
    r2List.append(r2_score(yTest, Y_pred))

    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta['filepath']}.csv", index=False) # Saving the metrics to a csv file

    dualPlot(yTestList, yPredList, meta) # Plotting the data (MSE hist + yhat v ytrue scatter plot)

    bestParams = model.best_params_
    results = model.cv_results_
    pd.DataFrame(results).to_csv(f"{meta["filepath"]}_GridSearch.csv", index=False) # Saving the results of the grid search to a csv file
    pd.DataFrame(bestParams, index=[0]).to_csv(f"{meta["filepath"]}_BestParams.csv", index=False)

    return yPredList, yTestList

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    st = time.time()
    meta = {"dataset" : "", #Setting up metadata
        "version" : "0.5.3",
        "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S"),
        "model" : ""}
    
    datasets = {"logHenry" : "MRobust"}#, #Datasets to run the grid search on
                # "logS" : "MRobust",
                # "logCMC" : "MStandard"}
    datasets = {"logS" : "MRobust"}

    models = {"KNN" : KNN(), #Models to run the grid search on
              "KernelRidgeRegression" : KRR(),
              "RandomForest" : rf(),
              "LGBM" : lgbm(),
              "AdaBoost" : AdaBoostModel(), 
              "SVR" : svrModel()}
    
    models = {"KernelRidgeRegression" : KRR()}
    for m in tqdm(list(models.keys())): #Iterating through the models
        meta["model"] = m 
        for dset in datasets.keys(): #Iterating through the datasets
            print(dset)
            meta["variant"] = datasets[dset]
            meta["dataset"] = dset
            meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/{meta["version"]}_{meta["variant"]}-{meta["timestamp"]}"

            checkPath(f"Results/{meta['dataset']}/{meta['model']}") #Checking the path exists, if not, creating folder(s)

            df = pd.read_csv(f"Data/Datasets/{meta['version']}-{meta["variant"]}_{meta['dataset']}.csv")
            inchi = df["InChI"].values.tolist()
            X = df.iloc[:, 5:].values
            Y = df[dset].values.astype(float)

            yHat, Y = performGridSearch(X, Y, meta, models[m])
        print("Completed")
        print("elapsed time: ", time.time()-st)