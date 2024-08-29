import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
from MiscScripts.isomerCount import isomerCountMain
warnings.filterwarnings("ignore")

## Melting and Boiling Points
williams = pd.read_csv("Data/Processed/0.0.0-Williams.csv") #Importing the data
williams = williams[["Compound", "SMILES", "InChI", "AverageValue"]] #Selecting columns
williams = williams.rename(columns={"AverageValue": "MeltingPoint/C"}) #Renaming columns

williams["MeltingPoint-dataSource"] = "A. Williams et al, 2015"
inchiList = williams["InChI"].values.tolist()


wiki = pd.read_csv("Data/Processed/0.0.0-WikiBP.csv") #Importing the data
wiki = wiki[["Compound", "canonical_smiles", "InChI", "bp", "mp"]] #Selecting columns
wiki = wiki.rename(columns={"mp": "MeltingPoint/C", "bp": "BoilingPoint/C", "canonical_smiles": "SMILES"}) #Renaming columns

wiki["Melting/BoilingPoint-dataSource"] = "WikiData, 2024"
inchiList.extend(wiki["InChI"].values.tolist())

pyrolysis = pd.read_csv("Data/Processed/0.0.0-pyrolysis.csv") #Importing the data
pyrolysisMP = pyrolysis[pyrolysis["QuantityType"] == "MeltingPoint"] #Selecting melting point only
pyrolysisMP = pyrolysisMP[["Compound", "SMILES", "InChI", "AverageValue"]] #Selecting columns
pyrolysisMP = pyrolysisMP.rename(columns={"AverageValue": "MeltingPoint/C"}) #Renaming columns

pyrolysisMP["MeltingPoint-dataSource"] = "A. Williams et al, 2015"
inchiList.extend(pyrolysisMP["InChI"].values.tolist())

bioquest = pd.read_csv("Data/Processed/0.3.1-bioquest.csv") #Importing the data
bioquest = bioquest[["Compound", "SMILES", "InChI", "MeltingPoint/C", "BoilingPoint/C"]] #Selecting columns

bioquest["Melting/BoilingPoint-dataSource"] = "BioQuest, 2024"
inchiList.extend(bioquest["InChI"].values.tolist())

## Solubility
solubility = pd.read_csv("Data/Processed/0.2.0-solubility.csv") #Importing the data
solubility = solubility[["Compound", "SMILES", "InChI", "logS", "Temperature"]] #Selecting columns
solubility["logS-dataSource"] = "AqSolDB + IUPAC SDS + DDB 2023"
inchiList.extend(solubility["InChI"].values.tolist())

lowe = pd.read_csv("Data/Processed/0.0.0-LoweSol.csv") #Importing the data
lowe = lowe[["Compound", "SMILES", "InChI", "logS", "Temperature"]] #Selecting columns
lowe["logS-dataSource"] = "Lowe et al 2023"
inchiList.extend(lowe["InChI"].values.tolist())

## Henry's Law
hl = pd.read_csv("Data/Processed/2.5.0-HenrysLaw.csv") #Importing the data
hl = hl[["Compound", "SMILES", "Temperature", "InChI", "Constants"]] #Selecting columns
hl = hl.rename(columns={"Constants": "HenryConstant"}) #Renaming columns
hl["HenryConstant-dataSource"] = "https://doi.org/10.5194/acp-23-10901-2023"
inchiList.extend(hl["InChI"].values.tolist())

## Combining the data
inchiList = list(set(inchiList)) 
print(len(inchiList)) #Number of unique inchi values
dataSources = [williams, wiki, pyrolysisMP, bioquest, solubility, lowe, hl] #List of dataframes

master = pd.DataFrame() #Creating an empty dataframe
for inchi in tqdm(inchiList): #Iterating over all inchi values, selecting subset with InChI and concatenating to main dataframe
    subList = []
    for ds in dataSources:
        subList.append(ds[ds["InChI"] == inchi])
    subConcat = pd.concat(subList, axis=0)

    master = pd.concat([master, subConcat], axis=0)
print(master.shape)
df = isomerCountMain(master) #Getting isomer count
master.to_csv("Data/Combined/LargeFiles/0.3.1-Master.csv", index=False) #Saving the data to a csv file