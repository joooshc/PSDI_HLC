from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors

def scatterPlot(yTest, yPred, meta):
    """ 
    Plots a scatter plot of the true vs predicted values.
    
    Inputs:
    yTest: np.array, the true values
    yPred: np.array, the predicted values
    meta: dict, the metadata
    
    Outputs:
    None
    """
    dset = meta["dataset"] #Extracting the dataset name

    bestFit = np.polyfit(yTest, yPred, 1) #Fitting a line of best fit
    bestFit_fn = np.poly1d(bestFit)
    y = bestFit_fn(yTest)
    
    mseList = calcMSE(yTest, yPred) #Calculating the MSE for each point
    mse = mean_squared_error(yTest, yPred) #Overall MSE and R2
    r2 = r2_score(yTest, yPred)

    fig, ax = plt.subplots(figsize=(8, 6)) #Creating the figure

    ax.plot(yTest, y, c="red", label = "Line of Best Fit")

    sc = ax.scatter(yTest, yPred, #Scatter plot
                s=10, 
                label="Predicted vs True", 
                cmap="plasma", 
                c=mseList, 
                norm=colors.SymLogNorm(linthresh=0.03), clip_on=True)
    sc.set_alpha(0.75)

    ax.set_title(f"True vs Predicted Values ({dset})\n MSE: %.2e, R2: %.2f" % (mse, r2)) #Labels
    ax.set_xlabel("True Values")
    ax.set_ylabel("Predicted Values")

    xlims = ax.get_xlim() #Setting the limits
    ax.set_ylim(xlims)

    cbar = fig.colorbar(sc, ax=ax, label="MSE", orientation="vertical", location="left", shrink=0.75) #Colour bar
    cbar.solids.set(alpha=1)

    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{meta["filepath"]}.png")

def calcMSE(yTest, yHat):
    """ 
    Calculates the Mean Squared Error for each point in the dataset.
    
    Inputs:
    yTest: np.array, the true values
    yHat: np.array, the predicted values
    
    Outputs:
    mse: list, the MSE for each point
    """
    print("Calculating MSE")
    yTest = np.array(yTest).reshape(-1, 1); yHat = np.array(yHat).reshape(-1, 1) #Array must be reshaped to work with the function
    mse = [mean_squared_error(y, yHat) for y, yHat in zip(yTest, yHat)]
    return mse

def dualPlot(yTest, yPred, meta):
    """
    Plots a scatter plot of the true vs predicted values and a histogram of the MSE values.
    
    Inputs:
    yTest: np.array, the true values
    yPred: np.array, the predicted values
    meta: dict, the metadata
    
    Outputs:
    None
    """

    dset = meta["dataset"] #Extracting the dataset name
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 6), layout = "constrained", dpi=300) #Creating the figure

    mseList = calcMSE(yTest, yPred) #Calculating the MSE for each point
    mse = mean_squared_error(yTest, yPred) #Overall MSE and R2
    r2 = r2_score(yTest, yPred)

    ax0.plot(yTest, yTest, c="red", label = "Ideal Prediction")

    myCmap = plt.cm.get_cmap("viridis", 10) #Creating a colour map
    myCmap.set_under("gray")

    sc = ax0.scatter(yTest, yPred, #Scatter plot
            s=10, 
            label = "Predicted vs True", 
            cmap = myCmap, 
            c = mseList, 
            clip_on=True)
    sc.set_alpha(0.75)

    xlims = ax0.get_xlim() #Setting the limits
    ax0.set_ylim(xlims)

    cbar = fig.colorbar(sc, ax=ax0, label="MSE", orientation="vertical", location="left", shrink=0.75) #Colour bar
    cbar.solids.set(alpha=1)
    cbar.set_ticklabels([f"{x:.1e}" for x in cbar.get_ticks()])

    ax0.set_xlabel("True Values") #Labels
    ax0.set_ylabel("Predicted Values")
    ax0.legend()
    ax0.set_title(f"True vs Predicted Values ({dset})\n MSE: %.2e, R2: %.2f" % (mse, r2))

    ### Histogram ###
    n, bins, patches = ax1.hist(mseList, bins=25, edgecolor = "black", linewidth = 1.2) #Creating the histogram
    binCentres = 0.5 * (bins[:-1] + bins[1:]) #Getting the bin centres
    col = binCentres - min(binCentres) #Normalising the colours
    col /= max(col) 

    for c, p in zip(col, patches): #Colouring the patches
        plt.setp(p, "facecolor", myCmap(c))

    ax1.set_title("MSE Distribution") #Labels
    ax1.set_yscale("log")
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.2e}"))
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.set_xlabel("MSE")
    ax1.set_ylabel("Log(Frequency)")
    
    plt.suptitle(f"{meta["version"]} {meta["dataset"]} {meta["model"]} {meta["variant"]}\n", fontsize=16) #Overall title
    plt.savefig(f"{meta["filepath"]}_DualPlot.png") #Saving the figure
    # plt.show()

if __name__ == "__main__": #Code used for tinkering with parameters to make the graph look pretty
    df = pd.read_csv("Results/logHenry/LGBM/1.3.0_Y_2024-07-17_17.15.28.csv")
    print("running")
    y = df["Y"].values.astype(float); yHat = df["Y_hat"].values.astype(float)
    meta = {"dataset" : "logHenry",
        "version" : "1.3.0",
        "timestamp" : "2024-07-17_17.15.28",
        "model" : "LGBM",
        "variant" : "Normalised"}

    dualPlot(y, yHat, meta)