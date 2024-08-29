import numpy as np
import cirpy as cp
from tqdm import tqdm

def casToInChI(casList):
    """ 
    This function converts CAS to canonical SMILES strings using cirpy.
    
    Parameters:
    casList: list of strings
    
    Returns:
    canonical_smiles: list of strings
    """
    smiles = []
    for cas in tqdm(casList, desc="Converting CAS to InChI"):
        try:
            smiles.append(cp.resolve(cas, 'stdinchi'))
        except:
            smiles.append(np.nan)
            print(f"Error with {cas}")
    return smiles