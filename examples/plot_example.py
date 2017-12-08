from chronoamperometry import plotting

# import data
data1 = '<path to data for first variable>'
data2 = '<path to data for second variable>'

# plot data
plot = plotting.ExperimentPlot(data1, data2).plot_t_test()