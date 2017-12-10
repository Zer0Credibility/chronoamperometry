Statistics
==========
.. automodule:: chronoamperometry.statistics

Statistics for Replicate Data
----------------------------------
.. autoclass:: chronoamperometry.statistics.Replicate_Statistics
    :members:

    .. automethod:: construct_lowess_regression
    .. automethod:: calculate_median_absolute_deviation_from_signal
    .. automethod:: calculate_absolute_deviation_from_signal_per_channel
    .. automethod:: anova_test

Statistics for Variable Testing
-------------------------------

.. autoclass:: chronoamperometry.statistics.Variable_Statistics
    :members:

    .. automethod:: compare_absolute_deviation_from_signal_between_experiments

Statistics for Experimental Validation
--------------------------------------

.. autoclass:: chronoamperometry.statistics.Experimental_Statistics
    :members:

    .. automethod:: t_test