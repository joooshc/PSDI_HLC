# Data

_This file was generated on 2024-06-28 by Joshua Cheung._  

Author: Joshua Cheung  
ORCID:  
Institution: University of Southampton  
Email: [jc10g22@soton.ac.uk]  

## File Naming Conventions

Semantic naming: 0.0.0-Name

## Data and File Overview

### /Williams/

Data downloaded from [figshare](https://figshare.com/articles/dataset/Melting_Point_and_Pyrolysis_Point_Data_for_Tens_of_Thousands_of_Chemicals/2007426) on 2024/06/24.

| File                | Description                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| pyrolysis_point.sdf | Unprocessed file downloaded from figshare.                                                                                                 |
| pyrolysis.csv       | Data table from pyrolysis_point.sdf in csv format extracted by copying and pasting to excel from DataWarrior v06.02.01 (built 22-May-2024) |
| Williams.csv        | Data table from Williams.sdf in csv format extracted by copying and pasting to excel from DataWarrior v06.02.01 (built 22-May-2024)        |
| Williams.sdf        | Unprocessed file downloaded from figshare.                                                                                                 |

### BioQuest.csv

The extracted data from the BioQuest website. Missing SMILES and InChI are NaN values.

Quest Database™ Boiling Point (BP) and Melting Point (MP) Reference Table." AAT Bioquest, Inc., 27 Jun. 2024, https://www.aatbio.com/data-sets/boiling-point-bp-and-melting-point-mp-reference-table.

| Version | Date       | Changelog                                 |
| ------- | ---------- | ----------------------------------------- |
| 0.0.0   | 2024-06-27 | Initial extraction from html file.        |
| 0.1.0   | 2024-06-27 | SMILES added using the PubChemPy library. |
| 0.2.0   | 2024-06-27 | InChI added using RDKit.                  |

### pyrolysis.csv

The extracted data from the pyrolysis_point.sdf file by Antony Williams, with added SMILES and InChI. Ranges of values have been separated into lower and higher, with an average column.  

| Version | Date       | Changelog        |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-06-27 | Initial revision |

### solubility.csv

The cleaned data from the solubility/miscibility project from Summer 2023. Features have been removed and InChI keys have been generated from SMILES strings.

| Version | Date       | Changelog        |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-06-26 | Initial revision |

### WikiBP.csv

The cleaned data from `/WikiBP/`. InChI keys have been generated from SMILES strings and added as a new column to the dataset.

| Version | Date       | Changelog        |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-06-27 | Initial revision |

### HenrysLaw

The extracted data from the `HscpSI.f90` file using the FortranExtraction script. The JSON is the same thing as the CSV.

| Version | Date       | Change log                                                                 |
| ------- | ---------- | -------------------------------------------------------------------------- |
| 0.0.0   | 2024-07-01 | Initial revision                                                           |
| 0.1.0   | 2024-07-01 | Added InChI and SMILES                                                     |
| 1.1.0   | 2024-07-02 | Expanded lists                                                             |
| 2.1.0   | 2024-07-04 | Re-extracted w/ assumption unknown temp is 25c                             |
| 2.2.0   | 2024-07-04 | Added InChI and SMILES                                                     |
| 2.3.0   | 2024-07-04 | Expanded lists                                                             |
| 2.4.0   | 2024-07-04 | Removed bad values                                                         |
| 2.5.0   | 2024-07-05 | Averaging values where there are multiple values for the same temperature. |


### QinCMC

The data from Qin et al (<https://pubs.acs.org/doi/full/10.1021/acs.jpcb.1c05264>)

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-08 | Initial revision |
