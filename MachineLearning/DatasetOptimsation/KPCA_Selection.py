import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import KernelPCA
import warnings
import lightgbm as lgb
import datetime as dt
from MyFuncs.plotters import dualPlot
from MyFuncs.checkDirs import checkPath
from tqdm import tqdm

def lgbmModel(X, Y, meta, inchi):
    """
    LightGBM Model using KernelPCA.

    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    inchi: list, the InChI keys

    Outputs:
    yPredList: list, the predicted data
    yTestList: list, the target data
    """

    mseList = []; r2List = [] # Intialising lists
    yPredList = []; yTestList = []

    gss = GroupShuffleSplit(n_splits = 5, train_size = 0.8, random_state = 42) # GroupShuffleSplit to ensure no data leakage, 5 splits, specified seed for reproducibility
    for train_index, test_index in tqdm(gss.split(X, Y, groups = inchi)): #Iterating through the splits
        xTrain, xTest = X[train_index], X[test_index]
        yTrain, yTest = Y[train_index], Y[test_index]

        model = lgb.LGBMRegressor(boosting_type="gbdt",  #Initialising model
                            n_estimators = 600,
                            early_stopping_rounds = 0,
                            num_leaves = 31,
                            max_bin = 255,
                            num_threads = 4,
                            learning_rate = 0.05)
        model.fit(xTrain, yTrain)
        Y_pred = model.predict(xTest)


        yPredList.extend(Y_pred); yTestList.extend(yTest) #Appending the predictions and test values to the lists
        mseList.append(mean_squared_error(yTest, Y_pred))
        r2List.append(r2_score(yTest, Y_pred))

    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta['filepath']}.csv", index=False) #Saving the metrics to a csv file

    dualPlot(yTestList, yPredList, meta) #Creating a pretty looking plot (hist + scatter)

    return yPredList, yTestList

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"dataset" : "", #Setting up metadata
    "version" : "0.5.3",
    "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S"),
    "model" : "KernelPCA",
    "variant" : ""}
    
    datasets = {"logHenry" : "MRobust", #Datasets to iterate through
                "logS" : "MRobust",
                "logCMC" : "MStandard"}

    results = {}

    for dset in datasets.keys(): #Iterating through the datasets
        print("\n", dset)
        meta["variant"] = datasets[dset] #Setting up metadata
        meta["dataset"] = dset

        checkPath(f"Results/{meta['dataset']}/{meta['model']}") #Checking if the path exists, if not, creating it

        df = pd.read_csv(f"Data/Datasets/{meta['version']}-{meta['variant']}_{meta['dataset']}.csv") #Reading the dataset
        nComps = np.linspace(1, df.shape[1], 10, dtype = int) #Setting up the number of components to iterate through
        inchi = df["InChI"].values.tolist() #Getting the InChI keys

        X = df.iloc[:, 5:].values #Selecting the data
        Y = df[dset].values.astype(float)

        for n in tqdm(nComps, desc = "Components"): #Iterating through the number of components 
            meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/{meta['version']}_{meta['variant']}_{n}-{meta['timestamp']}"
            pcaX = KernelPCA(kernel = "cosine", n_components = n).fit_transform(X) #Performing KernelPCA
            yPred, yTest = lgbmModel(pcaX, Y, meta, inchi) #Running the model
            results[n] = {"r2" : r2_score(yTest, yPred), 
                          "mse" : mean_squared_error(yTest, yPred)}
        
        results = pd.DataFrame(results).T
        results.to_csv(f"Results/{meta['dataset']}/{meta['model']}/{meta['version']}_{meta['variant']}_Results.csv")

    print("Completed")
