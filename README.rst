# chronoamperometry

## A toolset for analyzing chronoamperometric data

### This repository includes code that will:

1. Directly digest the output excel file from PalmSens MultiTrace potentiostat software.
2. Arrange the data into a standard dataframe format
3. Assist with statistical analysis for estimation of noise estimation and calculations for t-tests.
4. Plot the data using the python port of ggplot2, plotnine

To do:
1. Calculations for cohen's D
2. Implement integral calculation for chronoamperometric curves
3. Calculations for sensitivity index d'


## Usage

http://chronoamperometry.readthedocs.io/en/latest/?

## Dependencies

Several of these have sub-dependencies:

1. numpy
2. pandas
3. plotnine
4. scipy
5. tqdm
6. xlrd