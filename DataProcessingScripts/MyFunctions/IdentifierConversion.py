import numpy as np
import cirpy as cp
from tqdm import tqdm
import pubchempy as pcp
from rdkit import RDLogger
from rdkit import Chem

def validateTarget(target):
    validTargets = ["stdinchi", "stdinchikey", "inchi", "smiles", "ficts", "ficus", "uuuuu", "hashisy", "sdf", "names", "iupac_name", "cas", "formula"]
    print(target)
    if target not in validTargets:
        raise ValueError(f"Invalid target: {target}. Valid targets are: {validTargets}")

class convertors:
    def casToX(casList, target):
        """ 
        This function converts CAS to canonical SMILES/InChI strings using cirpy.
        
        Parameters:
        casList: list of strings
        target: string

        Returns:
        targVals: list of strings
        """

        # validateTarget(target)

        targVals = []
        for cas in tqdm(casList, desc=f"Converting CAS to {target}"):
            if cas == "UNKNOWN":
                targVals.append(np.nan)
                print(f"Error with {cas}")
            else:
                try:
                    targVals.append(cp.resolve(cas, target))
                except:
                    targVals.append(np.nan)
                    print(f"Error with {cas}")
        return targVals
    
    def nameToSmiles(nameList):
        """ 
        This function converts compound names to canonical SMILES strings using PubChemPy.
        
        Parameters:
        nameList: list of strings
        
        Returns:
        smiles: list of strings
        notFound: list of strings
        """

        smiles = []; notFound = []
        for i in tqdm(range(len(nameList))):
            comp = pcp.get_compounds(nameList[i], 'name')
            try:
                smile = comp[0].canonical_smiles
            except:
                smile = np.nan
                print(i, nameList[i], 'smile not found')
                notFound.append(nameList[i])
            smiles.append(smile)
        print(len(smiles), "found")

        return smiles, notFound
    
    def smilesToInChI(smiles):
        """ 
        This function converts SMILES to InChI strings and adds them to the dataframe. Where an InChI string cannot be found, a nan is added.
        
        Parameters:
        smiles: list of strings
        
        Returns:
        InChI: list of strings
        """
        RDLogger.DisableLog('rdApp.*')
        nErrors = 0; InChI = []
        
        for i in tqdm(range(len(smiles)), desc="Converting SMILES to InChI"): #Iterating through the SMILES strings and converting them to InChI strings
            try:
                mol = Chem.MolFromSmiles(smiles[i]) #Convert to mol object then add inchi to list
                InChI.append(Chem.MolToInchi(mol))
            except:
                InChI.append(np.nan) #Adding nan and incrementing the error count
                nErrors += 1
        print(nErrors, "errors occurred")

        return InChI