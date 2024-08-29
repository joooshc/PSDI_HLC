from sklearn.svm import SVR

class svrModel:
    def __init__(self):
        pass

    def logHenry():
        model = SVR(kernel = "linear", C = 1.0, epsilon = 0.4)
        return model
    
    def logCMC():
        model = SVR(kernel = "linear", C = 0.1, epsilon = 0.4)
        return model
    
    def logS():
        model = SVR(kernel = "linear", C = 1.0, epsilon = 0.1)
        return model
    
    def logHlogS():
        model = SVR(kernel = "linear", C = 1.0, epsilon = 0.4)
        return model
    
    def logSlogH():
        model = SVR(kernel = "linear", C = 1.0, epsilon = 0.1)
        return model