from sklearn.ensemble import AdaBoostRegressor

class Ada:
    def __init__(self):
        pass

    def logHenry():
        model = AdaBoostRegressor(n_estimators = 100,
                              learning_rate = 0.2,
                              loss = 'exponential') 
        return model
    
    def logCMC():
        model = AdaBoostRegressor(n_estimators = 50,
                              learning_rate = 0.1,
                              loss = 'linear') 
        return model

    def logS():
        model = AdaBoostRegressor(n_estimators = 200,
                                  learning_rate = 0.1,
                                  loss = 'exponential')
        return model
    
    def logSlogH():
        model = AdaBoostRegressor(n_estimators = 100,
                                  learning_rate = 0.1,
                                  loss = 'exponential')
        return model
    
    def logHlogS():
        model = AdaBoostRegressor(n_estimators = 100,
                                  learning_rate = 0.2,
                                  loss = 'exponential')
        return model