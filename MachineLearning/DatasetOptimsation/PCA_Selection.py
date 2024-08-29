import pandas as pd
import numpy as np
from tqdm import trange
import lightgbm as lgb
import datetime as dt
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
import warnings


def bisection(eqn, a, b, tol, nIt, X, Y, meta):
    """ 
    Uses the bisection method to find the maximum.
    Inputs: 
    eqn: function, the equation to be solved
    a: float, the left bound of the interval
    b: float, the right bound of the interval
    tol: float, the tolerance of the solution
    nIt: int, the number of iterations
    Outputs:
    mp: float, the root of the equation
    valList: list, the values of the equation at each iteration
    """

    valList = []
    t = trange(nIt, desc="Bisection", leave=True)
    for i in t:
        aLast = a; bLast = b
        
        t.set_description("Bisection" + f" {i+1}/{nIt}" + f" a = {a} b = {b}")
        aSol, bSol = eqn(X, Y, meta, a), eqn(X, Y, meta, b)
        if abs(bSol-aSol) > tol: # Check if the interval is smaller than the tolerance
            mp = (a+b)//2
            val = eqn(X, Y, meta, mp); valList.append(val)

            if abs(val - aSol) < tol: # Check if the value is smaller than the tolerance
                print("Root found at x =", mp, "with value =", val, "in", i, "iterations")
                return mp, valList
            elif bSol > aSol:
                a = mp
            else:
                b = mp

        if a == aLast and b == bLast:
            print("Root found at x =", mp, "with value =", val, "in", i, "iterations")
            return mp, valList
        
    print(f"Root not found in {nIt} iterations, value = {val} at x = {mp}")
    return mp, valList

def lgbmModel(X, Y, meta, nComps):
    """
    LightGBM Model using PCA.

    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    inchi: list, the InChI keys

    Outputs:
    r2_score: float, the R2 score
    """

    mseList = []; r2List = [] # Intialising lists
    yPredList = []; yTestList = []

    kf = GroupKFold(n_splits = 5) # GroupKFold to ensure no data leakage, 5 splits
    for train_index, test_index in kf.split(X, Y, groups = inchi):
        xTrain, xTest = X[train_index], X[test_index]
        yTrain, yTest = Y[train_index], Y[test_index]

        xTrain = PCA(n_components=nComps).fit_transform(xTrain) # PCA
        xTest = PCA(n_components=nComps).fit_transform(xTest)

        model = lgb.LGBMRegressor(boosting_type="gbdt", n_estimators= 100, verbose=-1).fit(xTrain, yTrain) # Initialising model
        Y_pred = model.predict(xTest)

        yPredList.extend(Y_pred); yTestList.extend(yTest) # Appending the predictions and test values to the lists
        mseList.append(mean_squared_error(yTest, Y_pred))
        r2List.append(r2_score(yTest, Y_pred))
    
    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta["filepath"]}_{nComps}.csv", index=False) # Saving the metrics to a csv file

    return r2_score(yTestList, yPredList)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"dataset" : "logHenry", #Setting up metadata
        "version" : "0.5.3",
        "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S"),
        "model" : "LGBM"}

    componentSelection = {}
    df = pd.read_csv(f"Data/Datasets/{meta["version"]}-MRobust_{meta["dataset"]}.csv") # Reading the dataset
    inchi = df["InChI"].values.tolist() # Getting the InChI keys

    meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/PCA/{meta["version"]}_{meta["timestamp"]}" # Setting up the filepath

    X = df.iloc[:, 5:].values # Getting the input data
    Y = df[meta["dataset"]].values.astype(float)

    best, r2list = bisection(lgbmModel, 1, X.shape[1], 0.001, 40, X, Y, meta) # Running the bisection method
    print(f"Best number of components: {best}, score = {r2list[-1]}")
    componentSelection[meta["dataset"]] = best
    
    pd.DataFrame(componentSelection, index=[0]).to_csv(f"{meta['filepath']}_componentSelection.csv", index=False)
    print("Completed")