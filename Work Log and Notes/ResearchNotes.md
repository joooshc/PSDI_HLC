- Determine if 2 film theory is relevant
- Possible extraction of thermodynamic properties with [Thermo](https://thermo.readthedocs.io/thermo.phases.html)
  - Especially important due to the relationship between Gibbs free energy and Henry's law constant

### CMC Notes

<https://pubs.acs.org/doi/full/10.1021/acs.jpcb.1c05264>

- GNN used to predict CMC values, but very small dataset (~200)
- K fold validation used, so only 100 in the training set
- GridSearchCV used
- Synthetic data generated to increase dataset size -> worth exploring over and undersampling in the combined dataset + possibly a model just for CMC because it has not been explored much
- Important to note the charge on the cmc molecule

> Saliency maps were created to gain insight into features of the molecular structure that best explains CMC values

sounds very interesting

> We used the proposed architecture to train the GCN with 10-fold CV, leading to 1638 training samples and 182 validation samples in each CV fold.

Figure out how they expanded their dataset so much

"To the authors’ knowledge, it is currently the largest public data set of CMCs for several classes of surfactants collected at standard conditions in an aqueous environment between 20 to 25 °C."

https://github.com/zavalab/ML/tree/master/CMC_GCN MORE CMC DATA

https://www.nature.com/articles/s41598-023-40466-1#Abs1 need to request data from here.  
Description of ML algorithms in miscibility paper need to be edited to include results.

Figure out how to get Tolman length of tail

https://pubs.acs.org/doi/10.1021/acs.jctc.3c00868

- feature vectors of atoms??
- Appears to be better version of first study found

https://github.com/a-ws-m/CaMCaNN/blob/main/camcann/data/datasets/nist-new-vals.csv Possibly same as some of Sam's data