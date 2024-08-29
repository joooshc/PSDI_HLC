import lightgbm as lgb

class lgbmModel:
    def __init__(self):
        pass

    def logHenry():
        model = lgb.LGBMRegressor(boosting_type="gbdt", 
                                n_estimators = 600,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.05,
                                verbose = -1)
        return model
    
    def logCMC():
        model = lgb.LGBMRegressor(boosting_type="gbdt", 
                                n_estimators = 400,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1)
        return model
    
    def logS():
        model = lgb.LGBMRegressor(boosting_type="gbdt",
                                n_estimators = 600,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1,
                                verbose = -1)
        
        return model
    
    def logSlogH():
        model = lgb.LGBMRegressor(boosting_type="gbdt",
                                n_estimators = 600,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1)
        
        return model
    
    def logHlogS():
        model = lgb.LGBMRegressor(boosting_type="gbdt", 
                            n_estimators = 600,
                            early_stopping_rounds = 0,
                            num_leaves = 31,
                            max_bin = 255,
                            num_threads = 4,
                            learning_rate = 0.05)
        return model

class randomForest:
    def __init__(self):
        pass

    def logHenry():
        model = lgb.LGBMRegressor(boosting_type="rf", 
                                n_estimators = 600,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.05,
                                bagging_freq = 1,
                                bagging_fraction = 0.8)
        return model
    
    def logCMC():
        model = lgb.LGBMRegressor(boosting_type="rf", 
                                n_estimators = 800,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1,
                                bagging_freq = 1,
                                bagging_fraction = 0.8)
        return model
    
    def logS():
        model = lgb.LGBMRegressor(boosting_type="rf",
                                n_estimators = 400,
                                early_stopping_rounds = 0,
                                num_leaves = 50,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1,
                                bagging_freq = 4,
                                bagging_fraction = 0.8,
                                verbose = -1)
        return model
    
    def logHlogS():
        model = lgb.LGBMRegressor(boosting_type="rf", 
                                n_estimators = 600,
                                early_stopping_rounds = 0,
                                num_leaves = 31,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.05,
                                bagging_freq = 1,
                                bagging_fraction = 0.8)
        return model
    
    def logSlogH():
        model = lgb.LGBMRegressor(boosting_type="rf",
                                n_estimators = 400,
                                early_stopping_rounds = 0,
                                num_leaves = 50,
                                max_bin = 255,
                                num_threads = 4,
                                learning_rate = 0.1,
                                bagging_freq = 4,
                                bagging_fraction = 0.8)
        return model