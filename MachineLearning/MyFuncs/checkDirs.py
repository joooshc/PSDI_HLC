import os

def checkPath(path):
    """
    Check if the path exists, if not, create it
    Inputs:
    path: str, the path to check
    
    Outputs:
    None
    """
    if not os.path.exists(path):
        print(f"Creating {path}")
        os.makedirs(path)