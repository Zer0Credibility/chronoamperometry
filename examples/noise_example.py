from chronoamperometry import statistics

# Point to location of Multi-Trace data
data = '<path to dataset>'

# Calculate the noise in the system
noise = statistics.Replicate_Statistics(data).calculate_median_absolute_deviation_from_signal()

print (noise)


