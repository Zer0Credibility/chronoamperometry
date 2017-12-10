Plotting
========
.. automodule:: chronoamperometry.plotting

Plotting for Replicate Data
---------------------------
.. autoclass:: chronoamperometry.plotting.ReplicatePlot
    :members:

    .. automethod:: plot_replicates
    .. automethod:: plot_replicates_log_axes
    .. automethod:: plot_replicates_greyscale
    .. automethod:: plot_replicates_lowess_regression_smoothing

Plotting for Variable Testing
-----------------------------

.. autoclass:: chronoamperometry.plotting.VariablePlot
    :members:


    .. automethod:: plot_absolute_deviation_from_signal_per_channel

Plotting for Experimental Validation
------------------------------------

.. autoclass:: chronoamperometry.plotting.ExperimentPlot
    :members:

    .. automethod:: plot_t_test
    .. automethod:: plot_means_after_t_test
    .. automethod:: plot_standard_deviation_after_t_test
    .. automethod:: plot_median_absolute_deviation_from_signal