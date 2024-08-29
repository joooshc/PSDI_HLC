import pandas as pd #Importing libraries
import numpy as np
import pubchempy as pcp
from tqdm import tqdm

def nameToSmiles(cnames):
    """ 
    This function converts compound names to canonical SMILES strings using PubChemPy.
    
    Parameters:
    cnames: list of strings
    
    Returns:
    canonical_smiles: list of strings
    """

    canonical_smiles = []; notFound = []
    for i in tqdm(range(len(cnames))):
        comp = pcp.get_compounds(cnames[i], 'name')
        try:
            smile = comp[0].canonical_smiles
        except:
            smile = np.nan
            print(i, cnames[i], 'smile not found')
            notFound.append(cnames[i])
        canonical_smiles.append(smile)
    print(len(canonical_smiles))
    return canonical_smiles, notFound