from sklearn.neighbors import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVR

def svrModel(): #Support Vector Regression
    paramGrid = {"kernel" : ["linear"],
                "C" : [0.1, 1, 10],
                "epsilon" : [0.1, 0.2, 0.4]}
    
    model = GridSearchCV(estimator = SVR(),
                        param_grid = paramGrid,
                        cv = 5,
                        verbose = 3,
                        n_jobs = -1,
                        scoring = "r2")
    return model


def KNN(): #K Nearest Neighbours
    paramGrid = {"weights" : ["uniform", "distance"],
                "n_neighbors" : [3, 5, 7, 9],
                "p" : [1, 2]}
    
    model = GridSearchCV(estimator = KNeighborsRegressor(),
                        param_grid = paramGrid,
                        cv = 5,
                        verbose = 3,
                        n_jobs = -1,
                        scoring = "r2")
    return model

def KRR(): #Kernel Ridge Regression
    paramGrid = {"alpha" : [0.05, 0.04, 0.03, 0.02]}
    # paramGrid = {"kernel" : ['linear', 'poly', 'polynomial', 'rbf', 'laplacian', 'sigmoid', 'cosine']}
    
    model = GridSearchCV(estimator = KernelRidge(kernel = "laplacian"),
                        param_grid = paramGrid,
                        cv = 5,
                        verbose = 3,
                        n_jobs = -1,
                        scoring = "r2")
    return model

def rf(): #Random Forest
    paramGrid = {"boosting_type": ["rf"],
            "n_estimators": [400, 600, 800],
            "learning_rate": [0.1, 0.2, 0.4],
            "early_stopping_rounds": [0],
            "num_leaves" : [31, 50],
            "max_bin" : [255],
            "num_threads" : [4],
            "bagging_freq" : [1, 2, 4],
            "bagging_fraction" : [0.8, 0.9, 1.0]}

    reg = GridSearchCV(estimator = lgb.LGBMRegressor(),
                param_grid = paramGrid, 
                cv = 5, 
                verbose = 3, 
                n_jobs = -1,
                scoring = "r2")
    
    return reg

def lgbm(): #LightGBM
    paramGrid = {"boosting_type": ["gbdt"],
                "n_estimators": [400, 600, 800],
                "learning_rate": [0.1, 0.2, 0.4],
                "early_stopping_rounds": [0],
                "num_leaves" : [31, 50],
                "max_bin" : [255],
                "num_threads" : [4]}

    reg = GridSearchCV(estimator = lgb.LGBMRegressor(),
                param_grid = paramGrid, 
                cv = 5, 
                verbose = 3, 
                n_jobs = -1,
                scoring = "r2")
    
    return reg

def AdaBoostModel():
    paramGrid = {"n_estimators" : [50, 100, 200],
                "learning_rate" : [0.1, 0.2, 0.4, 0.8],
                "loss" : ["linear", "square", "exponential"]}
    model = GridSearchCV(estimator = AdaBoostRegressor(),
                        param_grid = paramGrid,
                        cv = 5,
                        verbose = 3,
                        n_jobs = -1,
                        scoring = "r2")
    return model