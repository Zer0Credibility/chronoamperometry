Overview
========

Installation
------------
pip install chronoamperometry

Purpose
-------
Chronoamperometric measurement generates a such a large quantity of data that the usual high-level methods of data
manipulation such as MS Excel function poorly because they are not optimized to handle millions of datapoints.
Complex methods of analysis are also difficult or impossible to implement using Excel, Origin, etc.

It is also my hope that this tool-set will assist with the goal of using Microbial Fuel Cells to examine the
underlying biology of organisms by enabling the comparison of current production by various mutants, etc.

Finally, this tool produces publication-quality graphs via the PlotNine package.


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