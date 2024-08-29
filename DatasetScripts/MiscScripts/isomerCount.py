import pandas as pd #Importing libraries
from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
from tqdm import tqdm

def getMol(inchiKeys):
    """ 
    This function converts InChI strings to RDKit mol objects.
    
    Parameters:
    inchiKeys: list
    
    Returns:
    molecules: list of RDKit mol objects
    notFound: list of InChI strings that could not be converted to mol objects
    """

    notFound = []; molecules = []
    for inchi in tqdm(inchiKeys, desc="Adding isomer counts"):
        try:
            molecules.append(Chem.MolFromInchi(inchi, removeHs=False, sanitize=False))
        except:
            notFound.append(inchi)
    return molecules, notFound

def countIsomers(molecules):
    """
    This function counts the number of stereoisomers for each molecule.

    Parameters:
    molecules: list of RDKit mol objects

    Returns:
    nIsomers: list of integers
    """
    opts = StereoEnumerationOptions(unique=True)
    nIsomers = []
    for mol in molecules:
        isomers = tuple(EnumerateStereoisomers(mol, options=opts))
        nIsomers.append(len(isomers))
    return nIsomers

def isomerCountMain(df):
    inchi_keys = df["InChI"].values
    molecules, notFound = getMol(inchi_keys)
    print(notFound)

    nIsomers = countIsomers(molecules)
    df["nIsomers"] = nIsomers
    return df