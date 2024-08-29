# Modelling Phase Transitions: Characterising Henry's Law

Joshua Cheung  
0009-0003-9952-3468

## Abstract

Aqueous solubility is a highly important property in a range of scientific areas, ranging from mass production of chemicals in industry, to drug design and flow synthesis. Measured as $\log (\text{mol dm}^{-3})$ and denoted as $\log S$, it describes the amount of a solute that is dissolved in a solvent. Related to this is Henry's law constant ($k_H$), in units of $\frac{\text{mol}}{\text{atm}}$, which describes the proportion of a gas that is dissolved in a liquid.

Despite its importance, existing computational methods for predicting Henry's law constant are largely restricted to semi-empirical methods, and there is a significant lack of experimentation with machine learning. During the past 15 years, interest has started to arise in the use of machine learning to predict solubility, and this project hopes to expand this to the prediction of Henry's law constant.

In this project, data was curated from several sources of data to create a master dataset consisting of $\log S$, $k_H$, and a corresponding temperature, as well as chemical identifiers. A diverse assortment of data preparation methods were assessed, including normalization, feature selection based on variance, and KMeansBest. Various machine learning algorithms, such as LightGBM and K-Nearest Neighbours, were trialled for predicting $\log S$ and $k_H$ values.

The overall objective of this project was to experiment with machine learning for the prediction of $\log S$ and {$k_H$}, and explore the links between them.

## Software and Data Availability

All code used in this project is available in this repository. All the most up to date datasets have been provided except those containing data from the Dortmund Data Bank (DDB VLE), since that data now requires a licence to access (2024 edition). Python 3.12 was used, and the libraries required are detailed in `requirements.txt`.