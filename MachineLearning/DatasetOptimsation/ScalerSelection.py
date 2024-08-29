import pandas as pd #Scaling Method Determination
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb
import datetime as dt
from sklearn.model_selection import KFold
from MyFuncs.plotters import scatterPlot
from sklearn.preprocessing import StandardScaler, normalize, RobustScaler, MaxAbsScaler, PowerTransformer, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold

def lgbmModel(X, Y, meta, scaler):
    """ 
    LightGBM Model to determine the best scaling method.
    
    Inputs:
    X: np.array, the input data
    Y: np.array, the target data
    meta: dict, the metadata
    scaler: str, the scaling method
    
    Outputs:
    yPredList: list, the predicted data
    yTestList: list, the target data
    """

    mseList = []; r2List = [] # Intialising lists
    yPredList = []; yTestList = []

    kf = KFold(n_splits = 5, shuffle = True, random_state=3141) # Initialising KFold with 5 splits and specified seed for reproducibility
    for train_index, test_index in kf.split(X): # Looping through the splits
        xTrain, xTest = X[train_index], X[test_index]

        xTrain = scaleData(xTrain, scaler) # Scaling the data
        xTest = scaleData(xTest, scaler)
        yTrain, yTest = Y[train_index], Y[test_index]

        model = lgb.LGBMRegressor(boosting_type="gbdt", n_estimators= 100).fit(xTrain, yTrain) # Initialising the model
        Y_pred = model.predict(xTest)

        yPredList.extend(Y_pred); yTestList.extend(yTest) # Appending the predictions and test values to the lists
        mseList.append(mean_squared_error(yTest, Y_pred))
        r2List.append(r2_score(yTest, Y_pred))
    
    print(f"Mean MSE: {np.mean(mseList)}")
    print(f"Mean R2: {np.mean(r2List)}")

    pd.DataFrame({"MSE": mseList, "R2": r2List}).to_csv(f"{meta["filepath"]}.csv", index=False) # Saving the metrics to a csv file

    scatterPlot(yTestList, yPredList, meta)

    return yPredList, yTestList

def scaleData(X, method):
    """ 
    Scales the data using the scalers.
    
    Inputs:
    X: np.array, the input data
    method: str, the scaling method
    
    Outputs:
    np.array, the scaled data
    """
    if method == "None":
        return X
    
    elif method == "MinMax":
        return MinMaxScaler().fit_transform(X)

    elif method == "normalize":
        return normalize(X)

    else:
        # X = MinMaxScaler().fit_transform(X)
        X = normalize(X)
        # X = method.fit_transform(X)
        X = np.log1p(X)
    return X

if __name__ == "__main__":
    meta = {"dataset" : "logS", #Setting up metadata
        "version" : "0.4.2",
        "timestamp" : dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S"),
        "model" : "LGBM"}
    
    sets = ["HenryConstant", "logCMC", "CMC", "logS", "logHenry"] #Datasets to iterate through

    # scalers = [StandardScaler(), RobustScaler(), MaxAbsScaler(), #Scaling methods to iterate through
    #            PowerTransformer(method="yeo-johnson", standardize=False), 
    #            "None", "normalize", "MinMax"]
    scalers = ["log1p"]
    results = {}

    for dset in sets: #Iterating through the datasets
        meta["dataset"] = dset

        for s in scalers[:]: #Iterating through the scaling methods
            meta["version"] = f"0.4.2"
            df = pd.read_csv(f"Data/Datasets/{meta["version"]}-{meta["dataset"]}.csv")
            meta["version"] = f"0.4.2_N_{s}"

            meta["filepath"] = f"Results/{meta['dataset']}/{meta['model']}/Scaling/{meta["version"]}_{meta["timestamp"]}"
            X = df.iloc[:, 5:].values
            # X = VarianceThreshold(threshold=0).fit_transform(X)
            Y = df[meta["dataset"]].values.astype(float)

            yHat, Y = lgbmModel(X, Y, meta, s)

        results[dset] = [mean_squared_error(Y, yHat), r2_score(Y, yHat)]
    resultsdf = pd.DataFrame(results, index=["MSE", "R2"]).T
    print(resultsdf)
    resultsdf.to_csv(f"Results/log1p_ScalingComparison.csv")
    print("Completed")