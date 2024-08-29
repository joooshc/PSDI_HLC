# A Guide to the Files in this Folder

These scripts were used to add InChI keys and clean up data from various sources.

## File Overview

### BioQuest

A program which reads in data from the HTML saved from the website:  

Quest Database™ Boiling Point (BP) and Melting Point (MP) Reference Table." AAT Bioquest, Inc., 27 Jun. 2024, <https://www.aatbio.com/data-sets/boiling-point-bp-and-melting-point-mp-reference-table>.

and converts to InChI.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-01 | Initial revision |

### NIST_CMC

A program to extract the data provided by Samuel Munday from `Critical Micelle Concentrations of Aqueous Surfectant Systems` (1971).

| Version | Date       | Change log                                |
| ------- | ---------- | ----------------------------------------- |
| 0.0.0   | 2024-07-04 | Initial revision                          |
| 0.0.1   | 2024-07-05 | Power separation bug fix                  |
| 0.1.1   | 2024-07-05 | Unit conversion                           |
| 0.1.2   | 2024-07-08 | Unit conversion bug fixes                 |
| 0.2.2   | 2024-07-15 | Now uses SMILES provided by Samuel Munday |

### FortranExtraction

A program which reads in the data from the f90 file and outputs a json and a csv.

| Version | Date       | Change log                                                                 |
| ------- | ---------- | -------------------------------------------------------------------------- |
| 0.0.0   | 2024-07-01 | Initial revision                                                           |
| 0.1.0   | 2024-07-01 | Added temperature                                                          |
| 0.2.0   | 2024-07-04 | Assumption that missing temperatures are 25c                               |
| 0.3.0   | 2024-07-05 | Where there are multiple values for the same temperature, averaging values |

### IsomerCount

A program which counts the number of isomers that each compound has, and adds them as a new column in a dataframe. The Jupyter notebook is the same as the python file.

| Version | Date       | Change log             |
| ------- | ---------- | ---------------------- |
| 0.0.0   | 2024-06-24 | Initial revision       |
| 0.0.1   | 2024-07-01 | Cleaned up + commented |

### namesToSmiles

A program which uses the PubChem api to fetch canonical SMILES based on compound names and adds them as a new column in a dataframe.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-01 | Initial revision |

### smilesToInChI

A program which uses RDKit to convert SMILES strings to InChI and adds them as a new column in a dataframe.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-01 | Initial revision |

### solubility

A program which takes the data from the miscibility project and removes all features, and converts the SMILES strings to InChI.

| Version | Date       | Change log                                            |
| ------- | ---------- | ----------------------------------------------------- |
| 0.0.0   | 2024-07-01 | Initial revision                                      |
| 0.1.0   | 2024-07-05 | Removed non aqueous data, converted mole frac to logS |

### WikiBP

A program which generates InChI and cleans the data provided by Jo Grundy from WikiData.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-01 | Initial revision |

### Williams

A program which extracts data from the csv files which were manually generated from the sdf files provided by [Antony Williams](https://figshare.com/articles/dataset/Melting_Point_and_Pyrolysis_Point_Data_for_Tens_of_Thousands_of_Chemicals/2007426).

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-01 | Initial revision |

## Qin_CMC

A program which processes the data from the Qin et al paper.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-08 | Initial revision |

## RDKit_Features

A program to extract the RDKit descriptors and add them to the main dataset.

| Version | Date       | Change log       |
| ------- | ---------- | ---------------- |
| 0.0.0   | 2024-07-10 | Initial revision |
