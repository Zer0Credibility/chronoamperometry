from chronoamperometry import statistics

# importing datasets
data1 = '<path to data for first variable>'
data2 = '<path to data for second variable>'

# loading data into t-test
t_test = statistics.Experimental_Statistics(data1, data2).t_test()

print(t_test)