from rdkit import Chem
import numpy as np #Importing relevant libraries
import pandas as pd
from tqdm import tqdm
from rdkit import RDLogger

def smilesToInChI(smiles):
    """ 
    This function converts SMILES to InChI strings and adds them to the dataframe. Where an InChI string cannot be found, a nan is added.
    
    Parameters:
    data: DataFrame
    smiles: Series
    col: str
    
    Returns:
    DataFrame"""
    RDLogger.DisableLog('rdApp.*') #Disabling RDKit warnings
    nErrors = 0; InChI = []

    for i in tqdm(range(len(smiles)), desc="Converting SMILES to InChI"): #Iterating through the SMILES strings and converting them to InChI strings
        try:
            mol = Chem.MolFromSmiles(smiles[i]) #Convert to mol object then add inchi to list
            InChI.append(Chem.MolToInchi(mol))
        except:
            # print("Invalid SMILES:", smiles[i]) #If an error occurs, print the SMILES string and its index
            # print("Index:", np.where(smiles == smiles[i]))
            InChI.append(np.nan) #Adding nan and incrementing the error count
            nErrors += 1
    print(nErrors, "occurred")
    # data[col] = InChI #Adding the InChI strings to the dataframe
    # data.dropna(subset=[col], inplace=True)
    # print(nErrors, "occurred")

    return InChI