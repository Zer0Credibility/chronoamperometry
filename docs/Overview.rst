Overview
========

Installation
------------
pip install chronoamperometry

Purpose
-------
The philosophy behind the release of this toolset is that by standardising analysis and presentation
of chronoamperometric data, researchers in the microbial fuel cell community will find it easier to
focus on the reproducibility of their devices rather than on maximizing power output.


Tools
-----
This repository includes code that will:

1. Directly digest the output excel file from PalmSens MultiTrace potentiostat software.
2. Arrange the data into a standard dataframe format
3. Assist with statistical analysis for estimation of noise estimation and calculations for t-tests.
4. Plot the time series of raw chronoamperometric measurement using the python port of ggplot2, plotnine
5. Plot statistical or other analysis using plotnine

To do:

1. Calculations for cohen's D
2. Implement integral calculation for chronoamperometric curves
3. Calculations for sensitivity index d'