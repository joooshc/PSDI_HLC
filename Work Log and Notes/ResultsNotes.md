# Results Notes

same features for logS and logH except logS also has 'SMR_VSA3'

## logS

Scaler: MinMax -> Robust  
Algorithms: KRR and LGBM  

### Observations

- 20% error compared to logH (50%), despite much lower overall mse (0.85 vs ~9)
- Adding logH to features increases overall error by negligible amount (<1%)
- Max MSE decreased from 42 to 39

## logH

Scaler: MinMax -> Robust, simple log scaled targets  
Algorithms: LGBM, RandomForest  

### Observations

- R2 and MSE overall are much worse for unlogged data, but the percentage of predictions with an MSE greater than 1 are roughly the same (51% unlogged, 48% logged)
- Overlap of 3 in the worst entries
- Only overlap of 1 in 10 best entries
- Adding logS to features decreases error by negligible amount (<1%)
  - logS has negligible feature importance
  - If more time was available, RFE to determine feature importance and what has the most effect and contribution on logH -> more of a QSPR approach?

## Melting Point

Scaler: MinMax -> PowerTransformer or log1p. Custom log scaled targets (add abs(minVal) + 1 to all values first)  

- **Cannot log scale target because it introduces a lot of nans**
- MinMax scaling target looks promising (extremely low MSE, moderate r2)
  - Possibly try outlier removal before scaling target values
  - Low MSE is probably just due to smaller range of values rather than an actual improvement. MSE is likely to be massive if values unscaled.
Algorithms: TBD  

## Boiling Point

Scaler: Norm -> PowerTransformer or Robust. Custom log scaled targets.  
Algorithms: TBD  
