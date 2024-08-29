# General Notes

- Physico-chem based machine learning
- Link between Henry's law constant and Gibbs free energy
- What do we actually want to predict? -> Henry's law constant dependence on temperature.
- Relationship between gas dissolving in solution and solid dissolving in solution
  - Solid melting
  - Other phases and stuff
- QSPR studies?

Train models multiple times this time!!

Issues:  

- Henry's law database is only for compounds in _water_ -> cannot train with other mixtures because there is no other data.
- Missing InChI keys for enantiomeric compounds/loss of stereochemical information
- A lot of temperatures and SMILES missing for henrys law database

## Sander's Henry's Law Constants

### Proposed Handelling of Different Values for Henry's Law Constant

- Prioritise L and M values (literature and measurement)
  - Do not use E, ?, W values at all
- Where there are multiple L/M values for the same temperature, take an average

### Obtaining SMILES and InChI

- Use cactus, cirpy or pubchem (server availability?) to obtain canonical smiles
- Convert canonical smiles to InChI using `smilesToInChI.py`

## Combining Datasets

It is likely that there will not be much overlap between the datasets due to the obscurity of the compounds in the CMC data. 