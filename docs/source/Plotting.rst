Plotting
===================================
.. automodule:: plotting

Statistics for Replicate Data
----------------------------------
.. autoclass:: chronoamperometry.statistics.ReplicatePlot
    :members:

    .. automethod:: plot_replicates
    .. automethod:: plot_replicates_log_axes
    .. automethod:: plot_replicates_greyscale
    .. automethod:: plot_replicates_lowess_regression_smoothing

Statistics for Variable Testing
----------------------------------

.. autoclass:: chronoamperometry.statistics.VariablePlot
    :members:

    .. automethod:: plot_median_absolute_deviation_from_signal
    .. automethod:: plot_absolute_deviation_from_signal_per_channel

Statistics for Experimental Validation
----------------------------------

.. autoclass:: chronoamperometry.statistics.ExperimentPlot
    :members:

    .. automethod:: plot_t_test
    .. automethod:: plot_means_after_t_test
    .. automethod:: plot_standard_deviation_after_t_test