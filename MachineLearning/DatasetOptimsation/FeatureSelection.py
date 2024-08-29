import pandas as pd
import numpy as np
from tqdm import trange
import lightgbm as lgb
import datetime as dt
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, RobustScaler, normalize, StandardScaler
from sklearn.feature_selection import SelectKBest
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

def lgbmModel(X, Y, meta, nFeatures):
    """ 
    LightGBM Model using SelectKBest feature selection.
    
    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    nFeatures: int, the number of features to select
    Outputs:
    float, the R2 score of the model
    """

    mseList = []; r2List = [] #Initialising lists to store output values
    yPredList = []; yTestList = []

    X = SelectKBest(k=nFeatures).fit_transform(X, Y) # Selecting the best features
    kf = KFold(n_splits = 5, shuffle = True, random_state=3141) # Initialising KFold with 5 splits and specified seed for reproducibility
    for train_index, test_index in kf.split(X): # Looping through the splits
        xTrain, xTest = X[train_index], X[test_index]
        yTrain, yTest = Y[train_index], Y[test_index]

        xTrain = scaleData(xTrain) # Scaling the data
        xTest = scaleData(xTest)

        model = lgb.LGBMRegressor(boosting_type="gbdt", n_estimators= 100, verbose=-1).fit(xTrain, yTrain) # Initialising the model
        Y_pred = model.predict(xTest)

        yPredList.extend(Y_pred); yTestList.extend(yTest) # Appending the predictions and test values to the lists
        mseList.append(mean_squared_error(yTest, Y_pred))
        r2List.append(r2_score(yTest, Y_pred))
    
    print(f"Mean MSE: {np.mean(mseList)}") # Printing the mean values of the metrics
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta["filepath"]}_{nFeatures}.csv", index=False) # Saving the metrics to a csv file

    return r2_score(yTestList, yPredList)

def scaleData(X): 
    """ 
    Scales the data using the scalers.
    
    Inputs:
    X: np.array, the input data
    Outputs:
    np.array, the scaled data
    """
    X = MinMaxScaler().fit_transform(X)
    # X = normalize(X)
    X = RobustScaler().fit_transform(X)
    # X = StandardScaler().fit_transform(X)

    return X

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    meta = {"dataset" : "logHenry", #Setting up metadata
        "version" : "0.4.2",
        "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S"),
        "model" : "LGBM"}
    
    featureSelection = {} #Results dictionary

    df = pd.read_csv(f"Data/Datasets/{meta["version"]}-{meta["dataset"]}.csv") #Reading the dataset
    meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/FeatureSelection/{meta["version"]}_{meta["timestamp"]}" #Setting up the filepath

    X = df.iloc[:, 5:].values #Selecting data
    Y = df[meta["dataset"]].values.astype(float)

    best, r2list = bisection(lgbmModel, 1, X.shape[1], 0.001, 40, X, Y, meta) #Running the bisection method
    print(f"Best number of features: {best}, score = {r2list[-1]}")
    featureSelection[meta["dataset"]] = best
    
    pd.DataFrame(featureSelection, index=[0]).to_csv(f"{meta['filepath']}_FeatureSelection.csv", index=False)
    print("Completed")