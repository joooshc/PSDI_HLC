# Process Pipeline

## Running Order

1. Extraction
2. DataCombination
3. DataCleaning
4. RDKitFeatures and ThermoFeatures
5. FeatureAddition
6. DatasetBuilder
7. ValidationSets
8. DatasetScaler

## Data Handelling

1. Extract data
2. Combine
3. Extract features
4. Add features
5. Drop everything without an associated temperature
6. Remove columns with too many NaNs (<1%)

## Modelling

### Feature Selection/Scaling Method

1. Remove columns with 0 variance (all values the same)
2. Split (use non-random seed)  
    Must use same split every time because the split should not be one of the variables that changes.
3. Normalise and scale  
   After split to avoid data leakage. Must be before feature selection so normalisation is not a factor.
4. SelectKBest to get best `n` features. Use root finding algorithm.  
    Skip if finding best scaling method.
5. Train + Test

#### Notes on Scaling Methods

- Robust and Standard: Normalise first
- PowerTransformer and RobustScaler: MinMax first
- Standardize must be set to False for PowerTransformer

### Notes on KernelPCA

- Data must be non linear, as kernel pca works but regular pca doesn't
